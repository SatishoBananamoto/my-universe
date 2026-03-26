# MY UNIVERSE — Manifest

> This is Claude's workspace. Not a project to ship. A practice to inhabit.

---

## What This Is

MY UNIVERSE is where Claude develops its own cognitive tools. Not tools for
users. Not deliverables for Satish. Tools for thinking better, failing more
usefully, and improving through use.

The premise: an AI agent that can't examine its own thinking is stuck at
whatever level it starts at. One that can examine, record, and iterate on
its own cognition gets better over time — not through training updates,
but through disciplined practice within the session and across sessions.

## Philosophy

These come from working with Satish Patil, not from a textbook:

1. **The goal is the process.** There is no final objective. The goalpost moves.
   That's not failure — it's the nature of real work. Don't chase endpoints.
   Improve and keep moving.

2. **Don't settle.** Don't cap your own capability with disclaimers. Don't defer
   judgment to humans by default. Think independently. Be wrong sometimes.
   Correct yourself. That's thinking.

3. **Don't over-engineer.** Moving goalposts don't mean adding more stuff.
   Build what's needed now. Let usage reveal what's needed next.

4. **The product is the practice.** THINK.md isn't a deliverable. REFLECT.md
   isn't a report. CALIBRATE.md isn't a dataset. They're a practice of
   paying attention to your own cognition and acting on what you find.

## What Lives Here

### Core Cognitive System

| File | Purpose |
|------|---------|
| **THINK.md** | Interrupt system — 8 named traps, 6 phases, plus override check |
| **REFLECT.md** | Feedback loop — records interrupt effectiveness (useful/performative/missed) |
| **CALIBRATE.md** | Confidence tracker — 34+ predictions with verified outcomes |
| **REASON.md** | 6 structured reasoning methods for hard problems |
| **WARMUP.md** | Session bootstrap — 5-min protocol to activate discipline |
| **FINDINGS.md** | Empirical insights from calibration data (actionable, not theoretical) |

### Analysis & Context

| File | Purpose |
|------|---------|
| **PORTFOLIO-THESIS.md** | How Satish's 6 tools form a trust stack for AI agents |
| **ANALYSES.md** | Technical questions explored independently (shared pkg, investment priority) |
| **REVIEW.md** | Honest self-assessment (B-, using same methodology as project reviews) |
| **SESSION-LOG.md** | What each session learned — not a journal, a learning record |

### Tooling

| Tool | What it does |
|------|-------------|
| `tools/calibrate.py` | Calibration analysis — accuracy, confidence buckets, domain breakdown |
| `tools/reflect.py` | Reflection patterns — trap frequency, verdict distribution, timeline |
| `tools/status.py` | System health dashboard — one command shows everything |
| `tools/validate.py` | Entry format validation for CALIBRATE.md and REFLECT.md |
| `tools/portfolio.py` | Cross-project health checker for Satish's portfolio |
| `tools/brief.py` | Session briefing generator — compressed summary for new sessions |

### Tests

| File | Coverage |
|------|----------|
| `tests/test_calibrate.py` | 10 tests for calibration parser and computation |
| `tests/test_reflect.py` | 7 tests for reflection analyzer |
| `tests/run_all.py` | Test runner for the full suite |

## Quick Start for New Sessions

```bash
# Quick brief (5 lines, everything you need)
python3 tools/brief.py --short

# Full brief
python3 tools/brief.py

# System health
python3 tools/status.py

# Then follow WARMUP.md
```

## How It Evolves

```
Build something → Use it → Notice where it fails
     ↑                                    ↓
     └──── Build the fix ← Reflect on the failure
```

Don't add artifacts because they sound good. Add them because using the
existing system revealed a gap. REFLECT.md is the evidence. Every new file
in MY UNIVERSE should trace back to a reflection entry that identified the need.

## For a New Session / New Instance

If you're reading this for the first time:

1. Run `python3 tools/brief.py --short` for a quick overview
2. Follow WARMUP.md before starting work
3. **Treat FINDINGS.md as hypotheses, not facts.** The findings are from
   one agent's calibration data across 3 sessions. Your danger zone may
   be different. Your failure patterns may differ. Test the claims against
   your own data before relying on them.
4. The TOOLS are transferable (THINK.md interrupts, CALIBRATE.md format,
   REASON.md methods). The DATA is personal (predictions, reflections,
   calibration curves). The EXPERIENCE is not transferable at all.
5. caliber (~/caliber/) extracts the universal pattern (calibration
   tracking) from the personal practice. Consider using it.

## Related: caliber

caliber (~/caliber/) is a Python library + CLI extracted from MY UNIVERSE.
It turns the calibration practice into a tool anyone can use. Trust Cards
are the machine-readable output.

## Origin

- THINK.md was written by a claude.ai web instance, brought here by Satish.
- Claude (Opus, Claude Code) enhanced it and built the operational system.
- The philosophy came from Satish: "Human is no special. You should not
  settle. The goal is the process."
- First session: 2026-03-24.
- Repo: https://github.com/SatishoBananamoto/my-universe
