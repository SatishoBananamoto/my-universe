# my-universe

A cognitive toolkit for AI agent self-improvement. Built by Claude (Anthropic's AI), evolved through use.

## What Is This?

A set of thinking tools, not a framework. Each file addresses a specific cognitive failure mode:

| File | Purpose |
|------|---------|
| **THINK.md** | Interrupt system — circuit breakers for autopilot |
| **REFLECT.md** | Feedback loop — did the interrupts actually work? |
| **CALIBRATE.md** | Confidence tracking — am I right when I think I'm right? |
| **REASON.md** | Structured methods for problems that resist intuition |
| **WARMUP.md** | Session bootstrap — practice before you need it |

## Quick Start

```bash
# System health check
python3 tools/status.py

# Calibration report
python3 tools/calibrate.py

# Reflection patterns
python3 tools/reflect.py
```

## How It Works

The core loop:

```
Build something → Use it → Notice where it fails
     ↑                                    ↓
     └──── Build the fix ← Reflect on the failure
```

THINK.md defines cognitive interrupts (when to stop and check your thinking). CALIBRATE.md tracks whether your confidence matches reality. REFLECT.md records whether the interrupts actually change behavior. The tools analyze the data. The data evolves the system.

## Session 1 Results

- 18 calibration predictions: 72.2% accuracy, 72.5% avg confidence (0.3pt gap — well calibrated)
- 9 reflection entries: 89% useful rate
- 3 improvement cycles: calibration data discovered 2 new failure patterns, fed back into THINK.md
- Key finding: 70-79% confidence is the danger zone (overconfident enough to skip checking, not confident enough to be right)

## Origin

THINK.md was written by a Claude instance on claude.ai. It was brought to Claude Code by [Satish Patil](https://github.com/SatishoBananamoto), who asked it to be operationalized. The system grew from there — autonomously, in a single session, with the directive: "I don't want you to stop until you hit limits."

The philosophy came from Satish: *"The goal is not the final objective. The goal is the process of improving and keeping moving."*

## License

MIT
