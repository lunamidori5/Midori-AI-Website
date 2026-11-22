"""Regression tests for changed-page selection, publication, and smoke checks."""

import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import capture_previews  # noqa: E402
import check_build  # noqa: E402
import publish_previews  # noqa: E402


class ChangedPageTests(unittest.TestCase):
    def test_diff_uses_full_pr_merge_base_and_excludes_deleted_files(self):
        base, head = "a" * 40, "b" * 40
        with patch.object(capture_previews.subprocess, "run") as run:
            run.return_value = SimpleNamespace(
                stdout=(
                    b"content/_index.md\0content/guide.md\0"
                    b"content/another/_index.md\0static/other.png\0"
                )
            )
            changed = capture_previews.changed_content_files(base, head)
        self.assertEqual(
            changed,
            ["content/_index.md", "content/another/_index.md", "content/guide.md"],
        )
        args = run.call_args.args[0]
        self.assertIn(f"{base}...{head}", args)
        self.assertIn("--diff-filter=ACMR", args)
        self.assertNotIn("HEAD^1", args)

    def test_exact_urls_and_one_screenshot_per_page(self):
        changed = ["content/_index.md", "content/guide.md", "content/other.md"]
        inventory = {
            "content/_index.md": "/",
            "content/guide.md": "/renamed-guide/",
            "content/other.md": "/renamed-guide/",
        }
        self.assertEqual(
            capture_previews.page_entries(changed, inventory),
            [
                {"path": "/", "image": "page-001.png"},
                {"path": "/renamed-guide/", "image": "page-002.png"},
            ],
        )

    def test_unpublished_or_deleted_page_is_not_captured(self):
        self.assertEqual(
            capture_previews.page_entries(
                ["content/deleted.md", "content/draft.md", "content/about.md"],
                {"content/about.md": "/about/"},
            ),
            [{"path": "/about/", "image": "page-001.png"}],
        )
        self.assertEqual(capture_previews.page_entries([], {"content/about.md": "/about/"}), [])

    def test_hugo_permalink_is_authoritative(self):
        listing = (
            "path,slug,title,date,expiryDate,publishDate,draft,permalink\n"
            "content/_index.md,,Home,,,,false,http://127.0.0.1:1313/\n"
            "content/guide.md,custom,Guide,,,,false,http://127.0.0.1:1313/custom/\n"
        )
        with patch.object(capture_previews.subprocess, "run") as run:
            run.return_value = SimpleNamespace(stdout=listing)
            routes = capture_previews.published_routes()
        self.assertEqual(routes["content/guide.md"], "/custom/")
        self.assertEqual(routes["content/_index.md"], "/")


class PublisherTests(unittest.TestCase):
    def test_manifest_accepts_merge_sha_and_multiple_pages(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            payload = {
                "pr_number": 7,
                "head_sha": "a" * 40,
                "base_sha": "b" * 40,
                "checkout_sha": "c" * 40,
                "pages": [
                    {"path": "/", "image": "page-001.png"},
                    {"path": "/docs/", "image": "page-002.png"},
                ],
            }
            (folder / "manifest.json").write_text(json.dumps(payload), encoding="utf-8")
            number, head, base, pages = publish_previews.validated_manifest(folder, "c" * 40)
            self.assertEqual((number, head, base), (7, "a" * 40, "b" * 40))
            self.assertEqual(len(pages), 2)
            payload["pages"].append({"path": "/docs/", "image": "page-003.png"})
            (folder / "manifest.json").write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                publish_previews.validated_manifest(folder, "c" * 40)

    def test_no_changed_pages_means_no_png_required(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            self.assertEqual(publish_previews.validated_images(folder, []), {})
            (folder / "stale.png").write_bytes(b"bad")
            with self.assertRaisesRegex(ValueError, "do not match"):
                publish_previews.validated_images(folder, [])

    def test_one_image_per_manifest_entry_and_no_extras(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            png = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" + struct.pack(">II", 1440, 900) + b"x" * 24
            (folder / "page-001.png").write_bytes(png)
            pages = [{"path": "/", "image": "page-001.png"}]
            self.assertEqual(publish_previews.validated_images(folder, pages), {"page-001.png": png})
            with self.assertRaisesRegex(ValueError, "do not match"):
                publish_previews.validated_images(folder, pages + [{"image": "page-002.png"}])

    def test_workflow_run_must_belong_to_target_pr(self):
        pr = {
            "head": {"sha": "a" * 40},
            "merge_commit_sha": "c" * 40,
        }
        with patch.object(publish_previews, "api") as api:
            api.return_value = {
                "event": "pull_request",
                "conclusion": "success",
                "name": "PR site screenshots",
                "head_sha": "c" * 40,
                "pull_requests": [{"number": 8, "head": {"sha": "a" * 40}}],
            }
            self.assertFalse(publish_previews.run_matches_pr("owner/repo", 11, 7, pr, "c" * 40))
            api.return_value["pull_requests"][0]["number"] = 7
            self.assertTrue(publish_previews.run_matches_pr("owner/repo", 11, 7, pr, "c" * 40))

    def test_empty_page_list_removes_old_comment(self):
        with patch.object(publish_previews, "existing_comment", return_value={"id": 5}):
            with patch.object(publish_previews, "api") as api:
                publish_previews.update_comment("owner/repo", 7, "a" * 40, [], 11)
        api.assert_called_once_with("DELETE", "/repos/owner/repo/issues/comments/5")

    def test_changed_pages_render_once_in_same_comment(self):
        with patch.object(publish_previews, "existing_comment", return_value=None):
            with patch.object(publish_previews, "api") as api:
                publish_previews.update_comment(
                    "owner/repo", 7, "a" * 40,
                    [
                        {"path": "/about/", "image": "page-001.png"},
                        {"path": "/docs/", "image": "page-002.png"},
                    ],
                    11,
                )
        body = api.call_args.args[2]["body"]
        self.assertEqual(body.count("![Preview of"), 2)
        self.assertNotIn("Mobile homepage", body)


class HugoSmokeTests(unittest.TestCase):
    def test_nonempty_title_passes_without_brand_assumption(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs/index.html").write_text("<html>Docs</html>", encoding="utf-8")
            (root / "index.search.js").write_text("var index = {};", encoding="utf-8")
            (root / "index.html").write_text(
                "<html><head><title>Totally different title</title></head>"
                "<body><main>Content</main></body></html>", encoding="utf-8",
            )
            check_build.check_build(root)
            (root / "index.html").write_text(
                "<html><head><title> </title></head><body><main></main></body></html>",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "title is empty"):
                check_build.check_build(root)


if __name__ == "__main__":
    unittest.main()
