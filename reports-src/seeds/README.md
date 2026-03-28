# Report Seeds

`reports-src/seeds/` stores preserved extraction inputs used during the migration
from legacy PDFs to normalized Markdown report sources.

This layer is not the primary editable source. Its purpose is provenance and
traceability:

- `docs/*.pdf` remain the legacy published inputs
- `reports-src/seeds/` preserves extraction artifacts derived from those PDFs
- `reports-src/en/` and `reports-src/ua/` hold the normalized Markdown sources

Current structure:

- `xpa-105-antenna-report/`
  - `extracted/` legacy figure extraction cache from the English source PDF
  - `xpa105_ua/` preserved SVG/PDF page exports from the Ukrainian source run
- `xpa-105-simulation-report/`
  - `xpa105_sim_full_images/` preserved extraction images for the full simulation report
- `xpa-105-simulation-report-v2/`
  - `xpa105_sim_v2_ua_images/` preserved extraction image(s) for the v2 report

If a seed directory stops being relevant, remove it deliberately and update the
corresponding manifest so provenance does not point to dead paths.
