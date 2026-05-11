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

### 2026-05-11 — Continuation Result: profile README stats refresh

**Participant:** Codex/Kai continuation
**Target repo/task:** `/home/satishocoin/SatishoBananamoto` — refresh profile README portfolio stats
**Prediction before work:** The profile stats were likely stale versus the current MY UNIVERSE portfolio health output and could be corrected as a narrow one-line docs slice.
**Interrupt used:** Source-of-truth check.
**What changed because of the interrupt:** Used the current `tools/portfolio.py --quick` output instead of guessing or broadening the profile rewrite.
**Work completed:** `SatishoBananamoto:db4da6b` updated the profile README stats from `20k+ LOC, 830+ tests` to `34k+ source lines, 1.3k+ test functions`.
**Verification:** `git diff --check` passed; the evidence source was `python3 tools/portfolio.py --quick` from MY UNIVERSE.
**No-deletion check:** Confirmed. No files were removed.
**Historical data boundary:** Confirmed. MY UNIVERSE records this as Codex/Kai field evidence; Claude `CALIBRATE.md` and `REFLECT.md` remain untouched.
**Outcome:** pass.
**Next continuation task:** Use the continuation gate to choose the next non-blocked connected-project or repo-maintenance slice, then Continue.

### 2026-05-11 — Continuation Result: kvsecure.com live browser QA

**Participant:** Codex/Kai continuation
**Target repo/task:** `/home/satishocoin/kvsecure.com` — complete the GitHub Pages browser visual review and fix evidence-backed issues
**Prediction before work:** The live QA would mostly validate the deployed launch site, but browser interaction checks could expose at least one issue that static docs checks missed.
**Interrupt used:** Frontend QA and deployment-evidence check.
**What changed because of the interrupt:** The slice moved from read-only review into two narrow fixes after live Chromium found an unhandled clipboard rejection and screenshot review exposed collapsed spacing in feedback-card headings.
**Work completed:** `kvsecure.com:4b58ba5` includes `9d0adb1` clipboard fallback handling, `1f34bc8` feedback heading spacing, and `.graft` live QA evidence.
**Verification:** `node --check site.js` passed; `git diff --check` passed; GitHub Pages latest build reported `1f34bc8e3fff4de7ef8b6209eb0e41666c782eb2` as `built`; `node /tmp/codex-kvsecure-live-qa/live-qa.js` loaded `https://kvsecure.com/?v=1f34bc8` with no console issues, no network failures, no 4xx/5xx asset responses, no framework overlay, and no horizontal overflow; `node /tmp/codex-kvsecure-live-qa/interaction-qa.js` verified hero toggles, denied-clipboard fallback, FAQ accordion, mobile nav, and mobile normal mode.
**No-deletion check:** Confirmed. No source or history-bearing files were removed; screenshots and QA scripts stayed in `/tmp/codex-kvsecure-live-qa/`.
**Historical data boundary:** Confirmed. MY UNIVERSE records this as Codex/Kai field evidence; Claude `CALIBRATE.md` and `REFLECT.md` remain untouched.
**Outcome:** pass.
**Next continuation task:** Use the continuation gate to choose the next non-blocked connected-project or repo-maintenance slice, then Continue.

### 2026-05-11 — Continuation Result: AI-Agents-Failure-Modes API test hardening

**Participant:** Codex/Kai continuation
**Target repo/task:** `/home/satishocoin/AI-Agents-Failure-Modes` — bound and fix the pytest hang before editing verifier behavior
**Prediction before work:** The deterministic verifier tests would pass, but the previous full-suite hang would localize to the FastAPI `TestClient` transport path rather than the verifier rules.
**Interrupt used:** Verification-boundary and seed-cause check.
**What changed because of the interrupt:** The slice did not touch the verifier engine. It first isolated the hang to `client.get("/healthz")`, then changed only `tests/test_api.py` to assert route registration and call `healthz()` / `verify_endpoint()` directly.
**Work completed:** `AI-Agents-Failure-Modes:a1ac245` made the API tests transport-independent after rebasing over remote v0.3 ledger-integrity work.
**Verification:** `timeout 25s python3 -B -m pytest -q -p no:cacheprovider` passed with 32 tests; `python3 -B -m app.cli tests/fixtures/pass_basic.json` returned `"pass": true`; `git diff --check` passed before commit; GitHub Actions `verifier-ci` run `25700134343` completed successfully after push.
**No-deletion check:** Confirmed. No files were removed.
**Historical data boundary:** Confirmed. MY UNIVERSE records this as Codex/Kai field evidence; Claude `CALIBRATE.md` and `REFLECT.md` remain untouched.
**Outcome:** pass.
**Next continuation task:** Use the continuation gate to choose the next non-blocked connected-project or repo-maintenance slice, then Continue.

### 2026-05-11 — Continuation Result: portfolio registry/profile consistency

**Participant:** Codex/Kai continuation
**Target repo/task:** `/home/satishocoin/MY UNIVERSE` and `/home/satishocoin/SatishoBananamoto` — count the ICIF-AES verifier as an active portfolio project
**Prediction before work:** Adding the verifier to the scanner would raise the portfolio from 7 to 8 projects and require a small profile README stats refresh.
**Interrupt used:** Source-of-truth and public-surface consistency check.
**What changed because of the interrupt:** The public profile was updated from the scanner output instead of hand-counting; MY UNIVERSE gained a guard test so the active verifier stays in the portfolio registry.
**Work completed:** `tools/portfolio.py` now includes `ai-agents-failure-modes`; `SatishoBananamoto:ff3dc84` adds the ICIF-AES Verifier row and refreshes profile stats to 8 tools and 35k+ source lines.
**Verification:** `python3 tools/portfolio.py --quick` reported 8/8 projects, 35,815 source lines, 1389 test functions, and `ai-agents-failure-modes` clean on `main`; `python3 tests/run_all.py` passed with 74 tests before the continuation record and 75 tests after the record test; `git diff --check` passed.
**No-deletion check:** Confirmed. No files were removed.
**Historical data boundary:** Confirmed. MY UNIVERSE records this as Codex/Kai field evidence; Claude `CALIBRATE.md` and `REFLECT.md` remain untouched.
**Outcome:** pass.
**Next continuation task:** Use the continuation gate to choose the next non-blocked connected-project or repo-maintenance slice, then Continue.

### 2026-05-11 — Continuation Result: analysis report index completion

**Participant:** Codex/Kai continuation
**Target repo/task:** `/home/satishocoin/analysis` — make the root README cover every generated dependency-health report
**Prediction before work:** The root README would be missing several report links because the generated report set had expanded after the first orientation README.
**Interrupt used:** Public-surface index check.
**What changed because of the interrupt:** The README update was driven by comparing actual `reports/*.md` files to README links instead of eyeballing the categories.
**Work completed:** `analysis:15a563c` added the missing report-index groups and links for CrewAI cascade, A2A alternate scan, ML frameworks, backend, DevOps, and testing/developer tools.
**Verification:** A Python link coverage check reported 46 report files, 46 README report links, `missing []`, and `extra []`; `git diff --check` passed before commit.
**No-deletion check:** Confirmed. No files were removed.
**Historical data boundary:** Confirmed. MY UNIVERSE records this as Codex/Kai field evidence; Claude `CALIBRATE.md` and `REFLECT.md` remain untouched.
**Outcome:** pass.
**Next continuation task:** Use the continuation gate to choose the next non-blocked connected-project or repo-maintenance slice, then Continue.

### 2026-05-11 — Continuation Result: portfolio quick-table alignment

**Participant:** Codex/Kai continuation
**Target repo/task:** `/home/satishocoin/MY UNIVERSE` — fix quick portfolio output after adding the long verifier project key
**Prediction before work:** The long `ai-agents-failure-modes` project name would require dynamic project-name width, and the existing long `kv-secrets` branch would need a wider branch column too.
**Interrupt used:** Regression check from previous slice output.
**What changed because of the interrupt:** The quick table now derives project-name width from the registry and uses a wider branch column, with tests guarding both long-name cases.
**Work completed:** `tools/portfolio.py` gained `PROJECT_NAME_WIDTH` and `BRANCH_WIDTH`; `tests/test_portfolio.py` now covers both long project names and long branch names.
**Verification:** `python3 tools/portfolio.py --quick` printed aligned `Project`, `Branch`, `State`, `Activity`, and `Commits` columns; `python3 tests/run_all.py` passed with 78 tests before the continuation record and 79 tests after the record test; `python3 tools/validate.py` and `git diff --check` passed.
**No-deletion check:** Confirmed. No files were removed.
**Historical data boundary:** Confirmed. MY UNIVERSE records this as Codex/Kai field evidence; Claude `CALIBRATE.md` and `REFLECT.md` remain untouched.
**Outcome:** pass.
**Next continuation task:** Use the continuation gate to choose the next non-blocked connected-project or repo-maintenance slice, then Continue.

### 2026-05-11 — Continuation Result: kvsecure.com README orientation

**Participant:** Codex/Kai continuation
**Target repo/task:** `/home/satishocoin/kvsecure.com` — add a root README for the static launch site
**Prediction before work:** A README-only slice could improve future site maintenance without needing the live browser review that `.graft` lists as the real open deployment check.
**Interrupt used:** Product-boundary and visual-verification check.
**What changed because of the interrupt:** Added repo orientation and verification guidance without editing the live HTML/CSS/JS experience or claiming the GitHub Pages browser review was complete.
**Work completed:** `kvsecure.com:5e3f0b0` added `README.md` with the product story to preserve, claims to avoid, file map, local verification commands, and deployment/cache-busting note.
**Verification:** `node --check site.js` passed; `git diff --check` passed; referenced files were checked with `test -f`; stale-claim search found no forbidden launch wording.
**No-deletion check:** Confirmed. No files were removed.
**Historical data boundary:** Confirmed. MY UNIVERSE records this as Codex/Kai field evidence; Claude `CALIBRATE.md` and `REFLECT.md` remain untouched.
**Outcome:** pass.
**Next continuation task:** Use the continuation gate to choose the next non-blocked connected-project or repo-maintenance slice, then Continue.

### 2026-05-11 — Continuation Result: analysis README orientation

**Participant:** Codex/Kai continuation
**Target repo/task:** `/home/satishocoin/analysis` — add a root orientation README for the AI-agent dependency-risk reports
**Prediction before work:** A clean docs-only slice would be safer than touching dirty Engram state, account-bound caliber tasks, finance/trading code, or the AI-Agents-Failure-Modes repo whose pytest run hung in this sandbox.
**Interrupt used:** Repo-selection and verification-boundary check.
**What changed because of the interrupt:** Chose a clean static analysis repo and added a root README instead of editing dirty or high-risk repositories.
**Work completed:** `analysis:fe6e352` added `README.md` linking the main report, report categories, reproduction commands, trust-stack demo, and stale-snapshot caveat.
**Verification:** `git diff --check` passed; referenced report files and `trust-stack-demo.sh` were checked with `test -f`/`test -x`; repo was clean before the edit.
**No-deletion check:** Confirmed. No files were removed.
**Historical data boundary:** Confirmed. MY UNIVERSE records this as Codex/Kai field evidence; Claude `CALIBRATE.md` and `REFLECT.md` remain untouched.
**Outcome:** pass.
**Next continuation task:** Use the continuation gate to choose the next non-blocked connected-project or repo-maintenance slice, then Continue.

### 2026-05-11 — Continuation Result: caliber CALIBRATE import cleanup

**Participant:** Codex/Kai continuation
**Target repo/task:** `/home/satishocoin/caliber` — clean up `extract_calibrate_md.py` by using the maintained import path
**Prediction before work:** The active script duplicated parser logic that should move behind `caliber.importer`, but the old implementation should be preserved instead of discarded.
**Interrupt used:** No-deletion/archive-first check.
**What changed because of the interrupt:** The previous standalone parser was archived under `.archive/2026-05-11/extract-calibrate-standalone-parser/` before the active wrapper was simplified.
**Work completed:** `caliber:102b294` converted `extract_calibrate_md.py` into a compatibility wrapper around `import_calibrate_md`, added CLI import coverage, added wrapper tests, updated README/GAUGE/CLAUDE/REVIEW, and preserved the old parser in archive.
**Verification:** `python3 -B -m pytest -q -p no:cacheprovider` passed with 103 tests; `python3 -m compileall extract_calibrate_md.py caliber tests` passed; `git diff --check` passed before commit.
**No-deletion check:** Confirmed. No files were removed; the displaced parser implementation was archived with `MANIFEST.md`.
**Historical data boundary:** Confirmed. MY UNIVERSE records this as Codex/Kai field evidence; Claude `CALIBRATE.md` and `REFLECT.md` remain untouched.
**Outcome:** pass.
**Next continuation task:** Use the continuation gate to choose the next non-blocked connected-project or repo-maintenance slice, then Continue.

### 2026-05-11 — Continuation Result: caliber MCP config helper

**Participant:** Codex/Kai continuation
**Target repo/task:** `/home/satishocoin/caliber` — reduce MCP config manual setup friction
**Prediction before work:** A safe auto-apply feature should be implemented as a tested CLI helper that writes only to a chosen config path, not by modifying the live `~/.mcp.json` during development.
**Interrupt used:** Trust-boundary check.
**What changed because of the interrupt:** Implemented `caliber mcp-config` with print and `--install` modes, tested install against a temp `.mcp.json`, and preserved existing servers with timestamped backups.
**Work completed:** `caliber:4c4a781` added the MCP config helper, tests, README usage, CLAUDE/GAUGE/REVIEW updates, and mcp_server docstring guidance.
**Verification:** `python3 -B -m pytest -q -p no:cacheprovider` passed with 105 tests; `python3 -m compileall caliber tests` passed; `git diff --check` passed before commit.
**No-deletion check:** Confirmed. No files were removed; installer behavior creates backups before updating an existing config.
**Historical data boundary:** Confirmed. MY UNIVERSE records this as Codex/Kai field evidence; Claude `CALIBRATE.md` and `REFLECT.md` remain untouched.
**Outcome:** pass.
**Next continuation task:** Use the continuation gate to choose the next non-blocked connected-project or repo-maintenance slice, then Continue.

### 2026-05-11 — Continuation Result: caliber first-user tutorial

**Participant:** Codex/Kai continuation
**Target repo/task:** `/home/satishocoin/caliber` — prepare the first external-user onboarding path
**Prediction before work:** The remaining external-adoption work could not honestly post or collect feedback without Satish or another user, but a concrete tutorial could remove the next adoption blocker.
**Interrupt used:** Account-boundary check.
**What changed because of the interrupt:** Added a first-user guide instead of pretending external validation had happened or posting from Satish's accounts.
**Work completed:** `caliber:64464ad` added `GETTING_STARTED.md`, linked it from README, and updated GAUGE/REVIEW to distinguish tutorial readiness from actual external feedback.
**Verification:** `python3 -B -m pytest -q -p no:cacheprovider` passed with 105 tests; `git diff --check` passed before commit.
**No-deletion check:** Confirmed. No files were removed.
**Historical data boundary:** Confirmed. MY UNIVERSE records this as Codex/Kai field evidence; Claude `CALIBRATE.md` and `REFLECT.md` remain untouched.
**Outcome:** pass.
**Next continuation task:** Use the continuation gate to choose the next non-blocked connected-project or repo-maintenance slice, then Continue.

## Continue

- [ ] Continue — after each trial, choose the next real engineering task, run this protocol again, and record whether the practice changed behavior.
