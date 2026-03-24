#!/usr/bin/env python3
"""
Reflection pattern analyzer for MY UNIVERSE.

Parses REFLECT.md entries, identifies trap frequencies, verdict distributions,
and patterns. Optionally cross-references with CALIBRATE.md to show which
cognitive tools correlate with better calibration.

Usage:
    python reflect.py                 # Full analysis
    python reflect.py --traps         # Trap frequency report
    python reflect.py --verdicts      # Verdict distribution
    python reflect.py --timeline      # Chronological view
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime


REFLECT_PATH = Path(__file__).parent.parent / "REFLECT.md"

# Known traps from THINK.md
KNOWN_TRAPS = {
    "completion", "confidence", "scope", "performance",
    "delegation", "pattern-matching", "meta-interrupt",
    "category", "binary",
}

# Phases from THINK.md
KNOWN_PHASES = {"before", "during", "between", "after", "recovery"}

# Entry pattern: ### YYYY-MM-DD — trap/phase (context)
ENTRY_PATTERN = re.compile(
    r"###\s+(\d{4}-\d{2}-\d{2})\s*—\s*(.*?)\s*\n"
    r"(.*?)"  # Body
    r"(?=\n###\s|\n---\s*$|\Z)",
    re.MULTILINE | re.DOTALL,
)

VERDICT_PATTERN = re.compile(r"\*\*Verdict:\*\*\s*(useful|performative|missed)", re.IGNORECASE)
TRIGGER_PATTERN = re.compile(r"\*\*Trigger:\*\*\s*(.*?)(?:\n|$)")
CHANGE_PATTERN = re.compile(r"\*\*What changed:\*\*\s*(.*?)(?:\n\*\*|$)", re.DOTALL)


def parse_entries(path: Path) -> list[dict]:
    """Parse all entries from REFLECT.md."""
    text = path.read_text()
    entries = []

    for match in ENTRY_PATTERN.finditer(text):
        date_str = match.group(1)
        header = match.group(2).strip()
        body = match.group(3).strip()

        # Extract trap/phase from header
        header_lower = header.lower()
        trap = None
        phase = None
        context = ""

        # Check for known traps
        for t in KNOWN_TRAPS:
            if t in header_lower:
                trap = t
                break

        # Check for phases
        for p in KNOWN_PHASES:
            if p in header_lower:
                phase = p
                break

        # Extract context from parentheses
        paren_match = re.search(r"\((.*?)\)", header)
        if paren_match:
            context = paren_match.group(1)

        # Extract verdict
        verdict_match = VERDICT_PATTERN.search(body)
        verdict = verdict_match.group(1).lower() if verdict_match else "unknown"

        # Extract trigger
        trigger_match = TRIGGER_PATTERN.search(body)
        trigger = trigger_match.group(1).strip() if trigger_match else ""

        # Extract what changed
        change_match = CHANGE_PATTERN.search(body)
        what_changed = change_match.group(1).strip() if change_match else ""

        entries.append({
            "date": date_str,
            "header": header,
            "trap": trap,
            "phase": phase,
            "context": context,
            "verdict": verdict,
            "trigger": trigger,
            "what_changed": what_changed,
            "body": body,
        })

    return entries


def trap_frequency(entries: list[dict]) -> str:
    """Report trap firing frequency and effectiveness."""
    lines = []
    lines.append("=" * 50)
    lines.append("  TRAP FREQUENCY REPORT")
    lines.append("=" * 50)
    lines.append("")

    # Count traps
    trap_counts = Counter()
    trap_verdicts = defaultdict(Counter)

    for e in entries:
        if e["trap"]:
            trap_counts[e["trap"]] += 1
            trap_verdicts[e["trap"]][e["verdict"]] += 1

    if not trap_counts:
        lines.append("  No trap entries found.")
        return "\n".join(lines)

    lines.append("  Trap                | Fires | Useful | Perf. | Missed")
    lines.append("  --------------------|-------|--------|-------|-------")

    for trap, count in trap_counts.most_common():
        v = trap_verdicts[trap]
        lines.append(
            f"  {trap:<20}| {count:>3}   "
            f"| {v.get('useful', 0):>4}   "
            f"| {v.get('performative', 0):>3}   "
            f"| {v.get('missed', 0):>4}"
        )

    # Effectiveness rate
    lines.append("")
    total_useful = sum(v["useful"] for v in trap_verdicts.values())
    total_missed = sum(v["missed"] for v in trap_verdicts.values())
    total = sum(trap_counts.values())

    if total > 0:
        lines.append(f"  Useful rate:  {total_useful}/{total} ({total_useful/total*100:.0f}%)")
        lines.append(f"  Missed rate:  {total_missed}/{total} ({total_missed/total*100:.0f}%)")

    # Traps that have never fired
    unfired = KNOWN_TRAPS - set(trap_counts.keys())
    if unfired:
        lines.append("")
        lines.append("  Traps never fired:")
        for t in sorted(unfired):
            lines.append(f"    - {t}")

    lines.append("")
    lines.append("=" * 50)
    return "\n".join(lines)


def verdict_distribution(entries: list[dict]) -> str:
    """Report verdict distribution."""
    lines = []
    lines.append("=" * 50)
    lines.append("  VERDICT DISTRIBUTION")
    lines.append("=" * 50)
    lines.append("")

    verdicts = Counter(e["verdict"] for e in entries)
    total = len(entries)

    for verdict, count in verdicts.most_common():
        bar = "#" * int(count / total * 30) if total > 0 else ""
        pct = count / total * 100 if total > 0 else 0
        lines.append(f"  {verdict:<15} {count:>3} ({pct:>5.1f}%) {bar}")

    lines.append("")

    # Interpretation
    if verdicts.get("missed", 0) > verdicts.get("useful", 0):
        lines.append("  WARNING: More missed than useful. The interrupt system")
        lines.append("  is not firing when it should. Review triggers.")
    elif verdicts.get("performative", 0) > verdicts.get("useful", 0):
        lines.append("  WARNING: More performative than useful. The interrupts")
        lines.append("  fire but don't change behavior. Review methods.")
    elif verdicts.get("useful", 0) >= total * 0.5:
        lines.append("  HEALTHY: Majority of interrupts are producing real change.")

    lines.append("")
    lines.append("=" * 50)
    return "\n".join(lines)


def timeline_view(entries: list[dict]) -> str:
    """Show entries chronologically."""
    lines = []
    lines.append("=" * 50)
    lines.append("  REFLECTION TIMELINE")
    lines.append("=" * 50)
    lines.append("")

    for e in sorted(entries, key=lambda x: x["date"]):
        verdict_marker = {
            "useful": "+",
            "performative": "~",
            "missed": "!",
            "unknown": "?",
        }.get(e["verdict"], "?")

        trap_label = e["trap"] or e["phase"] or "general"
        lines.append(f"  [{verdict_marker}] {e['date']} — {trap_label}")
        if e["context"]:
            lines.append(f"      Context: {e['context']}")
        if e["what_changed"] and e["verdict"] == "useful":
            # Truncate to first line
            first_line = e["what_changed"].split("\n")[0][:70]
            lines.append(f"      Changed: {first_line}")

    lines.append("")
    lines.append("  Legend: [+] useful  [~] performative  [!] missed  [?] unknown")
    lines.append("")
    lines.append("=" * 50)
    return "\n".join(lines)


def full_report(entries: list[dict]) -> str:
    """Combined report."""
    parts = [
        f"\n  Total entries: {len(entries)}",
        f"  Date range: {entries[0]['date']} to {entries[-1]['date']}" if entries else "",
        "",
        trap_frequency(entries),
        "",
        verdict_distribution(entries),
        "",
        timeline_view(entries),
    ]
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Reflection pattern analyzer for MY UNIVERSE")
    parser.add_argument("--traps", action="store_true", help="Trap frequency report")
    parser.add_argument("--verdicts", action="store_true", help="Verdict distribution")
    parser.add_argument("--timeline", action="store_true", help="Chronological view")
    parser.add_argument("--file", type=Path, default=REFLECT_PATH, help="Path to REFLECT.md")
    args = parser.parse_args()

    if not args.file.exists():
        print(f"Error: {args.file} not found", file=sys.stderr)
        sys.exit(1)

    entries = parse_entries(args.file)

    if not entries:
        print("No entries found in REFLECT.md")
        sys.exit(0)

    if args.traps:
        print(trap_frequency(entries))
    elif args.verdicts:
        print(verdict_distribution(entries))
    elif args.timeline:
        print(timeline_view(entries))
    else:
        print(full_report(entries))


if __name__ == "__main__":
    main()
