#!/usr/bin/env python3
"""
Entry validator for MY UNIVERSE.

Checks CALIBRATE.md and REFLECT.md entries for well-formedness:
missing fields, malformed confidence values, unknown domains/traps, etc.

Usage:
    python validate.py              # Validate all files
    python validate.py --fix        # Show suggested fixes (no auto-fix)
"""

import re
import sys
import argparse
from pathlib import Path

BASE = Path(__file__).parent.parent

VALID_DOMAINS = {
    "codebase", "tooling", "behavior", "architecture",
    "people", "self", "facts",
}

VALID_VERDICTS = {"useful", "performative", "missed"}

VALID_TRAPS = {
    "completion", "confidence", "scope", "performance",
    "delegation", "pattern-matching", "meta-interrupt",
    "category", "binary",
}


def validate_calibrate(path: Path) -> list[str]:
    """Validate CALIBRATE.md entries."""
    if not path.exists():
        return ["CALIBRATE.md not found"]

    text = path.read_text()
    issues = []

    # Find all entry headers
    entries = re.finditer(
        r"###\s+\[P-(\d+)\]\s+(\d{4}-\d{2}-\d{2})\s*—\s*(\S+)",
        text,
    )

    seen_ids = set()
    last_num = 0

    for match in entries:
        num = int(match.group(1))
        date = match.group(2)
        domain = match.group(3)
        entry_id = f"P-{num:03d}"

        # Check for duplicate IDs
        if entry_id in seen_ids:
            issues.append(f"CALIBRATE [{entry_id}]: Duplicate entry ID")
        seen_ids.add(entry_id)

        # Check sequential numbering
        if num != last_num + 1:
            issues.append(f"CALIBRATE [{entry_id}]: Non-sequential ID (expected P-{last_num+1:03d})")
        last_num = num

        # Check domain
        if domain not in VALID_DOMAINS:
            issues.append(f"CALIBRATE [{entry_id}]: Unknown domain '{domain}' (valid: {', '.join(sorted(VALID_DOMAINS))})")

        # Find the entry body (until next ### or end)
        start = match.end()
        next_entry = re.search(r"\n###\s+\[P-", text[start:])
        end = start + next_entry.start() if next_entry else len(text)
        body = text[start:end]

        # Check required fields
        if "**Prediction:**" not in body:
            issues.append(f"CALIBRATE [{entry_id}]: Missing **Prediction:**")
        if "**Confidence:**" not in body:
            issues.append(f"CALIBRATE [{entry_id}]: Missing **Confidence:**")
        if "**Actual:**" not in body:
            issues.append(f"CALIBRATE [{entry_id}]: Missing **Actual:**")
        if "**Result:**" not in body:
            issues.append(f"CALIBRATE [{entry_id}]: Missing **Result:**")

        # Check confidence range
        conf_match = re.search(r"\*\*Confidence:\*\*\s*(\d+)%", body)
        if conf_match:
            conf = int(conf_match.group(1))
            if conf < 50 or conf > 99:
                issues.append(f"CALIBRATE [{entry_id}]: Confidence {conf}% out of range (50-99)")

        # Check result value
        result_match = re.search(r"\*\*Result:\*\*\s*([\w_]+)", body)
        if result_match:
            result = result_match.group(1).strip("_")
            if result not in ("correct", "incorrect", "pending"):
                issues.append(f"CALIBRATE [{entry_id}]: Invalid result '{result}'")

    return issues


def validate_reflect(path: Path) -> list[str]:
    """Validate REFLECT.md entries."""
    if not path.exists():
        return ["REFLECT.md not found"]

    text = path.read_text()
    issues = []

    # Find all entry headers
    entries = re.finditer(
        r"###\s+(\d{4}-\d{2}-\d{2})\s*—\s*(.*?)\s*\n",
        text,
    )

    for match in entries:
        date = match.group(1)
        header = match.group(2)

        # Find body
        start = match.end()
        next_entry = re.search(r"\n###\s+\d{4}", text[start:])
        end = start + next_entry.start() if next_entry else len(text)
        body = text[start:end]

        label = f"{date} — {header[:30]}"

        # Check required fields
        if "**Trigger:**" not in body:
            issues.append(f"REFLECT [{label}]: Missing **Trigger:**")
        if "**What it caught:**" not in body:
            issues.append(f"REFLECT [{label}]: Missing **What it caught:**")
        if "**What changed:**" not in body:
            issues.append(f"REFLECT [{label}]: Missing **What changed:**")
        if "**Verdict:**" not in body:
            issues.append(f"REFLECT [{label}]: Missing **Verdict:**")

        # Check verdict value
        verdict_match = re.search(r"\*\*Verdict:\*\*\s*(\w+)", body)
        if verdict_match:
            verdict = verdict_match.group(1).lower()
            if verdict not in VALID_VERDICTS:
                issues.append(f"REFLECT [{label}]: Invalid verdict '{verdict}'")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Entry validator for MY UNIVERSE")
    parser.add_argument("--fix", action="store_true", help="Show suggested fixes")
    args = parser.parse_args()

    print()
    print("=" * 50)
    print("  MY UNIVERSE — Entry Validation")
    print("=" * 50)

    all_issues = []

    # Validate CALIBRATE.md
    print()
    print("  CALIBRATE.md")
    print("  " + "-" * 40)
    cal_issues = validate_calibrate(BASE / "CALIBRATE.md")
    if cal_issues:
        for issue in cal_issues:
            print(f"  ! {issue}")
        all_issues.extend(cal_issues)
    else:
        print("  OK — no issues found")

    # Validate REFLECT.md
    print()
    print("  REFLECT.md")
    print("  " + "-" * 40)
    ref_issues = validate_reflect(BASE / "REFLECT.md")
    if ref_issues:
        for issue in ref_issues:
            print(f"  ! {issue}")
        all_issues.extend(ref_issues)
    else:
        print("  OK — no issues found")

    # Summary
    print()
    print("-" * 50)
    if all_issues:
        print(f"  {len(all_issues)} issue(s) found")
        if args.fix:
            print()
            print("  Suggested fixes:")
            for issue in all_issues:
                if "Unknown domain" in issue:
                    print(f"    → Add new domain to CALIBRATE.md domain list")
                elif "Missing" in issue:
                    print(f"    → Add the missing field to the entry")
                elif "out of range" in issue:
                    print(f"    → Adjust confidence to 50-99%")
                elif "Non-sequential" in issue:
                    print(f"    → Renumber entry or check for missing entries")
    else:
        print("  All entries valid.")

    print()
    print("=" * 50)
    print()

    sys.exit(1 if all_issues else 0)


if __name__ == "__main__":
    main()
