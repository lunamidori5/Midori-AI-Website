"""Smoke-test essential outputs from a production Hugo build."""

from html.parser import HTMLParser
from pathlib import Path


class PageStructure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = set()
        self.in_main = False
        self.main_text = []

    def handle_starttag(self, tag, attrs):
        self.tags.add(tag)
        if tag == "main":
            self.in_main = True

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False

    def handle_data(self, data):
        if self.in_main:
            self.main_text.append(data)


def check_build(output=Path("public")):
    for relative in ("index.html", "index.search.js"):
        file = output / relative
        if not file.is_file() or file.stat().st_size == 0:
            raise ValueError(f"Missing or empty Hugo output: {file}")

    home = PageStructure()
    home.feed((output / "index.html").read_text(encoding="utf-8"))
    if not {"html", "head", "main"}.issubset(home.tags):
        raise ValueError("Homepage is missing essential HTML elements")
    if not "".join(home.main_text).strip():
        raise ValueError("Homepage main content is empty")
    if not any(path != output / "index.html" for path in output.rglob("index.html")):
        raise ValueError("No rendered documentation pages were found")


def main():
    try:
        check_build()
    except ValueError as error:
        raise SystemExit(str(error)) from error
    print("Hugo smoke test passed: homepage, content pages, and search index")


if __name__ == "__main__":
    main()
