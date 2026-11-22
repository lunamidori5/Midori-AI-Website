"""Publish validated screenshot artifacts from a trusted workflow_run job."""

import base64
import json
import os
import re
import struct
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

PREVIEW_BRANCH = "pr-previews"
COMMENT_MARKER = "<!-- midori-site-preview -->"
IMAGES = ("desktop-home.png", "mobile-home.png", "changed-page.png")


def api(method, path, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        f"https://api.github.com{path}",
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.environ['GH_TOKEN']}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read())
    except HTTPError as error:
        if error.code == 404:
            return None
        raise RuntimeError(f"GitHub API {method} {path}: HTTP {error.code}") from error


def validated_manifest(folder, run_head):
    file = folder / "manifest.json"
    if not file.is_file() or file.stat().st_size > 4096:
        raise ValueError("Preview artifact has no valid manifest")
    manifest = json.loads(file.read_text(encoding="utf-8"))
    number = manifest.get("pr_number")
    sha = manifest.get("head_sha")
    route = manifest.get("page_path")
    if isinstance(number, bool) or not isinstance(number, int) or not 0 < number < 10000000:
        raise ValueError("Invalid PR number in manifest")
    if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("Invalid PR head SHA in manifest")
    if sha != run_head:
        raise ValueError("Screenshot artifact does not match the completed workflow run")
    if not isinstance(route, str) or not re.fullmatch(r"/[a-zA-Z0-9_/-]{0,140}/", route):
        raise ValueError("Invalid preview page path")
    return number, sha, route


def validated_images(folder):
    images = {}
    for name in IMAGES:
        image = folder / name
        if image.is_symlink() or not image.is_file():
            raise ValueError(f"Missing PNG screenshot: {name}")
        if not 32 <= image.stat().st_size <= 12 * 1024 * 1024:
            raise ValueError(f"Unexpected PNG size: {name}")
        content = image.read_bytes()
        if content[:16] != b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR":
            raise ValueError(f"Invalid PNG header: {name}")
        width, height = struct.unpack(">II", content[16:24])
        if not 0 < width <= 5000 or not 0 < height <= 30000:
            raise ValueError(f"Unexpected PNG dimensions: {name}")
        images[name] = content
    return images


def preview_ref(repo):
    path = f"/repos/{repo}/git/ref/heads/{PREVIEW_BRANCH}"
    ref = api("GET", path)
    if ref is not None:
        return ref
    tree = api("POST", f"/repos/{repo}/git/trees", {"tree": []})
    root = api(
        "POST",
        f"/repos/{repo}/git/commits",
        {"message": "Initialize PR preview images", "tree": tree["sha"], "parents": []},
    )
    api(
        "POST",
        f"/repos/{repo}/git/refs",
        {"ref": f"refs/heads/{PREVIEW_BRANCH}", "sha": root["sha"]},
    )
    return api("GET", path)


def publish_images(repo, number, images):
    ref = preview_ref(repo)
    parent = ref["object"]["sha"]
    commit = api("GET", f"/repos/{repo}/git/commits/{parent}")
    entries = []
    for name, content in images.items():
        blob = api(
            "POST",
            f"/repos/{repo}/git/blobs",
            {"content": base64.b64encode(content).decode("ascii"), "encoding": "base64"},
        )
        entries.append(
            {
                "path": f"previews/pr-{number}/{name}",
                "mode": "100644",
                "type": "blob",
                "sha": blob["sha"],
            }
        )
    tree = api(
        "POST",
        f"/repos/{repo}/git/trees",
        {"base_tree": commit["tree"]["sha"], "tree": entries},
    )
    new_commit = api(
        "POST",
        f"/repos/{repo}/git/commits",
        {
            "message": f"Update PR #{number} screenshot previews",
            "tree": tree["sha"],
            "parents": [parent],
        },
    )
    api(
        "PATCH",
        f"/repos/{repo}/git/refs/heads/{PREVIEW_BRANCH}",
        {"sha": new_commit["sha"], "force": False},
    )


def update_comment(repo, number, sha, route, run_id):
    image_root = f"https://raw.githubusercontent.com/{repo}/{PREVIEW_BRANCH}/previews/pr-{number}"
    desktop, mobile, changed = (f"{image_root}/{name}?run={run_id}" for name in IMAGES)
    body = "\n".join(
        [
            COMMENT_MARKER,
            "## Hugo PR previews",
            f"Built from commit `{sha[:12]}`. These images show this PR's Hugo site, not the live site.",
            "",
            "| Desktop homepage | Mobile homepage |",
            "| --- | --- |",
            f"| ![Desktop homepage]({desktop}) | ![Mobile homepage]({mobile}) |",
            "",
            f"**Content preview:** `{route}`",
            f"![Changed content page]({changed})",
            "",
            f"[Download PNGs from the Actions run](https://github.com/{repo}/actions/runs/{run_id})",
            "",
            "- Jade",
        ]
    )
    comments_path = f"/repos/{repo}/issues/{number}/comments"
    for page in range(1, 21):
        comments = api("GET", f"{comments_path}?per_page=100&page={page}")
        for comment in comments:
            if (
                COMMENT_MARKER in comment.get("body", "")
                and comment.get("user", {}).get("login") == "github-actions[bot]"
            ):
                api("PATCH", f"/repos/{repo}/issues/comments/{comment['id']}", {"body": body})
                print(f"Updated screenshots comment on PR #{number}")
                return
        if len(comments) < 100:
            break
    api("POST", comments_path, {"body": body})
    print(f"Posted screenshots comment on PR #{number}")


def main():
    folder = Path("pr-preview")
    run_head = os.environ["WORKFLOW_HEAD_SHA"]
    run_id = int(os.environ["WORKFLOW_RUN_ID"])
    repo = os.environ["GITHUB_REPOSITORY"]
    if not re.fullmatch(r"[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+", repo):
        raise ValueError("Invalid repository name")
    number, sha, route = validated_manifest(folder, run_head)
    pr = api("GET", f"/repos/{repo}/pulls/{number}")
    if not pr or pr["head"]["sha"] != sha or pr["base"]["ref"] != "master":
        raise ValueError("Artifact does not belong to an active PR targeting master")
    if pr["state"] != "open":
        print(f"PR #{number} is closed; skipping image publication")
        return
    images = validated_images(folder)
    publish_images(repo, number, images)
    update_comment(repo, number, sha, route, run_id)


if __name__ == "__main__":
    main()
