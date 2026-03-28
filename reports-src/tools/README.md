# Report Tools

`reports-src/tools/` stores the tracked helper scripts that connect legacy PDF
inputs, preserved extraction seeds, and normalized Markdown report sources.

These scripts are part of the migration and maintenance workflow for
`reports-src/`, not general-purpose project tooling.

Current scripts:

- `build_xpa105_report_ua.py`
- `build_xpa105_report_ua_vector.py`
- `build_xpa105_simulation_report_ua.py`
- `build_xpa105_simulation_report_v2_ua.py`

The intended chain is:

`docs/*.pdf` -> `reports-src/seeds/` -> `reports-src/{en,ua}/` -> optional rendered outputs
