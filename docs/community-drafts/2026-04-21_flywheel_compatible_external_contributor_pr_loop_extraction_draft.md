# Flywheel-Compatible External Contributor PR Loop Extraction Draft

**Date:** 2026-04-21  
**Status:** single-source local extraction draft, not canonical  
**Purpose:** extract evergreen operators from the AERIS-10 contributor PR loop into a candidate operator library that can later be compared against the upstream Flywheel methodology without dragging Jason/PLFM-specific volatility into the reusable layer

`Flywheel-compatible` here means only: **not obviously in conflict with the upstream Flywheel methodology**. It does **not** mean this draft is part of the upstream Flywheel kernel, an official Flywheel implementation, or a verified upstream artifact.

> **Note on private references.** Links prefixed with `/Users/sd/projects/PLFM_RADAR/.local/` and `/Users/sd/.codex/` point to private corpus not published in this repository. Load-bearing content is reproduced inline where needed.

## Scope warning

This is **not** a canonical methodology kernel.

More specifically:

- it is **not** an upstream-authored Flywheel document;
- it is **not** a verified upstream canonical methodology artifact;
- it is a **local extraction draft** produced from `PLFM_RADAR` materials using a local formalization schema.

Why:

- It is distilled from **one** project-local workflow document plus one upstream snapshot
- It has **not** been triangulated across 3+ corpora / 3+ models
- It contains no formal quote bank yet, only source anchors
- Its current structure is shaped by the local `operationalizing-expertise` schema, not by a single upstream canonical spec

Use this draft as:

- a candidate operator library
- a source corpus for later triangulation
- a worked example of an `external contributor PR loop`
- a bridge artifact between local `PLFM_RADAR` practice and the upstream Flywheel methodology

Do **not** use it yet as:

- a canonical kernel
- an upstream Flywheel kernel
- a stable onboarding prompt
- a validator target

## Provenance and primary sources

### Upstream methodology references

These are the best current upstream references for the broader methodology context.

- [THE_FLYWHEEL_CORE_LOOP.md](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup/blob/main/docs/THE_FLYWHEEL_CORE_LOOP.md#L1)
  - establishes that there is a documented **Flywheel methodology**;
  - separates planning substrate from the three-tool operating loop.
- `THE_FLYWHEEL_APPROACH_TO_PLANNING_AND_BEADS_CREATION.md` — four distinct sections, each with its own line anchor:
  - [`FLYWHEEL_KERNEL`](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup/blob/main/docs/THE_FLYWHEEL_APPROACH_TO_PLANNING_AND_BEADS_CREATION.md#L2053)
  - [`Operator Library`](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup/blob/main/docs/THE_FLYWHEEL_APPROACH_TO_PLANNING_AND_BEADS_CREATION.md#L2067)
  - [`Validation Gates`](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup/blob/main/docs/THE_FLYWHEEL_APPROACH_TO_PLANNING_AND_BEADS_CREATION.md#L2271)
  - [`Anti-Patterns`](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup/blob/main/docs/THE_FLYWHEEL_APPROACH_TO_PLANNING_AND_BEADS_CREATION.md#L2284)
- [THE_FLYWHEEL_APPROACH_TO_PLANNING_AND_BEADS_CREATION.md provenance note](https://github.com/Dicklesworthstone/agentic_coding_flywheel_setup/blob/main/docs/THE_FLYWHEEL_APPROACH_TO_PLANNING_AND_BEADS_CREATION.md#L2894)
  - states that the Flywheel methodology document is itself synthesized from X posts, ACFS documentation, and CASS-derived real-world usage patterns.

### Local formalization scaffold

This extraction draft uses the following local formalization schema:

- [operationalizing-expertise/SKILL.md](/Users/sd/.codex/skills/operationalizing-expertise/SKILL.md:1)
  - provides the local concepts `triangulated kernel`, `operator library`, `validators`, and `Track A/B/C`.

### Local extraction corpus

These are the actual local materials from which this draft is distilled.

- [aeris10-workflow-pipeline.md](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:53)
- [2026-04-21 upstream snapshot](/Users/sd/projects/PLFM_RADAR/.local/memory/upstream/2026-04-21.md:1)
- [maintainer-patterns.md](/Users/sd/projects/PLFM_RADAR/.local/memory/maintainer-patterns.md:1)
  - maintainer style reversals and conventions; load-bearing for the `Maintainer-Pattern-Preserve` operator.

## Architecture map

- **Upstream reference model:** Flywheel methodology as documented in ACFS
- **Formalization scaffold:** `operationalizing-expertise` Track C -> session/practice mining
- **Source corpus:** local operational workflow + local no-delta upstream snapshot + maintainer-patterns note
- **Target artifact:** evergreen operator cards for an external-contributor PR loop
- **Join key candidate:** `cycle_id` or `candidate_id` threaded across brief, diff, review rounds, PR, and memory note

## Source corpus

### Primary source A

- [aeris10-workflow-pipeline.md](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:53)

Load-bearing anchors:

- execution topology and frozen-review loop: [53-60](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:53)
- fast-path rule: [102-106](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:102)
- assertion-shape verification lesson: [116-126](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:116)
- draft/review artifact discipline: [128-160](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:128)
- emergency revalidate/rebase path: [162-186](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:162)
- maintainer relationship and style budget: [213-217](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:213)

### Primary source B

- [2026-04-21 upstream snapshot](/Users/sd/projects/PLFM_RADAR/.local/memory/upstream/2026-04-21.md:1)

Load-bearing anchors:

- no-delta/no-new-work rule: [3-5](/Users/sd/projects/PLFM_RADAR/.local/memory/upstream/2026-04-21.md:3)
- trigger-driven waiting discipline: [15-24](/Users/sd/projects/PLFM_RADAR/.local/memory/upstream/2026-04-21.md:15)

### Primary source C

- [maintainer-patterns.md](/Users/sd/projects/PLFM_RADAR/.local/memory/maintainer-patterns.md:1)

Load-bearing anchors:

- API symmetry outranks local-scope simplicity (Jason reversal in PR #115): [13-19](/Users/sd/projects/PLFM_RADAR/.local/memory/maintainer-patterns.md:13)
- warm cherry-pick pattern — issue+evidence can outperform PR+evidence: [21-27](/Users/sd/projects/PLFM_RADAR/.local/memory/maintainer-patterns.md:21)
- narrow scope + evidence + CI-safe tests as maintainer-trust signal: [29-38](/Users/sd/projects/PLFM_RADAR/.local/memory/maintainer-patterns.md:29)

## Evergreen vs volatile split

### Evergreen candidates

- Artifact-first review loop
- Freeze artifact during live external review
- Verify assertion shape, not just test names / implied coverage
- Fast-path for genuinely narrow changes
- Preserve maintainer-local patterns over model aesthetics
- Revalidate after upstream-trigger invalidation
- No-delta => no new work

### Volatile exclusions

Do **not** promote these into the kernel:

- Jason / JJassonn69 as a specific maintainer
- `PR #104`, `PR #120`, `E5`, `F2`
- `pre-bringup-audit-p0`
- `.local/...` path layout
- “Python cross-layer contract tests + docs + dead-code cleanup” as a universal lane
- specific repo branches, dates, merge counts, or contributor rank

## First-pass candidate kernel

This section is a **local candidate kernel** for the extracted PR-loop pattern. It is not claimed as the upstream Flywheel kernel.

<!-- CANDIDATE_KERNEL_START v0.1 -->

### Axioms (candidate, not triangulated)

1. **No new motion without new delta.** If the observed external state has not changed, do not invent a fresh cycle.
2. **Review consumes frozen artifacts, not live prose.** Once an external review round begins, the reviewed artifact must not mutate underneath it.
3. **Coverage claims are hypotheses until assertion shape is read.** Test names and summaries do not prove what a harness really catches.
4. **Small scope earns small process; shared risk earns full process.** Narrow fixes should use fast-path, but shared harness / API / CI risk promotes them back to the full loop.
5. **Maintainer-local patterns outrank model-local elegance.** If a recommendation breaks sibling symmetry or established maintainer conventions, default to the maintainer pattern unless evidence compels otherwise.
6. **Upstream motion invalidates stale confidence.** A merge, review event, or scope change can collapse prior reasoning; revalidate before proceeding.

### Objective function

Maximize:

- signal-bearing PRs per unit maintainer attention
- artifact clarity per review round
- bug-catching rigor per line changed

Minimize:

- review churn caused by live artifact mutation
- false confidence from implied coverage
- maintainer-noise from unnecessary cycles
- wasted work on stale upstream assumptions

<!-- CANDIDATE_KERNEL_END v0.1 -->

## Candidate operator cards

### 🧊 Freeze-Artifact

**Definition**: Lock the analysis+diff artifact for the full duration of a live external review round so the reviewer always critiques a stable target.

**When-to-Use Triggers**:
- Review round has started and the reviewer is citing specific lines or sections
- You discover additional fixes while the current artifact is still under review
- Multiple feedback streams exist and would otherwise tempt ad-hoc hot edits

**Failure Modes**:
- Hot-edit drift: you “improve” the artifact mid-review -> reviewer comments target text that no longer exists
- Feedback shredding: partial live edits absorb one comment but destroy the audit trail for the round

**Prompt Module** (copy/paste for agents):
~~~text
[OPERATOR: 🧊 Freeze-Artifact]
1) Treat the current analysis+diff artifact as immutable for the duration of the live review round.
2) Collect all feedback and self-discovered fixes into a revision queue; do not patch the artifact yet.
3) After the round completes, produce exactly one consolidated next revision.

Output (required): a revision queue with accepted/rejected feedback items and one new artifact revision.
Optional: note which comments were rendered stale by external state changes.
Anchors: cite source lines proving the freeze rule and why it exists.
~~~

**Canonical tag**: freeze-artifact

**Quote-bank anchors**: draft-only; source anchors not yet converted into a quote bank

**Source anchors**: [workflow:53-60](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:53), [workflow:122-138](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:122), [workflow:155-160](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:155)

**Sources**: PLFM_RADAR local workflow

### ⌁ Assertion-Shape-Verify

**Definition**: Read the actual assertion logic of an existing test before claiming coverage, and read the actual symbol definitions of every named identifier you plan to reference — whether in code-under-review or in your own draft/comment — before trusting that the identifier exists or behaves as you expect.

**When-to-Use Triggers**:
- Someone says "the harness already catches this"
- A test appears to be ground-truth-based but may really use a static dict or one-sided inequality
- A candidate gap depends on whether the existing test auto-adapts to upstream changes
- You are about to publish a review comment, issue, or PR body that names specific functions / macros / symbols from the target code
- You are about to cite a helper, method, or API by its "natural" semantic name rather than its literal name in the source

**Failure Modes**:
- Name-trust trap: you trust a test's name or docstring instead of its assertion shape -> ship a redundant or blind test
- One-sided coverage illusion: you verify only the target side and miss that the "ground truth" side is stale/static
- Own-draft hallucinated identifier: you cite a plausible-sounding helper (e.g. `RangeMode.build_range_mode_commands`) that does not actually exist in the source (actual name was `RadarProtocol.apply_range_preset`); external reviewer catches it, own credibility takes the hit

**Prompt Module** (copy/paste for agents):
~~~text
[OPERATOR: ⌁ Assertion-Shape-Verify]
1) Read the exact assertions of the claimed covering test, not just its name or comments.
2) Identify both sides of the contract: target-side parse/assertion and ground-truth-side source.
3) State explicitly whether a future widen/drift would fail loudly, fail silently, or auto-adapt.
4) Before publishing any artifact that cites named symbols, grep each such symbol in the actual source; do not trust inferred or remembered names.

Output (required): a short coverage verdict with the exact assertion shape and blind-spot class, plus a pass/fail on own-draft identifier check if an outbound artifact is being produced.
Optional: candidate replacement invariant if the existing check is asymmetric.
Anchors: cite the assertion lines (not summaries) and the exact grep proof for each own-draft identifier.
~~~

**Canonical tag**: assertion-shape-verify

**Quote-bank anchors**: draft-only; source anchors not yet converted into a quote bank

**Source anchors**: [workflow:116-126](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:116)

**Sources**: PLFM_RADAR local workflow; own-draft extension learned from PR #121 comment pre-post review (2026-04-22) — Codex caught hallucinated Python helper name in initial draft

### ∅ No-Delta-No-Work

**Definition**: When the monitored upstream/review state has not changed, do not spawn a new candidate cycle or invent fresh work.

**When-to-Use Triggers**:
- Routine upstream check returns the same HEADs / branch states / PR states as the prior snapshot
- Open PRs remain mergeable but without comments, reviews, or upstream motion
- You feel pressure to “do something” despite no new external signal

**Failure Modes**:
- Activity theater: you manufacture a new candidate or ping for no reason -> maintainer noise rises without new evidence
- Premature branch churn: you start work before the trigger state changes -> duplicate or stale effort

**Prompt Module** (copy/paste for agents):
~~~text
[OPERATOR: ∅ No-Delta-No-Work]
1) Compare the current external state to the previous snapshot.
2) If there is no meaningful delta, record the no-op result and stop.
3) List only the triggers that would justify re-entry.

Output (required): a no-delta note with explicit re-entry triggers.
Optional: refresh stale metadata if the no-op note itself was missing.
Anchors: cite the unchanged state and the rule against inventing work.
~~~

**Canonical tag**: no-delta-no-work

**Quote-bank anchors**: draft-only; source anchors not yet converted into a quote bank

**Source anchors**: [snapshot:3-5](/Users/sd/projects/PLFM_RADAR/.local/memory/upstream/2026-04-21.md:3), [snapshot:15-24](/Users/sd/projects/PLFM_RADAR/.local/memory/upstream/2026-04-21.md:15)

**Sources**: PLFM_RADAR upstream memory note

### ⚡ Narrow-Fast-Path

**Definition**: Route genuinely small, single-file, low-risk fixes through a shorter loop while preserving fail->pass verification and branch hygiene.

**When-to-Use Triggers**:
- Diff is under the local small-change threshold and touches one file
- No shared harness, API symmetry, or CI hazard is implicated
- The fix is symptom-level and does not require strategic adjudication

**Failure Modes**:
- False-triviality: a deceptively small diff touches a shared contract -> under-review causes regression
- Ritual drag: you run the full multi-round process on a one-line fix -> latency/noise exceeds value

**Prompt Module** (copy/paste for agents):
~~~text
[OPERATOR: ⚡ Narrow-Fast-Path]
1) Check whether the change is genuinely narrow: single file, small diff, low blast radius.
2) If yes, skip strategic review rounds and go straight to draft -> test -> ship.
3) Preserve the hard gates that still matter: negative check, positive check, branch hygiene, PR base hygiene, memory update.

Output (required): fast-path eligibility verdict and the reduced execution path.
Optional: explicit promotion reason if the change looked small but is not.
Anchors: cite the fast-path rule and any promotion trigger.
~~~

**Canonical tag**: narrow-fast-path

**Quote-bank anchors**: draft-only; source anchors not yet converted into a quote bank

**Source anchors**: [workflow:102-106](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:102), [workflow:183-186](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:183)

**Sources**: PLFM_RADAR local workflow

### ∥ Maintainer-Pattern-Preserve

**Definition**: Preserve established maintainer-local symmetry and sibling patterns unless there is strong evidence that breaking them is necessary.

**When-to-Use Triggers**:
- Model review recommends a “cleaner” refactor in a surface with sibling classes or symmetric APIs
- A narrow fix tempts you to improve style beyond the minimal behavioral correction
- The maintainer has previously reversed style-only changes in the same family of code

**Failure Modes**:
- Model-aesthetic drift: you optimize for elegance the maintainer will immediately revert -> wasted review budget
- Pattern breakage: a local cleanup makes sibling surfaces inconsistent -> future readers inherit asymmetry

**Prompt Module** (copy/paste for agents):
~~~text
[OPERATOR: ∥ Maintainer-Pattern-Preserve]
1) Inspect sibling classes / nearby APIs / established maintainer patterns before accepting a style recommendation.
2) Ask whether the recommendation changes behavior, or only changes shape.
3) If it is shape-only and breaks a local pattern, keep the maintainer pattern by default.

Output (required): a maintainership-style verdict: preserve, deviate-with-proof, or unclear.
Optional: note the exact sibling pattern being preserved.
Anchors: cite the local pattern and the gate requiring maintainer-style sanity.
~~~

**Canonical tag**: maintainer-pattern-preserve

**Quote-bank anchors**: draft-only; source anchors not yet converted into a quote bank

**Source anchors**: [maintainer-patterns:13-19](/Users/sd/projects/PLFM_RADAR/.local/memory/maintainer-patterns.md:13) (primary evidence: Jason reversal in PR #115), [workflow:134-138](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:134), [workflow:213-217](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:213), [workflow:282-282](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:282)

**Sources**: PLFM_RADAR maintainer-patterns note (primary evidence) + local workflow (secondary context)

### ↻ Trigger-Revalidate

**Definition**: When upstream or review state changes in a way that could invalidate assumptions, re-run evidence and scope checks before continuing. Applies at two distinct moments: (a) when a new invalidating trigger is detected during ongoing work, and (b) as a mandatory action-gate re-check immediately before any outbound action (PR comment, issue post, push, merge), because long internal verification loops can leave external state stale.

**When-to-Use Triggers**:
- Upstream lands a merge on a surface your branch depends on
- A late review reveals hidden shared-harness or contract risk
- Maintainer closes/rejects a PR with rationale that attacks premise rather than implementation details
- **Action-gate:** about to publish/post/push/merge an artifact whose validity depends on external state (target PR still open, target branch still current HEAD, target issue still unresolved)

**Failure Modes**:
- Momentum blindness: you keep iterating on a stale premise after upstream invalidated it
- Scope lag: you ship under the original process tier after the change has obviously moved into a riskier class
- Action-gate stale-premise: internal verification (e.g., Freeze-Artifact multi-round review of own comment) keeps the artifact stable but does not refresh external state; the artifact then lands on a venue that has changed (PR closed, branch retargeted, issue resolved) during the verification window

**Prompt Module** (copy/paste for agents):
~~~text
[OPERATOR: ↻ Trigger-Revalidate]
1) Detect the invalidating trigger: upstream merge, rejection rationale, or late shared-risk discovery.
2) Freeze the current branch/artifact state.
3) Re-run the smallest sufficient checks: evidence, scope, rebase-risk, and process-tier selection.
4) Action-gate: immediately before any outbound action (post/push/merge), re-fetch the minimal relevant external state (e.g. `gh pr view <n> --json state,mergedAt,closedAt,updatedAt`); abort or adapt if state has changed since the start of the current loop.

Output (required): revalidation verdict: continue, promote to full loop, or drop. For action-gate invocations: external-state-still-valid pass/fail with the concrete state snapshot that justified the action.
Optional: new base branch / new artifact revision plan.
Anchors: cite the trigger and the re-entry rule. For action-gate: cite the exact pre-action state query and its response.
~~~

**Canonical tag**: trigger-revalidate

**Quote-bank anchors**: draft-only; source anchors not yet converted into a quote bank

**Source anchors**: [workflow:170-186](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:170), [workflow:315-315](/Users/sd/projects/PLFM_RADAR/.local/workflow/aeris10-workflow-pipeline.md:315)

**Sources**: PLFM_RADAR local workflow; action-gate extension learned from PR #121 comment-post slip (2026-04-22) — PR closed 3h before comment landed because Trigger-Revalidate was only applied at Phase 0, not at action gate

## What is still missing before promotion

- 2+ additional corpora from other contributor / maintainer / review-loop workflows
- Quote bank with stable anchors instead of raw file:line references
- Multi-model distillation and triangulation
- Validation scripts for:
  - operator required fields
  - anchor existence
  - volatile-term leakage into candidate kernel

## Promotion checklist

- [ ] Gather at least 2 more corpora with comparable PR/review loops
- [ ] Build quote bank from all corpora
- [ ] Distill with 3+ models
- [ ] Promote only 3/3-agreed operators into the kernel
- [ ] Move single-source-only extractions into `DISPUTED` / `UNIQUE`, not the kernel
- [ ] Add validators before calling it canonical

## Next-step recommendation

The right next move is **not** “publish this as the canonical methodology” or “treat this as an upstream Flywheel kernel”.

The right next move is:

1. keep this file as a draft extraction
2. collect 2-3 more analogous workflows
3. run true triangulation
4. then spin out a reusable kernel such as:
   - `external-contributor-pr-loop`
   - `artifact-first-review-loop`
   - `maintainer-aware-narrow-pr-method`
