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

## Batch 3 — Targeting Weak Spots (2026-03-24)

Deliberately probing architecture and behavior domains where batches 1-2 showed weakness.

### [P-013] 2026-03-24 — architecture

**Prediction:** The `engram` project stores entries as individual files (one file per entry), not in a database or single JSON file.
**Confidence:** 75%
**Actual:** Yes — individual .md files: DEC-001.md, LRN-001.md, MST-001.md, OBS-001.md, GOL-001.md, etc. 47+ files total.
**Result:** correct
**Notes:** This aligned with DEC-001 in engram itself ("one file per entry"). My prediction was informed by having seen engram's design decisions in previous sessions.

### [P-014] 2026-03-24 — architecture

**Prediction:** The `scroll` project uses subprocess calls to `git log` rather than a Python git library (like gitpython) to read repository history.
**Confidence:** 70%
**Actual:** Yes — `subprocess.run(["git"...` in both git_reader.py and github_reader.py. No gitpython dependency.
**Result:** correct
**Notes:** Correct architecture prediction at 70%. I reasoned from Satish's preference for lightweight deps (Chromebook) rather than from the category. This is the right kind of reasoning.

### [P-015] 2026-03-24 — behavior

**Prediction:** Running `python3 tools/calibrate.py --domain codebase` will show 5 entries (P-001, P-002, P-005, P-007, P-012 are codebase-tagged).
**Confidence:** 80%
**Actual:** Shows 6 entries — I forgot P-008 (vigil LOC count) which is also codebase-tagged.
**Result:** incorrect
**Notes:** 80% confidence on a wrong answer. Simple counting error — I miscounted my own predictions. Overconfident about my own bookkeeping. Ironic that this happened while testing the calibration tool.

### [P-016] 2026-03-24 — architecture

**Prediction:** The `probe` project scans MCP server config files (JSON) rather than actually connecting to running MCP servers.
**Confidence:** 65%
**Actual:** Yes — has src/config.py for parsing configs, scanners analyze configuration files (filesystem, injection, secrets, transport scanners).
**Result:** correct
**Notes:** Appropriate confidence for a genuine uncertainty. I wasn't sure if probe was static analysis or runtime scanning. 65% was honest.

### [P-017] 2026-03-24 — behavior

**Prediction:** The `vigil` project has a CLI command that takes a package name and outputs a risk score or risk report.
**Confidence:** 85%
**Actual:** Yes — `@click.argument("package")` with options for detail, JSON output, and risk threshold. Classic CLI risk assessment interface.
**Result:** correct
**Notes:** High confidence justified — this is the core use case implied by "predictive risk intelligence."

### [P-018] 2026-03-24 — architecture

**Prediction:** The `svx` simulator works by creating a temporary copy of the filesystem (like a tmpdir or overlay) to run simulated operations against, rather than tracking changes in-memory.
**Confidence:** 60%
**Actual:** Neither. SVX uses a WorldSnapshot object and analyzes/predicts command outcomes through category-specific simulator functions (_simulate_git, _simulate_delete, etc.). No filesystem copy, no in-memory filesystem model. It reasons about what would happen by analyzing the command structure against the current state.
**Result:** incorrect
**Notes:** My 60% confidence was appropriate — I was genuinely unsure. But both options I considered (tmpdir vs in-memory tracking) were wrong. SVX is more elegant: it's analysis-based simulation, not execution-based. I failed to consider a third option because I was trapped in the binary of "copy files" vs "virtual filesystem." This is a variant of the Pattern-Matching Trap: having only two mental models for how simulation could work when there were actually three.

---

## Batch 4 — Edge Predictions (2026-03-24)

Pushing into areas where I'm most likely to be wrong. Testing behavior and cross-project patterns.

### [P-019] 2026-03-24 — behavior

**Prediction:** Running `python3 tools/reflect.py --traps` will list exactly 5 "never fired" traps.
**Confidence:** 75%
**Actual:** Lists 4 unfired traps (binary, category, completion, performance). The Scope trap fired during this session (observability Pre-Mortem), so it's not in the "never fired" list.
**Result:** incorrect
**Notes:** Off by 1. I forgot the Scope Trap fired when I did the observability Pre-Mortem. My own session's REFLECT.md entries changed the count. I was predicting based on earlier state.

### [P-020] 2026-03-24 — architecture

**Prediction:** The `vigil` project's cascade analyzer (cascade.py) analyzes transitive dependencies recursively, not just direct dependencies.
**Confidence:** 80%
**Actual:** Yes — `score_tree()` walks a DependencyNode tree, scoring all nodes at depth >= 1 with depth-weighted risk. Supports depths 1-3+ with configurable weights.
**Result:** correct
**Notes:** Reasoned from the module name (cascade = transitive propagation) and vigil's stated purpose. The prediction was informed by domain knowledge, not pattern-matching.

### [P-021] 2026-03-24 — behavior

**Prediction:** The total LOC across all tools/ Python files in MY UNIVERSE is between 400-500 lines.
**Confidence:** 70%
**Actual:** 677 lines. calibrate.py=218, reflect.py=274, status.py=185.
**Result:** incorrect
**Notes:** Underestimated status.py and reflect.py. I had just written them but didn't track their actual size. The same kind of bookkeeping error as P-015.

### [P-022] 2026-03-24 — architecture

**Prediction:** The `engram` project has a server component (FastAPI or Flask) for the MCP integration, not just CLI.
**Confidence:** 70%
**Actual:** Yes — `server.py` exists. (Did not inspect framework used, but server component confirmed.)
**Result:** correct
**Notes:** Reasoned from engram being an MCP tool (MCP servers need a server component). Good inference.

### [P-023] 2026-03-24 — facts

**Prediction:** There are more than 40 engram entries total across all types (DEC, LRN, MST, OBS, GOL).
**Confidence:** 85%
**Actual:** 49 entries total.
**Result:** correct

### [P-024] 2026-03-24 — self

**Prediction:** My architecture-domain calibration will improve this batch compared to batch 3 (above 60% accuracy for architecture predictions).
**Confidence:** 55%
**Actual:** Batch 4 architecture predictions: P-020 correct (1/1 = 100%). Tiny sample but above 60%.
**Result:** correct
**Notes:** 55% confidence on a correct meta-prediction. Honestly uncertain, appropriately so given small sample.

---

## Batch 5 — Warmup Simulation (2026-03-24)

Testing WARMUP.md protocol. All behavior-domain to target weakest area.

### [P-025] 2026-03-24 — behavior

**Prediction:** `git log --oneline` in MY UNIVERSE will show exactly 7 commits.
**Confidence:** 85%
**Actual:** Exactly 7 commits.
**Result:** correct
**Notes:** Good discrete-count prediction. I had been tracking commits deliberately.

### [P-026] 2026-03-24 — behavior

**Prediction:** REFLECT.md has more lines than REASON.md.
**Confidence:** 60%
**Actual:** REFLECT=105, REASON=184. REASON is 79 lines larger.
**Result:** incorrect
**Notes:** Recency bias — I've been actively adding to REFLECT.md all session, so it *felt* bigger. But REASON.md has 6 full method descriptions which are substantial. Size estimation of actively-edited files is a persistent weakness (P-015, P-021, P-026 all wrong on size/count).

### [P-027] 2026-03-24 — behavior

**Prediction:** The `calibrate.py --summary` one-liner will say "overconfident" (because our accuracy is below our avg confidence).
**Confidence:** 70%
**Actual:** "overconfident by 2pts" — correct.
**Result:** correct
**Notes:** Predicted the tool's output by reasoning about the data. This worked because I understood the logic, not just the data.

---

## Batch 6 — Portfolio Predictions (2026-03-24)

After running the quick portfolio check, making predictions about the full data.

### [P-028] 2026-03-24 — behavior

**Prediction:** The full portfolio report will show `kv-secrets` has the most source lines of any project.
**Confidence:** 60%
**Actual:** kv-secrets: 5199 lines. Next: vigil 2862. Easily the largest.
**Result:** correct
**Notes:** Underconfident at 60%. Should have reasoned from kv-secrets being the most mature (24 commits). Low confidence was unnecessary hedging.

### [P-029] 2026-03-24 — behavior

**Prediction:** `scroll` has more test functions than `engram`.
**Confidence:** 65%
**Actual:** scroll=97, engram=139. Engram has 42 more test functions.
**Result:** incorrect
**Notes:** Used stale data from memory (scroll had 75 tests at v0.1.0). Engram has grown significantly. This is the memory-vs-reality gap — when memory says one thing and the filesystem says another, the filesystem is right.

### [P-030] 2026-03-24 — architecture

**Prediction:** `kv-secrets` depends on SQLAlchemy (or aiosqlite at minimum) based on the `sqlite+aiosqlite://` URL pattern I saw earlier.
**Confidence:** 85%
**Actual:** Yes — SQLAlchemy with async (sqlalchemy[asyncio] + aiosqlite). Plus FastAPI, uvicorn, python-jose, bcrypt, Stripe.
**Result:** correct
**Notes:** Good inference from the URL pattern observed in test files. This time I reasoned from evidence (the URL I saw), not from category. That's the fix working.

---

## Batch 7 — Estimation vs Reasoning (2026-03-24)

Testing the hypothesis: reasoning from logic succeeds, estimation fails.
Pairs of predictions — one reasoned, one estimated.

### [P-031] 2026-03-24 — behavior

**Prediction:** (REASONING) Running `python3 tools/validate.py` will exit with code 0 (because I just ran it and all entries were valid, and I haven't added malformed entries since).
**Confidence:** 95%
**Actual:** Exit 0. All entries still valid.
**Result:** correct
**Notes:** Pure reasoning — I knew the state and nothing changed. High confidence justified.

### [P-032] 2026-03-24 — behavior

**Prediction:** (ESTIMATION) The THINK.md file now has between 300-310 lines.
**Confidence:** 65%
**Actual:** 309 lines. Within predicted range.
**Result:** correct
**Notes:** Estimation with a range (10 lines) succeeded. Previous estimation failures used point estimates or narrow comparisons. Wider ranges may be the fix for estimation — acknowledge uncertainty in the prediction itself.

### [P-033] 2026-03-24 — behavior

**Prediction:** (REASONING) `python3 tools/calibrate.py --domain architecture` will show accuracy above 60% because I know I improved from batch 2 onwards.
**Confidence:** 80%
**Actual:** 75% accuracy (6/8 correct). Well above 60%.
**Result:** correct
**Notes:** Reasoned from known trend + data. Threshold was conservative (60% when actual was 75%).

### [P-034] 2026-03-24 — behavior

**Prediction:** (ESTIMATION) The total number of files in MY UNIVERSE (excluding .git and __pycache__) is between 18-22.
**Confidence:** 70%
**Actual:** 21 files. Within range.
**Result:** correct
**Notes:** Range estimation (5-wide) succeeded. Both estimation predictions this batch used ranges. Both succeeded. Previous failures used point estimates or comparisons. Revised hypothesis: estimation fails on POINT estimates, succeeds on RANGE estimates with appropriate width.

---

## Batch 8 — Deliberate Difficulty (2026-03-24)

Predictions I expect to struggle with. Testing the edges.

### [P-035] 2026-03-24 — people

**Prediction:** When Satish sees MY UNIVERSE in the morning, his first reaction will be about the portfolio thesis or the analyses (the strategic content), not the calibration system (the mechanical content).
**Confidence:** 60%
**Actual:** _to be verified by Satish_
**Result:** _pending_
**Notes:** First "people" domain prediction. Genuinely uncertain.

### [P-036] 2026-03-24 — self

**Prediction:** In the next session, at least one of my calibration findings will turn out to be wrong or misleading due to small sample size.
**Confidence:** 75%
**Actual:** _to be verified next session_
**Result:** _pending_

### [P-037] 2026-03-24 — architecture

**Prediction:** The `probe` project uses click decorators for argument parsing in its CLI, similar to vigil and scroll.
**Confidence:** 80%
**Actual:** Yes — `import click`, `@click.group()`, `@click.option()` in src/cli.py. Same pattern as vigil and scroll.
**Result:** correct
**Notes:** This is cross-project pattern recognition working correctly. I knew the pattern because I'd seen it in vigil and scroll, and probe is built by the same developer in the same style.

### [P-038] 2026-03-24 — facts

**Prediction:** At least 3 of Satish's 6 projects have a REVIEW.md file (from my review work).
**Confidence:** 70%
**Actual:** 5 out of 6 have REVIEW.md (all except probe). Much more than 3.
**Result:** correct
**Notes:** Underconfident. I wrote most of these reviews myself. I should have been more confident — 70% was too cautious given my direct involvement.

---
