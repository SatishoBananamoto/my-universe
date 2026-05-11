# CODEX-PRISM — Kai/Codex Lane For MY UNIVERSE

> Codex/Kai working lane inside MY UNIVERSE.
> This is not a fork and not a replacement for Claude's practice data.

**Created**: 2026-05-10
**Status**: Active field lane
**Parent tracker**: PRISM.md

---

## Purpose

MY UNIVERSE was built as Claude's cognitive workspace: a practice of
thinking, calibration, reflection, and field-tested improvement.

This file is the Codex/Kai lane for continuing that work without mixing
evidence streams. Claude's `CALIBRATE.md` and `REFLECT.md` remain Claude's
historical/source data. Codex/Kai observations, field notes, and portability
findings live here until they are proven general enough to promote into
core docs.

## Source Boundaries

| Surface | Role | Rule |
|---------|------|------|
| `PRISM.md` | Project source of truth | Keep it aware of this lane. |
| `CODEX-PRISM.md` | Codex/Kai field lane | Record Codex-specific work here first. |
| `CODEX-REFLECT.md` | Codex/Kai reflection lane | Record Codex interrupt evidence here, not in Claude's `REFLECT.md`. |
| `CALIBRATE.md` | Claude calibration narrative | Do not add Codex predictions directly. |
| `REFLECT.md` | Claude interrupt/reflection data | Do not add Codex reflections directly. |
| `.archive/` | Archive lane | Use before displacing any source, doc, state, history, or user data. |
| Engram | Cross-project memory/context | Query first when prior project context matters. |
| `AGENTS.md` + Codex skills | Active Codex runtime layer | Use for Codex process rules and gates. |

## Engram Anchors

Live Engram MCP is connected in Codex. Relevant entries:

- `DEC-012`: Build caliber from real MY UNIVERSE data, not from a top-down spec.
- `DEC-013`: Keep MY UNIVERSE and caliber separate, bridge with import.
- `OBS-013`: Interrupts help conscious System 2 reasoning, but automatic failures need environmental checks.

Working implication: keep narrative practice, machine-readable measurement,
and runtime process lanes separate until evidence says they should merge.

## Current State

- Repo state before this lane was added: `main` clean and 1 commit ahead of `origin/main`.
- Current Codex/Kai lane state: latest in-repo verification passed with 68 tests.
- Current publish state before this continuation-gate slice: MY UNIVERSE `main` aligned with `origin/main`; `caliber` `master` aligned with `origin/master`.
- External field session state: `caliber` commit `7e390bd` pushed with 98 tests passing; fresh-agent trial commit `439b4b8` pushed with 98 tests passing; multi-agent hardening commit `45ea13d` pushed with 101 tests passing; import cleanup commit `102b294` pushed with 103 tests passing; MCP config helper commit `4c4a781` pushed with 105 tests passing; first-user tutorial commit `64464ad` pushed with 105 tests passing.
- Engram is available through native Codex MCP tools.
- `PRISM.md` priority has enough field evidence for a REVIEW update; external user validation remains a separate product/adoption question.
- The completed field tests now cover Claude-originated MY UNIVERSE discipline running through Codex/Kai runtime surfaces inside this repo and in connected `caliber` work.

## Active Field Test

Question:

Does the three-layer model survive Claude Code -> Codex/Kai portability?

Layers under test:

1. **Always-on process rules**: Codex `AGENTS.md`, Kai skills, and runtime instructions.
2. **Event-triggered gates**: first failure, familiarity, smooth sailing, and completion pressure.
3. **Manual/deep interrupts**: `$think`, `$meta-thinking`, `$kai-sdlc`, `$done`, and Engram lookup when context matters.

Success evidence:

- Codex uses Engram before relying on stale project memory.
- Codex keeps Claude calibration/reflection data unpolluted.
- Codex records field results here before promoting anything into `THINK.md`, `REFLECT.md`, `CALIBRATE.md`, or Engram.
- Completion claims are backed by current commands, diffs, or MCP/tool evidence.
- If a repeated miss appears, the fix becomes an environmental guard, not just a better-sounding reflection.

## Working Rules For Codex/Kai In This Repo

1. Read `PRISM.md` first, then this file.
2. Use Engram for cross-project context when the task touches prior decisions, trust stack, calibration, or connected repos.
3. Do not write Codex predictions into `CALIBRATE.md`.
4. Do not write Codex reflections into `REFLECT.md`.
5. Put Codex/Kai interrupt evidence in `CODEX-REFLECT.md`.
6. Put Codex/Kai field notes below until they are proven reusable.
7. Do not delete source, docs, state, history, or user data; archive first if anything must move.
8. End active task lists with a continuation task.
9. When `Continue` is reached, use `CONTINUATION-GATE.md`: reflect, check repo evidence, optionally ask an xhigh reviewer, create a new concrete task list, and put `Continue` at the end again.
10. Promote only stable lessons:
   - to `PRISM.md` if they change project direction,
   - to core MY UNIVERSE docs if they change the practice,
   - to Engram if they should persist across projects/sessions,
   - to Codex runtime files only if they should affect future Codex behavior.

## Work Queue

- [x] Connect Codex to Engram MCP.
- [x] Create labeled Codex/Kai lane inside MY UNIVERSE.
- [x] Run the first real Codex/Kai field session inside MY UNIVERSE.
- [x] Run an external connected-project field session against `caliber`.
- [x] Record whether the three-layer model actually changed behavior.
- [x] Decide whether any result should be promoted to `PRISM.md`, Engram, or Codex runtime.
- [x] Add no-deletion/archive-first and continuation-task constraints to the Codex/Kai lane.
- [x] Add `CODEX-REFLECT.md` so Codex/Kai interrupt evidence stays separate from Claude's `REFLECT.md`.
- [x] Add `CONTINUATION-GATE.md` so recursive Continue and optional xhigh review are inspectable.
- [x] Run first fresh-agent onboarding trial against `caliber` and record evidence in `ONBOARDING-TRIAL.md`.
- [x] Continue the trial into `caliber` multi-agent CLI hardening and record evidence in `ONBOARDING-TRIAL.md`.
- [x] Continue into `caliber` CALIBRATE import cleanup and record archive/no-deletion evidence in `ONBOARDING-TRIAL.md`.
- [x] Continue into `caliber` MCP config helper and record trust-boundary evidence in `ONBOARDING-TRIAL.md`.
- [x] Continue into `caliber` first-user tutorial and record external-adoption evidence in `ONBOARDING-TRIAL.md`.
- [ ] Continue — run the next transfer or connected-project field session and record evidence here.

## Field Notes

### 2026-05-10 — Lane Bootstrap

**Trigger**: Satish asked whether Codex should continue in MY UNIVERSE or create its own work/storage lane.

**Decision**: Continue inside MY UNIVERSE, but create a labeled Codex/Kai lane rather than mixing data into Claude's calibration/reflection stream.

**Evidence**:

- Engram `DEC-013` says MY UNIVERSE and caliber should stay separate because narrative practice and machine-readable analysis serve different purposes.
- Engram `OBS-013` says automatic failures need environmental checks, not only more self-awareness.
- Current Codex runtime has native Engram MCP access after reload.

**Result**: `CODEX-PRISM.md` exists as the Codex/Kai lane. `PRISM.md` points to it.

**Next**: Use this lane while doing real work, then judge behavior from evidence rather than from the existence of the lane.

### 2026-05-10 — Field Session 1: Validator False Positive

**Trigger**: `python3 tools/validate.py` failed after the lane bootstrap with four `CALIBRATE.md` non-sequential ID warnings.

**Task**: Make validation reflect real data quality without corrupting Claude's calibration history.

**Engram use**: Queried Engram first for prior context around CALIBRATE ordering and validation. No direct prior entry existed, so current repo evidence governed the decision.

**Seed cause**: `tools/validate.py` enforced file-order sequencing. `CALIBRATE.md` is grouped by session/topic, so valid entries can appear out of numeric order. After removing the file-order assumption, the only remaining gap was `P-070`, which never existed in git history.

**Decision**: Normal validation should check entry correctness and duplicate IDs. Gaps in historical prediction IDs are a strict audit concern, not a malformed-entry failure, because filling the gap would require fabricating a prediction or renumbering history.

**Changes**:

- `tools/validate.py`: replaced file-order sequencing with duplicate checks and optional `--strict-ids` gap reporting.
- `tests/test_validate.py`: added validation tests for out-of-order IDs, duplicate IDs, default gap tolerance, and strict gap reporting.
- `tests/run_all.py`: added the validation test module to the suite.

**Verification**:

- `python3 tools/validate.py` passes.
- `python3 tools/validate.py --strict-ids` reports the real historical gap: `P-070`.
- `python3 tests/run_all.py` passes with 46 tests.
- `python3 -m compileall tools tests` passes.

**Did the three-layer model change behavior?** Yes.

- Layer 1: The no-memory-counting rule pushed the work toward tool-backed validation and git history rather than assuming the numbering issue from visible output.
- Layer 2: The first-failure gate fired when validation still failed after the first validator patch; it revealed a real `P-070` gap instead of letting the first fix become a shallow completion claim.
- Layer 3: Engram lookup happened before repo edits, and the field result was recorded here instead of being mixed into Claude's `CALIBRATE.md` or `REFLECT.md`.

**Promotion decision**: Promote the validator behavior into repo docs/tests now. Do not promote to Engram yet; wait to see whether this pattern recurs outside MY UNIVERSE.

### 2026-05-10 — Field Session 2: caliber Tracking Drift

**Trigger**: Satish said to keep going after the MY UNIVERSE validation slice and use a connected project before updating the review.

**Task**: Test whether the Codex/Kai lane improves real work outside MY UNIVERSE without turning the exercise into more self-referential process.

**Engram use**: Queried Engram for prior context around connected-project field sessions. No direct entry governed the task, so current repo evidence and tracker docs governed the decision.

**Seed cause**: `caliber` already exposed `caliber trajectory` in `caliber/cli.py` and `caliber_trajectory` in `caliber/mcp_server.py`, but `GAUGE.md`, `README.md`, and `REVIEW.md` still treated trajectory CLI support as missing or future work. The bug was tracking drift, not missing implementation.

**Decision**: Do not reimplement trajectory. Add CLI regression coverage, fix the stale public/tracking surfaces, and commit the external repo slice separately.

**Changes in `/home/satishocoin/caliber`**:

- `tests/test_cli.py`: added CLI coverage for insufficient trajectory data and a successful trajectory summary.
- `README.md`: added the trajectory CLI example, corrected the roadmap, and listed `caliber_trajectory` in MCP tools.
- `REVIEW.md`: marked the trajectory CLI recommendation complete with regression coverage.
- `.graft` + `GAUGE.md`: added/committed the tracking entry point and updated next-session state.

**Verification**:

- `pytest -q` passes with 98 tests in `caliber`.
- `python3 -m compileall caliber tests` passes.
- `python3 -m caliber.cli --help` lists `trajectory`.
- `git diff --check` passes.
- Local commit: `caliber:7e390bd` (`Verify trajectory CLI and update tracking`).

**Did the three-layer model change behavior?** Yes.

- Layer 1: Repo/source-of-truth inspection prevented a fake feature implementation. The code already existed.
- Layer 2: Tracking-doc drift checks caught a contradiction between `GAUGE.md`/`REVIEW.md` and the actual CLI/MCP surfaces.
- Layer 3: The deeper interrupt kept the result scoped: fix stale evidence surfaces and tests in `caliber`, then return to MY UNIVERSE for review promotion.

**Promotion decision**: Promote this to `PRISM.md` and `REVIEW.md` as field validation evidence. Do not promote to Engram yet; this is evidence for MY UNIVERSE portability, not a durable cross-project rule beyond the existing "verify repo facts before claims" rule.
