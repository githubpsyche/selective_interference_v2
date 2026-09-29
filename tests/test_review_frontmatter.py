"""Regression checks for the regular manuscript HTML review render."""

from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class FrontmatterParser(HTMLParser):
    VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__()
        self.stack = []
        self.deletions = set()
        self.errors = []
        self.authors = 0
        self.reviewed_frontmatter = 0
        self.abstract = 0
        self.abstract_in_title = 0
        self.abstract_in_body = 0
        self.review_starts = set()
        self.suggestion_anchors = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = set(attrs.get("class", "").split())
        if "qr-boundary" in classes and attrs.get("data-review-edge") == "S":
            self.review_starts.add(attrs["data-review-id"])
        if "qr-suggestion" in classes:
            self.suggestion_anchors.add(attrs["data-anchor-id"])
        if "qr-boundary" in classes and attrs.get("data-review-kind") == "D":
            marker = attrs["data-review-id"]
            if attrs.get("data-review-edge") == "S":
                self.deletions.add(marker)
            else:
                self.deletions.discard(marker)
        if "quarto-title-meta-container" in classes or attrs.get("id") in {"abstract", "introduction"}:
            if self.deletions:
                self.errors.append(f"Deletion range crosses {attrs.get('id') or 'native author metadata'}: {self.deletions}")
        if "qr-reviewed-frontmatter" in classes:
            self.reviewed_frontmatter += 1
        if tag == "p" and "author" in classes and any("quarto-title-meta-container" in ancestor for ancestor in self.stack):
            self.authors += 1
        if attrs.get("id") == "abstract":
            self.abstract += 1
            if any("title-block-header" in ancestor for ancestor in self.stack):
                self.abstract_in_title += 1
            if any("quarto-document-content" in ancestor for ancestor in self.stack):
                self.abstract_in_body += 1
        if tag not in self.VOID_TAGS:
            self.stack.append(classes | {attrs.get("id", "")})

    def handle_endtag(self, tag):
        if tag not in self.VOID_TAGS and self.stack:
            self.stack.pop()


class RegularHtmlFrontmatterTest(unittest.TestCase):
    def test_review_ranges_do_not_hide_manuscript_frontmatter(self):
        output = ROOT / "docs/index-regular.html"
        if not output.exists():
            self.skipTest("Render regular HTML before running this check")
        parser = FrontmatterParser()
        parser.feed(output.read_text())
        self.assertEqual(parser.errors, [])
        self.assertEqual(parser.abstract, 1)
        self.assertEqual(parser.abstract_in_title, 0)
        self.assertEqual(parser.abstract_in_body, 1)
        self.assertEqual(parser.authors, 5)
        self.assertEqual(parser.reviewed_frontmatter, 1)
        self.assertTrue(parser.suggestion_anchors, "Suggestion cards missing")
        self.assertEqual(parser.suggestion_anchors - parser.review_starts, set(),
                         "A presentation filter discarded a suggestion's location")


if __name__ == "__main__":
    unittest.main()
