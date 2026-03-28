# PLFM_RADAR Repo Baseline And Agent Readiness Plan

**Status:** Draft v3  
**Date:** 2026-03-28  
**Current branch:** `codex/xpa-105-repo-baseline`  
**Git policy:** local-only work, local commits allowed, never push to `origin`, never push to `upstream`

## 1. Purpose

This plan defines how to turn the current `PLFM_RADAR` repository into a reliable, agent-readable, product-oriented engineering baseline for the `XPA-105` family.

The immediate goal is not to make the repository prettier. The goal is to make it:

- truthful
- navigable
- reproducible
- testable
- easier for humans and coding agents to modify without hallucinating structure
- suitable for long-term hardening toward a more serious product baseline

### 1.1 Epistemic Order

This plan is not absolute truth. It is the current guiding artifact and an evolving operational hypothesis that must be continuously checked against the repository itself.

Until explicitly superseded by a deliberate project decision, the current repository state is treated as the operative truth for pursuing product goals.

The project will be governed by the following order of authority:

1. **Repository reality**
   - actual files
   - runnable commands
   - passing or failing tests
   - actual artifact placement
   - actual current entrypoints
2. **Current plan and repo contract**
   - the current best interpretation of repo reality
   - the current execution sequence for improving the repo
3. **Agent instruction layers**
   - `.Codex/AGENTS.md`
   - `.claude/CLAUDE.md`
   - other tool-specific wrappers or instruction files

Operational rules:

- If observed repo reality conflicts with the plan, stop and correct the plan or explicitly record the divergence before continuing.
- Until we explicitly redefine a target architecture, target layout, or target workflow, the current repo state is the default truth baseline for decisions and implementation.
- If the plan conflicts with agent instructions, agent instructions must be updated to match the repo contract and current plan, not the other way around.
- No instruction layer may override directly observed repository state without explicit evidence and deliberate justification.
- Every implementation slice should be treated as a test of the plan itself, not only as execution of the plan.

## 2. Strategic Position

The repository is not starting from zero. It already contains real value:

- meaningful MCU tests that pass
- FPGA regression infrastructure
- working GUI and host-side tooling
- hardware design files, simulations, and manufacturing assets
- published docs and translated reports

The problem is not lack of content. The problem is lack of operating discipline at repo scale.

The repo currently behaves more like an accumulated engineering archive than a controlled system baseline.

That is acceptable history. It is not acceptable as the steady-state operating model if the repository is going to be used by multiple agents or evolved toward a more serious defense-oriented product baseline.

## 3. Current-State Diagnosis

### 3.1 What is already true

- The MCU test suite under `9_Firmware/9_1_Microcontroller/tests` runs successfully.
- The GUI side has explicit Python dependencies in `9_Firmware/9_3_GUI/requirements_dashboard.txt`.
- The FPGA side has runnable regression/build scripts under `9_Firmware/9_2_FPGA/`.
- Product-facing rebrand work to `XPA-105` has already started.

### 3.1.1 Concrete findings from direct repo inspection

- The current MCU control-plane entrypoint is `9_Firmware/9_1_Microcontroller/9_1_3_C_Cpp_Code/main.cpp`.
- The current FPGA split is one canonical core top, `9_Firmware/9_2_FPGA/radar_system_top.v`, plus board-specific wrapper tops such as:
  - `radar_system_top_te0712_dev.v`
  - `radar_system_top_te0713_dev.v`
  - `radar_system_top_te0713_umft601x_dev.v`
- The current host-side bring-up stack is not the legacy `GUI_V*` files. It is:
  - `9_Firmware/9_3_GUI/radar_dashboard.py`
  - `9_Firmware/9_3_GUI/radar_protocol.py`
  - `9_Firmware/9_3_GUI/smoke_test.py`
- Multiple legacy GUI generations are still present and materially increase ambiguity until they are explicitly marked historical, including:
  - `9_Firmware/9_3_GUI/GUI_V1.py`
  - `9_Firmware/9_3_GUI/GUI_V2.py`
  - `9_Firmware/9_3_GUI/GUI_V3.py`
  - `9_Firmware/9_3_GUI/GUI_V4.py`
  - `9_Firmware/9_3_GUI/GUI_V4_2_CSV.py`
  - `9_Firmware/9_3_GUI/GUI_V5.py`
  - `9_Firmware/9_3_GUI/GUI_V5_Demo.py`
  - `9_Firmware/9_3_GUI/GUI_V6.py`
  - `9_Firmware/9_3_GUI/GUI_V6_Demo.py`
- `docs/` is not random clutter. The HTML pages are the current published documentation surface, and `docs/artifacts/` is actively referenced by published bring-up and release-notes pages.
- The repo currently has two distinct host-facing protocol surfaces that should not be collapsed into one generic "interface" concept:
  - MCU USB CDC start/settings/GPS exchange
  - FPGA FT601 packet/status/command exchange
- Product naming is split: public-facing docs prefer `XPA-105`, while many tests, scripts, comments, and generated artifacts still use `AERIS-10`.

### 3.2 What is currently broken at repo level

- `README.md` and docs contain stale or false paths.
- The repo has no root-level validation contract.
- The repo leaks local machine assumptions into tracked code and docs.
- Published docs, engineering artifacts, release artifacts, and local-generated files are mixed together.
- Active entrypoints are not clearly separated from historical or legacy files.
- Product variants exist in prose only, not in machine-readable manifests.
- Interface contracts between firmware, FPGA, GUI, and replay/capture tooling are implicit.
- `.gitignore` does not fully contain current local workflow noise.
- The repo has many binary files but no explicit binary-handling policy.
- The `XPA-105` vs `AERIS-10` naming split is real but not yet governed, which makes current-vs-historical meaning ambiguous.
- The GUI validation path is incomplete at repo level: tests exist, but there is no root bootstrap for the Python dependencies they actually need.
- Running the MCU test suite currently leaves at least some host-built test executables in `9_Firmware/9_1_Microcontroller/tests` outside the current ignore rules, so even a healthy validation pass can dirty `git status`.
- At least one active test source still hardcodes a private absolute repo path (`9_Firmware/9_1_Microcontroller/tests/test_bug8_uart_commented_out.c`).
- Some tracked generated reports embed absolute build-host paths. Those are acceptable only as frozen evidence, not as canonical instructions.
- `docs/artifacts/` cannot be treated as generic clutter without first accounting for published pages that already link to it.

### 3.3 Why this matters specifically for agents

Agents do poorly in repos that are structurally ambiguous.

The most dangerous repo for an agent is not one that is incomplete. It is one that confidently suggests false structure:

- stale docs
- multiple competing "current" files
- hidden local assumptions
- inconsistent artifact placement
- missing validation commands

In that kind of repo, agents move fast in the wrong direction.

## 4. Design Principles For The Next Repo Baseline

### 4.1 Truth over convenience

If a path, command, or assumption is not portable and current, it should not be presented as canonical.

### 4.2 One canonical way to understand each domain

For each major domain, there must be a clearly declared current surface:

- documentation
- GUI/host software
- MCU firmware
- FPGA build and regression
- hardware and manufacturing assets
- simulation assets

### 4.3 Source vs generated vs published must be explicit

The repo must stop pretending that all tracked files are equal.

### 4.4 Validation must be runnable from the root

The repository needs a root-level operational contract that answers:

- how to bootstrap
- how to validate
- what is skipped if tools are missing
- what artifacts validation may generate

### 4.5 Product variants must be data, not just prose

The `XPA-105` family cannot live only in `README.md`. Product variants need machine-readable manifests.

### 4.6 Preserve evidence without promoting it to canon

This repo needs both canonical source surfaces and frozen engineering evidence.

Tracked bitstreams, timing reports, and bring-up artifacts may remain in the repository when they are intentionally part of the published engineering record. But they must not be treated as the current source of truth for setup, validation, or architecture.

## 5. Delta From The Previous Six-Step Outline

The earlier six-step outline was directionally correct but too shallow. It needs to be upgraded from cleanup guidance into a full repository operating model.

Previous outline:

1. Fix README/docs/license/path truth.
2. Establish canonical entrypoints.
3. Add root-level validate command.
4. Normalize local artifacts and ignore rules.
5. Split active baseline from fossils.
6. Only then write repo-local AGENTS.md.

Revised operating model:

0. Introduce a repo contract before any structural churn.
1. Repair repo truth in README/docs/license naming/path references.
2. Separate active and legacy surfaces across all domains, not just GUI.
3. Add reproducible environment bootstrap per domain.
4. Add root-level orchestration for validate/bootstrap tasks.
5. Parameterize host-specific paths instead of replacing them ad hoc.
6. Formalize artifact lifecycle: source, generated, published, release.
7. Add machine-readable variant manifests for XPA-105 family members.
8. Add protocol and sample-data contracts between domains.
9. Add licensing, provenance, and release metadata bundles.
10. Perform staged path normalization only after the repo contract exists.
11. Add repo-local AGENTS.md only after the repository actually behaves consistently.

### Why the revised plan is better

- It reduces accidental breakage during cleanup.
- It improves long-term maintainability instead of just reducing visible mess.
- It creates reusable infrastructure for future agent sessions.
- It turns undocumented assumptions into explicit project assets.
- It prepares the repo for productization and release management, not only for code edits.

## 6. Target Operating Model

The target state is a repository where a new human or agent can answer the following questions in minutes:

- What is the current product family and what are the supported variants?
- Which GUI is current?
- Which FPGA flow is canonical?
- Which firmware tests are authoritative?
- Which files are source, and which are generated?
- Where do release artifacts go?
- Which docs are published and which are engineering notes?
- How do I validate changes from the root?
- Which assumptions are machine-local and how are they configured?

## 7. Workstreams

### 7.A Dependency Map And Execution Risks

Critical path:

- `7.0 Repo Contract` -> `7.1 Truth Repair` and `7.2 Surface Separation` -> `7.3 Bootstrap`, `7.4 Path Parameterization`, and `7.5 Artifact Lifecycle` -> `7.6 Variant Manifests`, `7.7 Interface Contracts`, and `7.8 Licensing/Provenance` -> `7.10 Repo-Local Agent Instructions`
- `7.9 Staged Path Normalization` is intentionally late and should not begin until the earlier workstreams have stabilized the current naming, entrypoints, and validation paths.

Per-workstream prerequisites:

- `7.0 Repo Contract`: no prerequisites; establishes the canonical truth all later workstreams depend on.
- `7.1 Truth Repair`: depends on `7.0`; should apply the repo contract naming and artifact rules rather than inventing its own.
- `7.2 Surface Separation`: depends on `7.0`; should inform `7.3`, `7.6`, and `7.7` by declaring what is current versus historical.
- `7.3 Reproducible Environment Bootstrap`: depends on `7.0`; should use the current surfaces from `7.2` and the path rules from `7.4`.
- `7.4 Path Parameterization`: depends on `7.0` and is informed by `7.1`; otherwise bootstrap and docs cleanup risk baking private paths back in.
- `7.5 Artifact Lifecycle`: depends on `7.0` and `7.2`; otherwise cleanup work can accidentally delete or demote published evidence.
- `7.6 Variant Manifests`: depends on `7.0` and `7.2`; manifests need canonical naming and current surfaces first.
- `7.7 Interface Contracts And Replay Data`: depends on `7.0` and `7.2`; benefits from `7.3` and `7.6` once validation and variant context exist.
- `7.8 Licensing, Provenance, And Release Metadata`: depends on `7.0` and `7.5`; provenance work is much easier once artifact classes are explicit.
- `7.9 Staged Path Normalization`: depends on `7.0` and `7.2`; defer until the repo can already be navigated without renames.
- `7.10 Repo-Local Agent Instructions`: depends on `7.0`, `7.1`, `7.3`, and `7.5`; agent guidance should point to already-stable contracts, not replace them.

Primary execution risks:

- If `7.0` is skipped or weakened, every later cleanup becomes subjective again.
- If `7.2` is skipped before `7.7`, protocol documentation will mix current and legacy surfaces.
- If `7.3` starts before `7.4` is understood, bootstrap scripts may hardcode machine-local paths into the new baseline.
- If `7.5` is skipped, `docs/artifacts/` and other tracked evidence can be mistaken for disposable build debris.
- If `7.10` is done too early, tool-specific agent docs will fossilize current repo confusion.

## 7.0 Workstream 0: Repo Contract

### Objective

Create a top-level repo contract before any large structural changes.

### Proposed changes

- Add `REPO_CONTRACT.md` at repo root.
- Define domain ownership and current entrypoints.
- Declare the current MCU control-plane entrypoint:
  - `9_Firmware/9_1_Microcontroller/9_1_3_C_Cpp_Code/main.cpp`
- Declare the current FPGA structure:
  - `9_Firmware/9_2_FPGA/radar_system_top.v` as canonical core top
  - board-specific wrapper tops as separate bring-up targets, not competing canonical cores
- Declare the current host-side bring-up surface:
  - `9_Firmware/9_3_GUI/radar_dashboard.py`
  - `9_Firmware/9_3_GUI/radar_protocol.py`
  - `9_Firmware/9_3_GUI/smoke_test.py`
- Declare `9_Firmware/tools/uart_capture.py` as the current UART diagnostic capture helper.
- Declare `docs/*.html` as the current published docs surface and `docs/artifacts/` as a published evidence surface.
- Add an explicit naming policy for `XPA-105` vs `AERIS-10`:
  - use `XPA-105` in all new public-facing and current-baseline references
  - retain `AERIS-10` only in historical filenames, frozen artifacts, and intentionally grandfathered internal references until they are migrated
- Define artifact classes:
  - source
  - generated/local
  - published/docs
  - release artifacts
- Define validation commands and expected skip behavior.
- Define local-only git policy for this fork workflow.

### Why this improves the project

Without a repo contract, every later cleanup is subjective. With it, future changes can be judged against a stable baseline.

This is the single highest-leverage change for agent readiness because it creates explicit truth before code churn.

### Deliverables

- `REPO_CONTRACT.md`
- optional per-domain `CURRENT.md` files where ambiguity is high

### Acceptance criteria

- `REPO_CONTRACT.md` exists at repo root and explicitly names the current docs, GUI, MCU, and FPGA entrypoints.
- `REPO_CONTRACT.md` contains explicit sections for naming policy, artifact classes, validation routes, and local git policy.
- `REPO_CONTRACT.md` explicitly marks legacy GUI files, board-specific FPGA wrappers, and `docs/artifacts/` as scoped or non-canonical surfaces rather than generic "main" entrypoints.

## 7.1 Workstream 1: Truth Repair

### Objective

Remove false guidance from `README.md` and docs.

### Proposed changes

- Fix broken references to non-existent directories such as `10_docs`.
- Fix license filename references so docs match the actual file layout.
- Remove or rewrite stale build instructions that depend on private paths unless explicitly marked as examples.
- Add a short "repository status" note explaining that this is a working engineering baseline in transition.
- Reconcile current public docs with the actual FPGA target/baseline story:
  - avoid presenting `XC7A100T` as the current tracked bring-up baseline if current tracked docs and build scripts are centered on `XC7A200T`/TE071x work
  - if both matter, explain the distinction explicitly instead of letting them silently conflict
- Apply the Workstream 0 naming policy consistently in `README.md` and current docs instead of restating ad hoc naming exceptions in multiple places.
- Apply the Workstream 0 artifact classes consistently: tracked artifact reports with embedded absolute build-host paths are provenance records, not setup instructions.

### Why this improves the project

Bad docs are worse than missing docs. Agents trust markdown too readily. Humans do too.

Repairing repo truth reduces false navigation and avoids destructive edits based on stale assumptions.

### Deliverables

- corrected `README.md`
- corrected docs pages with no broken local references presented as canonical

### Acceptance criteria

- No broken path references remain in the current public-facing docs.
- No license text reference points to the wrong filename.
- Current public-facing docs do not silently present stale FPGA target state as canonical.
- `README.md` and current docs use `XPA-105` as the public/current product-family name unless a historical reference is explicitly called out.

## 7.2 Workstream 2: Active vs Legacy Surface Separation

### Objective

Make the current baseline obvious and reduce ambiguity from historical files.

### Proposed changes

- In `9_Firmware/9_3_GUI`, explicitly mark `radar_dashboard.py` and `radar_protocol.py` as current.
- Move older GUI generations into a `legacy/` subfolder or mark them as historical with a manifest, including the `GUI_V4_2_CSV.py`, `GUI_V5_Demo.py`, and `GUI_V6_Demo.py` variants.
- Apply the same pattern to FPGA build scripts if multiple build flows compete.
- Apply the same pattern to docs that are historical snapshots vs current docs.
- In `9_Firmware/9_2_FPGA`, explicitly distinguish:
  - canonical DSP core top (`radar_system_top.v`)
  - board-specific bring-up wrappers
  - regression/formal infrastructure
- In `docs/`, explicitly distinguish:
  - current published narrative pages
  - published evidence and artifact snapshots under `docs/artifacts/`
- In `9_Firmware/tools`, mark `uart_capture.py` as current bring-up tooling rather than leaving it as an unexplained helper script.

### Why this improves the project

This prevents agents from editing the wrong implementation just because it looks similar or newer by filename.

### Deliverables

- `CURRENT.md` or `legacy/` structure in high-ambiguity directories
- updated docs pointing to canonical entrypoints

### Acceptance criteria

- There is exactly one declared current GUI entrypoint.
- There is exactly one declared canonical validation route per domain.
- The canonical FPGA core and the board-specific wrapper entrypoints are explicitly differentiated.
- Legacy GUI files are either moved under an explicitly historical location or listed in a manifest that marks them non-current.

## 7.3 Workstream 3: Reproducible Environment Bootstrap

### Objective

Make setup reproducible from the repository root.

### Proposed changes

- Add root-level `Makefile`.
- Add targets such as:
  - `make bootstrap-gui` to install or sync the Python dependencies needed by `9_Firmware/9_3_GUI/requirements_dashboard.txt`
  - `make validate`
  - `make validate-mcu` to run `make test` in `9_Firmware/9_1_Microcontroller/tests`
  - `make validate-gui` as the canonical GUI validation route, implemented by running `python3 test_radar_dashboard.py` from `9_Firmware/9_3_GUI/` after `make bootstrap-gui`
  - `make validate-fpga-quick` to run `9_Firmware/9_2_FPGA/run_regression.sh --quick`
  - `make validate-fpga` for the fuller FPGA regression path
  - `make validate-docs` for lightweight repo-truth and docs-path checks
- Ensure each target prints explicit `PASS`, `FAIL`, or `SKIP`.
- Keep tool assumptions honest. Example: skip FPGA simulation if `iverilog` is missing.
- Keep Python assumptions honest. Example: report `SKIP` or `FAIL` clearly if `numpy`, `matplotlib`, or `h5py` are missing, instead of pretending the GUI validation route is available.

### Why this improves the project

The repo currently contains tests and scripts, but not a single top-level operational contract. That increases setup friction and causes drift between contributors.

Root orchestration makes the repo legible and stable.

### Deliverables

- root `Makefile`
- small helper scripts if needed under `tools/`

### Acceptance criteria

- `make validate` can run from repo root.
- `make validate-gui` has one canonical underlying command and does not depend on `pytest` being present.
- Missing tools or Python modules are reported as explicit `PASS`, `FAIL`, or `SKIP` outcomes with the missing executable or module name.

## 7.4 Workstream 4: Path Parameterization

### Objective

Remove host-specific assumptions from tracked scripts and docs.

### Proposed changes

- Replace hardcoded `/home/...` and `/Users/...` paths in scripts with configurable variables.
- Introduce environment or config defaults for:
  - Vivado project directory
  - bitstream path
  - capture output directory
  - replay/sample data directories
- Keep an example config checked in and personal configs ignored.
- Treat active source files and frozen artifact reports differently:
  - active scripts, tests, helper tools, and canonical docs must not require private absolute paths
  - frozen timing or build reports may legitimately contain historical host paths if clearly treated as evidence, not instructions
- Do not confuse intentional ephemeral use of `/tmp` in local validation scripts with the private absolute-path problem. Those are different issues.

### Why this improves the project

Hardcoded private paths create fake portability. Parameterization makes scripts honest and reusable.

It also prevents agents from copying private path assumptions into new code.

### Deliverables

- shared config example files
- updated TCL/scripts consuming config values

### Acceptance criteria

- Current scripts no longer require editing tracked files to run on a new machine.
- Private host paths are absent from canonical docs and active scripts.
- If private host paths remain inside frozen tracked artifacts, those artifacts are explicitly non-canonical and not presented as setup guidance.

## 7.5 Workstream 5: Artifact Lifecycle Formalization

### Objective

Stop mixing source files, local-generated outputs, published docs, and release artifacts.

### Proposed changes

- Expand `.gitignore` to contain current local workflow noise:
  - `tmp/` previews and PDF checks
  - generated captures
  - local reports
  - local environment directories
- Add ignore rules for host-built MCU test binaries and debug bundles produced by `9_Firmware/9_1_Microcontroller/tests`.
- Add `.gitattributes` for binary assets and line-ending policy.
- Keep `docs/` for published site and user-facing documents only.
- Keep `docs/artifacts/` only for artifacts intentionally referenced by published docs pages; move all other release bundles elsewhere.
- Define dedicated locations for:
  - generated local outputs
  - release bundles
  - published documentation

### Why this improves the project

This improves Git hygiene, site clarity, local cleanliness, and agent navigation simultaneously.

It also reduces the chance of accidental commits of noisy working files.

### Deliverables

- updated `.gitignore`
- new `.gitattributes`
- artifact directory policy documented in `REPO_CONTRACT.md`

### Acceptance criteria

- Current local workflows stop polluting `git status`.
- Published docs no longer share a directory with engineering release blobs unless explicitly intended.
- Running the MCU validation route does not leave untracked executables or local debug bundles behind in normal workflows.

## 7.6 Workstream 6: Variant Manifests

### Objective

Make `XPA-105` variants machine-readable.

### Proposed changes

- Add a `variants/` directory.
- Add `variants/schema.json` as the canonical manifest schema for the product-family YAML files.
- Create manifests for at least:
  - `xpa105-816`
  - `xpa105-3216`
- Include data such as:
  - manifest id and schema version
  - public product name
  - historical aliases
  - antenna type
  - intended range class
  - PA usage
  - expected board dependencies
  - current docs/report mappings
  - firmware/FPGA assumptions where stable
  - lifecycle/status classification
- Explicitly distinguish product-family variants from temporary FPGA bring-up targets such as TE0712/TE0713/UMFT601X-based validation stacks.

### Why this improves the project

Right now variants live mostly in prose. That is fragile.

Once variants are data, the docs, release process, and future validation logic can all consume the same truth source.

### Deliverables

- `variants/xpa105-816.yaml`
- `variants/xpa105-3216.yaml`
- `variants/schema.json`

### Acceptance criteria

- `variants/xpa105-816.yaml` and `variants/xpa105-3216.yaml` validate against `variants/schema.json`.
- Each variant manifest can answer, without falling back to README prose, the public name, historical aliases, board dependencies, and current docs/artifact mappings.
- TE0712/TE0713/UMFT601X bring-up stacks are not modeled as product variants inside the manifest set.

## 7.7 Workstream 7: Interface Contracts And Replay Data

### Objective

Reduce implicit coupling between firmware, FPGA, GUI, and tooling.

### Proposed changes

- Add `interfaces/` for protocol/data contracts.
- Define the current FPGA FT601 radar frame and status/command structures in a stable format.
- Define the current MCU USB CDC control/settings/GPS structures separately instead of folding them into the FT601 contract.
- Seed the first protocol descriptions from the implementations that already exist:
  - `9_Firmware/9_3_GUI/radar_protocol.py`
  - `9_Firmware/9_2_FPGA/radar_system_top.v`
  - `9_Firmware/9_1_Microcontroller/9_1_1_C_Cpp_Libraries/USBHandler.h`
  - `9_Firmware/9_1_Microcontroller/9_1_1_C_Cpp_Libraries/RadarSettings.h`
- Reuse the existing replay/golden corpus under `9_Firmware/9_2_FPGA/tb/cosim/real_data/` before inventing a parallel dataset structure from scratch.
- Ensure GUI tools and tests can run against replay data even without hardware.

### Why this improves the project

This is one of the strongest stability improvements available.

It makes cross-domain changes safer, improves regression testing, and makes the repo more useful without requiring live hardware.

### Deliverables

- separate machine-readable protocol descriptions for FT601 and MCU USB CDC surfaces
- small replay corpus
- tests wired to it where possible

### Acceptance criteria

- The FT601 contract and the MCU USB CDC contract exist as separate versioned files under `interfaces/`.
- GUI and host tools can validate at least one non-live FT601 replay scenario reproducibly without live hardware.

## 7.8 Workstream 8: Licensing, Provenance, And Release Metadata

### Objective

Turn legal and release state from inference into explicit assets.

### Proposed changes

- Add `LICENSES/` with normalized license texts.
- Add `THIRD_PARTY_NOTICES.md`.
- Add release manifests and checksums for tracked release artifacts.
- Distinguish raw source assets from released/generated outputs.
- Capture at least the obvious third-party provenance buckets already visible in the repo:
  - STM32 HAL / Cube-generated firmware scaffolding
  - Analog Devices no-OS and device-support code
  - FTDI FT601 host dependency expectations
  - TinyGPS++ and other bundled host/firmware support code

### Why this improves the project

For a more serious product trajectory, provenance and licensing cannot stay implicit.

This improves trust, release discipline, and later packaging.

### Deliverables

- `LICENSES/`
- `THIRD_PARTY_NOTICES.md`
- release manifests under `releases/` or equivalent

### Acceptance criteria

- `THIRD_PARTY_NOTICES.md` names at least the currently visible STM32 HAL, Analog Devices support code, FTDI dependency expectations, and TinyGPS++ provenance buckets.
- Every intentionally tracked release bundle has an accompanying manifest or checksum record under the chosen release-metadata location.

## 7.9 Workstream 9: Staged Path Normalization

### Objective

Prepare the repo for better portability and agent ergonomics without creating unnecessary churn too early.

### Proposed changes

- Do not immediately rename all top-level directories.
- First introduce canonical references in docs and manifests.
- Only then consider staged rename away from numbered, spaced directory names if the churn is justified.

### Why this improves the project

Immediate path renaming would create high churn across hardware, docs, scripts, and history. It is a worthwhile end-state goal, but a poor first move.

### Deliverables

- canonical path map in repo contract
- deferred rename plan

### Acceptance criteria

- A canonical path map exists in the repo contract before any high-churn rename proposal is approved.
- Any deferred rename plan explicitly references the already-declared canonical surfaces rather than redefining them.

## 7.10 Workstream 10: Repo-Local Agent Instructions

### Objective

Add repo-local agent instructions only after the repo itself becomes truthful and stable, and keep tool-specific wrappers thin.

### Proposed changes

- Keep the repo contract, validation commands, and naming policy as the primary truth source.
- Create `.Codex/AGENTS.md` only after:
  - repo contract exists
  - root validation exists
  - current entrypoints are explicit
  - artifact policy is explicit
- If Claude Code is part of the supported workflow for this repo, add `.claude/CLAUDE.md` as a thin companion file that points to the same canonical repo contracts and validation routes.
- Do not allow `.Codex/AGENTS.md` and `.claude/CLAUDE.md` to diverge on entrypoints, validation commands, naming policy, or artifact policy.

### Why this improves the project

Agent instruction files should codify stable practice, not compensate for missing structure.

### Deliverables

- repo-local `.Codex/AGENTS.md`
- repo-local `.claude/CLAUDE.md` if Claude Code is in the supported workflow

### Acceptance criteria

- Every supported agent instruction file points back to the same canonical repo contract and validation commands.
- If only one agent instruction format is intentionally supported, that scope is stated explicitly instead of being left implicit.
- The file set can remain short because the repository itself already expresses most of the truth.

## 8. Recommended Execution Order

Read and apply the dependency/prerequisite rules from Section 7.A before starting Phase A. If the phase list and a per-workstream prerequisite ever appear to conflict, Section 7.A wins.

### Phase A: Truth And Control

1. Add `REPO_CONTRACT.md`
2. Repair `README.md` and docs truth
3. Expand `.gitignore` and add `.gitattributes`
4. Remove current local workflow noise from `git status`

### Phase B: Reproducibility

5. Add root `Makefile`
6. Wire `make validate`, `validate-mcu`, `validate-gui`
7. Add explicit skip logic for missing tools

### Phase C: Surface Clarification

8. Separate current vs legacy GUI
9. Clarify current FPGA flow
10. Clarify docs publication vs engineering records

### Phase D: Product Baseline Maturity

11. Add `variants/`
12. Add `interfaces/`
13. Add replay/sample data corpus
14. Add licensing/provenance bundle

### Phase E: Final Codification

15. Write repo-local agent instruction files
16. Revisit staged path normalization only if still justified

## 9. Immediate First Implementation Slice

The best first tranche is:

1. `REPO_CONTRACT.md`
2. root `Makefile` with at least `validate`, `validate-mcu`, and `validate-gui`
3. `.gitignore` cleanup for current local noise, especially MCU test outputs and `tmp/` rendering debris
4. `README.md` truth repair

This gives the repository a truthful top-level contract before any bigger churn.

## 10. Non-Goals For The First Pass

The following should not happen in the first implementation slice:

- no giant directory rename
- no mass file rewrites for style only
- no premature AGENTS authoring
- no migration of every historical doc into a perfect taxonomy
- no attempt to solve productization, compliance, and architecture in one commit

## 11. Success Criteria

The first serious milestone is reached when all of the following are true:

- `git status` is clean during normal local workflows
- the repo has a root-level validation command
- active entrypoints are obvious
- current docs stop lying
- private path assumptions are no longer canonical
- `XPA-105` variants start existing as data
- supported agent instruction files, if present, do not diverge from the repo contract
- agents can enter the repo and reason from explicit contracts instead of archaeology

## 12. Final Recommendation

Do not start by writing a clever `AGENTS.md`.

Start by making the repository itself honest.

If the repo becomes truthful, parameterized, validated, and explicit about current surfaces, the eventual repo-local `AGENTS.md` can stay short and mostly point to existing repo contracts instead of trying to replace them.
