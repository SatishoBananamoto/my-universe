#!/usr/bin/env python3
"""
Portfolio health checker for Satish's developer tools.

Read-only scan of all projects: existence, git state, test count,
recent activity, and package metadata. Does NOT modify anything.

Usage:
    python portfolio.py              # Full report
    python portfolio.py --quick      # Just existence and git state
    python portfolio.py --project X  # Single project deep dive
"""

import subprocess
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime, timezone


HOME = Path.home()

# Project registry
PROJECTS = {
    "engram": {
        "path": HOME / "engram",
        "description": "Structured knowledge system",
        "type": "mcp-server",
    },
    "scroll": {
        "path": HOME / "scroll",
        "description": "Institutional memory from git history",
        "type": "cli-tool",
    },
    "svx": {
        "path": HOME / "svx",
        "description": "Safety layer for coding agents",
        "type": "cli-and-mcp",
    },
    "vigil": {
        "path": HOME / "vigil",
        "description": "Predictive risk intelligence",
        "type": "cli-tool",
        "pypi": "vigil-risk",
    },
    "kv-secrets": {
        "path": HOME / "kv-secrets",
        "description": "Encrypted secrets management",
        "type": "mcp-server",
        "pypi": "kv-secrets",
    },
    "caliber": {
        "path": HOME / "caliber",
        "description": "Trust protocol for AI agents",
        "type": "cli-and-mcp",
        "pypi": "caliber-trust",
    },
    "probe": {
        "path": HOME / "probe",
        "description": "MCP server security scanner",
        "type": "cli-tool",
        "pypi": "mcp-probe",
    },
}


def run_cmd(cmd: list[str], cwd: Path, timeout: int = 10) -> tuple[bool, str]:
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=cwd, timeout=timeout
        )
        return result.returncode == 0, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "timeout"
    except FileNotFoundError:
        return False, "command not found"


def check_exists(project: dict) -> bool:
    """Check if project directory exists."""
    return project["path"].exists()


def check_git_state(path: Path) -> dict:
    """Check git repository state."""
    if not (path / ".git").exists():
        return {"is_repo": False}

    # Current branch
    ok, branch = run_cmd(["git", "branch", "--show-current"], path)
    if not ok:
        branch = "unknown"

    # Clean working tree?
    ok, status = run_cmd(["git", "status", "--porcelain"], path)
    clean = ok and status == ""

    # Last commit date
    ok, date_str = run_cmd(
        ["git", "log", "-1", "--format=%ci"], path
    )
    last_commit = date_str if ok else "unknown"

    # Last commit message
    ok, msg = run_cmd(
        ["git", "log", "-1", "--format=%s"], path
    )
    last_message = msg[:60] if ok else "unknown"

    # Commit count
    ok, count_str = run_cmd(
        ["git", "rev-list", "--count", "HEAD"], path
    )
    commit_count = int(count_str) if ok and count_str.isdigit() else 0

    # Days since last commit
    days_since = None
    if ok and date_str != "unknown":
        try:
            # Parse git date format: 2026-03-24 05:00:00 -0000
            last_dt = datetime.strptime(date_str[:19], "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            days_since = (now - last_dt).days
        except ValueError:
            pass

    return {
        "is_repo": True,
        "branch": branch,
        "clean": clean,
        "last_commit": last_commit,
        "last_message": last_message,
        "commit_count": commit_count,
        "days_since": days_since,
    }


def check_tests(path: Path) -> dict:
    """Count test files and optionally check test count."""
    test_files = list(path.rglob("test_*.py")) + list(path.rglob("*_test.py"))
    # Exclude __pycache__ and .venv
    test_files = [
        f for f in test_files
        if "__pycache__" not in str(f) and ".venv" not in str(f)
    ]

    # Count test functions
    test_count = 0
    for tf in test_files:
        try:
            content = tf.read_text()
            test_count += len(re.findall(r"def test_", content))
        except (OSError, UnicodeDecodeError):
            pass

    return {
        "test_files": len(test_files),
        "test_functions": test_count,
    }


def check_package(path: Path) -> dict:
    """Check pyproject.toml for metadata."""
    pyproject = path / "pyproject.toml"
    if not pyproject.exists():
        return {"has_pyproject": False}

    try:
        content = pyproject.read_text()
    except OSError:
        return {"has_pyproject": False}

    # Extract version
    version_match = re.search(r'version\s*=\s*"([^"]+)"', content)
    version = version_match.group(1) if version_match else "unknown"

    # Extract description
    desc_match = re.search(r'description\s*=\s*"([^"]+)"', content)
    description = desc_match.group(1) if desc_match else ""

    # Count dependencies
    deps_section = re.search(r'dependencies\s*=\s*\[([^\]]*)\]', content, re.DOTALL)
    dep_count = 0
    if deps_section:
        dep_count = len([d for d in deps_section.group(1).split("\n") if d.strip().strip('",').strip()])

    return {
        "has_pyproject": True,
        "version": version,
        "description": description,
        "dep_count": dep_count,
    }


def check_source(path: Path) -> dict:
    """Count source files and lines."""
    py_files = list(path.rglob("*.py"))
    py_files = [
        f for f in py_files
        if "__pycache__" not in str(f)
        and ".venv" not in str(f)
        and "test" not in f.name.lower()
    ]

    total_lines = 0
    for f in py_files:
        try:
            total_lines += len(f.read_text().splitlines())
        except (OSError, UnicodeDecodeError):
            pass

    return {
        "source_files": len(py_files),
        "source_lines": total_lines,
    }


def format_quick(name: str, project: dict) -> str:
    """Quick one-line status."""
    if not check_exists(project):
        return f"  {name:<15} MISSING"

    git = check_git_state(project["path"])
    if not git["is_repo"]:
        return f"  {name:<15} exists (not a git repo)"

    clean_marker = "clean" if git["clean"] else "DIRTY"
    days = f"{git['days_since']}d ago" if git["days_since"] is not None else "?"
    return f"  {name:<15} {git['branch']:<10} {clean_marker:<8} {days:<10} {git['commit_count']} commits"


def format_full(name: str, project: dict) -> str:
    """Full project report."""
    lines = []
    lines.append(f"  {'=' * 50}")
    lines.append(f"  {name.upper()} — {project['description']}")
    lines.append(f"  Type: {project['type']}")
    lines.append(f"  Path: {project['path']}")
    lines.append(f"  {'=' * 50}")

    if not check_exists(project):
        lines.append("  STATUS: MISSING")
        return "\n".join(lines)

    # Git
    git = check_git_state(project["path"])
    lines.append("")
    lines.append("  GIT")
    if git["is_repo"]:
        clean = "clean" if git["clean"] else "UNCOMMITTED CHANGES"
        lines.append(f"    Branch:     {git['branch']}")
        lines.append(f"    State:      {clean}")
        lines.append(f"    Commits:    {git['commit_count']}")
        if git["days_since"] is not None:
            freshness = "fresh" if git["days_since"] <= 7 else "stale" if git["days_since"] > 30 else "recent"
            lines.append(f"    Last commit: {git['days_since']} days ago ({freshness})")
        lines.append(f"    Message:    {git['last_message']}")
    else:
        lines.append("    Not a git repository")

    # Package
    pkg = check_package(project["path"])
    lines.append("")
    lines.append("  PACKAGE")
    if pkg["has_pyproject"]:
        lines.append(f"    Version:    {pkg['version']}")
        lines.append(f"    Deps:       {pkg['dep_count']}")
        if pkg["description"]:
            lines.append(f"    Desc:       {pkg['description'][:60]}")
    else:
        lines.append("    No pyproject.toml")

    # Source
    src = check_source(project["path"])
    lines.append("")
    lines.append("  SOURCE")
    lines.append(f"    Files:      {src['source_files']}")
    lines.append(f"    Lines:      {src['source_lines']}")

    # Tests
    tests = check_tests(project["path"])
    lines.append("")
    lines.append("  TESTS")
    lines.append(f"    Files:      {tests['test_files']}")
    lines.append(f"    Functions:  {tests['test_functions']}")

    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Portfolio health checker")
    parser.add_argument("--quick", action="store_true", help="Quick status only")
    parser.add_argument("--project", help="Single project deep dive")
    args = parser.parse_args()

    if args.project:
        if args.project not in PROJECTS:
            print(f"Unknown project: {args.project}", file=sys.stderr)
            print(f"Available: {', '.join(PROJECTS.keys())}", file=sys.stderr)
            sys.exit(1)
        print(format_full(args.project, PROJECTS[args.project]))
        return

    print()
    print("=" * 55)
    print("  PORTFOLIO HEALTH — Satish Patil's Developer Tools")
    print("=" * 55)

    if args.quick:
        print()
        print(f"  {'Project':<15} {'Branch':<10} {'State':<8} {'Activity':<10} Commits")
        print(f"  {'-'*15} {'-'*10} {'-'*8} {'-'*10} {'-'*7}")
        for name, project in PROJECTS.items():
            print(format_quick(name, project))
    else:
        for name, project in PROJECTS.items():
            print()
            print(format_full(name, project))

    # Summary
    print()
    print("-" * 55)
    print("  SUMMARY")
    print("-" * 55)

    total_src = 0
    total_tests = 0
    total_commits = 0
    existing = 0

    for name, project in PROJECTS.items():
        if check_exists(project):
            existing += 1
            src = check_source(project["path"])
            tests = check_tests(project["path"])
            git = check_git_state(project["path"])
            total_src += src["source_lines"]
            total_tests += tests["test_functions"]
            total_commits += git.get("commit_count", 0)

    print(f"  Projects:     {existing}/{len(PROJECTS)}")
    print(f"  Total source: {total_src:,} lines")
    print(f"  Total tests:  {total_tests} functions")
    print(f"  Total commits: {total_commits}")
    print()
    print("=" * 55)
    print()


if __name__ == "__main__":
    main()
