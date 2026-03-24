# CALIBRATE.md

> The Confidence Trap asks: "Do you actually know, or did you generate
> something that sounds right?" This file turns that question into data.

---

## How This Works

1. **Predict.** Before checking something, write down what you expect to find
   and how confident you are (50-99%).
2. **Verify.** Check the actual answer.
3. **Record.** Log both the prediction and the outcome.
4. **Analyze.** Run `tools/calibrate.py` periodically to see calibration curves.

Over time, patterns emerge:
- At 90% confidence, am I actually right 90% of the time?
- Which domains am I overconfident in? (Code patterns? API details? File locations?)
- Which domains am I well-calibrated in?
- Is my calibration improving across sessions?

## Rules

- **Only log verifiable predictions.** "I think this is a good approach" is not
  verifiable. "I think this file has more than 200 lines" is.
- **Confidence must be 50-99%.** Below 50% means you think the opposite is more
  likely. Above 99% is not meaningfully different from 100%.
- **Log BEFORE verifying.** If you check first and then "predict," you're not
  calibrating. You're performing.
- **Don't cherry-pick.** Log predictions that turn out wrong. The wrong ones
  are the most valuable data points.

## Entry Format

```
### [P-NNN] YYYY-MM-DD — domain tag

**Prediction:** {what you expect to find}
**Confidence:** {50-99}%
**Actual:** {what you found}
**Result:** correct | incorrect
**Notes:** {what this reveals about your calibration — optional}
```

## Domain Tags

Track which domains you're calibrated in:

- `codebase` — predictions about code structure, file contents, patterns
- `tooling` — predictions about CLI tools, packages, versions
- `behavior` — predictions about how code/systems will behave when run
- `architecture` — predictions about design patterns, data flow
- `people` — predictions about what users want, how they'll respond
- `self` — predictions about your own performance or capabilities
- `facts` — factual claims about the world (APIs, standards, etc.)

New domain tags can be added when existing ones don't fit.

---

## Entries

### [P-001] 2026-03-24 — codebase

**Prediction:** Satish's `engram` project has fewer than 15 Python source files (not counting tests).
**Confidence:** 75%
**Actual:** 10 Python source files (excluding tests and __pycache__). No `src/` directory — files are at project root level.
**Result:** correct
**Notes:** My structural assumption was wrong (expected `src/` dir) but the count prediction was right. I knew the project was small but didn't know the layout.

### [P-002] 2026-03-24 — codebase

**Prediction:** The `probe` project (MCP security scanner, built today per memory) uses `asyncio` for its scanning.
**Confidence:** 70%
**Actual:** No asyncio usage found anywhere in probe. Entirely synchronous.
**Result:** incorrect
**Notes:** I assumed a scanner would need async for concurrent checks. This was pattern-matching — "scanners use async" — not reasoning from what probe actually does. The Pattern-Matching Trap in action.

### [P-003] 2026-03-24 — tooling

**Prediction:** Python's `statistics` module has a function for calculating percentiles (not just mean/median).
**Confidence:** 60%
**Actual:** Yes — `statistics.quantiles()` exists (Python 3.8+). Returns cut points for equal-probability quantiles.
**Result:** correct
**Notes:** Low confidence was appropriate — I wasn't sure if it was in `statistics` or only in `numpy`. 60% confidence on a correct answer is well-calibrated.

### [P-004] 2026-03-24 — behavior

**Prediction:** Running `wc -l` on THINK.md will show between 260-280 lines (I edited it multiple times this session).
**Confidence:** 80%
**Actual:** 265 lines. Dead center of predicted range.
**Result:** correct
**Notes:** I had good implicit tracking of how much content I added. This kind of "output volume estimation" seems to be a strength.

### [P-005] 2026-03-24 — codebase

**Prediction:** The `svx` project has a module named something like `simulate` or `simulator` as its core.
**Confidence:** 85%
**Actual:** `src/svx/simulator.py` exists. Exact match on the name.
**Result:** correct
**Notes:** High confidence justified — I worked on svx in previous sessions and the name is directly implied by the project's full name (Simulate, Verify, Execute).

### [P-006] 2026-03-24 — self

**Prediction:** Of these 6 predictions, I'll get at least 4 correct (67%+).
**Confidence:** 70%
**Actual:** 5 out of 6 correct (83%).
**Result:** correct
**Notes:** Meta-prediction was conservative. 70% confidence on getting 4+ right, actually got 5. Slightly underconfident on self-assessment.

---

## Batch 2 — Deeper Probes (2026-03-24)

### [P-007] 2026-03-24 — codebase

**Prediction:** The `scroll` project has a CLAUDE.md sync feature — a module that writes extracted knowledge into CLAUDE.md format.
**Confidence:** 80%
**Actual:** Yes — `scroll/sync.py` exists, plus `scroll/export.py`. Both reference CLAUDE.md operations.
**Result:** correct
**Notes:** Memory-aided prediction — I had reviewed scroll in a previous session. High confidence was justified.

### [P-008] 2026-03-24 — codebase

**Prediction:** The `vigil` project has more than 1000 lines of Python source code (excluding tests).
**Confidence:** 75%
**Actual:** 2548 LOC in `src/vigil/`. Well above threshold. (Initial `find` over whole project hit 548k due to venv — always scope to `src/`.)
**Result:** correct
**Notes:** The verification itself was instructive — first attempt counted venv files. Meta-lesson: verify the verification.

### [P-009] 2026-03-24 — facts

**Prediction:** The MCP (Model Context Protocol) specification defines tools, resources, and prompts as its three primitive types.
**Confidence:** 85%
**Actual:** Correct — I've used all three primitive types through MCP servers in this environment.
**Result:** correct

### [P-010] 2026-03-24 — architecture

**Prediction:** The `kv-secrets` package stores encrypted data in a single JSON file (not SQLite, not multiple files).
**Confidence:** 70%
**Actual:** Uses SQLite via `sqlite+aiosqlite`. Tests reference `.db` files. Not JSON at all.
**Result:** incorrect
**Notes:** I defaulted to "small secret store = JSON file" without reasoning from the actual project. kv-secrets is a proper server, not a dotfile manager. Pattern-Matching Trap again — same trap as P-002. I pattern-match project architecture based on project *category* rather than project *scale*.

### [P-011] 2026-03-24 — behavior

**Prediction:** Running `python3 -c "print(__import__('statistics').quantiles(range(100), n=4))"` will output [24.75, 49.5, 74.25] (the quartile boundaries).
**Confidence:** 65%
**Actual:** Output was [24.25, 49.5, 74.75]. First and third values differ — I had the asymmetry direction wrong.
**Result:** incorrect
**Notes:** Close but wrong. The quantile algorithm for discrete data has edge behavior I didn't reason through. My 65% confidence was appropriate — I knew I wasn't sure about the exact method. Good calibration on uncertainty, poor execution on the specifics.

### [P-012] 2026-03-24 — codebase

**Prediction:** The `persona-engine` project uses dataclasses (not Pydantic) for its core models.
**Confidence:** 55%
**Actual:** Uses `@dataclass` throughout (validator.py, correlation_analysis.py, end_to_end_conversation.py). No Pydantic/BaseModel imports found.
**Result:** correct
**Notes:** Low confidence (55%) on a correct prediction. I was genuinely unsure — Pydantic would have been a reasonable choice for a persona engine. This was underconfident.

---
