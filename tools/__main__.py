#!/usr/bin/env python3
"""
MY UNIVERSE CLI — single entry point for all tools.

Usage:
    python -m tools <command> [args]
    python -m tools status
    python -m tools brief --short
    python -m tools calibrate --domain behavior
    python -m tools reflect --traps
    python -m tools validate
    python -m tools portfolio --quick
    python -m tools changelog --days 7
    python -m tools audit /path/to/project
    python -m tools generate /path/to/project
    python -m tools next
    python -m tools test
"""

import sys
import subprocess
from pathlib import Path

TOOLS_DIR = Path(__file__).parent

COMMANDS = {
    "status": "status.py",
    "brief": "brief.py",
    "calibrate": "calibrate.py",
    "reflect": "reflect.py",
    "validate": "validate.py",
    "portfolio": "portfolio.py",
    "changelog": "changelog.py",
    "audit": "audit_claude_md.py",
    "generate": "gen_claude_md.py",
    "next": "next.py",
}


def print_help():
    print()
    print("MY UNIVERSE — Cognitive Toolkit")
    print()
    print("Usage: python -m tools <command> [args]")
    print()
    print("Commands:")
    print("  status      System health dashboard")
    print("  brief       Session briefing (--short for 5 lines)")
    print("  calibrate   Calibration analysis (--domain X, --summary)")
    print("  reflect     Reflection patterns (--traps, --verdicts, --timeline)")
    print("  validate    Validate entry formats")
    print("  portfolio   Cross-project health (--quick)")
    print("  changelog   Recent activity (--days N)")
    print("  audit       Audit a CLAUDE.md file")
    print("  generate    Generate CLAUDE.md from codebase")
    print("  next        What to work on next")
    print("  test        Run the test suite")
    print()


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print_help()
        sys.exit(0)

    command = sys.argv[1]

    if command == "test":
        test_runner = TOOLS_DIR.parent / "tests" / "run_all.py"
        result = subprocess.run([sys.executable, str(test_runner)])
        sys.exit(result.returncode)

    if command not in COMMANDS:
        print(f"Unknown command: {command}")
        print(f"Available: {', '.join(sorted(COMMANDS.keys()))}, test")
        sys.exit(1)

    script = TOOLS_DIR / COMMANDS[command]
    result = subprocess.run(
        [sys.executable, str(script)] + sys.argv[2:]
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
