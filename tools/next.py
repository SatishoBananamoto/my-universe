#!/usr/bin/env python3
"""
Suggests what to work on next based on MY UNIVERSE state.

Reads all artifacts and recommends the highest-value next action.
Not a planner — a signal aggregator.

Usage:
    python next.py
"""

import re
import sys
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent
sys.path.insert(0, str(BASE))

from tools.calibrate import parse_entries as parse_cal, compute_calibration
from tools.reflect import parse_entries as parse_ref


def get_pending_predictions() -> int:
    """Count pending calibration predictions."""
    cal = BASE / "CALIBRATE.md"
    if not cal.exists():
        return 0
    text = cal.read_text()
    return len(re.findall(r"\*\*Result:\*\*\s*_pending", text))


def get_weakest_domain(stats: dict) -> tuple[str, float] | None:
    """Find the weakest calibration domain with enough data."""
    if not stats.get("domains"):
        return None
    candidates = [
        (domain, data["correct"] / data["total"] * 100)
        for domain, data in stats["domains"].items()
        if data["total"] >= 3
    ]
    if not candidates:
        return None
    return min(candidates, key=lambda x: x[1])


def get_overconfident_bucket(stats: dict) -> tuple[int, float] | None:
    """Find the most overconfident confidence bucket."""
    if not stats.get("buckets"):
        return None
    worst = None
    worst_gap = 0
    for bucket, data in stats["buckets"].items():
        if data["total"] >= 3:
            actual = data["correct"] / data["total"] * 100
            expected = bucket + 5  # midpoint
            gap = expected - actual
            if gap > worst_gap:
                worst_gap = gap
                worst = (bucket, gap)
    return worst


def get_missed_count(entries: list[dict]) -> int:
    """Count missed interrupts."""
    return sum(1 for e in entries if e["verdict"] == "missed")


def get_unfired_traps(entries: list[dict]) -> set[str]:
    """Find traps that have never fired."""
    known = {"completion", "confidence", "scope", "performance",
             "delegation", "pattern-matching", "meta-interrupt",
             "category", "binary"}
    fired = {e["trap"] for e in entries if e["trap"]}
    return known - fired


def suggest_actions() -> list[str]:
    """Generate prioritized action suggestions."""
    actions = []

    # Check pending predictions
    pending = get_pending_predictions()
    if pending > 0:
        actions.append(f"Verify {pending} pending calibration prediction(s)")

    # Check calibration state
    cal_path = BASE / "CALIBRATE.md"
    if cal_path.exists():
        entries = parse_cal(cal_path)
        stats = compute_calibration(entries)

        if stats["resolved"] < 10:
            actions.append("Make more calibration predictions (need 10+ for reliable patterns)")

        weakest = get_weakest_domain(stats)
        if weakest and weakest[1] < 60:
            actions.append(f"Practice {weakest[0]} predictions ({weakest[1]:.0f}% accuracy — weakest domain)")

        bucket = get_overconfident_bucket(stats)
        if bucket and bucket[1] > 10:
            actions.append(f"Be careful at {bucket[0]}-{bucket[0]+9}% confidence (overconfident by {bucket[1]:.0f}pts)")

    # Check reflection state
    ref_path = BASE / "REFLECT.md"
    if ref_path.exists():
        ref_entries = parse_ref(ref_path)
        missed = get_missed_count(ref_entries)
        if missed > len(ref_entries) * 0.3:
            actions.append("Too many missed interrupts — review THINK.md triggers")

        unfired = get_unfired_traps(ref_entries)
        if unfired:
            actions.append(f"Traps never tested: {', '.join(sorted(unfired))}")

    # Check if warmup needed
    actions.append("If new session: run WARMUP.md protocol")

    # Default always-useful action
    if not any("project work" in a.lower() for a in actions):
        actions.append("Use MY UNIVERSE on real project work (not self-referential building)")

    return actions


def main():
    print()
    print("=" * 55)
    print("  WHAT TO DO NEXT")
    print("=" * 55)
    print()

    actions = suggest_actions()
    for i, action in enumerate(actions, 1):
        print(f"  {i}. {action}")

    print()
    print("-" * 55)
    print("  Pick one. Do it. Reflect on it.")
    print("=" * 55)
    print()


if __name__ == "__main__":
    main()
