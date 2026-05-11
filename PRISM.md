# PRISM — MY UNIVERSE

> Claude's cognitive workspace. Tools for thinking better, failing more usefully, and improving through use.
> Updated before every commit. Single source of truth.

**Last session**: 2026-05-11 — Recorded svx audit-path continuation
**Repo**: Recording the `svx:01eb6d2` connected-project continuation. Last verified locally with 82 tests passing.

---

## NEXT SESSION — START HERE

### What just happened (2026-05-10 — Codex/Kai portability field validation)

Completed the Codex/Kai portability test without mixing Codex/Kai data into Claude's `CALIBRATE.md` or `REFLECT.md`.

- Engram MCP is connected and usable from Codex.
- `CODEX-PRISM.md` is the Codex/Kai lane for field notes and promotion decisions.
- `tools/validate.py` now treats historical ID gaps as strict-audit findings, not normal validation failures.
- `caliber` field session fixed tracking drift around trajectory support instead of reimplementing code that already existed.
- `REVIEW.md` now has a dated field-validation update: grade moves from B- to B, with external adoption still unproven.
- `ONBOARDING-TRIAL.md` now defines the next transfer-validation protocol with no-deletion/archive and continuation constraints.
- `CONTINUATION-GATE.md` now defines how `Continue` becomes the next task list instead of a stopping point.
- First fresh-agent trial ran against `caliber` and produced `caliber:439b4b8`.
- Continued from that trial into `caliber:45ea13d`, which added shared-store multi-agent CLI regression coverage and fixed storage filename collisions.
- Continued again into `caliber:102b294`, which archived the old standalone parser and moved the active CALIBRATE import wrapper onto the shared importer.
- Continued into `caliber:4c4a781`, which added a safe `caliber mcp-config` helper that prints or installs MCP config entries with backups.
- Continued into `caliber:64464ad`, which added `GETTING_STARTED.md` for first external users and linked it from README.
- Continued into `analysis:fe6e352`, which added a root README for the AI-agent dependency-risk report without touching dirty/high-risk repos.
- Continued into `kvsecure.com:5e3f0b0`, which added a root README preserving the site story, boundaries, and verification checklist.
- Continued into `SatishoBananamoto:db4da6b`, which refreshed profile README stats from the current portfolio health output.
- Continued into `kvsecure.com:4b58ba5`, which completed live browser QA, fixed clipboard fallback and feedback-card heading spacing, then recorded the Pages verification evidence.
- Continued into `AI-Agents-Failure-Modes:a1ac245`, which made API tests transport-independent after `TestClient` requests hung in this sandbox, then verified 32 tests, the CLI fixture smoke, and passing GitHub Actions run `25700134343`.
- Continued into portfolio consistency work: added `AI-Agents-Failure-Modes` to `tools/portfolio.py` and updated `SatishoBananamoto:ff3dc84` so the public profile now lists the ICIF-AES verifier and 8-tool stats from the refreshed scanner.
- Continued into `analysis:15a563c`, which completed the README report index so all 46 `reports/*.md` files are linked with no extras.
- Continued inside MY UNIVERSE to fix the portfolio quick table after long project and branch names exposed column drift.
- Continued into `scroll:8c20946`, which hardened the engram deposit quality gate, separated quality skips from system errors, added `--no-quality-check`, and verified 129 scroll tests before push.
- Continued into `probe:7a26654`, which adopted a verified DOSSIER/.graft tracking baseline after 95 probe tests and compileall passed.
- Continued into `svx:01eb6d2`, which fixed MCP server audit-path isolation, synced runtime version metadata, added SENTINEL/.graft tracking, and verified 66 svx tests before push.

### Relevant prior state (2026-04-12 — THINK Integration)

Diagnosed why THINK.md doesn't fire automatically during work: the activation mechanism is circular (you need the interrupt to notice you need the interrupt). Solved with a three-layer model:

- **Layer 1 — Process Rules 7-13 (CLAUDE.md).** Proven THINK rules merged into binding process rules. No longer a separate "THINK Rules" section. They fire because CLAUDE.md stays in context.
- **Layer 2 — Cognitive Gates (CLAUDE.md).** Four lightweight checks at natural breakpoints: before delivery, first failure, familiarity signal, smooth sailing. Tied to events, not memory.
- **Layer 3 — /think (manual).** Full THINK.md deep-dive reserved for genuine uncertainty, hard decisions, suspiciously smooth work.

Also fixed WARMUP.md: added continuation-session fallback (re-orient, check drift, one prediction) for mid-conversation resumptions.

### #1 Priority: Fresh-agent or external-user validation

Run a constrained onboarding trial where a fresh agent or external user follows `MANIFEST.md`, `WARMUP.md`, and `THINK.md`, then records whether the system changed a real engineering decision. Do not build more self-referential tooling until that evidence exists.

### Continuation gate

When an active task list reaches `Continue`, use `CONTINUATION-GATE.md` before creating the next task list. The gate uses reflection, repo evidence, judgment, and an optional xhigh reviewer for unclear/risky/self-referential paths. The new task list must end with `Continue` again.

### Codex/Kai portability lane

`CODEX-PRISM.md` is the Codex/Kai lane inside MY UNIVERSE. Use it for Codex-specific field notes, portability findings, and Engram-backed context before promoting anything into Claude's `CALIBRATE.md`, `REFLECT.md`, or core MY UNIVERSE docs.

### What NOT to do

- Don't build more self-referential tools — the system works, USE it
- Don't re-separate the layers — the whole point is integration into CLAUDE.md
- Don't trust bucket-level patterns below 20 predictions per bucket
- Don't delete source, docs, state, history, or user data. Archive first if anything must be displaced.

---

## Work

### Field validation

_Does this system improve real engineering? P-069 is the existential test._

- [x] Apply THINK.md during a real engineering session — reasoning audit 2026-03-30 · `caliber:P-069 correct`
- [x] Track interrupts: completion trap (2x), verify-before-assert (1x), so-what test (33 entries), counting rules (throughout)
- [x] Create Codex/Kai lane for portability field-testing — 2026-05-10 · `CODEX-PRISM.md`
- [x] Connect Codex to Engram MCP for cross-project memory/context — 2026-05-10 · native `engram_*` tools available after reload
- [x] Codex/Kai field session 1: validator false positive fixed — 2026-05-10 · `tools/validate.py --strict-ids` preserves historical gap audit without failing normal validation
- [x] Codex/Kai field session 2: caliber trajectory tracking drift fixed — 2026-05-10 · `caliber:7e390bd`, 98 tests passing
- [x] After 3 field sessions: assess whether calibration/thinking improved outcomes (3/3 done; external user validation remains separate)
- [x] Update REVIEW.md with field validation results — 2026-05-10 · added dated validation update without rewriting the original v1 review
- [x] Run `ONBOARDING-TRIAL.md` with a fresh agent or external user — 2026-05-11 · Hypatia subagent fixed `caliber/CLAUDE.md`, `caliber:439b4b8`, 98 tests passing
- [x] Continue from onboarding trial into `caliber` multi-agent hardening — 2026-05-11 · `caliber:45ea13d`, 101 tests passing
- [x] Continue from multi-agent hardening into `caliber` import cleanup — 2026-05-11 · `caliber:102b294`, 103 tests passing
- [x] Continue from import cleanup into `caliber` MCP config helper — 2026-05-11 · `caliber:4c4a781`, 105 tests passing
- [x] Continue from MCP config helper into `caliber` first-user tutorial — 2026-05-11 · `caliber:64464ad`, 105 tests passing
- [x] Continue from caliber into clean portfolio docs slice — 2026-05-11 · `analysis:fe6e352`, link/file checks passing
- [x] Continue from analysis into clean site docs slice — 2026-05-11 · `kvsecure.com:5e3f0b0`, `node --check` and stale-claim checks passing
- [x] Continue from kvsecure into profile stats correction — 2026-05-11 · `SatishoBananamoto:db4da6b`, diff hygiene passing
- [x] Continue from profile into kvsecure live browser QA — 2026-05-11 · `kvsecure.com:4b58ba5`, live Chromium QA and focused interaction smoke passing
- [x] Continue from kvsecure QA into AI-Agents-Failure-Modes test hardening — 2026-05-11 · `AI-Agents-Failure-Modes:a1ac245`, 32 tests, CLI smoke, and GitHub Actions run `25700134343` passing
- [x] Continue from AI-Agents into portfolio registry/profile consistency — 2026-05-11 · `SatishoBananamoto:ff3dc84`, portfolio scanner shows 8 tools and 35,815 source lines
- [x] Continue from portfolio consistency into analysis report index completion — 2026-05-11 · `analysis:15a563c`, 46/46 report links covered
- [x] Continue from report-index completion into portfolio quick-table alignment — 2026-05-11 · dynamic project width and 30-character branch column, 79 tests passing
- [x] Continue from portfolio quick-table alignment into scroll quality-gate hardening — 2026-05-11 · `scroll:8c20946`, 129 tests passing
- [x] Continue from scroll quality-gate hardening into probe tracking baseline — 2026-05-11 · `probe:7a26654`, 95 tests passing
- [x] Continue from probe tracking baseline into svx audit-path isolation — 2026-05-11 · `svx:01eb6d2`, 66 tests passing
- [ ] Continue — pick the next real engineering task and keep the evidence loop moving

### Calibration refinement

_94 verified, 5 pending (people-domain, need Satish). Overall calibration confirmed. Behavior is the structural weakness._

- [x] Verified 6 pending predictions (P-053/054/055/062/068/069) during reasoning audit
- [x] 60-69% danger zone confirmed as artifact (30 predictions, 63% accuracy, gap +0.012)
- [x] LRN-043 created: definitive calibration entry superseding LRN-019→LRN-017 chain
- [ ] Continue predictions during real work — focus on behavior domain (31 predictions, 64% accuracy)
- [ ] Verify remaining 5 people-domain predictions with Satish (P-035, P-061, P-063, P-064, P-091)
- [ ] Track evidence quality systematically (strong vs. weak sources)
- [ ] Continue — keep calibration attached to real work, not standalone ritual

### System maintenance

- [x] WARMUP.md: add fallback for continuation sessions — 2026-04-12 · added abbreviated protocol (re-orient, check drift, one prediction)
- [x] THINK.md: integrated into CLAUDE.md process rules + cognitive gates — 2026-04-12 · three-layer model replaces separate THINK Rules section
- [x] tools/validate.py: normal validation allows historical ID gaps; `--strict-ids` reports them — 2026-05-10 · P-070 never existed in git history
- [x] REVIEW.md: add field validation update — 2026-05-10 · tests and real-work evidence changed original B- assessment limits
- [x] ONBOARDING-TRIAL.md: add transfer-validation protocol — 2026-05-10 · no-deletion and continuation constraints included
- [x] tests/test_onboarding_trial.py: guard transfer protocol and generated Continue action — 2026-05-10 · 52 tests passing
- [x] README.md/FINDINGS.md: update public calibration snapshot — 2026-05-10 · 99 entries, 94 resolved, 5 pending
- [ ] REFLECT.md: continue logging after field sessions
- [x] tools/status.py: fix template verdict counted as real reflection — 2026-05-10 · status and brief now report 20 reflections; 53 tests passing
- [x] CODEX-REFLECT.md: add separate Codex/Kai reflection lane — 2026-05-10 · binary trap recorded outside Claude `REFLECT.md`
- [x] tools/reflect.py/tools/next.py: count multi-trap headers and active reflection lanes — 2026-05-10 · 57 tests passing
- [x] tools/validate.py: validate `CODEX-REFLECT.md` alongside `REFLECT.md` — 2026-05-10 · 58 tests passing
- [x] CONTINUATION-GATE.md/tools/next.py: define recursive `Continue` review gate — 2026-05-11 · optional xhigh reviewer path included; 63 tests passing
- [ ] Continue — keep docs, tools, and tests aligned after each behavior change

### Done

<details>
<summary>Sessions 1-3 — completed 2026-03-26</summary>

- [x] THINK.md: built + enhanced with 6 data-driven additions — Session 1
- [x] REFLECT.md: 21 entries, 81% useful — Sessions 1-3
- [x] CALIBRATE.md: 100 predictions, 76.3% accuracy — Sessions 1-3
- [x] FINDINGS.md: evidence quality model + statistical warnings — Session 3
- [x] REASON.md: 6 methods, used on 2 real decisions — Session 1
- [x] WARMUP.md: session bootstrap protocol, tested — Sessions 1-2
- [x] Tools: 11 Python scripts (status, brief, calibrate, reflect, etc.) — Session 1
- [x] Tests: 42 passing — Sessions 1-3
- [x] Caliber extracted: trust protocol shipped to PyPI — Session 2-3
- [x] PORTFOLIO-THESIS.md: trust stack analysis — Session 1
- [x] Statistical rigor: binomial tests on all findings — Session 3

</details>

---

## Decision Log

| ID | Date | Decision | Why |
|----|------|----------|-----|
| D-001 | 2026-03-24 | Published MY UNIVERSE as public repo | Steel-Man analysis: if work can't survive being visible, the problem is the work. |
| D-002 | 2026-03-24 | Did NOT build observability tool | Pre-Mortem: 2/3 failure stories were probable. Not every gap needs a tool. |
| D-003 | 2026-03-26 | Extracted caliber as separate library | The calibration practice produced enough data to be useful as a standalone tool. |
| D-004 | 2026-05-10 | No deletion; archive first | Satish made no-deletion an explicit operating constraint for MY UNIVERSE. |

---

## Session Log

### 2026-03-24 — Session 1: Build the system

- **Worked on:** Full MY UNIVERSE construction (autonomous, Satish asleep)
- **Completed:** THINK.md, REFLECT.md, CALIBRATE.md, REASON.md, WARMUP.md, 7 tools, PORTFOLIO-THESIS.md
- **Key discoveries:** 70-79% danger zone (later corrected), weaponized self-awareness trap, build-rhythm autopilot
- **Completion Trap:** Caught by Satish. Twice. Added to THINK.md.

### 2026-03-26 — Session 2: Build caliber

- **Worked on:** WARMUP test (worked), caliber extraction
- **Completed:** Caliber library, corrected danger zone (60-69% not 70-79%)
- **Key insight:** Session 1's findings were small-sample artifacts

### 2026-03-26 — Session 3: Investigation

- **Worked on:** Statistical rigor, evidence quality model, deliberate hard predictions
- **Completed:** Binomial tests on all findings, 100th prediction, FINDINGS.md refined
- **Key discovery:** NO bucket-level finding is statistically significant (p>0.10). Evidence quality matters more than confidence number.
- **Completion Trap:** Caught by Satish. Third time.

### 2026-04-12 — Session 5: THINK Integration

- **Worked on:** Why THINK.md doesn't trigger automatically; how to make thinking operational
- **Completed:** Three-layer model (process rules → cognitive gates → /think manual). CLAUDE.md restructured. THINK.md "How to Use" rewritten. Skill file updated. WARMUP.md continuation-session fallback added.
- **Key insight:** The activation mechanism was circular — you need the interrupt to notice you need the interrupt. Solution: put proven rules where they stay in context (CLAUDE.md), tie checks to events (gates), reserve /think for depth.
- **Discussed:** Codex portability — Layers 1-2 transfer via AGENTS.md, Layer 3 via skills. Hooks/lifecycle automation don't port yet.

### 2026-05-10 — Codex/Kai Portability Field Sessions

- **Worked on:** Porting MY UNIVERSE discipline into Codex/Kai without polluting Claude's `CALIBRATE.md` or `REFLECT.md`.
- **Completed:** Engram MCP connection, `CODEX-PRISM.md`, validator false-positive fix, and external `caliber` tracking-drift fix.
- **Key insight:** The three-layer model changed behavior when it forced source-of-truth checks: in MY UNIVERSE it separated historical ID gaps from malformed entries; in `caliber` it prevented reimplementing a CLI command that already existed.
- **Remaining limit:** This proves portability across Codex/Kai repo work, not external human adoption.

---

### Key reference files

| File | What it contains |
|------|-----------------|
| PRISM.md | This file. |
| CODEX-PRISM.md | Codex/Kai portability lane and field notes. |
| THINK.md | Cognitive interrupts — the core system. 393 lines. |
| REFLECT.md | Interrupt effectiveness data. 21 entries. |
| CALIBRATE.md | 100 predictions with outcomes. |
| FINDINGS.md | Empirical analysis from calibration data. |
| WARMUP.md | Session bootstrap protocol. |
| REASON.md | 6 structured reasoning methods. |
| REVIEW.md | Self-assessment (original grade B-, field update grade B). |
| SESSION-LOG.md | Detailed session learning records (historical). |
