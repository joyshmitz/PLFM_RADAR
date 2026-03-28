#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_PDF = PROJECT_ROOT / "docs" / "XPA-105_Simulation_Report_en.pdf"
OUTPUT_PDF = PROJECT_ROOT / "docs" / "XPA-105_Simulation_Report_ua.pdf"
IMAGE_DIR = PROJECT_ROOT / "tmp" / "pdfs" / "xpa105_sim_full_images"
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


def build_styles():
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
            spaceAfter=6,
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
            fontSize=18.5,
            leading=22.5,
            textColor=BLUE,
            spaceAfter=10,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="PTSerif",
            fontSize=10.2,
            leading=13.7,
            alignment=TA_LEFT,
            textColor=TEXT,
            spaceAfter=8,
        ),
        "body_small": ParagraphStyle(
            "body_small",
            parent=base["BodyText"],
            fontName="PTSerif",
            fontSize=9.5,
            leading=12.6,
            alignment=TA_LEFT,
            textColor=TEXT,
            spaceAfter=8,
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=8.6,
            leading=11,
            alignment=TA_CENTER,
            textColor=MUTED,
            spaceAfter=8,
        ),
        "note": ParagraphStyle(
            "note",
            parent=base["BodyText"],
            fontName="PTSerif",
            fontSize=9.6,
            leading=12.6,
            alignment=TA_LEFT,
            textColor=TEXT,
            spaceAfter=0,
        ),
        "cell": ParagraphStyle(
            "cell",
            parent=base["BodyText"],
            fontName="Arial",
            fontSize=8.7,
            leading=10.6,
            textColor=TEXT,
        ),
        "cell_head": ParagraphStyle(
            "cell_head",
            parent=base["BodyText"],
            fontName="ArialBold",
            fontSize=8.9,
            leading=10.8,
            textColor=colors.white,
        ),
    }


def p(text: str, style: ParagraphStyle) -> Paragraph:
    replacements = [
        ("XPA-105 Radar Systems", PRODUCT_FAMILY_FOOTER),
        ("XPA-105 32x16", PRODUCT_VARIANT_3216),
        ("XPA-105 8x16", PRODUCT_VARIANT_816),
        ("XPA-105", PRODUCT_FAMILY),
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
    box = Table([[p(text, style_map["note"])]], colWidths=[PAGE_W - LEFT - RIGHT])
    box.setStyle(
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
    return box


def ensure_images() -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    if not (IMAGE_DIR / "img-000.png").exists():
        run(["pdfimages", "-all", str(INPUT_PDF), str(IMAGE_DIR / "img")])


def scaled_image(filename: str, width: float) -> Image:
    path = IMAGE_DIR / filename
    with PILImage.open(path) as img:
        w, h = img.size
    height = width * h / w
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
    ensure_images()
    story = []

    # Cover
    story += [
        Spacer(1, 1.45 * inch),
        p("ТЕХНІЧНИЙ ЗВІТ ПРО МОДЕЛЮВАННЯ", style_map["cover_title"]),
        p("XPA-105 X-діапазонний фазований радарний масив", style_map["cover_subtitle"]),
        p("Повноланцюгова симуляція обробки сигналів", style_map["cover_subtitle"]),
        p("з аналізом кореляції з апаратною реалізацією", style_map["cover_subtitle"]),
        Spacer(1, 0.22 * inch),
        make_table(
            style_map,
            ["10.5 GHz", "500 MHz BW", "16 елементів", "0.30 m розд. за дальністю"],
            [["2.67 m/s розд. за швидкістю", "32 chirps/beam", "ADC 400 MSPS", "AD9484, 8 біт"]],
            [1.42 * inch, 1.42 * inch, 1.42 * inch, 2.02 * inch],
        ),
        Spacer(1, 1.9 * inch),
        p("XPA-105 Radar Systems | Березень 2026 | Версія 1.0", style_map["cover_scope"]),
        p("Simulation code: aeris10_radar_sim.py | Based on github.com/NawfalMotii79/PLFM_RADAR", style_map["cover_scope"]),
        PageBreak(),
    ]

    # TOC
    story += [
        p("ЗМІСТ", style_map["h1"]),
        p("1. Вступ і огляд моделювання", style_map["body"]),
        p("2. Параметри системи (отримані з апаратури)", style_map["body"]),
        p("3. Ланцюг обробки сигналу", style_map["body"]),
        p("4. Сценарій A: базове демо (3 цілі)", style_map["body"]),
        p("4.1 Передавальний chirp-сигнал", style_map["body_small"]),
        p("4.2 Карта дальність-доплер", style_map["body_small"]),
        p("4.3 Профіль дальності", style_map["body_small"]),
        p("4.4 Доплерівський спектр", style_map["body_small"]),
        p("4.5 Діаграма променя масиву", style_map["body_small"]),
        p("4.6 Карта дальність-кут", style_map["body_small"]),
        p("4.7 Виявлення CFAR", style_map["body_small"]),
        p("4.8 Діаграма ланцюга обробки сигналу", style_map["body_small"]),
        p("4.9 Полярна діаграма антени", style_map["body_small"]),
        p("4.10 Часова діаграма CPI", style_map["body_small"]),
        p("4.11 Зведена панель", style_map["body_small"]),
        p("5. Сценарій B: Counter-UAS (5 цілей)", style_map["body"]),
        p("5.1 Карта дальність-доплер", style_map["body_small"]),
        p("5.2 Профіль дальності", style_map["body_small"]),
        p("5.3 Доплерівський спектр", style_map["body_small"]),
        p("5.4 Карта дальність-кут", style_map["body_small"]),
        p("5.5 Виявлення CFAR", style_map["body_small"]),
        p("5.6 Зведена панель", style_map["body_small"]),
        p("6. Підсумок кореляції з апаратурою", style_map["body"]),
        p("7. Оцінка готовності до демо", style_map["body"]),
        PageBreak(),
    ]

    # Intro
    story += [
        p("1. Вступ і огляд моделювання", style_map["h1"]),
        p(
            "Цей звіт подає результати повноланцюгової симуляції обробки сигналів для X-діапазонного фазованого радара XPA-105. Кожен параметр, використаний у моделюванні - центральна частота, смуга chirp-сигналу, частота дискретизації ADC, геометрія антенного масиву, ваги beamforming та часові параметри - був узятий безпосередньо з відкритих файлів апаратного проєкту PLFM_RADAR: Verilog, C firmware, схем і Python GUI.",
            style_map["body"],
        ),
        p(
            "Симуляція охоплює повний радарний тракт: генерацію FMCW chirp-сигналу (ADF4382A), поширення відбитого сигналу від цілі з амплітудою за радарним рівнянням, доплерівський зсув і просторову фазу, dechirp-змішування (LT5552), дискретизацію ADC (AD9484 на 400 MSPS, 8 біт), range FFT, Doppler FFT, звичайний beamforming для 16 елементів антени (4 beamformer-мікросхеми ADAR1000) та виявлення цілей за допомогою CA-CFAR.",
            style_map["body"],
        ),
        p(
            "Оцінено два робочі сценарії: базове демо з трьома добре розділеними цілями для інвесторської презентації та сценарій counter-UAS з п'ятьма малими дронами на різних дальностях і швидкостях, що відповідає основному комерційному ринку. Кожну фігуру супроводжує пояснення фізики моделювання та зелений callout-блок, який пояснює, який саме апаратний компонент реалізує цю функцію на фізичній платі XPA-105.",
            style_map["body"],
        ),
        PageBreak(),
    ]

    # System parameters
    story += [
        p("2. Параметри системи (отримані з апаратури)", style_map["h1"]),
        p(
            "Наведена нижче таблиця містить усі параметри моделювання разом із тим апаратним вузлом або файлом проєкту, з якого вони походять. Це не теоретичні припущення - це реальні налаштування регістрів, коефіцієнти дільників тактів і фізичні розміри, визначені у Verilog, firmware та schematic-файлах репозиторію PLFM_RADAR.",
            style_map["body"],
        ),
        make_table(
            style_map,
            ["Параметр", "Значення", "Апаратне джерело"],
            [
                ["Центральна частота", "10.5 GHz", "ADF4382A (synth), antenna design"],
                ["Смуга chirp-сигналу", "500 MHz (10.25 - 10.75 GHz)", "Реєстри ADF4382A"],
                ["Тривалість chirp (довга)", "30 µs", "STM32 firmware (T1 = 30.0)"],
                ["Тривалість chirp (коротка)", "0.5 µs", "STM32 firmware (T2 = 0.5)"],
                ["PRI (long / short)", "167 / 175 µs", "STM32 firmware (PRI1, PRI2)"],
                ["Chirps на позицію променя", "32", "STM32 firmware (m_max = 32)"],
                ["Частота дискретизації ADC", "400 MSPS", "AD9484; AD9523-1 OUT4 = VCO/9"],
                ["Розрядність ADC", "8 біт", "Даташит AD9484"],
                ["Проміжна частота", "120 MHz", "STM32 firmware (IF_freq = 120 MHz)"],
                ["Системний такт FPGA", "100 MHz", "AD9523-1 OUT6 = VCO/36"],
                ["Такт DAC", "120 MHz", "AD9523-1 OUT10 = VCO/30"],
                ["Частота VCO", "3.6 GHz", "AD9523-1: 100 MHz VCXO x 36"],
                ["Елементи масиву", "16 (4 x 4)", "4 x ADAR1000, по 4 елементи"],
                ["Крок елементів", "lambda/2 = 14.29 mm", "Antenna layout @ 10.5 GHz"],
                ["Позиції променя (elev x az)", "31 x 50", "STM32 firmware (n_max, y_max)"],
                ["Кроковий двигун", "200 steps/rev", "STM32 firmware (Stepper_steps)"],
                ["TX-потужність на PA", "~33 dBm", "QPA2962 GaN PA, VDD = 22 V"],
                ["Струм стоку PA (Idq)", "1.68 A", "Auto-bias loop у firmware"],
                ["Роздільна здатність за дальністю", "0.30 m", "c / (2 x BW)"],
                ["Роздільна здатність за швидкістю", "2.67 m/s", "lambda / (2 x CPI)"],
                ["Макс. неоднозначна швидкість", "+/-42.8 m/s", "lambda / (4 x PRI)"],
                ["Макс. неоднозначна дальність", "1,800 m", "c x T x (f_ADC/2) / (2 x BW)"],
            ],
            [2.15 * inch, 1.8 * inch, 2.55 * inch],
        ),
        Spacer(1, 0.15 * inch),
        note_box(
            style_map,
            "Апаратна кореляція: генератор тактів AD9523-1 є часовим каркасом усієї системи. Його VCO на 3.6 GHz (100 MHz VCXO x 36) роздає фазово-узгоджені такти на всі підсистеми: 400 MHz на ADC AD9484, опорні 300 MHz на TX/RX synth-блоки ADF4382A, 120 MHz на DAC AD9708 і 100 MHz на FPGA XC7A100T. Будь-який фазовий шум на VCO напряму впливає на рівень дальнісних бічних пелюсток і чутливість у доплері. Симуляція використовує саме ці коефіцієнти розподілу тактів для моделювання часової поведінки системи.",
        ),
        PageBreak(),
    ]

    # Signal processing chain
    story += [
        p("3. Ланцюг обробки сигналу", style_map["h1"]),
        p(
            "Симуляція відтворює вісім етапів обробки, кожен з яких відповідає окремій апаратній підсистемі на платі XPA-105. Нижче наведено повний ланцюг.",
            style_map["body"],
        ),
        scaled_image("img-000.png", 5.55 * inch),
        p("Рисунок 3.1 - Ланцюг обробки сигналу XPA-105. Кожен блок відповідає фізичній мікросхемі на радарній платі.", style_map["caption"]),
        make_table(
            style_map,
            ["Етап", "Функція моделювання", "Апаратний компонент", "Ключова характеристика"],
            [
                ["1. Генерація chirp", "generate_fmcw_chirp()", "ADF4382A + AD9523-1", "BW = 500 MHz, T = 30 µs"],
                ["2. Відбиття від цілі", "generate_target_echo()", "Антена + поширення", "Радарне рівняння, просторова фаза"],
                ["3. Dechirp-змішування", "Модель beat frequency", "LT5552 mixer", "IF = 120 MHz"],
                ["4. Дискретизація ADC", "add_noise() + quantize_adc()", "AD9484", "400 MSPS, 8 біт"],
                ["5. Range FFT", "range_fft()", "XC7A100T FPGA", "512-point FFT @ 100 MHz"],
                ["6. Doppler FFT", "doppler_fft()", "XC7A100T FPGA", "32-point FFT across chirps"],
                ["7. Beamforming", "beamform_conventional()", "ADAR1000 (analog) + FPGA", "16 елементів, lambda/2"],
                ["8. Виявлення", "cfar_2d()", "FPGA / STM32", "2D CA-CFAR, поріг 13 dB"],
            ],
            [1.45 * inch, 1.55 * inch, 1.75 * inch, 1.7 * inch],
        ),
        Spacer(1, 0.15 * inch),
        note_box(
            style_map,
            "Апаратна кореляція: у фізичному пристрої етапи 1-4 є аналоговими або змішаними (ADF4382A synthesizer -> ADAR1000 TR modules -> LT5552 mixer -> AD9484 ADC). Етапи 5-8 є цифровими й виконуються на Xilinx XC7A100T FPGA. У Verilog-коді з репозиторію PLFM_RADAR присутні модулі range FFT, Doppler processing і beamforming. MCU STM32F746 керує часовою структурою chirp-сигналів, послідовностями steering і передаванням даних через UART у Python GUI.",
        ),
        PageBreak(),
    ]

    # Scenario A intro
    story += [
        p("4. Сценарій A - базове демо (3 цілі)", style_map["h1"]),
        p(
            "Цей сценарій моделює три добре розділені цілі, підібрані так, щоб картинка була максимально читабельною під час інвесторського демо. Цілі рознесені за дальністю, швидкістю та азимутом, щоб задіяти кожну вісь вимірювання радара.",
            style_map["body"],
        ),
        make_table(
            style_map,
            ["Ціль", "Дальність", "Швидкість", "Азимут", "RCS", "Опис"],
            [
                ["T0", "200 m", "+10 m/s", "0° (по нормалі)", "+5 dBsm", "Близька, наближається, на осі"],
                ["T1", "600 m", "-5 m/s", "+20°", "0 dBsm", "Середня дальність, віддаляється, поза віссю"],
                ["T2", "1000 m", "0 m/s", "-15°", "+10 dBsm", "Далека, стаціонарна, поза віссю"],
            ],
            [0.55 * inch, 0.85 * inch, 0.85 * inch, 0.9 * inch, 0.75 * inch, 2.5 * inch],
        ),
        Spacer(1, 0.15 * inch),
        p(
            "Результат CFAR-виявлення: спрацювало 25 комірок, і всі вони кластеризуються біля цілі на 200 m. Саме ця ціль є найсильнішою через невелику дальність і помірний RCS (+5 dBsm). Цілі на 600 m і 1000 m видно на карті дальність-доплер, але в усередненому по елементах вигляді вони нижче порога CFAR - для надійного виявлення їм потрібне beamforming-підсилення у їхніх кутах.",
            style_map["body"],
        ),
        PageBreak(),
    ]

    def fig_page(title, image_file, image_width, caption, body1, body2=None, note=None, small=False):
        elems = [p(title, style_map["h1"]), scaled_image(image_file, image_width), p(caption, style_map["caption"]), p(body1, style_map["body_small" if small else "body"])]
        if body2:
            elems.append(p(body2, style_map["body_small" if small else "body"]))
        if note:
            elems += [Spacer(1, 0.12 * inch), note_box(style_map, note)]
        elems.append(PageBreak())
        return elems

    # Scenario A figures
    story += fig_page(
        "4.1 Передавальний chirp-сигнал",
        "img-002.png",
        5.5 * inch,
        "Рисунок 4.1 - FMCW передавальний chirp: квадратурна складова I (угорі) та миттєва частота sweep (унизу).",
        "Що це показує: верхня панель відображає дійсну (in-phase) складову одного FMCW chirp-сигналу - синусоїдальний сигнал, частота якого лінійно зростає протягом тривалості chirp. Нижня панель показує миттєву частоту й підтверджує чистий лінійний sweep від стартової частоти до старт + 500 MHz за 30 µs. Кутовий нахил chirp становить BW/T = 500 MHz / 30 µs = 16.67 THz/s.",
        "У FMCW-радарі інформація про дальність кодується у beat frequency, яка виникає після змішування переданого chirp-сигналу з прийнятим відбиттям. Ціль на дальності R породжує beat frequency f_beat = 2R x BW / (c x T). Наприклад, для цілі на 200 m отримуємо приблизно 22.2 MHz.",
        "Апаратна реалізація: chirp генерує дробовий PLL-синтезатор ADF4382A, який тактується опорними 300 MHz від AD9523-1 (OUT0/OUT1). Внутрішній ramp generator в ADF4382A формує лінійний sweep, а його фазовий шум визначає близькі дальнісні sidelobe-рівні. Кожний chirp запускає MCU STM32F746 через GPIO PD8 (\"new chirp toggle\") з мікросекундною точністю від TIM1.",
        small=True,
    )
    story += fig_page(
        "4.2 Карта дальність-доплер",
        "img-004.png",
        5.45 * inch,
        "Рисунок 4.2 - Карта дальність-доплер (усереднення по елементах). Зелені кола позначають істинні позиції цілей.",
        "Що це показує: карта Range-Doppler є базовим виходом FMCW-радара. Горизонтальна вісь - дальність, вертикальна - радіальна швидкість, а колір відображає прийняту потужність у dB. Кожна ціль виглядає як яскрава пляма в точці перетину своєї дальності та швидкості. Зелені маркери показують істинні координати симульованих цілей.",
        "Карту RD будують так: спочатку на відліках кожного chirp виконують range FFT, що перетворює beat frequency на дальність, а потім по 32 chirp у межах CPI виконують Doppler FFT, щоб відновити фазові зміни між chirp і таким чином оцінити швидкість. У результаті формується матриця 512 x 32 комплексних значень. На графіку показано модуль у квадраті в dB, усереднений за всіма 16 елементами антени.",
        "Апаратна реалізація: range FFT реалізується як конвеєрний Radix-2 FFT на XC7A100T FPGA при системному такті 100 MHz з AD9523-1 OUT6. Оцифровані відліки надходять із AD9484 ADC на 400 MSPS через LVDS-інтерфейс, що тактується AD9523-1 OUT4/OUT5. Doppler FFT виконується по CPI (32 chirps x 167 µs PRI = 5.34 ms coherent integration time). У Verilog-дизайні присутні окремі модулі range FFT і Doppler FFT.",
        small=True,
    )
    story += fig_page(
        "4.3 Профіль дальності",
        "img-006.png",
        5.3 * inch,
        "Рисунок 4.3 - Профіль дальності: зріз по нульовому доплеру через карту дальність-доплер.",
        "Що це показує: один горизонтальний зріз карти дальність-доплер у біні нульової швидкості. Це еквівалент фільтра, який бачить лише стаціонарні цілі. Піки відповідають цілям із близькою до нуля радіальною швидкістю. Стаціонарна ціль T2 на 1000 m із RCS +10 dBsm має бути добре помітною саме тут, тоді як рухомі T0 і T1 приглушуються, бо їхня енергія розмазана по ненульових доплерівських бінів.",
        "Роздільна здатність за дальністю Delta R = c / (2 x BW) = 0.30 m визначає, наскільки близько дві цілі можуть стояти одна до одної по дальності й усе ще залишатися розділеними. Вона повністю задається смугою chirp-сигналу 500 MHz.",
        "Апаратна реалізація: роздільна здатність за дальністю визначається саме chirp bandwidth у ADF4382A. Синтезатор повинен виконувати sweep від 10.25 до 10.75 GHz без глітчів і нелінійностей. Будь-яке відхилення від ідеально лінійного sweep формує парні відбиття, тобто ghost targets у range profile. Саме тому фазово-узгоджене 300 MHz reference від AD9523-1 до ADF4382A є критичним.",
        small=True,
    )
    story += fig_page(
        "4.4 Доплерівський спектр",
        "img-008.png",
        5.3 * inch,
        "Рисунок 4.4 - Доплерівський спектр у дальнісному біні найсильнішої цілі.",
        "Що це показує: вертикальний зріз карти дальність-доплер у біні, що відповідає найсильнішій цілі. Вісь X подає радіальну швидкість, обчислену з доплерівського зсуву частоти. Піки показують, які цілі на цій дальності рухаються з відповідною швидкістю. Роздільна здатність за швидкістю Delta V = lambda / (2 x CPI) = 28.57 mm / (2 x 5.34 ms) = 2.67 m/s, а максимальна неоднозначна швидкість дорівнює приблизно +/-42.8 m/s.",
        "Поліпшити роздільну здатність за швидкістю можна, збільшуючи CPI - тобто використовуючи більше chirps на позицію променя або довший PRI. XPA-105 використовує 32 chirps на промінь, що є компромісом між роздільною здатністю за швидкістю та часом повторного проходу променя.",
        "Апаратна реалізація: доплерівська обробка вимагає фазової когерентності протягом усього CPI (32 chirps x 167 µs = 5.34 ms). Саме тому XPA-105 використовує OCXO як master reference і має закодований у STM32 firmware 180-second warm-up. Фазовий шум у ланцюгу OCXO -> AD9523-1 -> ADF4382A напряму обмежує мінімальну детектовану швидкість, оскільки повільні цілі маскуються фазошумовими pedestal-рівнями в доплері.",
        small=True,
    )
    story += fig_page(
        "4.5 Діаграма променя масиву",
        "img-010.png",
        5.45 * inch,
        "Рисунок 4.5 - Array factor: broadside-промінь (ліворуч) і п'ять керованих променів (праворуч).",
        "Що це показує: array factor, тобто діаграму випромінювання, яку формує 16-елементний лінійний масив із кроком lambda/2 на 10.5 GHz. На лівій панелі broadside-промінь (0°) має ширину приблизно +/-3.6° за рівнем 3 dB і перші sidelobes близько -13 dB - це теоретична межа для рівномірного зважування. На правій панелі показано п'ять променів, керованих у кути -30°, -15°, 0°, +15° та +30° шляхом прогресивного фазового зсуву між елементами.",
        "Коли промінь відводиться від broadside, головний пелюсток ширшає, а підсилення зменшується. На кутах порядку +/-60° array factor уже помітно деградує, тому XPA-105 обмежує електронне сканування до +/-45° і використовує механічний stepper motor на 200 steps/revolution для повного азимутального покриття.",
        "Апаратна реалізація: електронне керування променем виконується чотирма аналоговими beamformer-мікросхемами ADAR1000. Кожна ADAR1000 керує чотирма антенними елементами й забезпечує фазовий зсув до 360° з кроком близько 2.8°, а також керування підсиленням у межах +/-31 dB на елемент. STM32 програмує ADAR1000 через SPI1, використовуючи таблицю з 31 позиції steering, зашиту у firmware. Для зниження sidelobes нижче -13 dB можна застосувати amplitude tapering через VGA-вузли ADAR1000.",
        small=True,
    )
    story += fig_page(
        "4.6 Карта дальність-кут (beamformed)",
        "img-012.png",
        5.45 * inch,
        "Рисунок 4.6 - Карта дальність-кут, отримана звичайним beamforming. Зелені кола позначають істинні позиції цілей.",
        "Що це показує: результат beamforming - масив сканується по 121 кутовій позиції від -60° до +60°, і для кожної комбінації кут-дальність обчислюється прийнята потужність. Цілі видно як яскраві точки на їхніх справжніх дальностях і азимутах. Саме так радар визначає не лише дальність, а й кутове положення цілі.",
        "Кутова роздільна здатність визначається апертурою масиву й становить приблизно lambda / (N x d x cos(theta)) ~ 7.2° поблизу broadside. Це добре узгоджується з механічним кроком азимута XPA-105: 360° / 50 позицій = 7.2°, тобто система дискретизована за кутом практично за критерієм Nyquist.",
        "Апаратна реалізація: у фізичному радарі beamforming є гібридним аналогово-цифровим. ADAR1000 виконує аналогове фазове зсування на RF-частоті 10.5 GHz, формує один промінь, після чого сигнал знижується по частоті та оцифровується. FPGA вже виконує цифрове пост-оброблення. У цій симуляції використано чисто цифровий beamforming, але для одного вузькосмугового сигналу він дає той самий результат. Demo-kit ADALM-PHASER побудований на такій самій гібридній архітектурі.",
        small=True,
    )
    story += fig_page(
        "4.7 Виявлення CFAR",
        "img-014.png",
        5.45 * inch,
        "Рисунок 4.7 - Виявлення CFAR: накладання на карту дальність-доплер (ліворуч) і сигнал проти адаптивного порога (праворуч).",
        "Що це показує: детектор Constant False Alarm Rate автоматично підлаштовує поріг виявлення до локального шумового фону. Ліворуч зелені квадрати показують комірки, що перевищили адаптивний поріг. Праворуч синя крива - це потужність сигналу на zero-Doppler зрізі, а пунктирна помаранчева крива - поріг CFAR. Виявлення відбувається там, де сигнал перевищує поріг.",
        "У моделі використано двовимірний Cell-Averaging CFAR із двома guard cells і вісьмома training cells з кожного боку. Пороговий коефіцієнт дорівнює 13 dB. У demo-сценарії спрацювало 25 CFAR-комірок навколо цілі на 200 m - наступний етап centroid або peak-picking згорнув би їх в одну фінальну детекцію.",
        "Апаратна реалізація: CFAR реалізується у FPGA як ковзне вікно з компаратором. У Verilog-коді з PLFM_RADAR уже є модуль CFAR, який проходить по range bins послідовно при системному такті 100 MHz. Виявлені цілі передаються в STM32 через спільну пам'ять, а далі MCU відправляє range, Doppler і amplitude у Python GUI через UART на 115200 baud.",
        small=True,
    )
    story += fig_page(
        "4.8 Діаграма ланцюга обробки сигналу",
        "img-016.png",
        5.55 * inch,
        "Рисунок 4.8 - Блок-схема ланцюга обробки сигналу XPA-105 із позначенням апаратної мікросхеми на кожному етапі.",
        "Що це показує: повний наскрізний потік сигналу від генерації chirp-сигналу до відображення результату, де кожному блоку відповідає конкретна мікросхема. Весь конвеєр природно ділиться на три домени: analog RF, mixed-signal і digital.",
        None,
        "Апаратна реалізація: фізична PCB-архітектура поділена на чотири плати: (1) Frequency Synthesizer Board з двома ADF4382A та AD9523-1 clock tree, (2) Beamformer Board з ADAR1000 x4 і TR-перемикачами ADTR1107, (3) Digital Board з FPGA XC7A100T, ADC AD9484 і MCU STM32F746 та (4) Power Board з багаторейковим живленням. У репозиторії є complete schematics для всіх чотирьох плат, але Gerber-файли присутні лише для Frequency Synthesizer Board. Layout Power Board автор прямо позначив як unfinished.",
        small=True,
    )
    story += fig_page(
        "4.9 Полярна діаграма антени",
        "img-018.png",
        4.0 * inch,
        "Рисунок 4.9 - Полярний графік 16-елементного array factor у broadside. Радіальна шкала показує потужність у dB (0 dB = пік).",
        "Що це показує: той самий broadside array factor, що і на рисунку 4.5, але в полярних координатах. Це традиційний формат для візуалізації антенних діаграм, бо він дає змогу легко побачити головний промінь, sidelobes і нульові напрями. Оскільки масив має рівномірне зважування та симетрично центрований, діаграма є симетричною.",
        "Ширина променя за рівнем 3 dB близько 3.6° з кожного боку broadside і рівень першої sidelobe близько -13.2 dB узгоджуються з теорією для рівномірно зваженого лінійного масиву. У реальній апаратурі цю картинку дещо змінять взаємний зв'язок елементів та виробничі допуски.",
        "Апаратна реалізація: антенний масив - це 16-елементна мікросмужкова патч-антена на 10.5 GHz на Rogers high-frequency substrate. У PLFM_RADAR є результати antenna simulation, але немає fabrication files. Demo-kit ADALM-PHASER містить готовий 8-елементний патч-масив на 10.0-10.5 GHz, який можна використати для попередньої валідації beam pattern перед переходом до повного 16-елементного кастомного дизайну.",
        small=True,
    )
    story += fig_page(
        "4.10 Часова діаграма CPI",
        "img-020.png",
        5.55 * inch,
        "Рисунок 4.10 - Часова структура CPI: 32 chirps із PRI 167 µs.",
        "Що це показує: часову структуру одного Coherent Processing Interval. Кожен трикутник відповідає одному FMCW chirp-сигналу - 30 µs sweep плюс dead time до наступного PRI на 167 µs. Радар передає 32 chirps на одну позицію променя, тому повний CPI становить 32 x 167 µs = 5.34 ms.",
        "CPI визначає дві фундаментальні межі: роздільну здатність за швидкістю lambda / (2 x CPI) = 2.67 m/s і частоту оновлення кадру. За 31 позиції по elev і 50 кроків по azimuth повний напівсферичний огляд займає 31 x 50 x 5.34 ms = 8.3 s на один оберт. Це дає приблизно 0.12 Hz для повного 360° scan - достатньо для surveillance, хоча tracking mode використовуватиме вузькіший сектор.",
        "Апаратна реалізація: CPI timing задає MCU STM32F746 через TIM1 з роздільністю 1 µs. MCU перемикає GPIO PD8 для сигналу нового chirp до FPGA, PD9 для зміни elev і PD10 для кроку azimuth. GPIO PD11 вмикає та вимикає mixer LT5552, щоб blanking відбувався у dead time. Guard time між довгими і короткими chirp-послідовностями становить 175.4 µs.",
        small=True,
    )
    story += fig_page(
        "4.11 Зведена панель",
        "img-022.png",
        5.45 * inch,
        "Рисунок 4.11 - Повна зведена панель моделювання: карта дальність-доплер, профіль дальності, діаграма променя, карта дальність-кут, доплерівський спектр і параметри системи.",
        "Що це показує: зведений шестипанельний огляд усіх ключових результатів симуляції для demo-сценарію. Це саме той один слайд, який дає інвестору цілісне уявлення про можливості радара: одночасне оцінювання дальності (0.30 m), швидкості (2.67 m/s) і кута (приблизно 7°). На панелі внизу праворуч зібрано головні системні параметри.",
        None,
        "Апаратна реалізація: ця панель є Python-еквівалентом GUI XPA-105, для якого у репозиторії PLFM_RADAR є вісім ітерацій. GUI отримує оброблені дані від STM32 через UART і відображає карти дальність-доплер, beam patterns і target detections у реальному часі. Для investor demo ADALM-PHASER також має власний Python GUI на базі PyADI-IIO з дуже схожими живими візуалізаціями.",
        small=True,
    )

    # Scenario B intro
    story += [
        p("5. Сценарій B - Counter-UAS (5 дронових цілей)", style_map["h1"]),
        p(
            "Counter-UAS, тобто виявлення дронів, є головним комерційним ринком для XPA-105. Цей сценарій моделює реалістичні малі дронові цілі: низький RCS від -15 до +5 dBsm, різні швидкості від 0 до 25 m/s і дальності до 2 km.",
            style_map["body"],
        ),
        make_table(
            style_map,
            ["Ціль", "Дальність", "Швидкість", "Азимут", "RCS", "Опис"],
            [
                ["T0", "500 m", "+15 m/s", "+5°", "-10 dBsm", "Малий дрон, швидко наближається"],
                ["T1", "1200 m", "-8 m/s", "-20°", "-5 dBsm", "Середній дрон, віддаляється"],
                ["T2", "300 m", "+25 m/s", "+12°", "-15 dBsm", "Дуже малий дрон, дуже швидкий"],
                ["T3", "2000 m", "0 m/s", "0°", "+5 dBsm", "Великий дрон, зависання на макс. дальності"],
                ["T4", "800 m", "-3 m/s", "-8°", "-8 dBsm", "Малий дрон, повільний дрейф"],
            ],
            [0.55 * inch, 0.8 * inch, 0.85 * inch, 0.8 * inch, 0.75 * inch, 2.65 * inch],
        ),
        Spacer(1, 0.14 * inch),
        p(
            "Результат CFAR: спрацювали лише 3 комірки, усі вони кластеризуються навколо цілі T0 на 500 m. У неї найкращий SNR завдяки помірній дальності й RCS -10 dBsm. Дрон T2 на 300 m зі швидкістю 25 m/s є граничним - з beamforming-підсиленням у +12° його можна витягнути, але в усередненому по елементах каналі він нижче порога. Ціль T3 на 2000 m уже стоїть на межі неоднозначної дальності та потребує повної когерентної інтеграції плюс beamforming, щоб бути видимою.",
            style_map["body"],
        ),
        p(
            "Ключовий висновок: в усередненому по елементах режимі без спрямованого beamforming радар обмежений приблизно 500 m для цілі з RCS -10 dBsm. Повний 16-елементний beamforming додає близько 12 dB і розтягує дальність виявлення до 800-1000 m для такого ж RCS. Варіант XPA-105 32x16 із GaN PA QPA2962 на рівні ~33 dBm на елемент просуває це вже до 3+ km.",
            style_map["body"],
        ),
        PageBreak(),
    ]

    # Scenario B figures
    story += fig_page(
        "5.1 Карта дальність-доплер",
        "img-024.png",
        5.45 * inch,
        "Рисунок 5.1 - Карта дальність-доплер для сценарію counter-UAS. Зелені кола позначають істинні позиції дронів.",
        "Що це показує: п'ять дронових цілей на різних дальностях і швидкостях. Дрон T0 на 500 m, який наближається зі швидкістю +15 m/s, видно як найяскравішу пляму. Дуже малий дрон T2 на 300 m із RCS -15 dBsm майже похований у шумі. Дрон T3 на 2000 m, що зависає, уже лежить на межі неоднозначної дальності.",
        "Цей сценарій добре показує основну проблему counter-UAS радарів: малі дрони з RCS -10...-15 dBsm, тобто приблизно на рівні птаха, потрібно знаходити на дальностях, де радарне рівняння вже дуже сильно послаблює зворотний сигнал. Велика перевага XPA-105 тут полягає у смузі 500 MHz - роздільна здатність 0.30 m допомагає відділяти відбиття дрона від земних завад і птахів.",
        "Апаратна реалізація: для виявлення цілей із RCS -15 dBsm потрібно оптимізувати весь gain chain: підсилення антени, потужність PA, шумову температуру приймального тракту та процесинговий виграш від FFT. Саме сукупний processing gain дозволяє побачити цілі, які в сирих часових відліках сидять нижче шумової підлоги.",
        small=True,
    )
    story += fig_page(
        "5.2 Профіль дальності",
        "img-026.png",
        5.3 * inch,
        "Рисунок 5.2 - Профіль дальності (zero-Doppler зріз) для сценарію counter-UAS.",
        "Що це показує: zero-Doppler профіль дальності для C-UAS сценарію. Єдина ціль із нульовою радіальною швидкістю - це завислий дрон T3 на 2000 m із RCS +5 dBsm, і саме він має проявлятися в цьому зрізі. Але на 2000 m втрати на шляху надзвичайно великі: порівняно з ціллю на 200 m сигнал слабший приблизно на 40 dB.",
        None,
        "Апаратна реалізація: для далеких цілей на кілометр і далі варіант XPA-105 32x16 додає 4 x QPA2962 GaN PA із живленням 22 V, струмом спокою 1.68 A та потужністю близько 33 dBm на елемент, а також щілинну хвилевідну антену з більшим підсиленням, ніж у патч-масиву. Ці GaN PA є одними з найдорожчих компонентів у BOM і вимагають уважного thermal management, тому firmware має auto-bias loop на INA241A3 та ADS7830.",
        small=True,
    )
    story += fig_page(
        "5.3 Доплерівський спектр",
        "img-028.png",
        5.3 * inch,
        "Рисунок 5.3 - Доплерівський спектр у дальнісному біні дрона на 500 m.",
        "Що це показує: доплерівський спектр у біні дальності 500 m. Дрон T0, який рухається назустріч зі швидкістю +15 m/s, має сформувати пік біля +15 m/s. За роздільної здатності 2.67 m/s пік потрапляє в межі одного доплерівського біна від істинного значення. Максимальна неоднозначна швидкість +/-42.8 m/s цілком достатня для будь-якого дронового сценарію цього класу.",
        None,
        "Апаратна реалізація: доплерівська обробка природно дає ефект MTI - стаціонарний clutter потрапляє в zero-Doppler bin і може пригнічуватися clutter filter-модулями FPGA. Для counter-UAS це критично: відрізнити завислий дрон від дерева часто можливо лише за micro-Doppler signatures ротора. Роздільна здатність XPA-105 на рівні 2.67 m/s уже достатня, щоб помітити періодичну модуляцію швидкості від лопатей.",
        small=True,
    )
    story += fig_page(
        "5.4 Карта дальність-кут",
        "img-030.png",
        5.45 * inch,
        "Рисунок 5.4 - Карта дальність-кут для сценарію counter-UAS. Зелені кола позначають істинні позиції дронів.",
        "Що це показує: beamformed карта дальність-кут показує азимут усіх п'яти дронів. Найяскравішою залишається ціль на 500 m під кутом +5°. Зверни увагу, що цілі на ширших кутах, наприклад -20° для T1 чи +12° для T2, виглядають слабшими, бо steering gain зменшується зі зростанням кута.",
        "Кутова роздільна здатність близько 7° означає, що дві цілі на однаковій дальності, розділені менше ніж на 7° по азимуту, уже не розв'язуються окремо. Для раннього попередження цього достатньо, але для точного трекінгу ні. Саме тому монопульсна оцінка кута в XPA-105 може уточнювати положення до близько 1° усередині ширини променя.",
        "Апаратна реалізація: ADAR1000 підтримує монопульсне beamforming, оскільки дозволяє окремо керувати амплітудою та фазою кожного елемента. У demo-kit ADALM-PHASER є готовий приклад із sum- та difference-beams для оцінки кута з точністю кращою за ширину променя. Це та сама техніка, яка використовується в головках самонаведення та fire-control радарах.",
        small=True,
    )
    story += fig_page(
        "5.5 Виявлення CFAR",
        "img-032.png",
        5.45 * inch,
        "Рисунок 5.5 - CFAR-виявлення для counter-UAS: менше спрацювань через низький RCS цілей і більші дальності.",
        "Що це показує: у цьому сценарії спрацьовують лише три CFAR-комірки, усі навколо цілі на 500 m. Це реалістичний результат: малі дрони на великих дальностях об'єктивно важко виявляти. CFAR-поріг адаптується до шумової підлоги, і тільки пік цілі на 500 m перевищує його.",
        "Що це означає для продукту: XPA-105 8x16 без GaN PA має практичну дальність C-UAS виявлення близько 500-800 m для малих дронів. XPA-105 32x16 з GaN PA, які дають ще близько 10 dB TX-потужності, розтягує цей діапазон приблизно до 1.5-3 km. Комерційні конкуренти на кшталт Echodyne EchoGuard досягають 2-3 km на схожій X-band phased-array архітектурі, але в ціні на порядок вище.",
        "Апаратна реалізація: підняти performance можна трьома шляхами: збільшити кількість елементів, подовжити CPI або перейти на GaN PA. Архітектура XPA-105 підтримує всі три варіанти без редизайну цифрового backend.",
        small=True,
    )
    story += fig_page(
        "5.6 Зведена панель",
        "img-034.png",
        5.45 * inch,
        "Рисунок 5.6 - Зведена панель симуляції counter-UAS.",
        "Що це показує: шестипанельний підсумок для counter-UAS сценарію. Порівняно з demo-сценарієм на рисунку 4.11 цілі тут слабші, а шумова підлога виразніша, що відображає реальну складність виявлення малих дронів на далеких рубежах. Beam pattern і системні характеристики однакові в обох сценаріях - змінюються лише цілі.",
        None,
        "Таку панель можна показувати defense/security інвесторам як доказ того, що XPA-105 здатний працювати з реалістичними counter-UAS цілями. Поруч із цим логічно демонструвати живий beam steering на ADALM-PHASER при 10.5 GHz.",
        small=True,
    )

    # Hardware correlation summary
    story += [
        p("6. Підсумок кореляції з апаратурою", style_map["h1"]),
        p(
            "Нижче узагальнено, як кожен вихід симуляції співвідноситься з фізичними компонентами плати XPA-105, що саме симуляція підтверджує і що вона принципово не може перевірити без реального апаратного тесту.",
            style_map["body"],
        ),
        make_table(
            style_map,
            ["Вихід симуляції", "Апаратні вузли", "Що валідовано", "Потрібен HW-тест"],
            [
                ["TX chirp waveform", "ADF4382A + AD9523-1", "Лінійність chirp, таймінг, BW", "Фазовий шум, спектральна чистота, spurs"],
                ["Range FFT / profile", "AD9484 ADC + FPGA", "Роздільна здатність за дальністю, bin mapping", "SFDR ADC, шум квантування, jitter тактів"],
                ["Doppler FFT / spectrum", "FPGA + OCXO", "Роздільна здатність за швидкістю, max velocity", "Міжchirpова фазова когерентність, стабільність OCXO"],
                ["Beam pattern", "ADAR1000 x4 + antenna", "Array factor, steering range", "Mutual coupling, розкид елементів, scan loss"],
                ["Range-angle map", "ADAR1000 + FPGA", "Кутова роздільна здатність, beam gain", "Реальні antenna patterns, near-field effects"],
                ["CFAR detection", "FPGA + STM32", "Поріг виявлення, Pfa", "Статистика clutter, multipath, завади"],
                ["CPI timing", "STM32 TIM1 + GPIO", "Frame rate, update time", "Jitter, latency, ISR overhead"],
                ["Noise model", "LNA + mixer + ADC", "Оцінки SNR, дальні межі", "Реальний NF, gain flatness, I/Q imbalance"],
            ],
            [1.55 * inch, 1.45 * inch, 1.7 * inch, 2.1 * inch],
        ),
        Spacer(1, 0.15 * inch),
        p(
            "Правий стовпець цієї таблиці фактично визначає перелік конкретних вимірювань, які потрібно буде зробити на demo-kit ADALM-PHASER і на майбутньому прототипі XPA-105. Саме ці ризики симуляція сама по собі закрити не здатна.",
            style_map["body"],
        ),
        PageBreak(),
    ]

    # Demo readiness assessment
    story += [
        p("7. Оцінка готовності до демо", style_map["h1"]),
        p(
            "Нижче наведено оцінку готовності до інвесторського демо, що поєднує цю симуляцію, апаратне демо на ADALM-PHASER і радарний evaluation module TI IWR1443.",
            style_map["body"],
        ),
        make_table(
            style_map,
            ["Елемент демо", "Джерело", "Статус", "Вплив на інвестора"],
            [
                ["Теорія FMCW signal processing", "Ця симуляція", "READY", "Показує глибоке технічне розуміння повного радарного ланцюга"],
                ["Роздільна здатність за дальністю/доплером/кутом", "Фігури з симуляції", "READY", "Дає кількісну картину можливостей і їхніх меж"],
                ["Живий beam steering на 10.5 GHz", "ADALM-PHASER kit", "PENDING HW", "HIGH - найсильніший елемент у презентації"],
                ["Живе виявлення реальної цілі", "ADALM-PHASER + IWR1443", "PENDING HW", "HIGH - виявлення людини або дрона сприймається дуже сильно"],
                ["FPGA real-time processing", "Arty A7-100T + Verilog", "PENDING HW", "MEDIUM - показує, що дизайн працює на реальному кремнії"],
                ["Оцінка дальності виявлення counter-UAS", "Ця симуляція", "READY", "Показує чесну оцінку можливостей і меж"],
                ["Валідація апаратної собівартості", "BOM у business proposal", "READY", "Підтверджує заяву про цінову перевагу в 5-10x"],
                ["Огляд архітектури системи", "Block diagram + schematics", "READY", "Показує, що існує повний і реальний hardware design"],
            ],
            [1.85 * inch, 1.35 * inch, 0.95 * inch, 3.05 * inch],
        ),
        Spacer(1, 0.15 * inch),
        note_box(
            style_map,
            "Підсумок: пакет симуляції, тобто цей звіт, разом із business proposal PDF дає аналітичний фундамент для investor pitch. Demo-kit ADALM-PHASER після закупівлі дасть візуальний і переконливий доказ того, що технологія працює в залізі. Разом це формує повний pre-seed investor package.",
        ),
        Spacer(1, 0.18 * inch),
        p(
            "XPA-105 Radar Systems | Технічний звіт про моделювання | Березень 2026 | Усі параметри взято з github.com/NawfalMotii79/PLFM_RADAR (MIT License)\nSimulation code: aeris10_radar_sim.py | PDF generator: generate_sim_report_pdf.py | Environment: Python 3.14 + NumPy + Matplotlib + ReportLab",
            style_map["caption"],
        ),
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
    story = build_story(build_styles())
    doc.build(story, onFirstPage=draw_cover, onLaterPages=draw_page)
    print(OUTPUT_PDF)


if __name__ == "__main__":
    main()
