#!/usr/bin/env python3
"""
Session briefing generator for MY UNIVERSE.

Produces a compressed summary for new sessions: what's working,
what needs attention, calibration patterns, and recent reflections.
Designed to replace manually reading every file at session start.

Usage:
    python brief.py          # Generate brief
    python brief.py --short  # Ultra-short version (5 lines)
"""

import re
import sys
import argparse
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent

sys.path.insert(0, str(BASE))
from tools.calibrate import parse_entries as parse_cal, compute_calibration
from tools.reflect import parse_entries as parse_ref


def get_trap_count() -> int:
    """Count traps in THINK.md."""
    think = BASE / "THINK.md"
    if not think.exists():
        return 0
    text = think.read_text()
    traps = re.findall(r"###\s+The\s+\w+.*?Trap", text)
    sub_traps = re.findall(r"\*\*The\s+\w+.*?trap", text, re.IGNORECASE)
    return len(traps) + len(sub_traps)


def get_session_count() -> int:
    """Count sessions from SESSION-LOG.md."""
    log = BASE / "SESSION-LOG.md"
    if not log.exists():
        return 0
    text = log.read_text()
    return len(re.findall(r"## Session \d+", text))


def generate_brief() -> str:
    """Generate a full session briefing."""
    lines = []
    lines.append("=" * 55)
    lines.append("  SESSION BRIEF — MY UNIVERSE")
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 55)

    # Calibration state
    cal_path = BASE / "CALIBRATE.md"
    if cal_path.exists():
        entries = parse_cal(cal_path)
        stats = compute_calibration(entries)
        lines.append("")
        lines.append("  CALIBRATION STATE")
        lines.append("  " + "-" * 45)
        if stats["resolved"] > 0:
            gap = stats["avg_confidence"] - stats["actual_accuracy"]
            direction = "overconfident" if gap > 3 else "underconfident" if gap < -3 else "calibrated"
            lines.append(f"  {stats['resolved']} predictions: {stats['correct']} correct ({stats['actual_accuracy']:.0f}%)")
            lines.append(f"  Confidence: {stats['avg_confidence']:.0f}% → {direction} by {abs(gap):.0f}pts")

            # Domain weak spots
            if stats.get("domains"):
                worst = min(stats["domains"].items(),
                           key=lambda x: x[1]["correct"]/x[1]["total"] if x[1]["total"] > 0 else 1)
                if worst[1]["total"] >= 3:
                    acc = worst[1]["correct"] / worst[1]["total"] * 100
                    lines.append(f"  Weakest domain: {worst[0]} ({acc:.0f}%)")

            # Bucket warnings
            if stats.get("buckets"):
                for bucket, data in stats["buckets"].items():
                    if data["total"] >= 3:
                        actual = data["correct"] / data["total"] * 100
                        expected = bucket + 5
                        if expected - actual > 15:
                            lines.append(f"  WARNING: {bucket}-{bucket+9}% confidence zone overconfident by {expected-actual:.0f}pts")
        else:
            lines.append(f"  {stats['pending']} predictions pending. Run warmup.")

    # Reflection state
    ref_path = BASE / "REFLECT.md"
    if ref_path.exists():
        entries = parse_ref(ref_path)
        lines.append("")
        lines.append("  REFLECTION STATE")
        lines.append("  " + "-" * 45)
        lines.append(f"  {len(entries)} entries")

        useful = sum(1 for e in entries if e["verdict"] == "useful")
        missed = sum(1 for e in entries if e["verdict"] == "missed")
        perf = sum(1 for e in entries if e["verdict"] == "performative")
        lines.append(f"  Useful: {useful}  Missed: {missed}  Performative: {perf}")

        # Most recent entries
        if entries:
            recent = sorted(entries, key=lambda x: x["date"], reverse=True)[:3]
            lines.append("")
            lines.append("  Recent:")
            for e in recent:
                trap = e["trap"] or "general"
                verdict = e["verdict"]
                ctx = e["context"][:40] if e["context"] else ""
                marker = {"useful": "+", "missed": "!", "performative": "~"}.get(verdict, "?")
                lines.append(f"    [{marker}] {trap}: {ctx}")

    # Think state
    trap_count = get_trap_count()
    lines.append("")
    lines.append("  THINK.MD")
    lines.append("  " + "-" * 45)
    lines.append(f"  {trap_count} named traps")

    # Key findings
    findings_path = BASE / "FINDINGS.md"
    if findings_path.exists():
        lines.append("")
        lines.append("  KEY FINDINGS TO REMEMBER")
        lines.append("  " + "-" * 45)
        lines.append("  1. 70-79% confidence is overconfident — verify in this zone")
        lines.append("  2. Architecture: reason from specifics, not categories")
        lines.append("  3. Behavior: use ranges, not point estimates")
        lines.append("  4. High confidence (80%+) is reliable — trust it")
        lines.append("  5. Low confidence (50-59%) is underconfident — trust yourself more")

    # Action items
    lines.append("")
    lines.append("  SESSION PRIORITIES")
    lines.append("  " + "-" * 45)
    lines.append("  1. Run WARMUP.md (orient → calibrate → interrupt)")
    lines.append("  2. If working on a project: use THINK.md actively")
    lines.append("  3. Log calibration predictions throughout the session")
    lines.append("  4. Update REFLECT.md at session end")

    lines.append("")
    lines.append("=" * 55)
    return "\n".join(lines)


def generate_short() -> str:
    """Ultra-short brief (5 lines)."""
    cal_path = BASE / "CALIBRATE.md"
    ref_path = BASE / "REFLECT.md"

    cal_summary = "no data"
    if cal_path.exists():
        entries = parse_cal(cal_path)
        stats = compute_calibration(entries)
        if stats["resolved"] > 0:
            cal_summary = f"{stats['correct']}/{stats['resolved']} ({stats['actual_accuracy']:.0f}%)"

    ref_count = 0
    if ref_path.exists():
        ref_count = len(parse_ref(ref_path))

    trap_count = get_trap_count()
    sessions = get_session_count()

    lines = [
        f"MY UNIVERSE | Session {sessions+1}",
        f"Calibration: {cal_summary} | {trap_count} traps | {ref_count} reflections",
        f"Weakest: behavior domain, 70-79% confidence zone",
        f"Remember: ranges not points, specifics not categories, verify at 60-79%",
        f"Start: run WARMUP.md",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Session briefing generator")
    parser.add_argument("--short", action="store_true", help="Ultra-short brief")
    args = parser.parse_args()

    if args.short:
        print(generate_short())
    else:
        print(generate_brief())


if __name__ == "__main__":
    main()
