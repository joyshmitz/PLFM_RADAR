# Reports Source Layer

`reports-src/` is the pilot canonical source layer for long-form reports that currently live as legacy PDFs under `docs/`.

The repository needs both English and Ukrainian report sources:

- `reports-src/en/` holds English Markdown report variants.
- `reports-src/ua/` holds Ukrainian Markdown report variants.
- `reports-src/manifests/` maps report IDs to their PDF inputs, language variants, assets, and migration status.
- `reports-src/assets/` is the managed destination for figure and diagram assets once they are curated out of temporary extraction outputs.
- `reports-src/seeds/` stores the preserved extraction inputs that connect legacy PDFs to normalized Markdown sources.
- `reports-src/tools/` stores the tracked helper scripts that bridge PDF inputs, extraction seeds, and normalized Markdown.

Rules for this layer:

- Markdown is the editable source once a report enters `reports-src/`.
- PDFs remain legacy published artifacts or render targets, not the only editable truth.
- Language variants can progress at different speeds, but the manifest must make that explicit.
- Extraction seeds that remain relevant to provenance should live under `reports-src/seeds/`, not under `tmp/`.

Current pilot:

- `xpa-105-antenna-report`
  - English variant normalized from `docs/XPA-105_Antenna_Report_en.pdf`
  - Ukrainian variant normalized from `docs/XPA-105_Antenna_Report_ua.pdf` and preserved SVG extraction outputs under `reports-src/seeds/`
  - Shared curated figures live under `reports-src/assets/xpa-105-antenna-report/common/`
  - Preserved extraction seeds live under `reports-src/seeds/xpa-105-antenna-report/`
- `xpa-105-simulation-report`
  - English variant normalized from `docs/XPA-105_Simulation_Report_en.pdf`
  - Ukrainian variant normalized from `docs/XPA-105_Simulation_Report_ua.pdf`
  - Shared curated figures live under `reports-src/assets/xpa-105-simulation-report/common/`
  - Preserved extraction seeds live under `reports-src/seeds/xpa-105-simulation-report/`
- `xpa-105-simulation-report-v2`
  - English variant normalized from `docs/XPA-105_Simulation_Report_v2_en.pdf`
  - Ukrainian variant normalized from `docs/XPA-105_Simulation_Report_v2_ua.pdf`
  - Shared curated figures live under `reports-src/assets/xpa-105-simulation-report-v2/common/`
  - Preserved extraction seeds live under `reports-src/seeds/xpa-105-simulation-report-v2/`
