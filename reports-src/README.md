# Reports Source Layer

`reports-src/` is the pilot canonical source layer for long-form reports that currently live as legacy PDFs under `docs/`.

The repository needs both English and Ukrainian report sources:

- `reports-src/en/` holds English Markdown report variants.
- `reports-src/ua/` holds Ukrainian Markdown report variants.
- `reports-src/manifests/` maps report IDs to their PDF inputs, language variants, assets, and migration status.
- `reports-src/assets/` is the managed destination for figure and diagram assets once they are curated out of temporary extraction outputs.

Rules for this layer:

- Markdown is the editable source once a report enters `reports-src/`.
- PDFs remain legacy published artifacts or render targets, not the only editable truth.
- Language variants can progress at different speeds, but the manifest must make that explicit.
- `tmp/` may be used as a migration seed, but it is not the canonical long-term home of report content.

Current pilot:

- `xpa-105-antenna-report`
  - English variant seeded from `docs/AERIS_Antenna_Report.pdf` via `pdftotext`
  - Ukrainian variant seeded from `docs/XPA-105_Antenna_Report_ua.pdf` plus `tmp/pdfs/aeris_ua/svg/page_*.svg`, because the current published Ukrainian PDF does not expose a useful text layer through `pdftotext`
