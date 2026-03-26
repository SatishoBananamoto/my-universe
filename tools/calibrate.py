#!/usr/bin/env python3
"""
Calibration analyzer for MY UNIVERSE.

Parses CALIBRATE.md, computes calibration scores, and identifies
over/underconfidence patterns by domain.

Usage:
    python calibrate.py                    # Full report
    python calibrate.py --domain codebase  # Filter by domain
    python calibrate.py --summary          # One-line summary
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict


CALIBRATE_PATH = Path(__file__).parent.parent / "CALIBRATE.md"

# Pattern to match entry blocks
ENTRY_PATTERN = re.compile(
    r"###\s+\[P-(\d+)\]\s+(\d{4}-\d{2}-\d{2})\s*—\s*(\S+)\s*\n+"
    r"\*\*Prediction:\*\*\s*(.*?)\n"
    r"\*\*Confidence:\*\*\s*(\d+)%\s*\n"
    r"(?:.*?\n)*?"  # tolerate optional extra fields (Source type, etc.)
    r"\*\*Actual:\*\*\s*(.*?)\n"
    r"\*\*Result:\*\*\s*(correct|incorrect|_pending_|pending)\s*",
    re.MULTILINE,
)


def parse_entries(path: Path) -> list[dict]:
    """Parse all entries from CALIBRATE.md."""
    text = path.read_text()
    entries = []
    for match in ENTRY_PATTERN.finditer(text):
        entry = {
            "id": f"P-{match.group(1)}",
            "date": match.group(2),
            "domain": match.group(3),
            "prediction": match.group(4).strip(),
            "confidence": max(50, min(99, int(match.group(5)))),
            "actual": match.group(6).strip(),
            "result": match.group(7).strip().strip("_"),
        }
        entries.append(entry)
    return entries


def compute_calibration(entries: list[dict]) -> dict:
    """Compute calibration metrics from resolved entries."""
    resolved = [e for e in entries if e["result"] in ("correct", "incorrect")]
    if not resolved:
        return {"total": len(entries), "resolved": 0, "pending": len(entries)}

    # Group by confidence bucket (10-point bins)
    buckets = defaultdict(lambda: {"correct": 0, "total": 0})
    for e in resolved:
        bucket = (e["confidence"] // 10) * 10  # 50, 60, 70, 80, 90
        buckets[bucket]["total"] += 1
        if e["result"] == "correct":
            buckets[bucket]["correct"] += 1

    # Domain breakdown
    domains = defaultdict(lambda: {"correct": 0, "total": 0})
    for e in resolved:
        domains[e["domain"]]["total"] += 1
        if e["result"] == "correct":
            domains[e["domain"]]["correct"] += 1

    # Overall stats
    total_correct = sum(1 for e in resolved if e["result"] == "correct")
    avg_confidence = sum(e["confidence"] for e in resolved) / len(resolved)
    actual_accuracy = total_correct / len(resolved) * 100

    # Calibration error: average |confidence - actual accuracy| per bucket
    cal_errors = []
    for bucket_val, stats in sorted(buckets.items()):
        if stats["total"] > 0:
            actual_rate = stats["correct"] / stats["total"] * 100
            cal_errors.append(abs(bucket_val + 5 - actual_rate))  # bucket midpoint

    avg_cal_error = sum(cal_errors) / len(cal_errors) if cal_errors else 0

    return {
        "total": len(entries),
        "resolved": len(resolved),
        "pending": len(entries) - len(resolved),
        "correct": total_correct,
        "incorrect": len(resolved) - total_correct,
        "avg_confidence": avg_confidence,
        "actual_accuracy": actual_accuracy,
        "calibration_error": avg_cal_error,
        "buckets": dict(sorted(buckets.items())),
        "domains": dict(sorted(domains.items())),
    }


def format_report(stats: dict, domain_filter: str = None) -> str:
    """Format calibration stats into a readable report."""
    lines = []
    lines.append("=" * 50)
    lines.append("  CALIBRATION REPORT")
    lines.append("=" * 50)

    if stats["resolved"] == 0:
        lines.append("")
        lines.append(f"  Total predictions: {stats.get('total', stats.get('pending', 0))}")
        lines.append(f"  Resolved: 0")
        lines.append(f"  Pending: {stats.get('pending', stats.get('total', 0))}")
        lines.append("")
        lines.append("  No resolved predictions yet.")
        lines.append("  Verify pending predictions to generate calibration data.")
        lines.append("")
        return "\n".join(lines)

    lines.append("")
    lines.append(f"  Total predictions:  {stats['total']}")
    lines.append(f"  Resolved:           {stats['resolved']}")
    lines.append(f"  Pending:            {stats['pending']}")
    lines.append(f"  Correct:            {stats['correct']}")
    lines.append(f"  Incorrect:          {stats['incorrect']}")
    lines.append("")
    lines.append(f"  Avg confidence:     {stats['avg_confidence']:.1f}%")
    lines.append(f"  Actual accuracy:    {stats['actual_accuracy']:.1f}%")
    lines.append(f"  Calibration error:  {stats['calibration_error']:.1f}%")
    lines.append("")

    # Interpretation
    gap = stats["avg_confidence"] - stats["actual_accuracy"]
    if abs(gap) < 5:
        lines.append("  Assessment: WELL CALIBRATED")
    elif gap > 0:
        lines.append(f"  Assessment: OVERCONFIDENT by ~{gap:.0f} points")
    else:
        lines.append(f"  Assessment: UNDERCONFIDENT by ~{abs(gap):.0f} points")

    # Bucket breakdown
    if stats.get("buckets"):
        lines.append("")
        lines.append("-" * 50)
        lines.append("  CONFIDENCE BUCKETS")
        lines.append("-" * 50)
        lines.append("")
        lines.append("  Confidence  | Correct | Total | Actual %  | Gap")
        lines.append("  ------------|---------|-------|-----------|------")
        for bucket, data in stats["buckets"].items():
            actual_pct = data["correct"] / data["total"] * 100 if data["total"] else 0
            expected = bucket + 5  # midpoint
            gap = expected - actual_pct
            direction = "over" if gap > 0 else "under" if gap < 0 else "="
            lines.append(
                f"  {bucket}-{bucket+9}%      "
                f"| {data['correct']:>5}   "
                f"| {data['total']:>3}   "
                f"| {actual_pct:>7.1f}%  "
                f"| {gap:+.0f} ({direction})"
            )

    # Domain breakdown
    if stats.get("domains"):
        lines.append("")
        lines.append("-" * 50)
        lines.append("  DOMAIN BREAKDOWN")
        lines.append("-" * 50)
        lines.append("")
        for domain, data in stats["domains"].items():
            if domain_filter and domain != domain_filter:
                continue
            pct = data["correct"] / data["total"] * 100 if data["total"] else 0
            lines.append(f"  {domain:<15} {data['correct']}/{data['total']} ({pct:.0f}%)")

    lines.append("")
    lines.append("=" * 50)
    return "\n".join(lines)


def format_summary(stats: dict) -> str:
    """One-line summary for quick checks."""
    if stats["resolved"] == 0:
        return f"Calibration: {stats.get('pending', 0)} predictions pending, none resolved yet."
    gap = stats["avg_confidence"] - stats["actual_accuracy"]
    direction = "overconfident" if gap > 0 else "underconfident" if gap < 0 else "calibrated"
    return (
        f"Calibration: {stats['correct']}/{stats['resolved']} correct "
        f"(avg conf: {stats['avg_confidence']:.0f}%, actual: {stats['actual_accuracy']:.0f}%, "
        f"{direction} by {abs(gap):.0f}pts) | {stats['pending']} pending"
    )


def main():
    parser = argparse.ArgumentParser(description="Calibration analyzer for MY UNIVERSE")
    parser.add_argument("--domain", help="Filter by domain tag")
    parser.add_argument("--summary", action="store_true", help="One-line summary")
    parser.add_argument("--file", type=Path, default=CALIBRATE_PATH, help="Path to CALIBRATE.md")
    args = parser.parse_args()

    if not args.file.exists():
        print(f"Error: {args.file} not found", file=sys.stderr)
        sys.exit(1)

    entries = parse_entries(args.file)

    if args.domain:
        entries = [e for e in entries if e["domain"] == args.domain]

    stats = compute_calibration(entries)

    if args.summary:
        print(format_summary(stats))
    else:
        print(format_report(stats, domain_filter=args.domain))


if __name__ == "__main__":
    main()
