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

## Continue

- [ ] Continue — after each trial, choose the next real engineering task, run this protocol again, and record whether the practice changed behavior.
