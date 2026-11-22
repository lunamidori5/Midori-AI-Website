"""Smoke-test essential outputs from a production Hugo build."""

from html.parser import HTMLParser
from pathlib import Path


class PageStructure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = set()
        self.in_title = False
        self.title = []

    def handle_starttag(self, tag, attrs):
        self.tags.add(tag)
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)


def main():
    output = Path("public")
    for relative in ("index.html", "about-us/index.html", "index.search.js"):
        file = output / relative
        if not file.is_file() or file.stat().st_size == 0:
            raise SystemExit(f"Missing or empty Hugo output: {file}")

    home = PageStructure()
    home.feed((output / "index.html").read_text(encoding="utf-8"))
    if not {"html", "head", "title", "main"}.issubset(home.tags):
        raise SystemExit("Homepage is missing essential HTML elements")
    if "Midori" not in "".join(home.title):
        raise SystemExit("Homepage title does not contain Midori")
    print("Hugo smoke test passed: homepage, about page, and search index")


if __name__ == "__main__":
    main()
