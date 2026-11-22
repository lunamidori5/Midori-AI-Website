"""Capture one screenshot per published Hugo content page changed in a PR."""

import argparse
import csv
import io
import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import quote, urlsplit

BASE_URL = "http://127.0.0.1:1313"
OUTPUT = Path("pr-preview")


def changed_content_files(base_sha, head_sha):
    """Compare the whole PR with its merge base, not only the last commit."""
    for sha in (base_sha, head_sha):
        if not re.fullmatch(r"[0-9a-f]{40}", sha):
            raise ValueError("Invalid commit SHA")
    result = subprocess.run(
        [
            "git", "diff", "--name-only", "-z", "--diff-filter=ACMR",
            f"{base_sha}...{head_sha}", "--", "content/",
        ],
        capture_output=True,
        check=True,
    )
    return sorted(
        {
            name
            for name in result.stdout.decode("utf-8").split("\0")
            if name.startswith("content/") and name.lower().endswith(".md")
        }
    )


def published_routes():
    """Ask Hugo for actual permalinks, including slug and URL overrides."""
    result = subprocess.run(
        ["hugo", "list", "published", "--baseURL", f"{BASE_URL}/"],
        capture_output=True,
        text=True,
        check=True,
    )
    routes = {}
    for row in csv.DictReader(io.StringIO(result.stdout)):
        source = row.get("path", "")
        permalink = row.get("permalink", "")
        parsed = urlsplit(permalink)
        if parsed.scheme != "http" or parsed.netloc != "127.0.0.1:1313":
            raise ValueError(f"Unexpected Hugo permalink for {source}: {permalink}")
        route = quote(parsed.path, safe="/%._~-")
        if (
            not re.fullmatch(r"/[A-Za-z0-9._~%/-]*", route)
            or "//" in route
            or any(part in {".", ".."} for part in route.split("/"))
        ):
            raise ValueError(f"Unsafe Hugo route for {source}: {route}")
        routes[source] = route
    return routes


def page_entries(changed_files, routes):
    """Deduplicate by rendered URL, not by Markdown filename."""
    unique = sorted({routes[name] for name in changed_files if name in routes})
    return [{"path": route, "image": f"page-{i:03d}.png"} for i, route in enumerate(unique, 1)]


def prepare_manifest():
    changed = changed_content_files(os.environ["PR_BASE_SHA"], os.environ["PR_HEAD_SHA"])
    pages = page_entries(changed, published_routes()) if changed else []
    manifest = {
        "pr_number": int(os.environ["PR_NUMBER"]),
        "head_sha": os.environ["PR_HEAD_SHA"],
        "base_sha": os.environ["PR_BASE_SHA"],
        "checkout_sha": os.environ["PR_CHECKOUT_SHA"],
        "pages": pages,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    print(f"Found {len(pages)} changed, published Hugo pages: {[p['path'] for p in pages]}")


def capture_pages():
    """Only launch a browser after the manifest reports pages to capture."""
    from playwright.sync_api import sync_playwright

    manifest = json.loads((OUTPUT / "manifest.json").read_text(encoding="utf-8"))
    pages = manifest["pages"]
    if not pages:
        return

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            context = browser.new_context(
                viewport={"width": 1440, "height": 900},
                device_scale_factor=1,
                color_scheme="dark",
                reduced_motion="reduce",
            )
            try:
                page = context.new_page()
                for item in pages:
                    url = BASE_URL + item["path"]
                    response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    if not response or response.status >= 400:
                        raise RuntimeError(f"Changed page did not render: {url}")
                    page.locator("body").wait_for(state="visible")
                    page.wait_for_timeout(650)
                    page.screenshot(
                        path=str(OUTPUT / item["image"]),
                        full_page=True,
                        animations="disabled",
                        timeout=30000,
                    )
            finally:
                context.close()
        finally:
            browser.close()
    print(f"Captured {len(pages)} changed pages")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=("prepare", "capture"))
    step = parser.parse_args().step
    if step == "prepare":
        prepare_manifest()
    else:
        capture_pages()


if __name__ == "__main__":
    main()
