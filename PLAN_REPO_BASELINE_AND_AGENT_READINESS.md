# PLFM_RADAR Repo Baseline And Agent Readiness Plan

**Status:** Draft v1  
**Date:** 2026-03-28  
**Current branch:** `codex/xpa105-rebrand-docs-gui`  
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

## 5. Delta From The Previous Six-Step Outline

The earlier six-step outline was directionally correct but too shallow. It needs to be upgraded from cleanup guidance into a full repository operating model.

```diff
- 1. Fix README/docs/license/path truth.
- 2. Establish canonical entrypoints.
- 3. Add root-level validate command.
- 4. Normalize local artifacts and ignore rules.
- 5. Split active baseline from fossils.
- 6. Only then write repo-local AGENTS.md.

+ 0. Introduce a repo contract before any structural churn.
+ 1. Repair repo truth in README/docs/license naming/path references.
+ 2. Separate active and legacy surfaces across all domains, not just GUI.
+ 3. Add reproducible environment bootstrap per domain.
+ 4. Add root-level orchestration for validate/bootstrap tasks.
+ 5. Parameterize host-specific paths instead of replacing them ad hoc.
+ 6. Formalize artifact lifecycle: source, generated, published, release.
+ 7. Add machine-readable variant manifests for XPA-105 family members.
+ 8. Add protocol and sample-data contracts between domains.
+ 9. Add licensing, provenance, and release metadata bundles.
+ 10. Perform staged path normalization only after the repo contract exists.
+ 11. Add repo-local AGENTS.md only after the repository actually behaves consistently.
```

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

## 7.0 Workstream 0: Repo Contract

### Objective

Create a top-level repo contract before any large structural changes.

### Proposed changes

- Add `REPO_CONTRACT.md` at repo root.
- Define domain ownership and current entrypoints.
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

- A new contributor can identify the current path for docs, GUI, MCU, and FPGA without asking.
- The contract explicitly states what is and is not canonical.

## 7.1 Workstream 1: Truth Repair

### Objective

Remove false guidance from `README.md` and docs.

### Proposed changes

- Fix broken references to non-existent directories such as `10_docs`.
- Fix license filename references so docs match the actual file layout.
- Remove or rewrite stale build instructions that depend on private paths unless explicitly marked as examples.
- Add a short "repository status" note explaining that this is a working engineering baseline in transition.

### Why this improves the project

Bad docs are worse than missing docs. Agents trust markdown too readily. Humans do too.

Repairing repo truth reduces false navigation and avoids destructive edits based on stale assumptions.

### Deliverables

- corrected `README.md`
- corrected docs pages with no broken local references presented as canonical

### Acceptance criteria

- No broken path references remain in the current public-facing docs.
- No license text reference points to the wrong filename.

## 7.2 Workstream 2: Active vs Legacy Surface Separation

### Objective

Make the current baseline obvious and reduce ambiguity from historical files.

### Proposed changes

- In `9_Firmware/9_3_GUI`, explicitly mark `radar_dashboard.py` and `radar_protocol.py` as current.
- Move older GUI generations into a `legacy/` subfolder or mark them as historical with a manifest.
- Apply the same pattern to FPGA build scripts if multiple build flows compete.
- Apply the same pattern to docs that are historical snapshots vs current docs.

### Why this improves the project

This prevents agents from editing the wrong implementation just because it looks similar or newer by filename.

### Deliverables

- `CURRENT.md` or `legacy/` structure in high-ambiguity directories
- updated docs pointing to canonical entrypoints

### Acceptance criteria

- There is exactly one declared current GUI entrypoint.
- There is exactly one declared canonical validation route per domain.

## 7.3 Workstream 3: Reproducible Environment Bootstrap

### Objective

Make setup reproducible from the repository root.

### Proposed changes

- Add root-level `Makefile`.
- Add targets such as:
  - `make bootstrap-gui`
  - `make validate`
  - `make validate-mcu`
  - `make validate-gui`
  - `make validate-fpga`
  - `make validate-docs`
- Ensure each target prints explicit `PASS`, `FAIL`, or `SKIP`.
- Keep tool assumptions honest. Example: skip FPGA simulation if `iverilog` is missing.

### Why this improves the project

The repo currently contains tests and scripts, but not a single top-level operational contract. That increases setup friction and causes drift between contributors.

Root orchestration makes the repo legible and stable.

### Deliverables

- root `Makefile`
- small helper scripts if needed under `tools/`

### Acceptance criteria

- `make validate` can run from repo root.
- It clearly reports missing tools instead of failing ambiguously.

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

### Why this improves the project

Hardcoded private paths create fake portability. Parameterization makes scripts honest and reusable.

It also prevents agents from copying private path assumptions into new code.

### Deliverables

- shared config example files
- updated TCL/scripts consuming config values

### Acceptance criteria

- Current scripts no longer require editing tracked files to run on a new machine.
- Private host paths are absent from canonical docs and active scripts.

## 7.5 Workstream 5: Artifact Lifecycle Formalization

### Objective

Stop mixing source files, local-generated outputs, published docs, and release artifacts.

### Proposed changes

- Expand `.gitignore` to contain current local workflow noise:
  - `tmp/` previews and PDF checks
  - generated captures
  - local reports
  - local environment directories
- Add `.gitattributes` for binary assets and line-ending policy.
- Keep `docs/` for published site and user-facing documents only.
- Move engineering release artifacts out of `docs/artifacts/` if they are not intended as site content.
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

## 7.6 Workstream 6: Variant Manifests

### Objective

Make `XPA-105` variants machine-readable.

### Proposed changes

- Add a `variants/` directory.
- Create manifests for at least:
  - `xpa105-816`
  - `xpa105-3216`
- Include data such as:
  - antenna type
  - intended range class
  - PA usage
  - expected board dependencies
  - current docs/report mappings
  - firmware/FPGA assumptions where stable

### Why this improves the project

Right now variants live mostly in prose. That is fragile.

Once variants are data, the docs, release process, and future validation logic can all consume the same truth source.

### Deliverables

- `variants/xpa105-816.yaml`
- `variants/xpa105-3216.yaml`

### Acceptance criteria

- Variant-specific docs and artifacts can be mapped from manifests rather than README prose alone.

## 7.7 Workstream 7: Interface Contracts And Replay Data

### Objective

Reduce implicit coupling between firmware, FPGA, GUI, and tooling.

### Proposed changes

- Add `interfaces/` for protocol/data contracts.
- Define current radar frame and status/command structures in a stable format.
- Add `sample_data/` or `replay/` corpus for host-side validation.
- Ensure GUI tools and tests can run against replay data even without hardware.

### Why this improves the project

This is one of the strongest stability improvements available.

It makes cross-domain changes safer, improves regression testing, and makes the repo more useful without requiring live hardware.

### Deliverables

- machine-readable protocol description
- small replay corpus
- tests wired to it where possible

### Acceptance criteria

- GUI and host tools can validate at least one non-live scenario reproducibly.

## 7.8 Workstream 8: Licensing, Provenance, And Release Metadata

### Objective

Turn legal and release state from inference into explicit assets.

### Proposed changes

- Add `LICENSES/` with normalized license texts.
- Add `THIRD_PARTY_NOTICES.md`.
- Add release manifests and checksums for tracked release artifacts.
- Distinguish raw source assets from released/generated outputs.

### Why this improves the project

For a more serious product trajectory, provenance and licensing cannot stay implicit.

This improves trust, release discipline, and later packaging.

### Deliverables

- `LICENSES/`
- `THIRD_PARTY_NOTICES.md`
- release manifests under `releases/` or equivalent

### Acceptance criteria

- A reviewer can understand licensing and artifact provenance without digging through source headers manually.

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

- The repo becomes easier to navigate before any high-churn path migration starts.

## 7.10 Workstream 10: Repo-Local AGENTS.md

### Objective

Add repo-local agent instructions only after the repo itself becomes truthful and stable.

### Proposed changes

- Create `.Codex/AGENTS.md` only after:
  - repo contract exists
  - root validation exists
  - current entrypoints are explicit
  - artifact policy is explicit

### Why this improves the project

`AGENTS.md` should codify stable practice, not compensate for missing structure.

### Deliverables

- repo-local `.Codex/AGENTS.md`

### Acceptance criteria

- The file can remain short because the repository itself already expresses most of the truth.

## 8. Recommended Execution Order

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

15. Write repo-local `.Codex/AGENTS.md`
16. Revisit staged path normalization only if still justified

## 9. Immediate First Implementation Slice

The best first tranche is:

1. `REPO_CONTRACT.md`
2. root `Makefile` with at least `validate`, `validate-mcu`, and `validate-gui`
3. `.gitignore` cleanup for current local noise
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
- agents can enter the repo and reason from explicit contracts instead of archaeology

## 12. Final Recommendation

Do not start by writing a clever `AGENTS.md`.

Start by making the repository itself honest.

If the repo becomes truthful, parameterized, validated, and explicit about current surfaces, the eventual repo-local `AGENTS.md` can stay short and mostly point to existing repo contracts instead of trying to replace them.
