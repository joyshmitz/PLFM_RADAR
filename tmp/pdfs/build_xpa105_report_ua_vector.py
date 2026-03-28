#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from reportlab.lib.colors import HexColor, white
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfgen import canvas
except ModuleNotFoundError as exc:
    raise SystemExit(
        "build_xpa105_report_ua_vector.py requires reportlab. "
        "Install it with `uv pip install reportlab` or use the canonical "
        "generator tmp/pdfs/build_xpa105_report_ua.py instead."
    ) from exc


PROJECT_ROOT = Path(__file__).resolve().parents[2]
# Experimental preview renderer only. The canonical published report generator is
# tmp/pdfs/build_xpa105_report_ua.py, which owns docs/XPA-105_Antenna_Report_ua.pdf.
LEGACY_PATH = PROJECT_ROOT / "tmp" / "pdfs" / "build_xpa105_report_ua.py"
INPUT_PDF = PROJECT_ROOT / "docs" / "XPA-105_Antenna_Report_en.pdf"
OUTPUT_PDF = PROJECT_ROOT / "tmp" / "pdfs" / "previews" / "XPA-105_Antenna_Report_ua_vector_preview.pdf"
IMAGE_DIR = PROJECT_ROOT / "tmp" / "pdfs" / "extracted"
PRODUCT_FAMILY = "XPA-105"
PRODUCT_FAMILY_FOOTER = "XPA-105 family"
PRODUCT_VARIANT_816 = "XPA-105 8x16"
PRODUCT_VARIANT_3216 = "XPA-105 32x16"

PAGE_W, PAGE_H = letter
LEFT = 56
RIGHT = 56
CONTENT_W = PAGE_W - LEFT - RIGHT

BLUE = HexColor("#2b3f67")
MID_BLUE = HexColor("#405a8a")
GRID = HexColor("#cfd7e5")
TEXT = HexColor("#29364b")
MUTED = HexColor("#6b778c")

def to_color(value: str):
    if value == "white":
        return white
    return HexColor(value)


def brand_text(text: str) -> str:
    replacements = [
        ("XPA-105 Radar Systems", PRODUCT_FAMILY_FOOTER),
        ("XPA-105 32x16", PRODUCT_VARIANT_3216),
        ("XPA-105 8x16", PRODUCT_VARIANT_816),
        ("XPA-105", PRODUCT_FAMILY),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def load_legacy_module():
    spec = importlib.util.spec_from_file_location("xpa105_legacy", LEGACY_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load legacy script: {LEGACY_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def font_for(size: float, weight: str) -> str:
    if weight == "700":
        return "Helvetica-Bold"
    if size >= 12:
        return "Helvetica"
    if size <= 9.3:
        return "Helvetica"
    return "Times-Roman"


def split_long_word(word: str, width: float, font_name: str, font_size: float) -> list[str]:
    pieces: list[str] = []
    current = ""
    for ch in word:
        test = current + ch
        if current and pdfmetrics.stringWidth(test, font_name, font_size) > width:
            pieces.append(current)
            current = ch
        else:
            current = test
    if current:
        pieces.append(current)
    return pieces or [word]


def wrap_text(content: str, width: float, font_name: str, font_size: float) -> list[str]:
    lines: list[str] = []
    for paragraph in content.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        words: list[str] = []
        for word in paragraph.split():
            if pdfmetrics.stringWidth(word, font_name, font_size) <= width:
                words.append(word)
            else:
                words.extend(split_long_word(word, width, font_name, font_size))
        current = ""
        for word in words:
            test = word if not current else f"{current} {word}"
            if current and pdfmetrics.stringWidth(test, font_name, font_size) > width:
                lines.append(current)
                current = word
            else:
                current = test
        if current:
            lines.append(current)
    return lines or [""]


@dataclass
class TextOp:
    x: float
    y: float
    width: float
    lines: list[str]
    font_name: str
    font_size: float
    line_height: float
    color: object
    align: str


class VectorPage:
    def __init__(self, number: int, title: str | None = None):
        self.number = number
        self.cursor = 94
        self.ops: list[tuple[str, object]] = []
        if title:
            self.line(LEFT, 58, PAGE_W - RIGHT, 58, "#2b3f67", 3)
            self.text(LEFT, 82, CONTENT_W, title, 18, color="#2b3f67", weight="700")
            self.cursor = 112

    def line(self, x1: float, y1: float, x2: float, y2: float, color: str = "#cfd7e5", width: float = 1) -> None:
        self.ops.append(("line", (x1, y1, x2, y2, to_color(color), width)))

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: str = "none",
        stroke: str = "#cfd7e5",
        stroke_width: float = 1,
        rx: float = 0,
    ) -> None:
        fill_color = None if fill == "none" else to_color(fill)
        self.ops.append(("rect", (x, y, w, h, fill_color, to_color(stroke), stroke_width, rx)))

    def text(
        self,
        x: float,
        y: float,
        width: float,
        content: str,
        size: float,
        *,
        color: str = "#29364b",
        weight: str = "400",
        align: str = "left",
        line_height: float | None = None,
    ) -> float:
        content = brand_text(content)
        font_name = font_for(size, weight)
        lh = line_height or size * 1.28
        lines = wrap_text(content, width, font_name, size)
        self.ops.append(
            (
                "text",
                TextOp(
                    x=x,
                    y=y,
                    width=width,
                    lines=lines,
                    font_name=font_name,
                    font_size=size,
                    line_height=lh,
                    color=to_color(color),
                    align=align,
                ),
            )
        )
        return y + lh * len(lines)

    def paragraph(self, content: str, size: float = 10.2, gap_after: float = 12) -> None:
        self.cursor = self.text(LEFT, self.cursor, CONTENT_W, content, size) + gap_after

    def section(self, heading: str, size: float = 13.5, gap_after: float = 8) -> None:
        self.cursor = self.text(LEFT, self.cursor, CONTENT_W, heading, size, color="#405a8a", weight="700") + gap_after

    def image(self, path: Path, width: float, gap_after: float = 10):
        from PIL import Image

        with Image.open(path) as img:
            img_w, img_h = img.size
        height = width * img_h / img_w
        x = LEFT + (CONTENT_W - width) / 2
        self.ops.append(("image", (path, x, self.cursor, width, height)))
        self.cursor += height + gap_after
        return width, height

    def caption(self, content: str, size: float = 8.5, gap_after: float = 10) -> None:
        self.cursor = self.text(LEFT, self.cursor, CONTENT_W, content, size, color="#6b778c", align="center") + gap_after

    def callout(self, content: str, size: float = 9.2, gap_after: float = 12) -> None:
        font_name = font_for(size, "400")
        lines = wrap_text(content, CONTENT_W - 16, font_name, size)
        line_height = size * 1.28
        height = 8 + len(lines) * line_height + 8
        y = self.cursor
        self.rect(LEFT, y, CONTENT_W, height, fill="#f4fbf6", stroke="#43b96d", stroke_width=1.5, rx=4)
        self.text(LEFT + 8, y + 14, CONTENT_W - 16, content, size, color="#29364b")
        self.cursor += height + gap_after

    def table(
        self,
        headers,
        rows,
        col_fracs,
        *,
        font_size: float = 8.9,
        header_font_size: float | None = None,
        aligns=None,
        gap_after: float = 12,
    ) -> None:
        header_size = header_font_size or font_size
        col_widths = [CONTENT_W * frac for frac in col_fracs]
        x_positions = [LEFT]
        for w in col_widths[:-1]:
            x_positions.append(x_positions[-1] + w)
        aligns = aligns or ["left"] * len(headers)
        padding_x = 6
        padding_y = 6

        def row_height(items, size: float, weight: str) -> float:
            font_name = font_for(size, weight)
            line_height = size * 1.2
            counts = []
            for item, col_w in zip(items, col_widths):
                lines = wrap_text(item, col_w - 2 * padding_x, font_name, size)
                counts.append(max(1, len(lines)))
            return max(counts) * line_height + 2 * padding_y

        y = self.cursor
        header_h = row_height(headers, header_size, "700")
        for x, w, text_value, align in zip(x_positions, col_widths, headers, aligns):
            self.rect(x, y, w, header_h, fill="#2b3f67", stroke="#cfd7e5")
            inner_y = y + padding_y + header_size
            if align == "center":
                self.text(x, inner_y, w, text_value, header_size, color="#ffffff", weight="700", align="center", line_height=header_size * 1.2)
            elif align == "right":
                self.text(x + padding_x, inner_y, w - 2 * padding_x, text_value, header_size, color="#ffffff", weight="700", align="right", line_height=header_size * 1.2)
            else:
                self.text(x + padding_x, inner_y, w - 2 * padding_x, text_value, header_size, color="#ffffff", weight="700", line_height=header_size * 1.2)
        y += header_h

        for row_index, row in enumerate(rows):
            fill = "#f9fbff" if row_index % 2 == 0 else "#ffffff"
            row_h = row_height(row, font_size, "400")
            for x, w in zip(x_positions, col_widths):
                self.rect(x, y, w, row_h, fill=fill, stroke="#cfd7e5")
            for x, w, text_value, align in zip(x_positions, col_widths, row, aligns):
                inner_y = y + padding_y + font_size
                if align == "center":
                    self.text(x, inner_y, w, text_value, font_size, align="center", line_height=font_size * 1.2)
                elif align == "right":
                    self.text(x + padding_x, inner_y, w - 2 * padding_x, text_value, font_size, align="right", line_height=font_size * 1.2)
                else:
                    self.text(x + padding_x, inner_y, w - 2 * padding_x, text_value, font_size, line_height=font_size * 1.2)
            y += row_h
        self.cursor = y + gap_after

    def footer(self, content: str | None = None) -> None:
        if content:
            self.line(LEFT, PAGE_H - 52, PAGE_W - RIGHT, PAGE_H - 52, "#2b3f67", 2)
            self.text(LEFT, PAGE_H - 34, CONTENT_W, content, 7.6, color="#6b778c", align="center")
        self.text(PAGE_W - RIGHT - 20, PAGE_H - 18, 20, str(self.number), 8.3, color="#6b778c", align="right")


def draw_pages(pages: list[VectorPage], output_path: Path) -> None:
    c = canvas.Canvas(str(output_path), pagesize=letter)
    c.setTitle("XPA-105 Antenna Report UA")
    for page in pages:
        for kind, payload in page.ops:
            if kind == "line":
                x1, y1, x2, y2, color, width = payload
                c.setStrokeColor(color)
                c.setLineWidth(width)
                c.line(x1, PAGE_H - y1, x2, PAGE_H - y2)
            elif kind == "rect":
                x, y, w, h, fill_color, stroke_color, stroke_width, radius = payload
                c.setLineWidth(stroke_width)
                c.setStrokeColor(stroke_color)
                if fill_color is not None:
                    c.setFillColor(fill_color)
                    c.roundRect(x, PAGE_H - y - h, w, h, radius, fill=1, stroke=1)
                else:
                    c.roundRect(x, PAGE_H - y - h, w, h, radius, fill=0, stroke=1)
            elif kind == "text":
                op: TextOp = payload
                c.setFillColor(op.color)
                c.setFont(op.font_name, op.font_size)
                for idx, line in enumerate(op.lines):
                    line_width = pdfmetrics.stringWidth(line, op.font_name, op.font_size)
                    if op.align == "center":
                        draw_x = op.x + (op.width - line_width) / 2
                    elif op.align == "right":
                        draw_x = op.x + op.width - line_width
                    else:
                        draw_x = op.x
                    baseline = op.y + idx * op.line_height
                    c.drawString(draw_x, PAGE_H - baseline, line)
            elif kind == "image":
                path, x, y, w, h = payload
                c.drawImage(str(path), x, PAGE_H - y - h, width=w, height=h, preserveAspectRatio=True, mask="auto")
        c.showPage()
    c.save()


def main() -> None:
    if not INPUT_PDF.exists():
        raise FileNotFoundError(INPUT_PDF)
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    legacy = load_legacy_module()
    legacy.ensure_extracted_images(INPUT_PDF, IMAGE_DIR)
    legacy.Page = VectorPage
    pages = legacy.build_pages(PROJECT_ROOT, IMAGE_DIR)
    draw_pages(pages, OUTPUT_PDF)
    print(OUTPUT_PDF)


if __name__ == "__main__":
    main()
