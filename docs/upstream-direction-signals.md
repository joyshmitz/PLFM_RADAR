# Reading upstream direction on PLFM_RADAR

One reader's map of how to tell what is currently being worked on in `NawfalMotii79/PLFM_RADAR`, given there is no `ROADMAP.md`, no milestones, and no pinned issues. Direction is encoded in distributed signals. This note catalogs them.

**Status:** external observation by a fork maintainer, not official project documentation. Verify against `git log` and live GitHub state before treating anything here as canonical.

## Branch names encode current phase

Branches form a readable sequence of phases, each building on the previous. Observed at the time of writing (2026-04-23):

```
develop
 └── fix/pre-bringup-audit-p0
      └── integration/fft-2048-on-p0
           └── feature/mcu-firmware-build-pr1
```

Reading the stack: the maintainer is stabilizing pre-silicon FPGA state, merging the earlier stranded FFT-2048 upgrade into it, and has started MCU firmware bring-up on top. PRs scoped to any of these lanes are plausibly in scope; work orthogonal to the stack often closes as "not a priority right now" — not because it is wrong, but because it does not match what is being built this week.

Prefix conventions observed across the branch history:

- `fix/` — bug or invariant correction
- `feat/` — a new feature (may end up stranded if broad-scope)
- `integration/` — a branch that merges one branch into another in explicit waves
- `feature/...-prN` — an incremental, numbered PR series building the same subsystem

## Tags are release milestones

Tags use the form `vM.m.p-<name>`, where `<name>` is the theme of the release, not a date. Recent examples:

- `v2.0.0-fft2048` — 2048-point FFT upgrade (initially stranded, later folded into the integration branch)
- `v2.0.1-reset-fanout` — 400 MHz reset fanout timing closure patch
- `v2.0.2-p0-audit` — pre-bringup P0 audit closure

Reading recent tags tells you which concerns the maintainer just stabilized. They describe what is, not what will be.

## Commit-message prefixes are coordinate badges

Maintainer commits often lead with a short tag that locates the change in a larger, privately-held plan. Observed taxonomy:

- **Subject-line prefix `F-x.y`** — FPGA audit items, numbered against a private task list. Observed examples: `F-0.9 option B — FT2232H output_delay 11.667→3.5 ns`, `F-3.2 add DDC cosim fuzz runner`, `F-4.1 lower broadcast writes to per-device unicast`. Only the F-number is visible externally; the parent list is private.
- **Body-paragraph prefix `C-n:` and `S-n:`** — in commit bodies, not subject lines. Group related fixes together. Observed: `C-1:` chirp-controller range-mode awareness, `C-3:` chirp counter reset at DONE, `C-4:` GUI Waveform Timing opcodes; `S-1:` test-label corrections, `S-2:` replace hardcoded CHIRP_MAX constant, `S-3:` opcode clamping for reserved codes. What each letter stands for is not publicly documented.
- **Merge-wave markers** — two forms observed. As a subject-parens suffix: `feat(fpga): integrate 2048-pt FFT upgrade — non-conflicting RTL (wave 1/3)`. As a subject-prefix function: `merge(wave2): manual resolution of 6 shared files — fft-2048 × p0 audit`, `merge(wave3/tier2): port testbenches and cosim goldens`. Each wave handles a different conflict class.
- **Subject-parens suffix `(PR N of ...)`** — incremental PR series for a larger subsystem. Observed exact wording: `build(mcu): vendor STM32F7 HAL + gcc Makefile (PR 1 of firmware bring-up)`, `build(mcu): add linker script + USB CDC glue (PR 2 — firmware links)`.

The specific numbers are less informative than the pattern: a prefix or suffix marker means the commit is not standalone — it belongs to a batch you can partially reconstruct by scrolling `git log`.

## Two lanes: maintainer and owner

The signals above describe the **maintainer lane** — commits from the primary maintainer, which follow conventional-commit prefixes, numbered audit badges (`F-/C-/S-`), wave markers, and a visible branch stack.

The repository owner runs a separate **hardware lane** with different conventions:

- commits land **directly on `main`** without a PR
- subject lines are plain English — no `fix:/feat:/build()` prefix, no coordinate badge, no wave marker
- content is hardware artefacts: BOM, Gerbers, mechanical parts, PCB imagery

Observed examples on `main`:

- `Add Mechanical parts` — waveguide and heat sinks
- `Added BOM and Gerbers`
- `Add files via upload`
- `Fix image link and update mixer model in README`

Implication: if your proposal is purely hardware — a mechanical part, a BOM correction, a footprint fix — it does not need to stack on top of the pre-bringup audit branch or match the commit-style conventions described above. Related hardware changes may also land directly on `main` without PR coordination while your contribution is in review, so `main` is worth watching independently of the `develop` stack when scoping hardware work.

## How to apply this when proposing a PR

1. `git fetch upstream --prune --tags` — check the current stack of branches and recent tags.
2. `git log upstream/develop --since=2.weeks` — read the last two weeks of merged work.
3. Compare the lane of your proposed change against the current stack. If your change is orthogonal, expect it to either wait or close politely.
4. Match commit-message style: if the maintainer prefixes related work with `F-x.y` or `wave N/M`, your commits should be named so a reader can tell at a glance where they sit.

## What this document is not

- Not official project documentation.
- Not a commitment by the upstream maintainer about what ships when — the plan is deliberately kept liquid, and the signals above describe the present, not future milestones.
- Not a substitute for reading recent `git log` on upstream before proposing work.
