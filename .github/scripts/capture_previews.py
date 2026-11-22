"""Capture three Hugo PR screenshots in a read-only CI job."""

import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:1313"
OUTPUT = Path("pr-preview")


def changed_content_route():
    """Find a changed Hugo Markdown page; fall back to the About page."""
    diff = subprocess.run(
        ["git", "diff", "--name-only", "HEAD^1", "HEAD", "--", "content/"],
        capture_output=True,
        text=True,
        check=False,
    )
    if diff.returncode != 0:
        return "/about-us/"

    for filename in diff.stdout.splitlines():
        source = Path(filename)
        if source.suffix.lower() != ".md" or source.parts[0] != "content":
            continue
        pieces = list(source.with_suffix("").parts[1:])
        if pieces and pieces[-1] in {"_index", "index"}:
            pieces.pop()
        if not pieces:
            continue  # the homepage is already captured twice
        route = "/" + "/".join(pieces) + "/"
        if re.fullmatch(r"/[a-zA-Z0-9_/-]{1,140}/", route):
            return route
    return "/about-us/"


def capture(browser, filename, route, viewport, mobile=False):
    context = browser.new_context(
        viewport=viewport,
        device_scale_factor=1,
        is_mobile=mobile,
        color_scheme="dark",
        reduced_motion="reduce",
    )
    try:
        page = context.new_page()
        url = BASE_URL + quote(route, safe="/")
        response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
        if not response or response.status >= 400:
            raise RuntimeError(f"Hugo returned an invalid response for {url}")
        page.locator("body").wait_for(state="visible")
        page.wait_for_timeout(650)
        page.screenshot(
            path=str(OUTPUT / filename),
            full_page=True,
            animations="disabled",
            timeout=30000,
        )
    finally:
        context.close()


def main():
    OUTPUT.mkdir(exist_ok=True)
    route = changed_content_route()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            capture(browser, "desktop-home.png", "/", {"width": 1440, "height": 900})
            capture(browser, "mobile-home.png", "/", {"width": 390, "height": 844}, mobile=True)
            try:
                capture(browser, "changed-page.png", route, {"width": 1440, "height": 900})
            except RuntimeError:
                route = "/about-us/"
                capture(browser, "changed-page.png", route, {"width": 1440, "height": 900})
        finally:
            browser.close()

    manifest = {
        "pr_number": int(os.environ["PR_NUMBER"]),
        "head_sha": os.environ["PR_HEAD_SHA"],
        "page_path": route,
    }
    (OUTPUT / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    print(f"Captured desktop, mobile, and {route} for PR #{manifest['pr_number']}")


if __name__ == "__main__":
    main()
