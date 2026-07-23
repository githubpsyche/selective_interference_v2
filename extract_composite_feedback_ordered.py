#!/usr/bin/env python3
"""Extract DOCX comments and tracked changes in document order.

This is intentionally a source extractor, not a triage tool. It preserves the
order of comments and tracked insertions/deletions from the composite DOCX and
emits Markdown without assessing whether any item is resolved.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}
W = f"{{{NS['w']}}}"


def attr(el: ET.Element, name: str) -> str | None:
    return el.attrib.get(f"{W}{name}")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def quote_block(text: str) -> str:
    text = text.strip()
    if not text:
        return "> "
    return "\n".join(f"> {line}" if line else ">" for line in text.splitlines())


def collect_visible_text(el: ET.Element) -> str:
    parts: list[str] = []

    def rec(node: ET.Element, in_deleted: bool = False) -> None:
        name = local_name(node.tag)
        if name == "del":
            in_deleted = True
        if name == "t" and node.text and not in_deleted:
            parts.append(node.text)
        elif name == "tab" and not in_deleted:
            parts.append("\t")
        elif name == "br" and not in_deleted:
            parts.append("\n")
        for child in node:
            rec(child, in_deleted)

    rec(el)
    return norm("".join(parts))


def collect_all_text(el: ET.Element) -> str:
    parts: list[str] = []
    for node in el.iter():
        name = local_name(node.tag)
        if name in {"t", "delText"} and node.text:
            parts.append(node.text)
        elif name == "tab":
            parts.append("\t")
        elif name == "br":
            parts.append("\n")
    return norm("".join(parts))


def collect_deleted_text(el: ET.Element) -> str:
    parts: list[str] = []
    for node in el.iter():
        name = local_name(node.tag)
        if name == "delText" and node.text:
            parts.append(node.text)
        elif name == "tab":
            parts.append("\t")
        elif name == "br":
            parts.append("\n")
    return norm("".join(parts))


def render_with_tracked_changes(el: ET.Element) -> str:
    parts: list[str] = []

    def rec(node: ET.Element, in_deleted: bool = False) -> None:
        name = local_name(node.tag)
        if name == "ins":
            text = collect_visible_text(node)
            if text:
                parts.append(f"[INS:{text}]")
            return
        if name == "del":
            text = collect_deleted_text(node) or collect_all_text(node)
            if text:
                parts.append(f"[DEL:{text}]")
            return
        if name == "t" and node.text and not in_deleted:
            parts.append(node.text)
        elif name == "tab" and not in_deleted:
            parts.append("\t")
        elif name == "br" and not in_deleted:
            parts.append("\n")
        for child in node:
            rec(child, in_deleted)

    rec(el)
    return norm("".join(parts))


def comment_text(comment_el: ET.Element) -> str:
    paras = []
    for para in comment_el.iter(f"{W}p"):
        text = collect_visible_text(para)
        if text:
            paras.append(text)
    return "\n\n".join(paras)


@dataclass
class CommentInfo:
    comment_id: str
    author: str = ""
    date: str = ""
    initials: str = ""
    body: str = ""


@dataclass
class ParaInfo:
    block_index: int
    style_id: str = ""
    heading: str = ""
    text: str = ""
    tracked_text: str = ""


@dataclass
class ChangeFragment:
    kind: str
    order: int
    change_id: str = ""
    author: str = ""
    date: str = ""
    text: str = ""


@dataclass
class Event:
    kind: str
    block_index: int
    order: int
    heading: str
    paragraph_text: str
    paragraph_tracked_text: str
    comment_id: str | None = None
    selected_text: str = ""
    comment_author: str = ""
    comment_date: str = ""
    comment_body: str = ""
    change_fragments: list[ChangeFragment] = field(default_factory=list)


@dataclass
class Extraction:
    comments: dict[str, CommentInfo]
    events: list[Event] = field(default_factory=list)
    referenced_comment_ids: set[str] = field(default_factory=set)
    anchored_comment_ids: set[str] = field(default_factory=set)
    paragraph_count: int = 0
    comment_reference_count: int = 0
    tracked_insertion_count: int = 0
    tracked_deletion_count: int = 0


def read_comments(zipf: zipfile.ZipFile) -> dict[str, CommentInfo]:
    try:
        root = ET.fromstring(zipf.read("word/comments.xml"))
    except KeyError:
        return {}

    comments: dict[str, CommentInfo] = {}
    for el in root.findall(f"{W}comment"):
        comment_id = attr(el, "id")
        if comment_id is None:
            continue
        comments[comment_id] = CommentInfo(
            comment_id=comment_id,
            author=attr(el, "author") or "",
            date=attr(el, "date") or "",
            initials=attr(el, "initials") or "",
            body=comment_text(el),
        )
    return comments


def heading_level(style_id: str) -> int | None:
    match = re.search(r"Heading(\d+)$", style_id or "")
    if match:
        return int(match.group(1))
    match = re.search(r"heading(\d+)$", style_id or "", re.I)
    if match:
        return int(match.group(1))
    return None


def paragraph_style(para: ET.Element) -> str:
    p_style = para.find(f"./{W}pPr/{W}pStyle")
    return attr(p_style, "val") if p_style is not None else ""


def update_heading_stack(stack: list[tuple[int, str]], style_id: str, text: str) -> None:
    level = heading_level(style_id)
    if level is None or not text:
        return
    while stack and stack[-1][0] >= level:
        stack.pop()
    stack.append((level, text))


def heading_path(stack: list[tuple[int, str]]) -> str:
    return " > ".join(text for _, text in stack)


def extract_events(docx_path: Path) -> Extraction:
    with zipfile.ZipFile(docx_path) as zipf:
        comments = read_comments(zipf)
        root = ET.fromstring(zipf.read("word/document.xml"))

    extraction = Extraction(comments=comments)
    heading_stack: list[tuple[int, str]] = []
    comment_selected_text: dict[str, list[str]] = {}
    comment_event: dict[str, Event] = {}
    active_comments: list[str] = []
    order_counter = 0

    def next_order() -> int:
        nonlocal order_counter
        order_counter += 1
        return order_counter

    paragraphs = list(root.iter(f"{W}p"))
    extraction.paragraph_count = len(paragraphs)

    for block_index, para in enumerate(paragraphs, start=1):
        style_id = paragraph_style(para)
        text = collect_visible_text(para)
        tracked_text = render_with_tracked_changes(para)
        update_heading_stack(heading_stack, style_id, text)
        current_heading = heading_path(heading_stack)

        def add_comment_event(comment_id: str, order: int) -> None:
            if comment_id in comment_event:
                return
            info = comments.get(comment_id, CommentInfo(comment_id=comment_id))
            event = Event(
                kind="comment",
                block_index=block_index,
                order=order,
                heading=current_heading,
                paragraph_text=text,
                paragraph_tracked_text=tracked_text,
                comment_id=comment_id,
                comment_author=info.author,
                comment_date=info.date,
                comment_body=info.body,
            )
            comment_event[comment_id] = event
            extraction.events.append(event)

        change_fragments: list[ChangeFragment] = []
        first_change_order: int | None = None

        def record_change(node: ET.Element, kind: str, order: int) -> None:
            nonlocal first_change_order
            if kind == "tracked insertion":
                change_text = collect_visible_text(node)
                extraction.tracked_insertion_count += 1
            else:
                change_text = collect_deleted_text(node) or collect_all_text(node)
                extraction.tracked_deletion_count += 1
            if not change_text:
                return
            if first_change_order is None:
                first_change_order = order
            change_fragments.append(
                ChangeFragment(
                    kind=kind,
                    order=order,
                    change_id=attr(node, "id") or "",
                    author=attr(node, "author") or "",
                    date=attr(node, "date") or "",
                    text=change_text,
                )
            )

        def add_text_to_active(value: str) -> None:
            if not value:
                return
            for comment_id in active_comments:
                comment_selected_text.setdefault(comment_id, []).append(value)

        def walk(node: ET.Element, in_deleted: bool = False) -> None:
            name = local_name(node.tag)
            if name == "commentRangeStart":
                comment_id = attr(node, "id")
                if comment_id is not None:
                    extraction.anchored_comment_ids.add(comment_id)
                    extraction.referenced_comment_ids.add(comment_id)
                    active_comments.append(comment_id)
                    add_comment_event(comment_id, next_order())
                return
            if name == "commentRangeEnd":
                comment_id = attr(node, "id")
                if comment_id in active_comments:
                    active_comments.remove(comment_id)
                return
            if name == "commentReference":
                comment_id = attr(node, "id")
                if comment_id is not None:
                    extraction.referenced_comment_ids.add(comment_id)
                    extraction.comment_reference_count += 1
                    add_comment_event(comment_id, next_order())
                return
            if name == "ins":
                record_change(node, "tracked insertion", next_order())
                for child in node:
                    walk(child, in_deleted=in_deleted)
                return
            if name == "del":
                record_change(node, "tracked deletion", next_order())
                for child in node:
                    walk(child, in_deleted=True)
                return
            if name in {"t", "delText"}:
                add_text_to_active(node.text or "")
                return
            if name == "tab":
                add_text_to_active("\t")
                return
            if name == "br":
                add_text_to_active("\n")
                return
            for child in node:
                walk(child, in_deleted=in_deleted)

        walk(para)
        if change_fragments and first_change_order is not None:
            extraction.events.append(
                Event(
                    kind="tracked changes",
                    block_index=block_index,
                    order=first_change_order,
                    heading=current_heading,
                    paragraph_text=text,
                    paragraph_tracked_text=tracked_text,
                    change_fragments=change_fragments,
                )
            )

    for comment_id, chunks in comment_selected_text.items():
        if comment_id in comment_event:
            comment_event[comment_id].selected_text = norm("".join(chunks))

    extraction.events.sort(key=lambda ev: (ev.block_index, ev.order))
    return extraction


def write_markdown(extraction: Extraction, docx_path: Path, output_path: Path) -> None:
    now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    lines: list[str] = []
    lines.append("# Composite Feedback Ordered Extraction")
    lines.append("")
    lines.append(f"Source: `{docx_path}`")
    lines.append(f"Generated: `{now}`")
    lines.append("")
    lines.append(
        "This file preserves feedback order from the composite DOCX. It is not "
        "a triage memo and does not assess whether items are resolved."
    )
    lines.append("")
    lines.append("## Extraction Notes")
    lines.append("")
    lines.append("- Comments are extracted from DOCX comment anchors and references.")
    lines.append("- Tracked insertions and deletions are extracted from `w:ins` and `w:del` elements.")
    lines.append("- Items are listed in DOCX paragraph order.")
    lines.append("- Paragraph context includes tracked-change markers only when tracked changes are present in that paragraph.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Paragraphs scanned: {extraction.paragraph_count}")
    lines.append(f"- Comments in `comments.xml`: {len(extraction.comments)}")
    lines.append(f"- Comment references found in `document.xml`: {extraction.comment_reference_count}")
    lines.append(f"- Tracked insertions found: {extraction.tracked_insertion_count}")
    lines.append(f"- Tracked deletions found: {extraction.tracked_deletion_count}")
    orphan_comments = sorted(set(extraction.comments) - extraction.referenced_comment_ids, key=lambda x: int(x) if x.isdigit() else x)
    if orphan_comments:
        lines.append(f"- Comments not referenced in `document.xml`: {', '.join(orphan_comments)}")
    else:
        lines.append("- Comments not referenced in `document.xml`: none")
    lines.append("")
    lines.append("## Items")
    lines.append("")

    for idx, ev in enumerate(extraction.events, start=1):
        lines.append(f"### CF-{idx:04d}")
        lines.append("")
        lines.append(f"- Type: {ev.kind}")
        lines.append(f"- DOCX paragraph index: {ev.block_index}")
        if ev.heading:
            lines.append(f"- Section: {ev.heading}")
        if ev.kind == "comment":
            lines.append(f"- Comment id: `{ev.comment_id}`")
            if ev.comment_author:
                lines.append(f"- Author: {ev.comment_author}")
            if ev.comment_date:
                lines.append(f"- Date: {ev.comment_date}")
            lines.append("")
            lines.append("- Selected text:")
            lines.append(quote_block(ev.selected_text))
            lines.append("")
            lines.append("- Comment:")
            lines.append(quote_block(ev.comment_body))
        else:
            insertions = [frag for frag in ev.change_fragments if frag.kind == "tracked insertion"]
            deletions = [frag for frag in ev.change_fragments if frag.kind == "tracked deletion"]
            lines.append(f"- Tracked insertion fragments: {len(insertions)}")
            lines.append(f"- Tracked deletion fragments: {len(deletions)}")
            if insertions:
                lines.append("")
                lines.append("- Inserted text fragments:")
                for frag in insertions:
                    meta = []
                    if frag.change_id:
                        meta.append(f"id `{frag.change_id}`")
                    if frag.author:
                        meta.append(frag.author)
                    if frag.date:
                        meta.append(frag.date)
                    suffix = f" ({'; '.join(meta)})" if meta else ""
                    lines.append(f"  - Insertion{suffix}:")
                    lines.append("\n".join(f"    {line}" for line in quote_block(frag.text).splitlines()))
            if deletions:
                lines.append("")
                lines.append("- Deleted text fragments:")
                for frag in deletions:
                    meta = []
                    if frag.change_id:
                        meta.append(f"id `{frag.change_id}`")
                    if frag.author:
                        meta.append(frag.author)
                    if frag.date:
                        meta.append(frag.date)
                    suffix = f" ({'; '.join(meta)})" if meta else ""
                    lines.append(f"  - Deletion{suffix}:")
                    lines.append("\n".join(f"    {line}" for line in quote_block(frag.text).splitlines()))
        lines.append("")
        if ev.paragraph_tracked_text and ev.paragraph_tracked_text != ev.paragraph_text:
            lines.append("- Paragraph context with tracked changes:")
            lines.append(quote_block(ev.paragraph_tracked_text))
        else:
            lines.append("- Paragraph context:")
            lines.append(quote_block(ev.paragraph_text))
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "docx",
        nargs="?",
        default="notes/advisor_feedback_composite_0630_intro_0703_model.docx",
        type=Path,
        help="Composite DOCX to extract",
    )
    parser.add_argument(
        "--output",
        default="notes/composite_feedback_ordered.md",
        type=Path,
        help="Markdown output path",
    )
    args = parser.parse_args()
    extraction = extract_events(args.docx)
    write_markdown(extraction, args.docx, args.output)
    print(f"Wrote {args.output}")
    print(f"Items: {len(extraction.events)}")
    print(f"Comments: {len(extraction.comments)}")
    print(f"Tracked insertions: {extraction.tracked_insertion_count}")
    print(f"Tracked deletions: {extraction.tracked_deletion_count}")
    orphan_comments = sorted(set(extraction.comments) - extraction.referenced_comment_ids)
    if orphan_comments:
        print(f"Unreferenced comments: {', '.join(orphan_comments)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
