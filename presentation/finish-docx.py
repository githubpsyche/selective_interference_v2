"""Apply the manuscript's APA Word layout after native review records are restored.

Only layout properties change. Text, review elements and comment parts are retained.
The review render hash is updated so repeated finishing remains idempotent.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile


def format_document(path: Path) -> None:
    from lxml import etree

    w = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    wp = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
    a = "http://schemas.openxmlformats.org/drawingml/2006/main"
    ns = {"w": w, "wp": wp, "a": a}
    q = lambda name: f"{{{w}}}{name}"
    with ZipFile(path) as archive:
        infos = archive.infolist()
        parts = {info.filename: archive.read(info.filename) for info in infos}
        comment = archive.comment
    doc = etree.fromstring(parts["word/document.xml"])
    styles = etree.fromstring(parts["word/styles.xml"])

    def child(parent, name, first=False):
        node = parent.find(q(name))
        if node is None:
            node = etree.Element(q(name))
            parent.insert(0, node) if first else parent.append(node)
        return node

    def value(parent, name, val):
        child(parent, name).set(q("val"), str(val))

    for style in styles.findall("w:style", ns):
        sid = style.get(q("styleId"))
        if sid in {"FigureTitle", "Caption"}:
            props = child(style, "pPr")
            value(props, "keepNext", 1)
            value(props, "keepLines", 1)
            spacing = child(props, "spacing")
            spacing.set(q("line"), "240")
            spacing.set(q("lineRule"), "auto")
            spacing.set(q("after"), "120")
        if sid == "TableNote":
            props = child(style, "pPr")
            value(props, "keepNext", 0)
            value(props, "keepLines", 0)
            child(props, "ind").set(q("firstLine"), "0")
            spacing = child(props, "spacing")
            spacing.set(q("line"), "240")
            spacing.set(q("lineRule"), "auto")
            spacing.set(q("after"), "240")

    section = doc.find(".//w:sectPr", ns)
    page = section.find("w:pgSz", ns)
    margins = section.find("w:pgMar", ns)
    width = int(page.get(q("w"))) - sum(int(margins.get(q(x), "0")) for x in ("left", "right", "gutter"))
    for table in doc.findall(".//w:tbl", ns):
        first = table.find("w:tr", ns)
        headers = ["".join(cell.itertext()).strip() for cell in first.findall("w:tc", ns)]
        if headers != ["Symbol", "Value", "Role"]:
            continue
        widths = [round(width * .16), round(width * .20)]
        widths.append(width - sum(widths))
        grid = table.find("w:tblGrid", ns)
        for col, target in zip(grid, widths, strict=True):
            col.set(q("w"), str(target))
        for row in table.findall("w:tr", ns):
            value(child(row, "trPr", first=True), "cantSplit", 1)
            for col, cell in enumerate(row.findall("w:tc", ns)):
                cellwidth = child(child(cell, "tcPr", first=True), "tcW")
                cellwidth.set(q("w"), str(widths[col]))
                cellwidth.set(q("type"), "dxa")
                cellprops = child(cell, "tcPr", first=True)
                value(cellprops, "vAlign", "center")
                padding = child(cellprops, "tcMar")
                for side in ("left", "right"):
                    margin = child(padding, side)
                    margin.set(q("w"), "100")
                    margin.set(q("type"), "dxa")
                for para in cell.findall("w:p", ns):
                    props = child(para, "pPr", first=True)
                    value(props, "keepNext", 0)
                    value(props, "keepLines", 1)
                    value(props, "jc", "right" if col == 1 else "left")
                    indent = child(props, "ind")
                    for name in ("left", "right", "firstLine", "hanging"):
                        indent.set(q(name), "0")
                    spacing = child(props, "spacing")
                    for name, val in {"before": "0", "after": "80", "line": "240", "lineRule": "auto"}.items():
                        spacing.set(q(name), val)

    # Preserve the accepted figure order and each before/after picture.
    # Allow a redline picture pair to flow across pages instead of treating
    # both full-size drawings as an indivisible paragraph.
    max_width = width * 635
    max_height = 5.8 * 914400
    for para in doc.findall(".//w:p", ns):
        drawings = para.findall(".//w:drawing", ns)
        if not drawings:
            continue
        props = child(para, "pPr", first=True)
        value(props, "keepNext", 0)
        value(props, "keepLines", 0)
        # Each image is an entire line. Default widow/orphan control would
        # keep a two-image revision pair together despite keepLines=false.
        value(props, "widowControl", 0)
        if len(drawings) > 1 and not any(
            (node.text or "").strip() for node in para.findall(".//w:t", ns)
        ):
            picture_runs = [node for node in para if node.find(".//w:drawing", ns) is not None]
            for node in picture_runs[1:]:
                previous = node.getprevious()
                if previous is None or previous.find("w:br", ns) is None:
                    line = etree.Element(q("r"))
                    etree.SubElement(line, q("br"))
                    node.addprevious(line)
        for drawing in drawings:
            extent = drawing.find(".//wp:extent", ns)
            if extent is None:
                continue
            cx, cy = int(extent.get("cx")), int(extent.get("cy"))
            scale = min(1, max_width / cx, max_height / cy)
            if scale < 1:
                for size in [extent, *drawing.findall(".//a:xfrm/a:ext", ns)]:
                    size.set("cx", str(round(cx * scale)))
                    size.set("cy", str(round(cy * scale)))

    # Preserve OOXML property ordering when adding layout controls to imported
    # paragraphs and template styles. pPrChange remains last, if present.
    order = """pStyle keepNext keepLines pageBreakBefore framePr widowControl
numPr suppressLineNumbers pBdr shd tabs suppressAutoHyphens kinsoku wordWrap
overflowPunct topLinePunct autoSpaceDE autoSpaceDN bidi adjustRightInd snapToGrid
spacing ind contextualSpacing mirrorIndents suppressOverlap jc textDirection
textAlignment textboxTightWrap outlineLvl divId cnfStyle rPr sectPr pPrChange""".split()
    ranks = {name: i for i, name in enumerate(order)}
    for root in (doc, styles):
        for props in root.findall(".//w:pPr", ns):
            props[:] = sorted(props, key=lambda n: ranks.get(etree.QName(n).localname, len(order)))
    for kind, names in {
        "tcPr": "cnfStyle tcW gridSpan hMerge vMerge tcBorders shd noWrap tcMar textDirection tcFitText vAlign hideMark headers cellIns cellDel cellMerge tcPrChange",
        "trPr": "cnfStyle divIdBefore divIdAfter wBefore wAfter gridBefore gridAfter cantSplit trHeight tblHeader tblCellSpacing jc hidden ins del trPrChange",
    }.items():
        ranks = {name: i for i, name in enumerate(names.split())}
        for props in doc.findall(f".//w:{kind}", ns):
            props[:] = sorted(props, key=lambda n: ranks.get(etree.QName(n).localname, len(ranks)))

    for name, root in [("word/document.xml", doc), ("word/styles.xml", styles)]:
        parts[name] = etree.tostring(root, encoding="UTF-8", xml_declaration=True, standalone=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, suffix=".docx", delete=False) as tmp:
        temporary = Path(tmp.name)
    try:
        with ZipFile(temporary, "w") as archive:
            archive.comment = comment
            for info in infos:
                archive.writestr(info, parts[info.filename])
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def finish_outputs() -> None:
    root = Path(os.environ["QUARTO_REVIEW_PROJECT"]).resolve()
    plans = root / ".quarto/review/plans"
    for name in os.environ["QUARTO_PROJECT_OUTPUT_FILES"].splitlines():
        path = (root / name).resolve()
        if path.suffix.lower() != ".docx":
            continue
        if not path.is_relative_to(root):
            raise ValueError("Word output must be inside the project")
        matches = [(p, json.loads(p.read_text())) for p in plans.glob("*.json")]
        matches = [(p, r) for p, r in matches if Path(r["output"]).name == path.name]
        if len(matches) != 1:
            raise ValueError("Expected one Word review render record")
        plan, record = matches[0]
        if record.get("finished_hash") != hashlib.sha256(path.read_bytes()).hexdigest():
            raise ValueError("Native review finishing must run before Word presentation")
        format_document(path)
        record["finished_hash"] = hashlib.sha256(path.read_bytes()).hexdigest()
        plan.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    if "--apply" in sys.argv:
        finish_outputs()
    else:
        runtime = Path(os.environ["QUARTO_REVIEW_COMMAND"]).parent / "python"
        subprocess.run([str(runtime), "-B", __file__, "--apply"], check=True)
