"""Publish validated changed-page screenshots from trusted workflow_run code."""

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
MAX_IMAGE_SIZE = 12 * 1024 * 1024


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
            body = response.read()
            return json.loads(body) if body else {}
    except HTTPError as error:
        if error.code == 404:
            return None
        raise RuntimeError(f"GitHub API {method} {path}: HTTP {error.code}") from error


def valid_sha(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value)


def valid_route(route):
    return (
        isinstance(route, str)
        and re.fullmatch(r"/[A-Za-z0-9._~%/-]*", route)
        and "//" not in route
        and all(part not in {".", ".."} for part in route.split("/"))
    )


def validated_manifest(folder, run_head):
    file = folder / "manifest.json"
    if file.is_symlink() or not file.is_file() or file.stat().st_size > 128 * 1024:
        raise ValueError("Preview artifact has no valid manifest")
    manifest = json.loads(file.read_text(encoding="utf-8"))
    number = manifest.get("pr_number")
    head = manifest.get("head_sha")
    base = manifest.get("base_sha")
    checkout = manifest.get("checkout_sha")
    pages = manifest.get("pages")
    if isinstance(number, bool) or not isinstance(number, int) or not 0 < number < 10000000:
        raise ValueError("Invalid PR number in manifest")
    if not all(valid_sha(value) for value in (head, base, checkout, run_head)):
        raise ValueError("Invalid commit SHA in manifest or workflow run")
    if run_head not in {head, checkout}:
        raise ValueError("Preview artifact is not from the completed workflow run")
    if not isinstance(pages, list) or len(pages) > 999:
        raise ValueError("Invalid number of changed pages")
    routes = set()
    for i, page in enumerate(pages, 1):
        if not isinstance(page, dict) or not valid_route(page.get("path")):
            raise ValueError("Invalid changed-page URL")
        if page.get("image") != f"page-{i:03d}.png" or page["path"] in routes:
            raise ValueError("Duplicate page or unexpected image name")
        routes.add(page["path"])
    return number, head, base, pages


def validated_images(folder, pages):
    expected = {page["image"] for page in pages}
    if {path.name for path in folder.glob("*.png")} != expected:
        raise ValueError("Screenshots do not match the changed-page manifest")
    images = {}
    for name in sorted(expected):
        image = folder / name
        if image.is_symlink() or not image.is_file():
            raise ValueError(f"Missing PNG screenshot: {name}")
        if not 32 <= image.stat().st_size <= MAX_IMAGE_SIZE:
            raise ValueError(f"Unexpected PNG size: {name}")
        content = image.read_bytes()
        if content[:16] != b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR":
            raise ValueError(f"Invalid PNG header: {name}")
        width, height = struct.unpack(">II", content[16:24])
        if not 0 < width <= 5000 or not 0 < height <= 30000:
            raise ValueError(f"Unexpected PNG dimensions: {name}")
        images[name] = content
    return images


def preview_ref(repo, *, create=False):
    path = f"/repos/{repo}/git/ref/heads/{PREVIEW_BRANCH}"
    ref = api("GET", path)
    if ref is not None or not create:
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
    """Replace the PR's entire preview directory, removing stale PNGs."""
    ref = preview_ref(repo, create=bool(images))
    if ref is None:
        return
    directory = f"previews/pr-{number}"
    if not images:
        existing = api("GET", f"/repos/{repo}/contents/{directory}?ref={PREVIEW_BRANCH}")
        if existing is None:
            return
    parent = ref["object"]["sha"]
    commit = api("GET", f"/repos/{repo}/git/commits/{parent}")
    if images:
        entries = []
        for name, content in sorted(images.items()):
            blob = api(
                "POST",
                f"/repos/{repo}/git/blobs",
                {"content": base64.b64encode(content).decode("ascii"), "encoding": "base64"},
            )
            entries.append({"path": name, "mode": "100644", "type": "blob", "sha": blob["sha"]})
        subtree = api("POST", f"/repos/{repo}/git/trees", {"tree": entries})
        sha = subtree["sha"]
    else:
        sha = None
    tree = api(
        "POST",
        f"/repos/{repo}/git/trees",
        {
            "base_tree": commit["tree"]["sha"],
            "tree": [{"path": directory, "mode": "040000", "type": "tree", "sha": sha}],
        },
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


def existing_comment(repo, number):
    comments_path = f"/repos/{repo}/issues/{number}/comments"
    for page in range(1, 21):
        comments = api("GET", f"{comments_path}?per_page=100&page={page}")
        for comment in comments:
            if (
                COMMENT_MARKER in comment.get("body", "")
                and comment.get("user", {}).get("login") == "github-actions[bot]"
            ):
                return comment
        if len(comments) < 100:
            break
    return None


def update_comment(repo, number, sha, pages, run_id):
    existing = existing_comment(repo, number)
    if not pages:
        if existing:
            api("DELETE", f"/repos/{repo}/issues/comments/{existing['id']}")
            print(f"Removed obsolete screenshot comment on PR #{number}")
        else:
            print(f"No changed pages and no screenshot comment on PR #{number}")
        return

    image_root = f"https://raw.githubusercontent.com/{repo}/{PREVIEW_BRANCH}/previews/pr-{number}"
    lines = [
        COMMENT_MARKER,
        "## Changed Hugo pages",
        f"Captured from PR commit `{sha[:12]}`. One screenshot per changed published page.",
        "",
    ]
    for page in pages:
        route, filename = page["path"], page["image"]
        lines.extend([f"**`{route}`**", f"![Preview of {route}]({image_root}/{filename}?run={run_id})", ""])
    lines.extend(
        [
            f"[Download screenshots from the Actions run](https://github.com/{repo}/actions/runs/{run_id})",
            "",
            "- Jade",
        ]
    )
    body = "\n".join(lines)
    if existing:
        api("PATCH", f"/repos/{repo}/issues/comments/{existing['id']}", {"body": body})
        print(f"Updated screenshot comment on PR #{number}")
    else:
        api("POST", f"/repos/{repo}/issues/{number}/comments", {"body": body})
        print(f"Posted screenshot comment on PR #{number}")


def run_matches_pr(repo, run_id, number, pr, run_head):
    """Tie untrusted artifacts to the actual GitHub pull-request workflow run."""
    run = api("GET", f"/repos/{repo}/actions/runs/{run_id}")
    if (
        not run
        or run.get("event") != "pull_request"
        or run.get("conclusion") != "success"
        or run.get("name") != "PR site screenshots"
        or run.get("head_sha") != run_head
    ):
        return False
    linked = run.get("pull_requests") or []
    if linked:
        return any(
            item.get("number") == number
            and item.get("head", {}).get("sha", pr["head"]["sha"]) == pr["head"]["sha"]
            for item in linked
        )
    # GitHub may omit linked PRs for fork runs. Then require the run's
    # actual commit to match the PR head or GitHub's synthetic merge commit.
    return run_head in {pr["head"]["sha"], pr.get("merge_commit_sha")}


def main():
    folder = Path("pr-preview")
    run_head = os.environ["WORKFLOW_HEAD_SHA"]
    run_id = int(os.environ["WORKFLOW_RUN_ID"])
    repo = os.environ["GITHUB_REPOSITORY"]
    if not re.fullmatch(r"[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+", repo):
        raise ValueError("Invalid repository name")
    number, head, base, pages = validated_manifest(folder, run_head)
    pr = api("GET", f"/repos/{repo}/pulls/{number}")
    if not pr or pr["base"]["ref"] != "master":
        raise ValueError("Artifact does not belong to a PR targeting master")
    if pr["state"] != "open":
        print(f"PR #{number} is closed; skipping screenshot publication")
        return
    if pr["head"]["sha"] != head or pr["base"]["sha"] != base:
        print(f"PR #{number} moved since capture; skipping stale screenshots")
        return
    if not run_matches_pr(repo, run_id, number, pr, run_head):
        raise ValueError("Screenshot workflow run is not associated with this PR")
    images = validated_images(folder, pages)
    publish_images(repo, number, images)
    update_comment(repo, number, head, pages, run_id)


if __name__ == "__main__":
    main()
