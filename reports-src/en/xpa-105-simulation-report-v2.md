---
report_id: xpa-105-simulation-report-v2
language: en
status: normalized-markdown-v1
source_pdf: docs/XPA-105_Simulation_Report_v2_en.pdf
source_sha256: ae8ce4b16360ea5c627e2c3798e9c6d591ac27cfd3c2c5a04ca64f0c979fa63e
assets_dir: reports-src/assets/xpa-105-simulation-report-v2/en
shared_assets_dir: reports-src/assets/xpa-105-simulation-report-v2/common
product_variants:
  - XPA-105
---

# XPA-105 Simulation Report V2

## Status And Lineage

This is the normalized English Markdown source for the current-state FPGA and bring-up baseline report.

- Product family now carried by this source: `XPA-105`
- Active naming set: `XPA-105`
- Original PDF input: [XPA-105_Simulation_Report_v2_en.pdf](/Users/sd/projects/PLFM_RADAR/docs/XPA-105_Simulation_Report_v2_en.pdf)
- Shared curated figure: [common assets](/Users/sd/projects/PLFM_RADAR/reports-src/assets/xpa-105-simulation-report-v2/common)

The goal of this file is not byte-for-byte reproduction of the legacy PDF. The goal is to preserve the engineering baseline in a searchable, reviewable, and editable source form.

## Cover Summary

| Item | Value |
| --- | --- |
| Product family | XPA-105 |
| Product title | XPA-105 Simulation Technical Report |
| Report role | Current FPGA and bring-up baseline |
| Scope | Post-timing-closure verification baseline, debug instrumentation status, and hardware bring-up readiness for XC7A200T deployment |
| Legacy report date | 2026-03-18 |
| Version | 2.0 |

## 1. Executive Summary

This report supersedes earlier simulation-only summaries by aligning to the current hardware-targeted state of the project. The production FPGA target is now `XC7A200T-2FBG484I`, Build 13 is frozen as the bring-up baseline, and both no-ILA and debug-ILA bitstreams have been generated. Verification includes regression suites, golden-match integration checks, CDC review with waivers for validated false positives, and implementation timing closure.

| Metric | Current Value | Status |
| --- | --- | --- |
| FPGA target | XC7A200T-2FBG484I | Current production baseline |
| Build freeze | Build 13 (`build13_candidate_v1`) | Frozen candidate |
| Timing (baseline) | WNS +0.311 ns / TNS 0.000 | PASS |
| Regression suites | 13/13 | PASS |
| Integration golden match | 2048 / 2048 | PASS |
| ILA debug build | 4 cores, 92 bits, depth 4096 | Generated |
| Bring-up scripts | `program_fpga.tcl` + `ila_capture.tcl` | Ready |

## 2. Current Architecture Baseline

The active signal chain remains centered on 10.5 GHz carrier, 120 MHz IF, 400 MSPS ADC, CIC decimation, FIR cleanup, matched filtering, and Doppler processing. The current hardware-verification policy requires simulation plus implementation-centric checks such as timing, CDC, constraints, and warnings triage before physical-board execution.

![Figure 2.1: architecture reference](../assets/xpa-105-simulation-report-v2/common/architecture-reference.jpg)

Figure 2.1. Architecture reference carried by the current-state report lineage.

| Parameter | Value |
| --- | --- |
| Carrier frequency | 10.5 GHz |
| IF | 120 MHz |
| ADC sample rate | 400 MSPS |
| System clock | 100 MHz |
| CIC decimation | 4x |
| Matched filter FFT | 1024-point chain |
| Doppler FFT | 32-point |
| Range bins | 64 |
| Chirps per frame | 32 |

## 3. Verification And Quality Gates

| Gate | Result | Notes |
| --- | --- | --- |
| Unit/co-sim test suites | PASS | 13/13 regression suites passed |
| Integration testbench | PASS | 2048/2048 golden reference match |
| CDC static analysis | PASS with waivers | 5 criticals validated false positive |
| DRC/methodology triage | Reviewed | Warnings categorized, non-blocking documented |
| Constraint/timing coverage | PASS | No failing user timing constraints on baseline |

Key project lesson: simulation alone is not sufficient for FPGA pre-hardware sign-off. CDC review, timing closure, methodology warnings triage, and constraint coverage are required to prevent bring-up surprises.

## 4. Debug Instrumentation And Bring-Up Readiness

| Artifact | Current State |
| --- | --- |
| Baseline bitstream | Generated (no ILA) |
| Debug bitstream | Generated with 4 ILA cores |
| Probe coverage | 92 bits total |
| ILA timing | 100 MHz domain clean; 400 MHz debug path has negative slack and is marked debug-use |
| Net mapping strategy | Post-synth targeted net discovery + robust wildcard/pin-based resolution |

Bring-up scripts are prepared and validated in flow: FPGA programming and structured ILA capture scenarios. This supports staged hardware execution from clock/reset sanity through DDC, matched filter, and range/doppler validation.

## 5. Development-Board Migration Strategy

| Target | Top Wrapper | Constraint File | Build Script |
| --- | --- | --- | --- |
| Production | `radar_system_top` | `constraints/xc7a200t_fbg484.xdc` | project main flow |
| TE0712/TE0701 | `radar_system_top_te0712_dev` | `constraints/te0712_te0701_minimal.xdc` | `scripts/build_te0712_dev.tcl` |
| TE0713/TE0701 | `radar_system_top_te0713_dev` | `constraints/te0713_te0701_minimal.xdc` | `scripts/build_te0713_dev.tcl` |

This split-target architecture isolates board-specific pinout and clocking decisions from core RTL, minimizing risk while enabling early hardware testing on in-stock modules.

## 6. Key Change Log (Current Generation)

| Commit | Change Summary |
| --- | --- |
| `f6877aa` | Phase 1 bring-up prep: ILA debug probes, CDC waivers, programming scripts |
| `12e63b7` | Hardened ILA insertion script (deferred core creation, net resolution, `MU_CNT` fix) |
| `0ae7b40` | Added TE0712/TE0701 split target with dedicated top/XDC/build flow |
| `967ce17` | Added TE0713/TE0701 alternate in-stock SoM target |
| `fcdd270` | Published initial docs and report PDFs on GitHub Pages |
| `94eed1e` | Expanded into full multi-page engineering documentation site |

## 7. Conclusion

XPA-105 has transitioned from simulation-centric readiness into a hardware-targeted baseline with timing closure, robust debug instrumentation, and reproducible bring-up workflows. Remaining uncertainty is now primarily physical-board execution risk, not unresolved architecture or verification gaps. This report should be treated as the current state reference replacing older simulation-only summaries.

Report classification: engineering baseline (current state).
