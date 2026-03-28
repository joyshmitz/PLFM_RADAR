#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import math
import os
import subprocess
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape


PAGE_W = 612
PAGE_H = 792
LEFT = 56
RIGHT = 56
CONTENT_W = PAGE_W - LEFT - RIGHT

BLUE = "#2b3f67"
MID_BLUE = "#405a8a"
LIGHT_BLUE = "#eef3fb"
GRID = "#cfd7e5"
TEXT = "#29364b"
MUTED = "#6b778c"
BOX_FILL = "#f4fbf6"
BOX_STROKE = "#43b96d"

FONT_PATH_CANDIDATES = (
    "/System/Library/Fonts/Supplemental/PTSans.ttc",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
)
EXTRACTED_SOURCE_HASH = ".source_sha256"
PRODUCT_FAMILY = "XPA-105"
PRODUCT_FAMILY_FOOTER = "XPA-105 family"
PRODUCT_VARIANT_816 = "XPA-105 8x16"
PRODUCT_VARIANT_3216 = "XPA-105 32x16"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def xml(text: str) -> str:
    return escape(text, {"'": "&apos;", '"': "&quot;"})


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_cached_source_hash(image_dir: Path) -> str | None:
    hash_path = image_dir / EXTRACTED_SOURCE_HASH
    if not hash_path.exists():
        return None
    return hash_path.read_text(encoding="utf-8").strip() or None


def clear_extracted_images(image_dir: Path) -> None:
    for path in image_dir.glob("img-*"):
        if path.is_file() or path.is_symlink():
            path.unlink()


def ensure_extracted_images(input_pdf: Path, image_dir: Path) -> None:
    current_hash = sha256_file(input_pdf)
    cached_hash = read_cached_source_hash(image_dir)
    has_extracted_images = any(image_dir.glob("img-*"))
    if cached_hash == current_hash and has_extracted_images:
        return
    clear_extracted_images(image_dir)
    run(["pdfimages", "-all", str(input_pdf), str(image_dir / "img")])
    (image_dir / EXTRACTED_SOURCE_HASH).write_text(f"{current_hash}\n", encoding="utf-8")


def normalize_remote_url(url: str) -> str:
    url = url.strip()
    if not url:
        return ""
    if url.startswith("git@github.com:"):
        path = url.removeprefix("git@github.com:")
        if path.endswith(".git"):
            path = path[:-4]
        return f"https://github.com/{path}"
    if url.startswith("https://github.com/") and url.endswith(".git"):
        return url[:-4]
    return url


def git_remote_url(project_root: Path, remote_name: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(project_root), "remote", "get-url", remote_name],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    normalized = normalize_remote_url(result.stdout)
    return normalized or None


def repo_provenance_text(project_root: Path) -> str:
    upstream_url = git_remote_url(project_root, "upstream")
    origin_url = git_remote_url(project_root, "origin")
    if upstream_url and origin_url and upstream_url != origin_url:
        return f"Джерело даних: {upstream_url} | Поточний репозиторій: {origin_url}"
    repo_url = origin_url or upstream_url
    if repo_url:
        return f"Репозиторій: {repo_url}"
    return "Репозиторій: локальна робоча копія"


def resolve_magick_font() -> str | None:
    explicit_font = os.environ.get("XPA105_REPORT_FONT")
    if explicit_font:
        return explicit_font
    for candidate in FONT_PATH_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return None


def brand_text(text: str) -> str:
    replacements = [
        ("XPA-105 Radar Systems", PRODUCT_FAMILY_FOOTER),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def wrap_text(text: str, width: float, font_size: float, factor: float = 0.53) -> list[str]:
    max_chars = max(12, int(width / (font_size * factor)))
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        lines.extend(
            textwrap.wrap(
                paragraph,
                width=max_chars,
                break_long_words=False,
                break_on_hyphens=False,
            )
        )
    return lines or [""]


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Not a PNG file: {path}")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


@dataclass
class Page:
    number: int
    title: str | None = None

    def __post_init__(self) -> None:
        self.cursor = 94
        self.parts: list[str] = [
            (
                f"<svg xmlns='http://www.w3.org/2000/svg' width='{PAGE_W}' height='{PAGE_H}' "
                f"viewBox='0 0 {PAGE_W} {PAGE_H}'>"
            ),
            f"<rect x='0' y='0' width='{PAGE_W}' height='{PAGE_H}' fill='white'/>",
        ]
        if self.title:
            self.parts.append(
                f"<line x1='{LEFT}' y1='58' x2='{PAGE_W - RIGHT}' y2='58' stroke='{BLUE}' stroke-width='3'/>"
            )
            self.text(LEFT, 82, CONTENT_W, self.title, 18, color=BLUE, weight="700")
            self.cursor = 112

    def line(self, x1: float, y1: float, x2: float, y2: float, color: str = GRID, width: float = 1) -> None:
        self.parts.append(
            f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{color}' stroke-width='{width}'/>"
        )

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: str = "none",
        stroke: str = GRID,
        stroke_width: float = 1,
        rx: float = 0,
    ) -> None:
        self.parts.append(
            f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='{fill}' "
            f"stroke='{stroke}' stroke-width='{stroke_width}' rx='{rx}' ry='{rx}'/>"
        )

    def text(
        self,
        x: float,
        y: float,
        width: float,
        content: str,
        size: float,
        *,
        color: str = TEXT,
        weight: str = "400",
        align: str = "left",
        line_height: float | None = None,
    ) -> float:
        content = brand_text(content)
        lh = line_height or size * 1.28
        lines = wrap_text(content, width, size)
        if align == "center":
            anchor = "middle"
            x_pos = x + width / 2
        elif align == "right":
            anchor = "end"
            x_pos = x + width
        else:
            anchor = "start"
            x_pos = x
        self.parts.append(
            f"<text x='{x_pos}' y='{y}' font-size='{size}' font-weight='{weight}' "
            f"font-family='sans-serif' fill='{color}' text-anchor='{anchor}'>"
        )
        for idx, line in enumerate(lines):
            dy = 0 if idx == 0 else lh
            attr = f"x='{x_pos}'"
            if idx == 0:
                self.parts.append(f"<tspan {attr} y='{y}'>{xml(line)}</tspan>")
            else:
                self.parts.append(f"<tspan {attr} dy='{dy}'>{xml(line)}</tspan>")
        self.parts.append("</text>")
        return y + lh * len(lines)

    def paragraph(self, content: str, size: float = 10.2, gap_after: float = 12) -> None:
        self.cursor = self.text(LEFT, self.cursor, CONTENT_W, content, size) + gap_after

    def section(self, heading: str, size: float = 13.5, gap_after: float = 8) -> None:
        self.cursor = self.text(LEFT, self.cursor, CONTENT_W, heading, size, color=MID_BLUE, weight="700") + gap_after

    def image(self, path: Path, width: float, gap_after: float = 10) -> tuple[float, float]:
        img_w, img_h = png_size(path)
        height = width * img_h / img_w
        x = LEFT + (CONTENT_W - width) / 2
        self.parts.append(
            f"<image href='{path.as_posix()}' x='{x}' y='{self.cursor}' width='{width}' height='{height}'/>"
        )
        self.cursor += height + gap_after
        return width, height

    def caption(self, content: str, size: float = 8.5, gap_after: float = 10) -> None:
        self.cursor = self.text(LEFT, self.cursor, CONTENT_W, content, size, color=MUTED, align="center") + gap_after

    def callout(self, content: str, size: float = 9.2, gap_after: float = 12) -> None:
        lines = wrap_text(content, CONTENT_W - 16, size)
        line_height = size * 1.28
        height = 8 + len(lines) * line_height + 8
        y = self.cursor
        self.rect(LEFT, y, CONTENT_W, height, fill=BOX_FILL, stroke=BOX_STROKE, stroke_width=1.5, rx=4)
        self.text(LEFT + 8, y + 14, CONTENT_W - 16, content, size, color=TEXT)
        self.cursor += height + gap_after

    def table(
        self,
        headers: list[str],
        rows: list[list[str]],
        col_fracs: list[float],
        *,
        font_size: float = 8.9,
        header_font_size: float | None = None,
        aligns: list[str] | None = None,
        gap_after: float = 12,
    ) -> None:
        header_size = header_font_size or font_size
        col_widths = [CONTENT_W * frac for frac in col_fracs]
        padding_x = 6
        padding_y = 6
        x_positions = [LEFT]
        for w in col_widths[:-1]:
            x_positions.append(x_positions[-1] + w)
        aligns = aligns or ["left"] * len(headers)

        def row_height(items: list[str], size: float) -> float:
            line_height = size * 1.2
            counts = []
            for item, col_w in zip(items, col_widths):
                lines = wrap_text(item, col_w - 2 * padding_x, size, factor=0.5)
                counts.append(max(1, len(lines)))
            return max(counts) * line_height + 2 * padding_y

        y = self.cursor
        header_h = row_height(headers, header_size)
        for idx, (x, w, text_value, align) in enumerate(zip(x_positions, col_widths, headers, aligns)):
            self.rect(x, y, w, header_h, fill=BLUE, stroke=GRID)
            tx = x + padding_x
            if align == "center":
                self.text(x, y + padding_y + header_size, w, text_value, header_size, color="white", weight="700", align="center", line_height=header_size * 1.2)
            elif align == "right":
                self.text(x + padding_x, y + padding_y + header_size, w - 2 * padding_x, text_value, header_size, color="white", weight="700", align="right", line_height=header_size * 1.2)
            else:
                self.text(tx, y + padding_y + header_size, w - 2 * padding_x, text_value, header_size, color="white", weight="700", line_height=header_size * 1.2)
        y += header_h

        for row_index, row in enumerate(rows):
            row_h = row_height(row, font_size)
            fill = "#f9fbff" if row_index % 2 == 0 else "white"
            for x, w in zip(x_positions, col_widths):
                self.rect(x, y, w, row_h, fill=fill, stroke=GRID)
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
            self.line(LEFT, PAGE_H - 52, PAGE_W - RIGHT, PAGE_H - 52, BLUE, 2)
            self.text(LEFT, PAGE_H - 34, CONTENT_W, content, 7.4, color=MUTED, align="center")
        self.text(PAGE_W - RIGHT - 20, PAGE_H - 18, 20, str(self.number), 8, color=MUTED, align="right")

    def render(self) -> str:
        return "\n".join(self.parts + ["</svg>"])


def build_pages(project_root: Path, image_dir: Path) -> list[Page]:
    pages: list[Page] = []

    # Page 1 - Cover
    page = Page(1)
    page.line(165, 132, 447, 132, BLUE, 3)
    page.text(60, 195, PAGE_W - 120, "ЗВІТ ПРО МОДЕЛЮВАННЯ АНТЕНИ", 28, color=BLUE, weight="700", align="center")
    page.text(60, 240, PAGE_W - 120, "XPA-105 X-діапазонна фазована радарна решітка", 16, color=MID_BLUE, align="center")
    page.text(60, 272, PAGE_W - 120, "Аналіз OpenEMS FDTD - одиночний патч-елемент на 10.5 GHz", 12.5, color=MID_BLUE, align="center")
    page.line(165, 318, 447, 318, BLUE, 3)
    card_y = 362
    card_w = 114
    card_h = 34
    gap = 2
    top_cards = ["10.5 GHz", "S11: -30.6 dB", "7.19 dBi", "Узгодження 50 Ohm"]
    bottom_cards = ["Підкладка RO4350B", "ККД 56.7%", "Смуга 50 MHz", "Масив 128 ел."]
    for row, labels in enumerate((top_cards, bottom_cards)):
        for idx, label in enumerate(labels):
            x = 72 + idx * (card_w + gap)
            y = card_y + row * (card_h + 10)
            page.rect(x, y, card_w, card_h, fill=BLUE, stroke=BLUE)
            page.text(x, y + 21, card_w, label, 9, color="white", align="center")
    page.text(70, 548, PAGE_W - 140, "XPA-105 Radar Systems | Березень 2026 | Версія 1.0", 11, color="#99a3b4", align="center")
    page.text(
        64,
        570,
        PAGE_W - 128,
        "Розв'язувач: OpenEMS v0.0.36 (FDTD) | Платформа: macOS ARM64 | Час виконання: ~130 s (360k cells)",
        8.5,
        color="#99a3b4",
        align="center",
    )
    page.footer()
    pages.append(page)

    # Page 2 - TOC
    page = Page(2, "ЗМІСТ")
    toc = [
        "1. Підсумок для керівництва",
        "2. Параметри конструкції",
        "   2.1 Підкладка: Rogers RO4350B",
        "   2.2 Геометрія патч-елемента",
        "   2.3 Помилка у patch_antenna.py в репозиторії",
        "3. Налаштування моделювання",
        "   3.1 Конфігурація FDTD",
        "   3.2 Калібрування точки живлення",
        "4. Результати",
        "   4.1 S-параметри (втрати на відбиття)",
        "   4.2 Вхідний імпеданс",
        "   4.3 VSWR",
        "   4.4 Діаграма спрямованості",
        "   4.5 Полярна діаграма спрямованості",
        "   4.6 Тривимірна діаграма спрямованості",
        "   4.7 Зведена панель",
        "5. ККД та оцінка характеристик масиву",
        "6. Перевірка проти теорії",
        "7. Ключові висновки та рекомендації",
    ]
    for line in toc:
        size = 11 if not line.startswith("   ") else 10
        color = BLUE if not line.startswith("   ") else TEXT
        weight = "700" if not line.startswith("   ") else "400"
        page.cursor = page.text(LEFT, page.cursor, CONTENT_W, line, size, color=color, weight=weight) + 8
    page.footer()
    pages.append(page)

    # Page 3 - Executive summary
    page = Page(3, "1. Підсумок для керівництва")
    page.paragraph(
        "Було змодельовано та проаналізовано один прямокутний мікросмужковий патч-елемент для фазованої решітки радара XPA-105 8x16 за допомогою розв'язувача OpenEMS FDTD. Моделювання підтверджує роботу антени на 10.5 GHz на підкладці Rogers RO4350B і показує, що одиночний елемент виконує всі цільові вимоги перед інтеграцією у повний масив 8 x 16 (128 елементів).",
        size=10.1,
    )
    page.table(
        ["Метрика", "Значення", "Оцінка"],
        [
            ["Резонансна частота", "10.495 GHz", "Точно в ціль (0.05% від 10.5 GHz)"],
            ["Втрати на відбиття (S11)", "-30.6 dB", "Відмінне узгодження"],
            ["Вхідний імпеданс", "47.1 + j0.2 Ohm", "Майже ідеальне узгодження з 50 Ohm"],
            ["Смуга за рівнем -10 dB", "50 MHz (0.48%)", "Вузька, що очікувано для тонкої підкладки"],
            ["Пікова директивність", "7.19 dBi", "Класичне значення для одиночного патча"],
            ["ККД випромінювання", "56.7%", "Адекватно для підкладки 0.102 mm"],
            ["Реалізоване підсилення", "4.72 dBi", "Узгоджується з D x eta"],
        ],
        [0.24, 0.24, 0.52],
        aligns=["left", "center", "center"],
    )
    page.callout(
        "Ключовий висновок: моделювання підтверджує, що патч-елемент XPA-105 коректно спроєктований для роботи на 10.5 GHz. Дуже добре узгодження імпедансу (S11 = -30.6 dB, Zin = 47.1 Ohm) означає мінімальне відбиття потужності в точці живлення, а директивність 7.19 dBi узгоджується з опублікованими даними для прямокутних мікросмужкових патчів. Для повного масиву з 128 елементів очікуване підсилення близько 25.8 dBi є конкурентним для X-діапазонних фазованих решіток.",
    )
    page.footer()
    pages.append(page)

    # Page 4 - Design parameters
    page = Page(4, "2. Параметри конструкції")
    page.section("2.1 Підкладка: Rogers RO4350B", size=12.5)
    page.paragraph(
        "XPA-105 використовує Rogers RO4350B - високочастотний термореактивний ламінат, який широко застосовується в X-діапазонних радарах і 5G-вузлах. Основні параметри підкладки було взято зі схем Qucs у репозиторії PLFM_RADAR, калькулятора патч-антени та документації зі стеку плати.",
        size=9.4,
        gap_after=10,
    )
    page.table(
        ["Параметр", "Значення", "Джерело"],
        [
            ["Діелектрична проникність (eps_r)", "3.48", "patch_antenna.py, Qucs, datasheet"],
            ["Кут втрат (tan d)", "0.0037", "Даташит RO4350B при 10 GHz"],
            ["Товщина підкладки", "0.102 mm", "Зображення стеку плати (L1-L2 core)"],
            ["Товщина міді", "0.035 mm (1 oz)", "Стек плати, визначення SUBST у Qucs"],
        ],
        [0.28, 0.18, 0.54],
        font_size=8.6,
        header_font_size=8.7,
        aligns=["left", "center", "left"],
        gap_after=10,
    )
    page.section("2.2 Геометрія патч-елемента", size=12.5)
    page.table(
        ["Параметр", "Значення", "Примітки"],
        [
            ["Ширина патча (W)", "9.545 mm", "Формула Balanis: c/(2f) x sqrt(2/(eps_r+1))"],
            ["Довжина патча (L)", "7.401 mm", "Підігнано FDTD під резонанс 10.5 GHz"],
            ["Тип живлення", "Щупове (lumped port)", "Узгодження 50 Ohm при y = 1.49 mm від центру"],
            ["Земляна площина", "38.1 x 36.0 mm", "Запас близько lambda/2 за межами патча"],
            ["Крок елементів", "14.285 mm", "lambda/2 на 10.5 GHz"],
            ["Конфігурація масиву", "8 x 16 (128 елементів)", "Повна специфікація XPA-105 8x16"],
        ],
        [0.26, 0.22, 0.52],
        font_size=8.4,
        header_font_size=8.7,
        aligns=["left", "center", "left"],
        gap_after=10,
    )
    page.section("2.3 Помилка у patch_antenna.py в репозиторії", size=12.5)
    page.paragraph(
        "Калькулятор розмірів патча в PLFM_RADAR/8_Utils/Python/patch_antenna.py містить помилку у формулі ефективної діелектричної проникності. У рівнянні Hammerstad у знаменнику має бути ширина патча W, але код репозиторію помилково підставляє array[1] x h_cu.",
        size=9.1,
        gap_after=8,
    )
    page.table(
        ["Параметр", "Помилково (репозиторій)", "Правильно (Hammerstad)"],
        [
            ["Знаменник формули", "array[1] x h_cu", "W (ширина патча)"],
            ["eps_r_eff", "2.637", "3.407"],
            ["Довжина патча", "8.694 mm", "7.641 mm"],
            ["Резонансна частота", "~9.0 GHz", "~10.5 GHz"],
            ["Похибка частоти", "14%", "< 1%"],
        ],
        [0.28, 0.36, 0.36],
        font_size=8.5,
        header_font_size=8.6,
        aligns=["left", "center", "center"],
        gap_after=8,
    )
    page.paragraph(
        "Наслідок: помилкова формула дає патч, який резонує приблизно на 9.0 GHz замість цільових 10.5 GHz, тобто помилка становить близько 14% і робить антену непридатною. У цьому звіті використано виправлену формулу Hammerstad, що дало точність 0.05% за частотою.",
        size=9.1,
        gap_after=6,
    )
    page.footer()
    pages.append(page)

    # Page 5 - Simulation setup
    page = Page(5, "3. Налаштування моделювання")
    page.section("3.1 Конфігурація FDTD", size=12.5)
    page.paragraph(
        "Антену змодельовано в OpenEMS - це відкритий електромагнітний розв'язувач типу FDTD (Finite-Difference Time-Domain). Модель враховує повну тривимірну структуру: патч, підкладку, землю та щуп живлення всередині області з поглинальними межами.",
        size=9.6,
        gap_after=10,
    )
    page.table(
        ["Параметр", "Значення"],
        [
            ["Збудження", "Гаусовий імпульс, f0 = 10.5 GHz, BW = 4 GHz"],
            ["Частотний прогін", "8.5 - 12.5 GHz (801 точка)"],
            ["Граничні умови", "MUR, 1-й порядок, поглинальні, всі 6 граней"],
            ["Розмір області", "80 x 80 x 50 mm"],
            ["Кількість комірок", "~360,750"],
            ["Крок часу (Courant)", "79.5 fs"],
            ["Максимум кроків", "120,000"],
            ["Критерій зупинки", "-50 dB (досягнуто -49 dB)"],
            ["Роздільна здатність сітки", "lambda/20 при 12.5 GHz (~1.2 mm)"],
            ["Комірки по товщині підкладки", "4 (через 0.102 mm)"],
        ],
        [0.42, 0.58],
        font_size=8.7,
        header_font_size=8.8,
        aligns=["left", "center"],
        gap_after=10,
    )
    page.section("3.2 Калібрування точки живлення", size=12.5)
    page.paragraph(
        "Положення щупа живлення було підібрано ітераційним моделюванням. Вхідний імпеданс probe-fed патча змінюється за законом Z(y) = Z_edge x sin^2(pi y / L) від центру до краю, де для цієї геометрії Z_edge становить близько 144 Ohm. Оптимальний зсув для узгодження з 50 Ohm знайдено на відстані y = 1.49 mm від центру патча.",
        size=9.3,
        gap_after=10,
    )
    page.table(
        ["Ітерація", "Зсув живлення (мм)", "Zin (Ohm)", "S11 (dB)", "f_res (GHz)"],
        [
            ["1 (початкова)", "2.78", "100.4 + j6.1", "-9.4", "9.03"],
            ["2 (виправлення L)", "2.76", "118.4 - j7.0", "-7.8", "10.23"],
            ["3 (ближче)", "1.54", "49.3 + j0.5", "-41.7", "10.17"],
            ["4 (фінальна)", "1.49", "47.1 + j0.2", "-30.6", "10.50"],
        ],
        [0.2, 0.18, 0.24, 0.16, 0.22],
        font_size=8.3,
        header_font_size=8.4,
        aligns=["left", "center", "center", "center", "center"],
        gap_after=8,
    )
    page.paragraph(
        "Третя ітерація дала найкраще значення S11 (-41.7 dB), але на частоті 10.17 GHz. Фінальна тонка підстройка до 1.49 mm зсунула резонанс у точку 10.50 GHz і зберегла дуже добре узгодження S11 = -30.6 dB. Невелике відхилення від теоретично оптимальної точки пояснюється паразитною індуктивністю щупа, яка впливає і на імпеданс, і на резонансну частоту.",
        size=9.2,
        gap_after=6,
    )
    page.footer()
    pages.append(page)

    # Page 6 - S11
    page = Page(6, "4. Результати")
    page.section("4.1 S-параметри (втрати на відбиття)", size=12.5)
    page.image(image_dir / "img-000.png", width=500, gap_after=6)
    page.caption("Рисунок 4.1 - Втрати на відбиття S11 залежно від частоти. Глибокий мінімум на 10.495 GHz підтверджує резонанс із рівнем -30.6 dB.")
    page.paragraph(
        "Що це показує: параметр S11 описує, яка частка потужності відбивається назад від точки живлення антени. Значення нижче -10 dB означає, що понад 90% потужності випромінюється або поглинається, тобто узгодження є прийнятним. Патч XPA-105 досягає -30.6 dB на 10.495 GHz, отже антена приймає приблизно 99.9% падаючої потужності.",
        size=9.5,
    )
    page.table(
        ["Параметр", "Значення"],
        [
            ["Резонансна частота", "10.495 GHz (ціль: 10.5 GHz)"],
            ["S11 у резонансі", "-30.63 dB"],
            ["Смуга за рівнем -10 dB", "50 MHz (10.470 - 10.520 GHz)"],
            ["Відносна смуга", "0.48%"],
        ],
        [0.4, 0.6],
        font_size=8.8,
        header_font_size=8.9,
        aligns=["left", "center"],
        gap_after=10,
    )
    page.callout(
        "Примітка щодо конструкції: вузька смуга 0.48% є фізично коректною для підкладки товщиною 0.102 mm (h/lambda = 0.0036). Типові X-діапазонні патчі на 4-mil Rogers дають близько 0.3-0.8% смуги. Це означає високу чутливість до виробничих допусків: зміна довжини патча на 0.1 mm зсуває резонанс приблизно на 140 MHz. Для виготовлення PCB потрібен допуск не гірше +/-0.025 mm (+/-1 mil).",
        size=8.8,
    )
    page.footer()
    pages.append(page)

    # Page 7 - Impedance
    page = Page(7, "4. Результати")
    page.section("4.2 Вхідний імпеданс", size=12.5)
    page.image(image_dir / "img-002.png", width=500, gap_after=6)
    page.caption("Рисунок 4.2 - Дійсна та уявна частини вхідного імпедансу залежно від частоти. Дійсна частина проходить через 50 Ohm, а уявна - через нуль у точці резонансу.")
    page.paragraph(
        "Що це показує: комплексний вхідний імпеданс Z_in = R + jX як функцію частоти. У справжньому резонансі уявна частина переходить через нуль, тобто антена є чисто активною, а дійсна частина дорівнює 50 Ohm і збігається з опором тракту. Для патча XPA-105 отримано 47.1 + j0.2 Ohm на 10.495 GHz - це майже ідеальне узгодження із системою 50 Ohm.",
        size=9.4,
    )
    page.table(
        ["Параметр", "Значення"],
        [
            ["Zin у резонансі", "47.1 + j0.2 Ohm"],
            ["Пік дійсної частини (антирезонанс)", "~150 Ohm"],
            ["Нульове перетинання уявної частини", "10.495 GHz (підтверджує справжній резонанс)"],
        ],
        [0.42, 0.58],
        font_size=8.7,
        header_font_size=8.8,
        aligns=["left", "center"],
        gap_after=10,
    )
    page.paragraph(
        "Практичне значення для плати: вхідний імпеданс 47.1 Ohm дозволяє підключати антену безпосередньо до 50-омних ліній передачі та мікросхеми формувача променя ADAR1000 без окремої мережі узгодження. Це спрощує топологію PCB і знижує втрати. Внутрішні підсилювачі ADAR1000 теж розраховані на джерело й навантаження 50 Ohm.",
        size=9.2,
        gap_after=6,
    )
    page.footer()
    pages.append(page)

    # Page 8 - VSWR
    page = Page(8, "4. Результати")
    page.section("4.3 VSWR", size=12.5)
    page.image(image_dir / "img-004.png", width=500, gap_after=8)
    page.caption("Рисунок 4.3 - Коефіцієнт стоячої хвилі за напругою (VSWR) залежно від частоти. Межа VSWR < 2:1 задає корисну робочу смугу.")
    page.paragraph(
        "Що це показує: VSWR є альтернативним способом описати якість узгодження імпедансу. VSWR = 1.0 означає ідеальне узгодження, а VSWR < 2.0, що відповідає S11 < -10 dB, є стандартним порогом прийнятної роботи. Патч XPA-105 має мінімум VSWR близько 1.06 на 10.495 GHz, тобто узгодження є відмінним.",
        size=9.6,
        gap_after=12,
    )
    page.paragraph(
        "Смуга VSWR < 2:1 відповідає тим самим 50 MHz, які було визначено в розділі 4.1 за критерієм S11 = -10 dB. Поза цією смугою розузгодження швидко зростає через резонансну природу патч-антени.",
        size=9.6,
        gap_after=6,
    )
    page.footer()
    pages.append(page)

    # Page 9 - Radiation pattern
    page = Page(9, "4. Результати")
    page.section("4.4 Діаграма спрямованості", size=12.5)
    page.image(image_dir / "img-006.png", width=500, gap_after=8)
    page.caption("Рисунок 4.4 - Зрізи директивності в E-площині (phi = 0 deg) та H-площині (phi = 90 deg) на частоті 10.5 GHz.")
    page.paragraph(
        "Що це показує: далеку зону випромінювання одиночного патч-елемента у вигляді залежності директивності (dBi) від кута піднесення theta. Подано два головні зрізи: E-площина, яка містить вектор електричного поля, та H-площина, яка містить вектор магнітного поля.",
        size=9.4,
    )
    page.table(
        ["Параметр", "Значення"],
        [
            ["Пікова директивність", "7.19 dBi"],
            ["HPBW в E-площині", "~75 deg"],
            ["HPBW в H-площині", "~85 deg"],
            ["Відношення вперед/назад", "> 15 dB"],
        ],
        [0.46, 0.54],
        font_size=8.8,
        header_font_size=8.9,
        aligns=["left", "center"],
        gap_after=10,
    )
    page.paragraph(
        "Наслідок для масиву: діаграма одиночного елемента задає оболонку, всередині якої можна електронно сканувати промінь. Ширина пелюстка близько 75-85 deg дозволяє масиву з 128 елементів відхиляти промінь до +/-45 deg без суттєвого падіння підсилення. Після +/-60 deg підсилення елемента швидко зменшується, тому XPA-105 використовує механічний обертач для повного азимутального покриття.",
        size=9.0,
        gap_after=6,
    )
    page.footer()
    pages.append(page)

    # Page 10 - Polar pattern
    page = Page(10, "4. Результати")
    page.section("4.5 Полярна діаграма спрямованості", size=12.5)
    page.image(image_dir / "img-008.png", width=520, gap_after=6)
    page.caption("Рисунок 4.5 - Полярні діаграми випромінювання для E-площини та H-площини на 10.5 GHz.")
    page.paragraph(
        "Що це показує: ті самі дані випромінювання, що й на рисунку 4.4, але в полярних координатах - це традиційний формат для антенних діаграм. Головний пелюсток спрямований на theta = 0 deg, тобто перпендикулярно до поверхні патча, а до горизонту рівень плавно спадає приблизно за косинусоподібним законом. Зворотне випромінювання в районі theta = 180 deg пригнічується земною площиною.",
        size=9.2,
        gap_after=12,
    )
    page.paragraph(
        "E-площина трохи вужча за H-площину - це типовий результат для прямокутних патчів. E-площина пов'язана з резонансним розміром L = 7.401 mm, тоді як H-площина визначається ширшим нерезонансним розміром W = 9.545 mm.",
        size=9.2,
        gap_after=6,
    )
    page.footer()
    pages.append(page)

    # Page 11 - 3D pattern
    page = Page(11, "4. Результати")
    page.section("4.6 Тривимірна діаграма спрямованості", size=12.5)
    page.image(image_dir / "img-010.png", width=470, gap_after=8)
    page.caption("Рисунок 4.6 - Тривимірна поверхня діаграми спрямованості. Колір показує рівень директивності в dBi.")
    page.paragraph(
        "Що це показує: повну тривимірну візуалізацію діаграми випромінювання, де і відстань від початку координат, і колір відповідають директивності в dBi. Форма має характерний вигляд широкоспрямованого патча - максимум на theta = 0 deg, тобто в напрямку від земної площини, і мінімальне випромінювання в задню півсферу.",
        size=9.2,
        gap_after=12,
    )
    page.paragraph(
        "Виробнича примітка: тривимірна діаграма не показує неочікуваних бічних пелюстків або спотворень від скінченної земної площини чи щупа живлення. У реальному масиві взаємний зв'язок між сусідніми елементами з кроком 14.285 mm = lambda/2 змінить вбудовану діаграму елемента, зазвичай зменшуючи ширину H-площини на 5-10 deg і додаючи невеликі асиметрії. Повна симуляція масиву на 128 елементів врахує ці ефекти, але вимагатиме приблизно в 1000 разів більше обчислень.",
        size=8.9,
        gap_after=6,
    )
    page.footer()
    pages.append(page)

    # Page 12 - Dashboard
    page = Page(12, "4. Результати")
    page.section("4.7 Зведена панель", size=12.5)
    page.image(image_dir / "img-012.png", width=520, gap_after=8)
    page.caption("Рисунок 4.7 - Зведена панель із чотирма графіками: S11, імпеданс, VSWR та діаграма спрямованості.")
    page.paragraph(
        "Що це показує: зібраний на одній сторінці набір основних метрик антени. Такий огляд дає швидку оцінку для технічних рев'ю та презентацій інвесторам. Усі чотири графіки підтверджують, що антена коректно працює на проєктній частоті 10.5 GHz.",
        size=9.5,
        gap_after=6,
    )
    page.footer()
    pages.append(page)

    # Page 13 - Efficiency and array estimate
    page = Page(13, "5. ККД та оцінка характеристик масиву")
    page.section("5.1 ККД одиночного елемента", size=12.5)
    page.table(
        ["Параметр", "Значення"],
        [
            ["ККД випромінювання", "56.7%"],
            ["Реалізоване підсилення", "4.72 dBi"],
            ["Директивність", "7.19 dBi"],
            ["Перевірка Gain = D x eta", "7.19 - 2.47 = 4.72 dBi  OK"],
        ],
        [0.46, 0.54],
        font_size=8.8,
        header_font_size=8.9,
        aligns=["left", "center"],
        gap_after=10,
    )
    page.paragraph(
        "ККД 56.7% в основному обмежується діелектричними втратами: tan d = 0.0037 є помірним значенням для RO4350B на 10 GHz. Втрати в провіднику з міді 1 oz є другорядними, а втрати на поверхневі хвилі для такої товщини підкладки мінімальні. Підняти ККД до приблизно 75% можна за рахунок товстішої підкладки 0.254 mm (10 mil), але ціною збільшення висоти масиву.",
        size=9.1,
        gap_after=12,
    )
    page.section("5.2 Оцінка характеристик масиву", size=12.5)
    page.paragraph(
        "Для повного фазованого масиву сімейства XPA-105 8x16 з кроком елементів lambda/2:",
        size=9.4,
        gap_after=8,
    )
    page.table(
        ["Параметр", "Розрахунок", "Результат"],
        [
            ["Підсилення множника масиву", "10 x log10(128)", "21.1 dB"],
            ["Директивність масиву", "7.19 + 21.1 dBi", "28.3 dBi"],
            ["Підсилення масиву (по нормалі)", "4.72 + 21.1 dBi", "25.8 dBi"],
            ["Втрати сканування на максимумі", "~2-3 dB при +/-45 deg", "~23-24 dBi"],
            ["EIRP при 1 W Tx", "25.8 + 30 dBm", "55.8 dBm"],
        ],
        [0.33, 0.39, 0.28],
        font_size=8.5,
        header_font_size=8.7,
        aligns=["left", "center", "center"],
        gap_after=10,
    )
    page.paragraph(
        "Конкурентний контекст: комерційні X-діапазонні фазовані решітки Echodyne EchoGuard і Fortem TrueView зазвичай лежать у діапазоні 25-30 dBi. Оцінене підсилення XPA-105 8x16 на рівні 25.8 dBi є цілком конкурентним і підтверджує правильність вибраної антенної архітектури. Варіант XPA-105 32x16 із підсилювачами потужності на GaN додає ще близько 10 dB по тракту передавання, частково компенсуючи втрати ККД одиночного елемента.",
        size=9.0,
        gap_after=6,
    )
    page.footer()
    pages.append(page)

    # Page 14 - Validation
    page = Page(14, "6. Перевірка проти теорії")
    page.section("6.1 Швидкі sanity-check перевірки", size=12.5)
    page.table(
        ["Перевірка", "Очікування", "Виміряно", "Статус"],
        [
            ["Резонанс біля 10.5 GHz", "10.5 GHz", "10.495 GHz", "PASS"],
            ["S11 < -10 dB", "< -10 dB", "-30.6 dB", "PASS"],
            ["Директивність 6-8 dBi", "6-8 dBi", "7.19 dBi", "PASS"],
            ["Смуга < 1% для тонкої підкладки", "< 1%", "0.48%", "PASS"],
            ["Zin близько 50 Ohm", "50 Ohm", "47.1 Ohm", "PASS"],
            ["ККД > 30%", "> 30%", "56.7%", "PASS"],
        ],
        [0.42, 0.18, 0.22, 0.18],
        font_size=8.4,
        header_font_size=8.6,
        aligns=["left", "center", "center", "center"],
        gap_after=12,
    )
    page.section("6.2 Порівняння з аналітичною теорією (Balanis)", size=12.5)
    page.table(
        ["Параметр", "Теорія (Balanis)", "Результат FDTD", "Похибка"],
        [
            ["f_res", "10.5 GHz (ціль)", "10.495 GHz", "0.05%"],
            ["Директивність", "6.6-7.5 dBi", "7.19 dBi", "У межах очікуваного"],
            ["Ширина патча", "9.545 mm", "9.545 mm (вхідні дані)", "Точно"],
            ["Довжина патча", "7.641 mm (аналітика)", "7.401 mm (після FDTD-підстройки)", "3.1% коротше"],
        ],
        [0.22, 0.27, 0.31, 0.20],
        font_size=8.1,
        header_font_size=8.3,
        aligns=["left", "center", "center", "center"],
        gap_after=10,
    )
    page.paragraph(
        "Різниця 3.1% між аналітичною довжиною патча та значенням, яке підібрано у FDTD, є типовою та очікуваною. Формули Balanis і Hammerstad не враховують паразитну індуктивність щупа, дифракцію на краях скінченної земної площини та близькість поглинальних меж MUR. Для виробництва PCB слід використовувати саме FDTD-підігнану довжину 7.401 mm.",
        size=9.2,
        gap_after=6,
    )
    page.footer()
    pages.append(page)

    # Page 15 - Findings
    page = Page(15, "7. Ключові висновки та рекомендації")
    findings = [
        (
            "Висновок 1: підтверджено помилку в репозиторії",
            "Калькулятор patch_antenna.py у PLFM_RADAR має помилку у формулі ефективної діелектричної проникності, яка дає зсув частоти приблизно на 14%. Помилку варто передати в основний репозиторій і виправити. У цьому моделюванні вже використано коректну формулу.",
        ),
        (
            "Висновок 2: компроміс тонкої підкладки",
            "Підкладка RO4350B товщиною 0.102 mm дає дуже компактний профіль фазованої решітки - загальна товщина масиву менша за 2 mm, але водночас обмежує смугу приблизно до 50 MHz і ККД до 57%. Для задач, де потрібна ширша смуга, наприклад краща роздільна здатність за дальністю на коротких дистанціях, товстіша підкладка 0.254 mm дасть близько 1.5% смуги, тобто приблизно 160 MHz, і ККД близько 75%, але зробить масив товщим.",
        ),
        (
            "Висновок 3: характеристики масиву конкурентні",
            "Підсилення одиночного елемента 4.72 dBi у поєднанні з множником масиву для 128 елементів на рівні 21.1 dB повинно дати приблизно 25-26 dBi підсилення масиву по нормалі. Це відповідає рівню комерційних X-діапазонних фазованих решіток Echodyne, Fortem та інших, тобто архітектура антени XPA-105 виглядає ринково життєздатною для систем контр-UAS і радарів спостереження.",
        ),
        (
            "Висновок 4: висока чутливість до виробництва",
            "Смуга 50 MHz означає, що антена дуже чутлива до допуску за довжиною патча. Помилка виготовлення 0.1 mm зсуває резонанс приблизно на 140 MHz і виводить антену за межі смуги -10 dB. Виробництво PCB має тримати розмір патча в межах +/-0.025 mm (+/-1 mil). Сучасні RF-виробники на кшталт TTM Technologies або Rogers-certified фабрик це забезпечують, але собівартість буде вищою, ніж у стандартного FR-4.",
        ),
        (
            "Висновок 5: шлях валідації на етапі 1",
            "Коли буде доступне апаратне забезпечення для етапів 1-3 демо-плану, змодельований S11 можна напряму звірити з вимірюваннями на VNA. Вузька смуга робить цю антену дуже показовим тест-кейсом: добре узгоджений виміряний S11 на 10.5 GHz одночасно підтвердить коректність симуляції та якість виготовлення PCB.",
        ),
    ]
    for heading, body in findings:
        page.cursor = page.text(LEFT, page.cursor, CONTENT_W, heading, 10.8, color=MID_BLUE, weight="700") + 6
        page.cursor = page.text(LEFT, page.cursor, CONTENT_W, body, 9.15) + 14
    footer_text = (
        "Звіт сформовано в межах XPA-105 Phase 0 - програмне моделювання та валідація\n"
        "Моделювання OpenEMS FDTD на Apple Silicon M-series, macOS 15.x | Джерело: legacy antenna simulation workflow\n"
        f"{repo_provenance_text(project_root)}"
    )
    page.footer(footer_text)
    pages.append(page)

    return pages


def main() -> None:
    script_path = Path(__file__).resolve()
    project_root = script_path.parents[2]
    input_pdf = project_root / "docs" / "XPA-105_Antenna_Report_en.pdf"
    output_pdf = project_root / "docs" / "XPA-105_Antenna_Report_ua.pdf"
    work_dir = project_root / "reports-src" / "seeds" / "xpa-105-antenna-report" / "xpa105_ua"
    image_dir = project_root / "tmp" / "pdfs" / "extracted"
    svg_dir = work_dir / "svg"
    pdf_dir = work_dir / "pdf"

    work_dir.mkdir(parents=True, exist_ok=True)
    svg_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    image_dir.mkdir(parents=True, exist_ok=True)

    if not input_pdf.exists():
        raise FileNotFoundError(f"Input PDF not found: {input_pdf}")

    ensure_extracted_images(input_pdf, image_dir)

    pages = build_pages(project_root, image_dir)
    magick_font = resolve_magick_font()
    pdf_parts: list[str] = []
    for idx, page in enumerate(pages, start=1):
        svg_path = svg_dir / f"page_{idx:02d}.svg"
        pdf_path = pdf_dir / f"page_{idx:02d}.pdf"
        svg_path.write_text(page.render(), encoding="utf-8")
        magick_cmd = ["magick"]
        if magick_font:
            magick_cmd.extend(["-font", magick_font])
        magick_cmd.extend([str(svg_path), str(pdf_path)])
        run(magick_cmd)
        pdf_parts.append(str(pdf_path))

    run(["pdfunite", *pdf_parts, str(output_pdf)])
    print(output_pdf)


if __name__ == "__main__":
    main()
