# CODEX-REFLECT.md

> Codex/Kai reflection lane for MY UNIVERSE.
> This is separate from Claude's historical `REFLECT.md`.

---

## Purpose

Use this file for Codex/Kai interrupt evidence while working inside
MY UNIVERSE. Do not write these entries into Claude's `REFLECT.md`.

The format intentionally matches `REFLECT.md` so existing reflection tools can
parse this file with `python3 tools/reflect.py --file CODEX-REFLECT.md`.

## Entry Format

```markdown
### YYYY-MM-DD — [trap name or phase]

**Trigger:** What made the interrupt fire
**What it caught:** The specific failure it prevented or exposed
**What changed:** How the work changed after the interrupt
**Verdict:** useful | performative | missed
```

---

### 2026-05-10 — Binary Trap (continue vs overbuild)

**Trigger:** Satish said to keep working and not stop, while the repo also warned against more self-referential tooling.
**What it caught:** A false two-option frame: either stop after a neat summary or keep building process artifacts indefinitely. The better option C was chunked continuation: finish one evidence-backed slice, verify it, commit it, then choose the next concrete repo drift or bug.
**What changed:** Work proceeded through bounded chunks: onboarding protocol, stale public calibration docs, status/brief count mismatch, then this separate Codex reflection lane instead of polluting Claude's `REFLECT.md`.
**Verdict:** useful

### 2026-05-11 — Meta-Interrupt (recursive Continue gate)

**Trigger:** Satish clarified that every new task list must also end with `Continue`, and that an optional xhigh reviewer should help choose the next path before the new task list is created.
**What it caught:** The earlier version treated `Continue` as a task-list item, but not as a recursively specified gate. That left room for a clean checkpoint to become another stopping point.
**What changed:** Added `CONTINUATION-GATE.md`, taught `tools/next.py --task-list` to emit a review-gate task list, added tests for review-gate and recursive Continue behavior, and kept Claude's historical reflection data separate.
**Verdict:** useful

### 2026-05-11 — Meta-Interrupt (unattended onboarding trial)

**Trigger:** Satish said he would not be there and did not need stopping updates.
**What it caught:** The next task list included people-domain calibration verification, but those predictions require Satish. Continuing by forcing them would fabricate evidence. The viable unattended path was a fresh-agent connected-project trial.
**What changed:** Used the continuation gate to skip blocked people predictions, ran a fresh subagent trial against clean `caliber`, and recorded the result in `ONBOARDING-TRIAL.md` instead of Claude's historical files.
**Verdict:** useful

### 2026-05-11 — Meta-Interrupt (multi-agent storage boundary)

**Trigger:** The next continuation task looked like a test-only `caliber` regression.
**What it caught:** The public CLI path could prove ordinary two-agent separation, but `FileStorage` still used a lossy sanitizer where distinct names such as space and slash variants could collide into one JSON file.
**What changed:** Widened the slice from test-only to causal hardening: URL-safe agent filenames, legacy sanitized-file load fallback, CLI shared-store regression, and storage collision tests in `caliber:45ea13d`.
**Verdict:** useful

### 2026-05-11 — Meta-Interrupt (archive before cleanup)

**Trigger:** The next `caliber` continuation task was to clean up `extract_calibrate_md.py`.
**What it caught:** Replacing the duplicate parser in the active script would remove history-bearing code unless the old standalone implementation was preserved elsewhere.
**What changed:** Archived the previous standalone parser under `caliber/.archive/2026-05-11/extract-calibrate-standalone-parser/` before committing the shared-importer wrapper in `caliber:102b294`.
**Verdict:** useful

### 2026-05-11 — Meta-Interrupt (MCP config trust boundary)

**Trigger:** The next `caliber` continuation task was MCP config auto-apply.
**What it caught:** Directly editing the real `~/.mcp.json` during implementation would cross the user's live-tooling boundary. The safe product change was a tested helper that can install into a chosen path and keeps backups.
**What changed:** Added `caliber mcp-config` with print and `--install` modes, tested install against a temp config, and did not touch the live MCP config while producing `caliber:4c4a781`.
**Verdict:** useful

### 2026-05-11 — Meta-Interrupt (external adoption boundary)

**Trigger:** The next `caliber` continuation task was external adoption.
**What it caught:** Writing and posting as Satish, or claiming external validation, would cross an account/user boundary. The unattended slice could only prepare the first-user path.
**What changed:** Added `GETTING_STARTED.md` in `caliber:64464ad` and left actual posting, use, feedback, and adoption claims open for Satish or an external user.
**Verdict:** useful

### 2026-05-11 — Meta-Interrupt (portfolio repo selection)

**Trigger:** The continuation gate needed a new connected-project slice after `caliber` reached account-bound/external-user work.
**What it caught:** `engram` was broadly dirty, finance-oriented `monetization` was high-risk for unattended changes, and `AI-Agents-Failure-Modes` pytest hung in this sandbox before producing evidence. The clean, verifiable slice was the static `analysis` repo's missing README.
**What changed:** Skipped dirty/high-risk/blocked repos, added a root orientation README to `analysis:fe6e352`, and verified referenced files instead of forcing a code change.
**Verdict:** useful

## Continue

- [ ] Continue — use this file for Codex/Kai reflections when an interrupt changes behavior, then keep working from `PRISM.md`.
