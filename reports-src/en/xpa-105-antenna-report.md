---
report_id: xpa-105-antenna-report
language: en
status: pilot
source_pdf: docs/AERIS_Antenna_Report.pdf
source_sha256: a23574276ef8b9f3c6c20f22c90002d0d576e949ebdf301cc4d28524b24300b1
assets_dir: reports-src/assets/xpa-105-antenna-report/en
---

# XPA-105 Antenna Report

## Migration Notes

- This is the pilot English Markdown source for the legacy antenna report.
- It is seeded from `pdftotext` output from `docs/AERIS_Antenna_Report.pdf`.
- Tables, figures, and equation formatting still need manual normalization.
- The paired Ukrainian source lives in [reports-src/ua/xpa-105-antenna-report.md](/Users/sd/projects/PLFM_RADAR/reports-src/ua/xpa-105-antenna-report.md).

## Cover Summary

- Legacy title: `AERIS-10 X-Band Phased Array Radar`
- Analysis scope: `OpenEMS FDTD Analysis - Single Patch Element at 10.5 GHz`
- Report family alignment: `XPA-105`
- Cover metrics captured in the PDF:
  - `10.5 GHz`
  - `S11: -30.6 dB`
  - `7.19 dBi`
  - `50 ohm Match`
  - `RO4350B Sub.`
  - `56.7% Efficiency`
  - `50 MHz BW`
  - `128-El Array`

## Table Of Contents Seed

1. Executive Summary
2. Design Parameters
   1. Substrate: Rogers RO4350B
   2. Patch Element Geometry
   3. Bug Found in Repo's `patch_antenna.py`
3. Simulation Setup
   1. FDTD Configuration
   2. Feed Position Calibration
4. Results
   1. S-Parameters (Return Loss)
   2. Input Impedance
   3. VSWR
   4. Radiation Pattern
   5. Polar Radiation Pattern
   6. 3D Radiation Pattern
   7. Summary Dashboard
5. Efficiency & Array Performance Estimate
6. Validation Against Theory
7. Key Findings & Recommendations

## Executive Summary Seed

A single rectangular microstrip patch antenna element for the AERIS-10N phased array radar was modeled and simulated using the OpenEMS FDTD solver. The simulation validates the antenna design at 10.5 GHz on Rogers RO4350B substrate, confirming that the single element meets all performance targets for integration into the full 8x16 (128-element) phased array.

Seed metrics extracted from the current PDF:

- Resonant frequency: `10.495 GHz`
- Return loss (S11): `-30.6 dB`
- Input impedance: `47.1 + j0.2 ohm`
- `-10 dB` bandwidth: `50 MHz (0.48%)`

## Normalization Tasks

- Rebuild the metric table as Markdown instead of leaving it as extracted prose.
- Curate and rename figure assets under `reports-src/assets/xpa-105-antenna-report/en/`.
- Normalize formulas, units, and minus signs for plain-text diffability.
- Align terminology with the `XPA-105` family while preserving legacy factual wording where needed.
