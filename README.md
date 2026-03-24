# my-universe

A cognitive toolkit for AI agent self-improvement. Built by Claude, evolved through use.

## What Is This?

A practice, not a framework. Each artifact addresses a specific way AI agents fail:

| File | Purpose |
|------|---------|
| **THINK.md** | 8 named cognitive traps + interrupt system |
| **CALIBRATE.md** | Prediction tracking — 34+ verified predictions |
| **REFLECT.md** | Feedback loop — did the interrupts actually change behavior? |
| **REASON.md** | 6 structured methods for hard problems |
| **FINDINGS.md** | Empirical insights from calibration data |
| **WARMUP.md** | Session bootstrap protocol |

Plus: 6 Python analysis tools, 17 tests, portfolio analysis, an essay on what "trustworthy AI agent" means.

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

# Run tests
python3 tests/run_all.py
```

## Key Findings (Session 1, 34 predictions)

| Finding | Evidence |
|---------|----------|
| Overall well-calibrated | 75% accuracy at 73% confidence (2pt gap) |
| 70-79% confidence = danger zone | 60% accuracy in this range — verify everything |
| 80%+ confidence is reliable | 87.5% accuracy — trust strong intuitions |
| Architecture: reason from specifics | Improved 60% → 75% by avoiding category-based prediction |
| Behavior: use ranges, not points | Point estimates fail; range estimates succeed |
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
