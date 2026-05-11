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

## Continue

- [ ] Continue — use this file for Codex/Kai reflections when an interrupt changes behavior, then keep working from `PRISM.md`.
