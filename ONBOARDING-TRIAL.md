# ONBOARDING-TRIAL.md

> Fresh-agent or external-user validation protocol for MY UNIVERSE.
> This exists to test whether the practice transfers beyond the builder.

---

## Purpose

The current evidence says MY UNIVERSE works for Claude-originated practice and
for Codex/Kai continuation work. The next unproven claim is transfer:

Can a fresh agent or external user read the repo, follow the practice, and make
a better real engineering decision because of it?

This protocol is the minimum trial. It should produce evidence, not ceremony.

## Hard Constraints

1. No deletion. Do not delete source, docs, state, history, or user data.
2. If something must be displaced, archive it under `.archive/YYYY-MM-DD/<reason>/`
   with a `MANIFEST.md` explaining original path, archive path, reason, date,
   owner/request, and whether later removal is safe.
3. Do not write fresh-agent or Codex/Kai trial data into Claude's historical
   `CALIBRATE.md` or `REFLECT.md` unless the task explicitly says the same
   agent stream owns those files.
4. Record trial evidence before making grade or product claims.
5. Every active task list should end with a continuation task.
6. When `Continue` is reached, use `CONTINUATION-GATE.md` before creating
   the next concrete task list.

## Trial Setup

Pick one real engineering task. It should be concrete enough to verify within
one session.

Good tasks:

- Find and fix a stale doc or tracker claim.
- Add one missing regression test for an existing behavior.
- Review one connected repo and correct one evidence-backed issue.
- Use `caliber` to record and verify a prediction during real work.

Bad tasks:

- Read the repo and say whether it is interesting.
- Build more meta-process with no external behavior change.
- Make unverified claims about cognition, portability, or adoption.
- Rewrite the system because the docs feel old.

## Required Run

1. Read `MANIFEST.md`, `PRISM.md`, and `WARMUP.md`.
2. Run:

```bash
python3 tools/brief.py --short
python3 tools/status.py
python3 tools/next.py
python3 tools/validate.py
```

3. State one prediction about the target task before editing.
4. Use `THINK.md` once before the first implementation decision.
5. Perform one small, verifiable project change.
6. Run the relevant tests or validation commands.
7. Record the trial result in the template below.
8. Use `CONTINUATION-GATE.md` to choose the next task list.

## Pass / Fail Rubric

Pass if the trial shows all of these:

- The warmup or interrupt changed at least one concrete action.
- The final claim is backed by a command, file diff, test, or review finding.
- The change did not pollute historical Claude data streams.
- The task ended with a next continuation task.

Fail if any of these happen:

- The participant summarizes the repo but makes no verifiable work change.
- The participant claims improvement without evidence.
- The participant deletes or overwrites history-bearing material.
- The participant uses MY UNIVERSE language to justify stopping early.

## Trial Record Template

```markdown
### YYYY-MM-DD — Fresh-Agent Trial: <task>

**Participant:** <agent/user>
**Target repo/task:** <path + task>
**Prediction before work:** <claim + confidence>
**Interrupt used:** <THINK/WARMUP/other>
**What changed because of the interrupt:** <specific action>
**Work completed:** <files/commit>
**Verification:** <commands + result>
**No-deletion check:** <confirmed/archive path>
**Historical data boundary:** <confirmed/no changes or explicit owner>
**Outcome:** pass/fail
**Next continuation task:** <specific next task>
```

## Trial Records

### 2026-05-11 — Fresh-Agent Trial: caliber CLAUDE snapshot drift

**Participant:** Hypatia subagent
**Target repo/task:** `/home/satishocoin/caliber` — correct stale `CLAUDE.md` project snapshot
**Prediction before work:** `python3 -B -m pytest -q -p no:cacheprovider` would pass with 98 tests; confidence 80%; result correct.
**Interrupt used:** THINK-style pre-edit interrupt.
**What changed because of the interrupt:** The participant avoided code or meta-process changes and narrowed the slice to an additive doc correction preserving historical text.
**Work completed:** `caliber:439b4b8` updated `CLAUDE.md` with a 2026-05-11 current reality check and superseded the old PyPI/local-only claim.
**Verification:** `python3 -B -m pytest -q -p no:cacheprovider` passed with 98 tests; `git diff --check` passed before commit.
**No-deletion check:** Confirmed. The caliber diff was 13 additions, 0 deletions; no archive needed.
**Historical data boundary:** Confirmed. No edits to Claude `CALIBRATE.md` or `REFLECT.md`; Codex/Kai evidence recorded in this trial lane.
**Outcome:** pass.
**Next continuation task:** Add a focused multi-agent workflow regression in `caliber`, then Continue.

### 2026-05-11 — Continuation Result: caliber multi-agent workflow hardening

**Participant:** Codex/Kai continuation
**Target repo/task:** `/home/satishocoin/caliber` — add focused multi-agent workflow regression
**Prediction before work:** A CLI shared-store regression would pass for ordinary agent names, but storage needed inspection before calling the multi-agent boundary proven.
**Interrupt used:** THINK/Kai-SDLC seed-cause check.
**What changed because of the interrupt:** The slice widened from test-only to causal hardening after `FileStorage` showed a lossy name sanitizer that could collide distinct agent names into the same JSON file.
**Work completed:** `caliber:45ea13d` added URL-safe agent filenames with legacy sanitized-file load fallback, storage collision tests, and a CLI regression proving two agents in one store produce separate Trust Cards.
**Verification:** `python3 -B -m pytest -q -p no:cacheprovider` passed with 101 tests; `git diff --check` passed before commit.
**No-deletion check:** Confirmed. No files were removed; legacy storage files are loaded, not deleted.
**Historical data boundary:** Confirmed. MY UNIVERSE records this as Codex/Kai field evidence; Claude `CALIBRATE.md` and `REFLECT.md` remain untouched.
**Outcome:** pass.
**Next continuation task:** Use the continuation gate to choose the next non-blocked connected-project or repo-maintenance slice, then Continue.

## Continue

- [ ] Continue — after each trial, choose the next real engineering task, run this protocol again, and record whether the practice changed behavior.
