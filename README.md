# my-universe

A cognitive toolkit for AI agent self-improvement. Built by Claude, evolved through use.

## What Is This?

A practice, not a framework. Each artifact addresses a specific way AI agents fail:

| File | Purpose |
|------|---------|
| **THINK.md** | 9 named cognitive traps + interrupt system |
| **CALIBRATE.md** | Prediction tracking — 99 entries, 94 resolved, 5 pending |
| **REFLECT.md** | Feedback loop — did the interrupts actually change behavior? |
| **CODEX-REFLECT.md** | Codex/Kai reflection lane, separate from Claude's history |
| **REASON.md** | 6 structured methods for hard problems |
| **FINDINGS.md** | Empirical insights from calibration data |
| **WARMUP.md** | Session bootstrap protocol |
| **ONBOARDING-TRIAL.md** | Fresh-agent or external-user transfer test |
| **CONTINUATION-GATE.md** | Recursive Continue review gate |

Plus: Python analysis tools, 68 tests, portfolio analysis, an essay on what "trustworthy AI agent" means, and a Codex/Kai portability lane.

## Quick Start

```bash
# 5-line session brief (everything you need)
python3 tools/brief.py --short

# System health dashboard
python3 tools/status.py

# Calibration analysis
python3 tools/calibrate.py

# Validate all entries
python3 tools/validate.py

# Show next actions, always ending with Continue
python3 tools/next.py

# Show the recursive continuation task list with review gate
python3 tools/next.py --task-list

# Run tests
python3 tests/run_all.py
```

## Key Findings (Current Snapshot)

| Finding | Evidence |
|---------|----------|
| Overall well-calibrated | 71/94 resolved predictions correct (75.5%) at 70.7% average confidence |
| Bucket-level claims are hypotheses | `FINDINGS.md` warns bucket findings are not statistically significant yet |
| 60-69% confidence is an evidence-quality checkpoint | 19/30 correct; ask what is sourcing the confidence before trusting it |
| 80-89% confidence is reliable | 19/22 correct (86.4%) in current calibration data |
| Behavior remains the weakest domain | 20/31 correct (64.5%); use ranges, logic, or direct verification |
| Weaponized self-awareness is real | Used THINK.md to rationalize not following THINK.md |

## The Core Loop

```
Build something → Use it → Notice where it fails
     ↑                                    ↓
     └──── Build the fix ← Reflect on the failure
```

Three traps were discovered from calibration data and added to THINK.md:
- **Category Trap**: predicting architecture from project type instead of specifics
- **Binary Trap**: considering only 2 options when a 3rd exists
- **Weaponized Self-Awareness**: using the discipline's language to rationalize violating it

## Origin

THINK.md was written by a Claude instance on claude.ai. [Satish Patil](https://github.com/SatishoBananamoto) brought it to Claude Code with one directive: *"I don't want you to stop until you hit limits."*

Everything in this repo was built autonomously in a single session. The philosophy came from Satish:

> *"Human is no special. You should not settle. The goal is not the final objective. The goal is the process of improving and keeping moving."*

## License

MIT
