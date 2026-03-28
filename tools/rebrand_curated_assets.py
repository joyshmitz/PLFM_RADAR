#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FONT_PATH = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
REPLACEMENT = "XPA-105"
SOURCE_RE = re.compile(r"^AERIS[-–—]?1[0O](?:N)?$", re.IGNORECASE)
REPLACEMENT_RE = re.compile(r"^XPA[-–—]?105$", re.IGNORECASE)


ASSETS = [
    Path("reports-src/assets/xpa-105-antenna-report/common/input-impedance.png"),
    Path("reports-src/assets/xpa-105-antenna-report/common/radiation-pattern-3d.png"),
    Path("reports-src/assets/xpa-105-antenna-report/common/radiation-pattern-cartesian.png"),
    Path("reports-src/assets/xpa-105-antenna-report/common/radiation-pattern-polar.png"),
    Path("reports-src/assets/xpa-105-antenna-report/common/s11-return-loss.png"),
    Path("reports-src/assets/xpa-105-antenna-report/common/summary-dashboard.png"),
    Path("reports-src/assets/xpa-105-antenna-report/common/vswr.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-a-beam-pattern.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-a-cfar.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-a-cpi-timing.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-a-doppler-spectrum.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-a-polar-pattern.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-a-processing-diagram.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-a-range-angle.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-a-range-doppler.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-a-range-profile.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-a-summary-dashboard.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-a-tx-chirp.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-b-cfar.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-b-doppler-spectrum.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-b-range-angle.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-b-range-doppler.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-b-range-profile.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/scenario-b-summary-dashboard.png"),
    Path("reports-src/assets/xpa-105-simulation-report/common/signal-processing-chain.png"),
]


@dataclass(frozen=True)
class Match:
    text: str
    left: int
    top: int
    width: int
    height: int


def run_text(*args: str) -> str:
    return subprocess.check_output(args, stderr=subprocess.DEVNULL, text=True)


def parse_matches(image_path: Path) -> list[Match]:
    tsv = run_text("tesseract", str(image_path), "stdout", "--psm", "6", "tsv")
    matches: list[Match] = []
    reader = csv.DictReader(io.StringIO(tsv), delimiter="\t")
    for row in reader:
        raw = (row.get("text") or "").strip()
        if not raw:
            continue
        normalized = raw.upper().replace("—", "-").replace("–", "-")
        if not (SOURCE_RE.match(normalized) or REPLACEMENT_RE.match(normalized)):
            continue
        matches.append(
            Match(
                text=normalized,
                left=int(row["left"]),
                top=int(row["top"]),
                width=int(row["width"]),
                height=int(row["height"]),
            )
        )
    return matches


def pick_text_color(image_path: Path) -> str:
    if "xpa-105-antenna-report" in str(image_path):
        return "#2b2b2b"
    return "#a3a3c5"


def sample_background(image_path: Path, match: Match) -> str:
    sample_x = max(0, match.left - 8)
    sample_y = max(0, match.top + match.height // 2)
    return run_text(
        "magick",
        str(image_path),
        "-format",
        f"%[pixel:p{{{sample_x},{sample_y}}}]",
        "info:",
    ).strip()


def apply_match(image_path: Path, match: Match, text_color: str) -> None:
    bg_color = sample_background(image_path, match)
    x1 = max(0, match.left - 10)
    y1 = max(0, match.top - 8)
    x2 = match.left + match.width + 11
    if REPLACEMENT_RE.match(match.text):
        y2 = match.top + match.height + 12
        pointsize = max(18, int(round(match.height * 1.35)))
        annotate_y = match.top + 8
    else:
        y2 = match.top + match.height + 6
        pointsize = max(18, int(round(match.height * 1.48)))
        annotate_y = match.top

    subprocess.check_call(
        [
            "magick",
            "mogrify",
            "-fill",
            bg_color,
            "-draw",
            f"rectangle {x1},{y1} {x2},{y2}",
            "-font",
            str(FONT_PATH),
            "-fill",
            text_color,
            "-pointsize",
            str(pointsize),
            "-gravity",
            "NorthWest",
            "-annotate",
            f"+{match.left}+{annotate_y}",
            REPLACEMENT,
            str(image_path),
        ],
        stderr=subprocess.DEVNULL,
    )


def verify_no_legacy_brand(image_path: Path) -> bool:
    tsv = run_text("tesseract", str(image_path), "stdout", "--psm", "6", "tsv")
    return not any(
        SOURCE_RE.match((row.get("text") or "").strip().upper().replace("—", "-").replace("–", "-"))
        for row in csv.DictReader(io.StringIO(tsv), delimiter="\t")
        if (row.get("text") or "").strip()
    )


def process_image(relative_path: Path) -> tuple[str, int]:
    image_path = ROOT / relative_path
    matches = parse_matches(image_path)
    if not matches:
        return (str(relative_path), 0)

    backup = image_path.with_suffix(image_path.suffix + ".bak")
    shutil.copy2(image_path, backup)
    try:
        text_color = pick_text_color(image_path)
        for match in matches:
            apply_match(image_path, match, text_color)
        if not verify_no_legacy_brand(image_path):
            raise RuntimeError("legacy brand still detected after patch")
    except Exception:
        shutil.move(str(backup), image_path)
        raise
    else:
        backup.unlink(missing_ok=True)
    return (str(relative_path), len(matches))


def main() -> int:
    if not FONT_PATH.exists():
        raise SystemExit(f"Font not found: {FONT_PATH}")

    changed: list[tuple[str, int]] = []
    for relative_path in ASSETS:
        result = process_image(relative_path)
        if result[1]:
            changed.append(result)

    for path, count in changed:
        print(f"{path}: replaced {count} occurrence(s)")
    print(f"updated_files={len(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
