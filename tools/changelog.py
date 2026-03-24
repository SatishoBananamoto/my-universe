#!/usr/bin/env python3
"""
Cross-project changelog — recent activity across all projects.

Shows recent git commits across all portfolio projects in chronological order.
Useful for understanding what happened recently without checking each project.

Usage:
    python changelog.py              # Last 7 days
    python changelog.py --days 30    # Last 30 days
    python changelog.py --project X  # Single project
"""

import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta


HOME = Path.home()

PROJECTS = {
    "engram": HOME / "engram",
    "scroll": HOME / "scroll",
    "svx": HOME / "svx",
    "vigil": HOME / "vigil",
    "kv-secrets": HOME / "kv-secrets",
    "probe": HOME / "probe",
    "my-universe": HOME / "MY UNIVERSE",
}


def get_recent_commits(path: Path, days: int = 7) -> list[dict]:
    """Get recent git commits from a project."""
    if not (path / ".git").exists():
        return []

    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    try:
        result = subprocess.run(
            ["git", "log", f"--since={since}", "--format=%H|%ci|%s", "--no-merges"],
            capture_output=True, text=True, cwd=path, timeout=10,
        )
        if result.returncode != 0:
            return []
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []

    commits = []
    for line in result.stdout.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("|", 2)
        if len(parts) == 3:
            commits.append({
                "hash": parts[0][:8],
                "date": parts[1][:19],
                "message": parts[2][:80],
                "project": path.name,
            })

    return commits


def format_changelog(all_commits: list[dict], days: int) -> str:
    """Format commits as a chronological changelog."""
    lines = []
    lines.append("")
    lines.append("=" * 60)
    lines.append(f"  CROSS-PROJECT CHANGELOG — Last {days} day(s)")
    lines.append("=" * 60)

    if not all_commits:
        lines.append("")
        lines.append(f"  No commits in the last {days} days.")
        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)

    # Sort by date descending
    all_commits.sort(key=lambda c: c["date"], reverse=True)

    # Group by date
    current_date = None
    for commit in all_commits:
        date_str = commit["date"][:10]
        if date_str != current_date:
            current_date = date_str
            lines.append("")
            lines.append(f"  {date_str}")
            lines.append("  " + "-" * 50)

        project = commit["project"]
        msg = commit["message"]
        lines.append(f"  [{project:<14}] {msg}")

    # Summary
    lines.append("")
    lines.append("-" * 60)
    projects_active = len(set(c["project"] for c in all_commits))
    lines.append(f"  {len(all_commits)} commits across {projects_active} projects")
    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Cross-project changelog")
    parser.add_argument("--days", type=int, default=7, help="Look back N days (default: 7)")
    parser.add_argument("--project", help="Single project only")
    args = parser.parse_args()

    if args.project:
        if args.project not in PROJECTS:
            print(f"Unknown project: {args.project}", file=sys.stderr)
            print(f"Available: {', '.join(PROJECTS.keys())}", file=sys.stderr)
            sys.exit(1)
        projects = {args.project: PROJECTS[args.project]}
    else:
        projects = PROJECTS

    all_commits = []
    for name, path in projects.items():
        if path.exists():
            commits = get_recent_commits(path, days=args.days)
            all_commits.extend(commits)

    print(format_changelog(all_commits, args.days))


if __name__ == "__main__":
    main()
