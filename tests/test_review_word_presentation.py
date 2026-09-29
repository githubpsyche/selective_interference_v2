"""Check Word presentation and preservation of native review information."""

from collections import Counter
import importlib.util
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W, "m": "http://schemas.openxmlformats.org/officeDocument/2006/math"}


def text(node):
    return "".join(node.xpath(".//w:t/text()", namespaces=NS))


def style(node):
    found = node.find("w:pPr/w:pStyle", NS)
    return found.get(f"{{{W}}}val") if found is not None else "Normal"


class WordPresentationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / "docs/index.docx"
        if not path.exists():
            raise unittest.SkipTest("Render APA Word before checking presentation")
        with ZipFile(path) as archive:
            cls.parts = {name: archive.read(name) for name in archive.namelist()}
        cls.doc = etree.fromstring(cls.parts["word/document.xml"])

    def test_heading_and_bibliography_membership(self):
        references = False
        count = 0
        for p in self.doc.findall("w:body/w:p", NS):
            words, kind = text(p), style(p)
            if words == "Testing Competitor Learning and Retrieval Selectivity":
                self.assertEqual(kind, "Heading2")
            if words.startswith("A dual-list externalized"):
                self.assertFalse(kind.startswith("Heading"))
            if words == "References":
                references = True
            elif words == "Supplementary Material":
                self.assertNotEqual(kind, "Bibliography")
                references = False
            elif references and words.strip():
                self.assertEqual(kind, "Bibliography", words[:70])
                count += 1
        self.assertGreater(count, 50)

    def test_table_and_future_tracking(self):
        settings = etree.fromstring(self.parts["word/settings.xml"])
        flag = settings.find("w:trackRevisions", NS)
        self.assertIsNotNone(flag)
        self.assertNotIn(flag.get(f"{{{W}}}val", "true"), {"0", "false", "off"})
        table = next(t for t in self.doc.findall(".//w:tbl", NS)
                     if [text(c) for c in t.findall("w:tr", NS)[0].findall("w:tc", NS)]
                     == ["Symbol", "Value", "Role"])
        widths = [int(n.get(f"{{{W}}}w")) for n in table.findall("w:tblGrid/w:gridCol", NS)]
        self.assertGreater(widths[2], sum(widths) / 2)
        self.assertLess(widths[0], sum(widths) / 4)
        self.assertIsNotNone(table.find("w:tr/w:trPr/w:tblHeader", NS))
        self.assertTrue(any(style(p) == "TableNote" and text(p).startswith("Note.")
                            for p in self.doc.findall("w:body/w:p", NS)))

    def test_layout_finisher_preserves_text_reviews_and_other_parts(self):
        spec = importlib.util.spec_from_file_location("word_layout", ROOT / "presentation/finish-docx.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        def words(root):
            return root.xpath(".//w:t/text() | .//w:delText/text() | .//m:t/text()", namespaces=NS)

        def reviews(root):
            return Counter((etree.QName(n).localname, n.get(f"{{{W}}}id"),
                            n.get(f"{{{W}}}author"), n.get(f"{{{W}}}date"))
                           for n in root.iter() if etree.QName(n).localname in
                           {"ins", "del", "pPrChange", "rPrChange", "conflictIns", "conflictDel"})

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.docx"
            path.write_bytes((ROOT / "docs/index.docx").read_bytes())
            module.format_document(path)
            first = path.read_bytes()
            module.format_document(path)
            self.assertEqual(path.read_bytes(), first, "Layout finishing must be idempotent")
            with ZipFile(path) as archive:
                for name, content in self.parts.items():
                    if name not in {"word/document.xml", "word/styles.xml"}:
                        self.assertEqual(archive.read(name), content, name)
                after = etree.fromstring(archive.read("word/document.xml"))
                self.assertEqual(words(after), words(self.doc))
                self.assertEqual(reviews(after), reviews(self.doc))
                for para in after.findall(".//w:p", NS):
                    if len(para.findall(".//w:drawing", NS)) > 1:
                        for name in ("keepNext", "keepLines", "widowControl"):
                            flag = para.find(f"w:pPr/w:{name}", NS)
                            self.assertIsNotNone(flag)
                            self.assertEqual(flag.get(f"{{{W}}}val"), "0")
                        self.assertIsNotNone(para.find("w:r/w:br", NS))


if __name__ == "__main__":
    unittest.main()
