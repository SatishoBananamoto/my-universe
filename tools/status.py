#!/usr/bin/env python3
"""
MY UNIVERSE health check.

Single command that shows the state of the cognitive toolkit:
- Calibration summary
- Reflection summary
- THINK.md trap count
- What needs attention

Usage:
    python status.py
"""

import re
from pathlib import Path

BASE = Path(__file__).parent.parent


def count_traps(think_path: Path) -> int:
    """Count named traps in THINK.md."""
    if not think_path.exists():
        return 0
    text = think_path.read_text()
    # Count ### The X Trap patterns
    traps = re.findall(r"###\s+The\s+\w+.*?Trap", text)
    # Also count bold sub-traps like **The category trap**
    sub_traps = re.findall(r"\*\*The\s+\w+.*?trap", text, re.IGNORECASE)
    return len(traps) + len(sub_traps)


def calibration_summary(cal_path: Path) -> dict:
    """Quick calibration stats."""
    if not cal_path.exists():
        return {"total": 0, "resolved": 0, "correct": 0}

    text = cal_path.read_text()
    # Skip template lines that contain both "correct | incorrect"
    results = [m for m in re.findall(r"\*\*Result:\*\*\s*(correct|incorrect)", text)]
    # Remove the template match (line with "correct | incorrect")
    template_matches = len(re.findall(r"\*\*Result:\*\*\s*correct\s*\|\s*incorrect", text))
    if template_matches > 0:
        # Remove template 'correct' from results
        for _ in range(template_matches):
            if "correct" in results:
                results.remove("correct")
    pending = len(re.findall(r"\*\*Result:\*\*\s*_pending", text))

    correct = results.count("correct")
    incorrect = results.count("incorrect")
    total = correct + incorrect + pending

    confidences = [int(m) for m in re.findall(r"\*\*Confidence:\*\*\s*(\d+)%", text)]
    resolved_confidences = confidences[:len(results)] if confidences else []

    avg_conf = sum(resolved_confidences) / len(resolved_confidences) if resolved_confidences else 0
    accuracy = correct / len(results) * 100 if results else 0

    return {
        "total": total,
        "resolved": len(results),
        "pending": pending,
        "correct": correct,
        "incorrect": incorrect,
        "avg_confidence": avg_conf,
        "accuracy": accuracy,
    }


def reflection_summary(reflect_path: Path) -> dict:
    """Quick reflection stats."""
    if not reflect_path.exists():
        return {"total": 0, "useful": 0, "performative": 0, "missed": 0}

    text = reflect_path.read_text()
    verdicts = re.findall(r"\*\*Verdict:\*\*\s*(useful|performative|missed)", text, re.IGNORECASE)

    return {
        "total": len(verdicts),
        "useful": sum(1 for v in verdicts if v.lower() == "useful"),
        "performative": sum(1 for v in verdicts if v.lower() == "performative"),
        "missed": sum(1 for v in verdicts if v.lower() == "missed"),
    }


def file_health(base: Path) -> list[tuple[str, bool, str]]:
    """Check which files exist and their rough state."""
    files = [
        ("MANIFEST.md", "orientation"),
        ("THINK.md", "interrupts"),
        ("REFLECT.md", "feedback loop"),
        ("CALIBRATE.md", "confidence tracking"),
        ("REASON.md", "reasoning methods"),
        ("WARMUP.md", "session bootstrap"),
        ("PORTFOLIO-THESIS.md", "portfolio analysis"),
    ]
    return [(name, (base / name).exists(), desc) for name, desc in files]


def main():
    print()
    print("=" * 55)
    print("  MY UNIVERSE — System Health")
    print("=" * 55)

    # File check
    print()
    print("  FILES")
    print("  " + "-" * 50)
    health = file_health(BASE)
    for name, exists, desc in health:
        marker = "OK" if exists else "MISSING"
        print(f"  [{marker:>7}]  {name:<25} {desc}")

    # THINK.md traps
    trap_count = count_traps(BASE / "THINK.md")
    print()
    print(f"  THINK.md: {trap_count} named traps")

    # Calibration
    cal = calibration_summary(BASE / "CALIBRATE.md")
    print()
    print("  CALIBRATION")
    print("  " + "-" * 50)
    if cal["resolved"] > 0:
        gap = cal["avg_confidence"] - cal["accuracy"]
        direction = "overconfident" if gap > 5 else "underconfident" if gap < -5 else "calibrated"
        print(f"  Predictions:  {cal['total']} ({cal['resolved']} resolved, {cal['pending']} pending)")
        print(f"  Accuracy:     {cal['correct']}/{cal['resolved']} ({cal['accuracy']:.1f}%)")
        print(f"  Avg conf:     {cal['avg_confidence']:.1f}%")
        print(f"  Assessment:   {direction} (gap: {gap:+.1f}pts)")
    else:
        print(f"  Predictions:  {cal['total']} ({cal['pending']} pending)")
        print(f"  No resolved predictions yet.")

    # Reflection
    ref = reflection_summary(BASE / "REFLECT.md")
    print()
    print("  REFLECTION")
    print("  " + "-" * 50)
    print(f"  Entries:       {ref['total']}")
    print(f"  Useful:        {ref['useful']}")
    print(f"  Performative:  {ref['performative']}")
    print(f"  Missed:        {ref['missed']}")
    if ref["total"] > 0:
        useful_rate = ref["useful"] / ref["total"] * 100
        print(f"  Useful rate:   {useful_rate:.0f}%")

    # Needs attention
    print()
    print("  ATTENTION NEEDED")
    print("  " + "-" * 50)
    issues = []

    if cal["pending"] > 0:
        issues.append(f"  - {cal['pending']} calibration predictions pending verification")
    if cal["resolved"] > 5 and cal["accuracy"] < 60:
        issues.append(f"  - Calibration accuracy below 60% — review prediction approach")
    if ref["missed"] > ref["useful"]:
        issues.append("  - More missed than useful interrupts — triggers need strengthening")
    if ref["performative"] > ref["useful"]:
        issues.append("  - More performative than useful — interrupts not changing behavior")
    if ref["total"] == 0:
        issues.append("  - No reflection entries — start logging interrupt events")
    if cal["total"] == 0:
        issues.append("  - No calibration data — run the warmup protocol")

    missing_files = [name for name, exists, _ in health if not exists]
    if missing_files:
        issues.append(f"  - Missing files: {', '.join(missing_files)}")

    if not issues:
        issues.append("  - None. System healthy.")

    for issue in issues:
        print(issue)

    print()
    print("=" * 55)
    print()


if __name__ == "__main__":
    main()
