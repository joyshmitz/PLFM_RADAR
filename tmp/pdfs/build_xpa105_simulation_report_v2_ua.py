#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from PIL import Image as PILImage


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PDF = PROJECT_ROOT / "docs" / "XPA-105_Simulation_Report_v2_en.pdf"
OUTPUT_PDF = PROJECT_ROOT / "docs" / "XPA-105_Simulation_Report_v2_ua.pdf"
IMAGE_DIR = PROJECT_ROOT / "tmp" / "pdfs" / "xpa105_sim_v2_ua_images"
PRODUCT_FAMILY = "XPA-105"
PRODUCT_FAMILY_FOOTER = "XPA-105 family"
PRODUCT_VARIANT_816 = "XPA-105 8x16"
PRODUCT_VARIANT_3216 = "XPA-105 32x16"

PAGE_W, PAGE_H = letter
LEFT = RIGHT = 54
TOP = 54
BOTTOM = 46

BLUE = colors.HexColor("#2b3f67")
MID_BLUE = colors.HexColor("#405a8a")
GRID = colors.HexColor("#cfd7e5")
LIGHT_FILL = colors.HexColor("#f7faff")
NOTE_FILL = colors.HexColor("#eef8f0")
NOTE_BORDER = colors.HexColor("#43b96d")
TEXT = colors.HexColor("#29364b")
MUTED = colors.HexColor("#6b778c")


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def register_fonts() -> None:
    fonts = [
        ("PTSerif", "/System/Library/Fonts/Supplemental/PTSerif.ttc", 0),
        ("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf", 0),
        ("ArialBold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf", 0),
    ]
    for name, path, index in fonts:
        if name not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont(name, path, subfontIndex=index))


def styles():
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Title"],
            fontName="ArialBold",
            fontSize=25,
            leading=30,
            alignment=TA_CENTER,
            textColor=BLUE,
            spaceAfter=10,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            parent=base["Title"],
            fontName="Arial",
            fontSize=15,
            leading=19,
            alignment=TA_CENTER,
            textColor=MID_BLUE,
            spaceAfter=8,
        ),
        "cover_scope": ParagraphStyle(
            "cover_scope",
            parent=base["BodyText"],
            fontName="PTSerif",
            fontSize=11.5,
            leading=16,
            alignment=TA_CENTER,
            textColor=TEXT,
            spaceAfter=6,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="ArialBold",
            fontSize=19,
            leading=23,
            textColor=BLUE,
            spaceAfter=10,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="PTSerif",
            fontSize=10.4,
            leading=14,
            textColor=TEXT,
            alignment=TA_LEFT,
            spaceAfter=8,
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=8.6,
            leading=11,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "note": ParagraphStyle(
            "note",
            parent=base["BodyText"],
            fontName="PTSerif",
            fontSize=10.0,
            leading=13.3,
            textColor=TEXT,
            spaceAfter=0,
        ),
        "footer_note": ParagraphStyle(
            "footer_note",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=8.4,
            leading=10.2,
            alignment=TA_CENTER,
            textColor=MUTED,
        ),
        "cell": ParagraphStyle(
            "cell",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=9.0,
            leading=11,
            textColor=TEXT,
        ),
        "cell_head": ParagraphStyle(
            "cell_head",
            parent=base["BodyText"],
            fontName="ArialBold",
            fontSize=9.1,
            leading=11,
            textColor=colors.white,
        ),
    }


def p(text: str, style: ParagraphStyle) -> Paragraph:
    replacements = [
        ("XPA-105 Radar Systems", PRODUCT_FAMILY_FOOTER),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return Paragraph(text.replace("\n", "<br/>"), style)


def make_table(style_map, headers, rows, widths):
    data = [[p(h, style_map["cell_head"]) for h in headers]]
    for row in rows:
        data.append([p(str(cell), style_map["cell"]) for cell in row])
    table = Table(data, colWidths=widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("GRID", (0, 0), (-1, -1), 0.6, GRID),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_FILL, colors.white]),
            ]
        )
    )
    return table


def note_box(style_map, text: str):
    table = Table([[p(text, style_map["note"])]], colWidths=[PAGE_W - LEFT - RIGHT])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NOTE_FILL),
                ("BOX", (0, 0), (-1, -1), 1.2, NOTE_BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def extract_architecture_image() -> Path:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    target = IMAGE_DIR / "img-000.jpg"
    if not target.exists():
        run(["pdfimages", "-all", str(INPUT_PDF), str(IMAGE_DIR / "img")])
    if not target.exists():
        raise FileNotFoundError("Не вдалося витягнути схему з PDF")
    return target


def scaled_image(path: Path, width: float) -> Image:
    with PILImage.open(path) as img:
        img_w, img_h = img.size
    height = width * img_h / img_w
    out = Image(str(path), width=width, height=height)
    out.hAlign = "CENTER"
    return out


def draw_cover(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setStrokeColor(BLUE)
    canvas_obj.setLineWidth(2.2)
    canvas_obj.line(126, PAGE_H - 132, PAGE_W - 126, PAGE_H - 132)
    canvas_obj.line(126, PAGE_H - 318, PAGE_W - 126, PAGE_H - 318)
    canvas_obj.restoreState()


def draw_page(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setStrokeColor(BLUE)
    canvas_obj.setLineWidth(2.2)
    canvas_obj.line(LEFT, PAGE_H - 56, PAGE_W - RIGHT, PAGE_H - 56)
    canvas_obj.setFont("Arial", 8.5)
    canvas_obj.setFillColor(MUTED)
    canvas_obj.drawRightString(PAGE_W - RIGHT, 18, str(doc.page))
    canvas_obj.restoreState()


def build_story(style_map):
    architecture_img = extract_architecture_image()
    story = []

    # Cover
    story += [
        Spacer(1, 1.55 * inch),
        p("Технічний звіт про моделювання XPA-105", style_map["cover_title"]),
        p("Версія 2 - поточна FPGA та базова лінія пусконалагодження", style_map["cover_subtitle"]),
        Spacer(1, 0.2 * inch),
        p(
            "Охоплення: базова лінія після замикання таймінгу, стан debug-інструментування та готовність до апаратного пусконалагодження для розгортання на XC7A200T.",
            style_map["cover_scope"],
        ),
        Spacer(1, 2.4 * inch),
        p("XPA-105 Radar Systems | 2026-03-18 | Версія 2.0", style_map["cover_scope"]),
        p("Вихідний репозиторій: PLFM_RADAR (fork/main)", style_map["cover_scope"]),
        PageBreak(),
    ]

    # Section 1
    story += [
        p("1. Підсумок для керівництва", style_map["h1"]),
        p(
            "Цей звіт замінює попередні підсумки, що спиралися лише на моделювання, оскільки тепер він прив'язаний до актуального апаратно-орієнтованого стану проєкту. Поточною виробничою ціллю є FPGA XC7A200T-2FBG484I, Build 13 зафіксований як базова лінія для пусконалагодження, а також уже сформовано і базовий бітстрім без ILA, і debug-версію з ILA. Перевірка охоплює regression suites, інтеграційні golden-match тести, CDC-рев'ю з waivers для підтверджених false positive, а також замикання таймінгу на імплементації.",
            style_map["body"],
        ),
        make_table(
            style_map,
            ["Метрика", "Поточне значення", "Статус"],
            [
                ["FPGA-ціль", "XC7A200T-2FBG484I", "Поточна виробнича базова лінія"],
                ["Замороження збірки", "Build 13 (tag build13_candidate_v1)", "Кандидат зафіксований"],
                ["Таймінг (baseline)", "WNS +0.311 ns / TNS 0.000", "PASS"],
                ["Regression suites", "13/13", "PASS"],
                ["Integration golden match", "2048 / 2048", "PASS"],
                ["ILA debug build", "4 ядра, 92 біти, глибина 4096", "Згенеровано"],
                ["Bring-up scripts", "program_fpga.tcl + ila_capture.tcl", "Готово"],
            ],
            [1.65 * inch, 2.25 * inch, 2.35 * inch],
        ),
        PageBreak(),
    ]

    # Section 2
    story += [
        p("2. Поточна архітектурна базова лінія", style_map["h1"]),
        p(
            "Активний тракт сигналу, як і раніше, побудований навколо носія 10.5 GHz, ПЧ 120 MHz, ADC на 400 MSPS, CIC-децимації, FIR-очищення, узгодженої фільтрації та доплерівської обробки. Поточна політика апаратної верифікації вимагає не лише моделювання, а й перевірок, орієнтованих на імплементацію: таймінг, CDC, constraints і triage попереджень до виходу на фізичну плату.",
            style_map["body"],
        ),
    ]
    img = scaled_image(architecture_img, 5.0 * inch)
    story += [
        img,
        p("Рисунок 2.1 - Опорна архітектура XPA-105.", style_map["caption"]),
        make_table(
            style_map,
            ["Параметр", "Значення"],
            [
                ["Несуча частота", "10.5 GHz"],
                ["Проміжна частота (IF)", "120 MHz"],
                ["Частота дискретизації ADC", "400 MSPS"],
                ["Системний такт", "100 MHz"],
                ["CIC-децимація", "4x"],
                ["FFT matched filter", "Ланцюжок на 1024 точки"],
                ["Doppler FFT", "32 точки"],
                ["Range bins", "64"],
                ["Chirps на кадр", "32"],
            ],
            [2.8 * inch, 3.0 * inch],
        ),
        PageBreak(),
    ]

    # Section 3
    story += [
        p("3. Перевірка та критерії якості", style_map["h1"]),
        make_table(
            style_map,
            ["Гейт", "Результат", "Примітки"],
            [
                ["Набори unit/co-sim тестів", "PASS", "Пройдено 13/13 regression suites"],
                ["Integration testbench", "PASS", "2048/2048 збіг із golden reference"],
                ["CDC static analysis", "PASS with waivers", "5 criticals підтверджені як false positive"],
                ["DRC/methodology triage", "Reviewed", "Попередження класифіковані, неблокувальні задокументовані"],
                ["Покриття constraints і таймінгу", "PASS", "На базовій лінії немає failing user timing constraints"],
            ],
            [2.25 * inch, 1.3 * inch, 2.95 * inch],
        ),
        Spacer(1, 0.18 * inch),
        note_box(
            style_map,
            "Ключовий урок проєкту: для sign-off перед виходом на апаратну плату одного лише моделювання недостатньо. Потрібні CDC-рев'ю, замикання таймінгу, triage methodology warnings і перевірка покриття constraints, інакше сюрпризи на пусконалагодженні майже гарантовані.",
        ),
        PageBreak(),
    ]

    # Section 4
    story += [
        p("4. Debug-інструментування та готовність до пусконалагодження", style_map["h1"]),
        make_table(
            style_map,
            ["Артефакт", "Поточний стан"],
            [
        ["Базовий бітстрім", "Згенеровано (без ILA)"],
        ["Debug-бітстрім", "Згенеровано з 4 ILA-ядрами"],
                ["Покриття probe-сигналів", "Загалом 92 біти"],
                ["ILA timing", "Домен 100 MHz чистий; debug-шлях 400 MHz має негативний slack і позначений як debug-use"],
                ["Стратегія мапінгу нетів", "Post-synth пошук цільових нетів + стійке wildcard/pin-based розв'язання"],
            ],
            [2.35 * inch, 3.85 * inch],
        ),
        Spacer(1, 0.18 * inch),
        p(
            "Скрипти пусконалагодження вже підготовлені та перевірені в потоці: програмування FPGA і структуровані сценарії ILA capture. Це підтримує поетапне апаратне виконання - від перевірки clock/reset до валідації DDC, matched filter і range/doppler тракту.",
            style_map["body"],
        ),
        PageBreak(),
    ]

    # Section 5
    story += [
        p("5. Стратегія міграції на dev-board", style_map["h1"]),
        make_table(
            style_map,
            ["Ціль", "Top wrapper", "Constraint file", "Build script"],
            [
                ["Production", "radar_system_top", "constraints/xc7a200t_fbg484.xdc", "project main flow"],
                ["TE0712/TE0701", "radar_system_top_te0712_dev", "constraints/te0712_te0701_minimal.xdc", "scripts/build_te0712_dev.tcl"],
                ["TE0713/TE0701", "radar_system_top_te0713_dev", "constraints/te0713_te0701_minimal.xdc", "scripts/build_te0713_dev.tcl"],
            ],
            [1.1 * inch, 1.8 * inch, 2.15 * inch, 1.95 * inch],
        ),
        Spacer(1, 0.18 * inch),
        p(
            "Таке розділення цілей ізолює pinout і clocking, специфічні для плати, від ядра RTL. Це знижує ризик і дає змогу почати апаратні тести раніше на доступних у наявності модулях.",
            style_map["body"],
        ),
        PageBreak(),
    ]

    # Sections 6 and 7
    story += [
        p("6. Ключовий журнал змін (поточне покоління)", style_map["h1"]),
        make_table(
            style_map,
            ["Commit", "Зміни"],
            [
                ["f6877aa", "Підготовка до Phase 1 bring-up: ILA debug probes, CDC waivers, programming scripts"],
                ["12e63b7", "Посилено скрипт вставки ILA: deferred core creation, net resolution, виправлення MU_CNT"],
                ["0ae7b40", "Додано split-target для TE0712/TE0701 з окремими top/XDC/build flow"],
                ["967ce17", "Додано альтернативну in-stock ціль TE0713/TE0701"],
                ["fcdd270", "Опубліковано початкові docs і report PDF на GitHub Pages"],
                ["94eed1e", "Розгорнуто повну багатосторінкову engineering documentation site"],
            ],
            [1.1 * inch, 5.9 * inch],
        ),
        Spacer(1, 0.22 * inch),
        p("7. Висновок", style_map["h1"]),
        p(
            "XPA-105 перейшов від готовності, що спиралася лише на моделювання, до апаратно-орієнтованої базової лінії із замиканням таймінгу, надійним debug-інструментуванням і відтворюваними workflow пусконалагодження. Основний залишковий ризик тепер пов'язаний уже не з архітектурою або прогалинами у верифікації, а з реальною фізичною платою. Цей звіт слід вважати поточним опорним документом стану, який замінює старі simulation-only підсумки.",
            style_map["body"],
        ),
        Spacer(1, 0.1 * inch),
        note_box(style_map, "Класифікація звіту: інженерна базова лінія (поточний стан)."),
    ]

    return story


def main() -> None:
    register_fonts()
    if not INPUT_PDF.exists():
        raise FileNotFoundError(INPUT_PDF)

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        leftMargin=LEFT,
        rightMargin=RIGHT,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title="XPA-105 Simulation Technical Report UA",
    )
    story = build_story(styles())
    doc.build(story, onFirstPage=draw_cover, onLaterPages=draw_page)
    print(OUTPUT_PDF)


if __name__ == "__main__":
    main()
