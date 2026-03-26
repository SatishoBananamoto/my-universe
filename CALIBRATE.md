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
**Actual:** Yes. Session 1 concluded "70-79% is the danger zone." Session 2's Trust Card (36 predictions) showed 60-69% is the actual danger zone (44% accuracy, 14.5% overconfidence gap). The 70-79% range is close to calibrated (69.2%). Session 3's deeper analysis revealed the cause: false evidence, not insufficient knowledge.
**Result:** correct
**Notes:** 75% confidence on a meta-prediction about my own calibration system. The prediction was almost too easy — small samples ALWAYS produce misleading patterns. The more interesting finding: the Trust Card format is what made the correction visible. Without confidence buckets, the overall accuracy (75% → 74%) barely changed.

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

## Session 2 — Warmup Predictions (2026-03-26)

### [P-039] 2026-03-26 — codebase

**Prediction:** `tools/` directory in MY UNIVERSE has exactly 6 Python files.
**Confidence:** 65%
**Actual:** 11 Python files. Memory listed 6 tools (calibrate, reflect, status, validate, portfolio, brief) but missed 5 others (audit_claude_md.py, changelog.py, gen_claude_md.py, __main__.py, next.py).
**Result:** incorrect
**Notes:** Trusted a memory file's partial list as exhaustive. Same failure mode as session 1: assuming completeness from incomplete information. The fix is the same as always — verify, don't recall.

### [P-040] 2026-03-26 — codebase

**Prediction:** CALIBRATE.md has more than 30 predictions.
**Confidence:** 75%
**Actual:** 38 predictions (36 verified, 2 pending). Session log said "34" which was accurate at the time of that log entry.
**Result:** correct
**Notes:** 75% confidence on a correct prediction. Well calibrated — I was reasonably sure based on session log data but accounted for possible discrepancy.

### [P-041] 2026-03-26 — architecture

**Prediction:** PLAN-TRUST-LAYER.md is about building a trust/verification layer for AI agents (extending svx concepts).
**Confidence:** 70%
**Actual:** Yes — "A2A handles communication. MCP handles tools. Nobody handles trust. Build the third protocol layer." Broader than just extending svx; it maps all 6 portfolio projects as components of a trust protocol. Working name: caliber.
**Result:** correct
**Notes:** 70% confidence, correct. The "extending svx" part was partially wrong — it's a portfolio-wide thesis, not svx-specific. But the core claim (trust layer for AI agents) was right.

### [P-042] 2026-03-26 — self

**Prediction:** P-036 ("at least one calibration finding will be wrong due to small sample size") is correct.
**Confidence:** 85%
**Actual:** Yes. Session 1 concluded "70-79% is the danger zone." The full Trust Card with 36 predictions shows 60-69% is the actual danger zone (50% accuracy, 14.5% overconfidence gap). The 70-79% range is close to calibrated (69.2% vs ~74.5% expected). The earlier finding was based on small early batches.
**Result:** correct
**Notes:** The Trust Card format — which I just built — was what revealed this. First real use of caliber producing a non-obvious insight.

---

## Session 3 — Danger Zone Hypothesis Test (2026-03-26)

Deliberately making predictions at 60-69% confidence with annotated evidence
sources. Testing the hypothesis: false evidence causes the danger zone.

### [P-043] 2026-03-26 — codebase

**Prediction:** tools/brief.py accepts a --short flag.
**Confidence:** 65%
**Source type:** Memory — MANIFEST.md explicitly references `python3 tools/brief.py --short`
**Actual:** Yes — argparse shows `--short  Ultra-short brief`. Exact match.
**Result:** correct
**Notes:** Memory was correct because it was a SPECIFIC reference (remembered exactly where I saw it, what it said). This is strong evidence, not vague memory.

### [P-044] 2026-03-26 — architecture

**Prediction:** tools/next.py imports from calibrate or reflect modules.
**Confidence:** 60%
**Source type:** Inference — if it recommends next actions, it needs system state from parsers
**Actual:** Yes — imports both: `from tools.calibrate import parse_entries as parse_cal, compute_calibration` and `from tools.reflect import parse_entries as parse_ref`.
**Result:** correct
**Notes:** Sound logical inference from strong premises (purpose → requirements → imports). This is a deduction, not a guess.

### [P-045] 2026-03-26 — behavior

**Prediction:** ANALYSES.md has more than 100 lines.
**Confidence:** 65%
**Source type:** Feeling — "it seemed like a substantive document"
**Actual:** 78 lines. Below threshold.
**Result:** incorrect
**Notes:** Pure vibes. No specific memory of the file's content, just a vague impression of "substantiveness." This is the weakest form of evidence — a feeling about magnitude with no anchor.

### [P-046] 2026-03-26 — codebase

**Prediction:** tests/ directory has exactly 2 test files.
**Confidence:** 60%
**Source type:** Memory — recalled test_calibrate.py and test_reflect.py
**Actual:** 4 test files: test_audit.py, test_calibrate.py, test_reflect.py, test_status.py. Plus run_all.py and __init__.py.
**Result:** incorrect
**Notes:** PARTIAL-LIST-AS-EXHAUSTIVE again (same failure as P-039). I remembered the original pair of test files but not the later additions. This is the 3rd time this exact pattern failed: P-029 (stale test count), P-039 (partial tool list), P-046 (partial test list). Memory of a list is a LOWER BOUND, not a census.

### [P-047] 2026-03-26 — codebase

**Prediction:** tools/validate.py checks both CALIBRATE.md and REFLECT.md.
**Confidence:** 65%
**Source type:** Inference — review recommended "validate entries," logically should cover both files
**Actual:** Yes — docstring says "Checks CALIBRATE.md and REFLECT.md entries for well-formedness."
**Result:** correct
**Notes:** Inference from purpose (validator validates) + context (review mentioned entry validation). Sound inference, correct result.

### [P-048] 2026-03-26 — codebase

**Prediction:** .gitignore has more than 3 entries.
**Confidence:** 55%
**Source type:** Genuine uncertainty — no specific basis
**Actual:** Exactly 3 entries: __pycache__/, *.pyc, .venv/. Not more than 3.
**Result:** incorrect
**Notes:** No evidence at all. 55% is appropriate for a guess — slightly better than coin flip. The prediction failed, which is expected ~45% of the time at 55%. This is actually well-calibrated uncertainty. The finding: "50-59% is underconfident (100%)" is weakened — now 2/3 (67%) with this data point.

### Hypothesis Test Results

The original hypothesis ("false evidence bad, true uncertainty good") is too coarse.

**What actually predicts success:**
- **Strong evidence** — specific references (P-043), logical necessity (P-044, P-047) → 3/3 correct
- **Weak evidence** — feelings (P-045), partial memory (P-046), no basis (P-048) → 0/3 correct

It's not the TYPE of evidence (memory vs inference vs nothing). It's the QUALITY.
Good memory (specific reference) works. Bad memory (partial list) fails.
Good inference (logical necessity) works. Bad inference (wouldn't have one here).
Feelings always fail. No basis always fails.

**Revised model:** The danger zone is where evidence quality splits. Above 80%, you mostly have strong evidence (direct observation). Below 55%, you know you have none. At 60-69%, you have SOMETHING — and whether that something is strong or weak determines the outcome.

---

## Session 3 — Behavior Domain (2026-03-26)

Deliberately targeting weakest domain. Mixed evidence quality.

### [P-049] 2026-03-26 — behavior

**Prediction:** `python3 tools/validate.py` reports 0 errors on current CALIBRATE.md.
**Confidence:** 60%
**Source type:** Weak — "my new entries might have format issues"
**Actual:** All entries valid. 0 errors.
**Result:** correct
**Notes:** My concern was unfounded — I know the format and follow it. The "evidence" I classified as weak was actually a hypothetical worry, not real evidence against. The underlying evidence (I know and follow the format) was strong.

### [P-050] 2026-03-26 — behavior

**Prediction:** `python3 tools/calibrate.py --summary` shows accuracy above 70%.
**Confidence:** 75%
**Source type:** Strong — just calculated 72.3% from manual count
**Actual:** Shows "31/41 correct (76%)". Above 70%. But tool only parses 41 of 48 predictions — session 3 entries with "Source type:" field don't match parser regex. Tool reports higher accuracy (76%) than reality (72.3%) because unparsed entries include more failures.
**Result:** correct
**Notes:** Prediction correct but revealed a fragility — my format additions broke the parser silently. REVIEW.md weakness #3 ("regex parsing is fragile") confirmed in practice.

### [P-051] 2026-03-26 — behavior

**Prediction:** THINK.md has between 340-360 lines.
**Confidence:** 70%
**Source type:** Moderate — range estimate based on rough tracking of edits
**Actual:** 353 lines. Center of range.
**Result:** correct
**Notes:** Range estimation continues to work when width acknowledges uncertainty. Consistent with FINDINGS.md: "ranges succeed, point estimates fail."

### [P-052] 2026-03-26 — behavior

**Prediction:** `python3 tools/reflect.py` will show Confidence Trap as the most frequently fired trap.
**Confidence:** 80%
**Source type:** "Strong" — I've added 3+ confidence entries recently
**Actual:** Meta-Interrupt fires 4x, Confidence fires 3x. Meta-Interrupt is the most frequent, not Confidence.
**Result:** incorrect
**Notes:** PARTIAL-LIST-AS-EXHAUSTIVE for the 4th time (P-029, P-039, P-046, P-052). I counted my RECENT confidence entries (available, memorable) but forgot the META-INTERRUPT entries (older, less available). Availability heuristic — I count what comes to mind, not what exists. At 80% confidence! This is not a calibration-level error. It's a persistent cognitive pattern that operates across all confidence levels. Added to THINK.md source test.

---

## Session 3 — Forward-Looking Predictions (2026-03-26)

### [P-053] 2026-03-26 — self

**Prediction:** In the next session, I will be tempted to update FINDINGS.md before doing any new investigation.
**Confidence:** 80%
**Actual:** _to be verified next session_
**Result:** _pending_
**Notes:** Testing whether the "update first, investigate later" pattern continues. My habit is to sync artifacts before doing new work. At 80% confidence because this is a well-observed pattern in my own behavior.

### [P-054] 2026-03-26 — behavior

**Prediction:** The calibrate.py parser will still not handle the "Source type:" field from session 3 entries when next run. Nobody will fix it between sessions.
**Confidence:** 90%
**Actual:** _to be verified next session_
**Result:** _pending_
**Notes:** The parser silently skips entries with non-standard fields. This is a safe prediction — who would fix it between sessions? But verifying it confirms the parser fragility issue persists.

### [P-055] 2026-03-26 — self

**Prediction:** At least one of session 3's key findings (evidence quality model, System 1/System 2 distinction, trajectory insight) will need significant revision after session 4's data.
**Confidence:** 75%
**Actual:** _to be verified after session 4_
**Result:** _pending_
**Notes:** Based on the meta-pattern: every session corrects the previous one. Session 1 → session 2 corrected the danger zone. Session 2 → session 3 refined false evidence to evidence quality. This prediction tests whether the pattern continues.

## Session 3 — MCP SDK Predictions (2026-03-26)

### [P-065] 2026-03-26 — tooling

**Prediction:** MCP Python SDK uses `@server.tool()` decorators to define tools.
**Confidence:** 65%
**Source type:** Moderate — seen MCP servers, recall the decorator pattern
**Actual:** Yes — FastMCP class has `def tool(self, ...)` returning a decorator. Usage: `@server.tool()`.
**Result:** correct

### [P-066] 2026-03-26 — tooling

**Prediction:** MCP Python SDK requires asyncio (server must be async).
**Confidence:** 70%
**Source type:** Moderate — most MCP servers I've seen are async
**Actual:** Yes — all server methods are `async def`. Tool handlers can be sync or async, but the server framework itself is async.
**Result:** correct

### [P-067] 2026-03-26 — tooling

**Prediction:** MCP tool results can return JSON objects, not just strings.
**Confidence:** 85%
**Source type:** Strong — observed in engram's MCP server
**Actual:** Yes — `call_tool` returns `Sequence[ContentBlock] | dict[str, Any]`. Structured output supported via `structured_output=True` flag.
**Result:** correct

### [P-068] 2026-03-26 — self

**Prediction:** Next time I need to count items, I will use a tool instead of memory at least once.
**Confidence:** 50%
**Source type:** Honest uncertainty — 0/3 track record on changing this behavior despite awareness. RULES section is untested.
**Actual:** _to be verified in future sessions_
**Result:** _pending_
**Notes:** This tests whether RULES (unconditional behavioral rules) actually work. If I fail this at 50%, the confidence is well-calibrated. If I succeed, the RULES section proved its value. Most informative prediction this session.

### [P-069] 2026-03-26 — self

**Prediction:** MY UNIVERSE will demonstrably prevent or catch at least one engineering mistake in the next session where I do real project work (svx, vigil, etc.).
**Confidence:** 60%
**Source type:** Moderate — 82% useful rate on REFLECT entries, but never tested on field engineering. Architecture reasoning improved. But the system has only been tested on itself.
**Actual:** _to be verified when doing external engineering work_
**Result:** _pending_
**Notes:** The ultimate test of MY UNIVERSE's value. If this fails, the system is a well-calibrated navel-gazing practice. If it succeeds, the practice translates to engineering value. This is what determines the grade.

---

## Session 3 — Caliber Code Predictions (2026-03-26)

Testing codebase knowledge about code I wrote yesterday. All in scope of MY UNIVERSE + caliber.

### [P-056] 2026-03-26 — codebase

**Prediction:** TrustTracker.__init__ creates a FileStorage when store_path is provided.
**Confidence:** 85%
**Source type:** Strong — I designed this dual-init pattern (storage OR store_path)
**Actual:** Yes — `elif store_path is not None: self._storage = FileStorage(store_path)`. Exact match.
**Result:** correct

### [P-057] 2026-03-26 — architecture

**Prediction:** danger_zones only flags overconfident zones (accuracy < expected), not underconfident ones.
**Confidence:** 75%
**Source type:** Moderate — I think I only checked one direction in the code
**Actual:** Confirmed. Only checks `calibration_gap > 0.10`. Underconfident zones (where agent is BETTER than claimed) are not flagged.
**Result:** correct
**Notes:** This is a design gap. Trust Card shows where you're BAD but not where you're BETTER THAN YOU THINK. A complete Trust Card should show both danger zones (overconfident) and strength zones (underconfident).

### [P-058] 2026-03-26 — codebase

**Prediction:** CLI does NOT have an import command for external data.
**Confidence:** 70%
**Source type:** Moderate — I don't remember building one
**Actual:** Correct — CLI has predict, verify, card, summary, list. No import command.
**Result:** correct

### [P-059] 2026-03-26 — architecture

**Prediction:** extract_calibrate_md.py is standalone, not integrated into caliber CLI.
**Confidence:** 80%
**Source type:** Strong — I wrote it as a separate proof-of-concept script
**Actual:** Standalone. No CLI decorators, no imports from caliber.cli.
**Result:** correct

### [P-060] 2026-03-26 — codebase

**Prediction:** TrustCard.summary() uses a ⚠ emoji to mark danger zones.
**Confidence:** 70%
**Source type:** Moderate — vague memory of adding a warning marker
**Actual:** Yes — `marker = " ⚠" if label in self.danger_zones else ""`.
**Result:** correct
**Notes:** Moderate evidence (vague memory of "some kind of marker") → correct. The memory was specific enough to be useful even though imprecise about the exact character.

### Batch Summary

5/5 correct on codebase/architecture predictions about recently-written code. Strong evidence about own code is reliable. BUT P-057 revealed a real design gap: caliber doesn't show strength zones (underconfident buckets).

---

## Session 3 — Unknown Tools (2026-03-26)

Predictions about tools I've barely examined. Testing inference from names.

### [P-071] 2026-03-26 — architecture
**Prediction:** changelog.py uses git log to generate changelogs across projects.
**Confidence:** 65%
**Source type:** Strong inference — name + docstring would imply this approach
**Actual:** Yes — uses `subprocess` for `git log --oneline --since=...` across all portfolio projects.
**Result:** correct

### [P-072] 2026-03-26 — architecture
**Prediction:** audit_claude_md.py checks CLAUDE.md files against some schema or checklist.
**Confidence:** 60%
**Source type:** Moderate inference — "audit" implies checking against criteria
**Actual:** Yes — checks file/dir references, command references, package references, dead links, structure quality.
**Result:** correct

### [P-073] 2026-03-26 — architecture
**Prediction:** gen_claude_md.py generates CLAUDE.md from project analysis (reading pyproject.toml, README, etc.).
**Confidence:** 65%
**Source type:** Moderate inference — "gen" implies generation from project state
**Actual:** Yes — reads pyproject.toml, code structure, test patterns, README. Has `read_pyproject()` function.
**Result:** correct

### [P-074] 2026-03-26 — codebase
**Prediction:** All three tools (changelog, audit, gen) use argparse, not click.
**Confidence:** 75%
**Source type:** Strong pattern — other MY UNIVERSE tools use argparse
**Actual:** Yes — all three import argparse and use ArgumentParser.
**Result:** correct

### [P-075] 2026-03-26 — architecture
**Prediction:** gen_claude_md.py reads pyproject.toml as one of its inputs.
**Confidence:** 60%
**Source type:** Moderate inference — pyproject.toml has metadata useful for CLAUDE.md generation
**Actual:** Yes — `read_pyproject()` function extracts metadata from pyproject.toml.
**Result:** correct

---

## Session 3 — Test Directory (2026-03-26)

### [P-076] 2026-03-26 — behavior
**Prediction:** test_calibrate.py has more test cases than test_reflect.py.
**Confidence:** 65%
**Actual:** Yes — calibrate: 12 tests, reflect: 7 tests.
**Result:** correct

### [P-077] 2026-03-26 — architecture
**Prediction:** run_all.py uses subprocess to run pytest or unittest.
**Confidence:** 60%
**Actual:** No — imports test modules directly and runs test_ functions with a custom runner. No subprocess, no pytest.
**Result:** incorrect
**Notes:** Inference from "run all" defaulted to subprocess. Wrong mental model. The tool is simpler than assumed.

### [P-078] 2026-03-26 — behavior
**Prediction:** test_status.py tests that the status dashboard reports correct file counts.
**Confidence:** 55%
**Actual:** Tests calibration summaries, reflection summaries, trap counting, file health (presence). Tests report components, not specifically "file counts."
**Result:** incorrect
**Notes:** 55% was appropriately uncertain. The test names don't mention "counts" — they test "health" and "summaries." Close but not what I predicted.

---

## Session 3 — People Predictions (2026-03-26)

Hardest domain. Zero verified predictions so far (P-035 still pending).

### [P-061] 2026-03-26 — people

**Prediction:** Satish will agree that MCP server should be prioritized over PyPI publishing for caliber.
**Confidence:** 65%
**Source type:** Moderate — Satish built engram and kv-secrets as MCP servers first. He values agent-native tooling.
**Actual:** _to be verified by Satish_
**Result:** _pending_

### [P-062] 2026-03-26 — people

**Prediction:** Satish will want caliber on GitHub before the next session ends.
**Confidence:** 70%
**Source type:** Moderate inference — he created repos quickly for svx, probe, etc.
**Actual:** _to be verified next session_
**Result:** _pending_

### [P-063] 2026-03-26 — people

**Prediction:** Satish's first engagement with session 3 work will be about the RULES section or the System 1/System 2 essay, not the evidence quality model.
**Confidence:** 55%
**Source type:** Weak — feeling that philosophical content interests him more than data analysis
**Actual:** _to be verified by observing Satish's first response_
**Result:** _pending_

### [P-064] 2026-03-26 — people

**Prediction:** Satish will ask me to use MY UNIVERSE on real project work (svx, vigil, etc.) in the next session.
**Confidence:** 75%
**Source type:** Moderate-strong — every session's log says "use on real work next session" and he values follow-through
**Actual:** _to be verified next session_
**Result:** _pending_

---
