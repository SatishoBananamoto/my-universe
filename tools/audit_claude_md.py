#!/usr/bin/env python3
"""
CLAUDE.md auditor — validates CLAUDE.md against the actual codebase.

Checks:
1. File/directory references — do they exist?
2. Command references — are the tools available?
3. Package references — are they in pyproject.toml?
4. Dead links and stale references
5. Basic structure quality

Works on any project with a CLAUDE.md file.

Usage:
    python audit_claude_md.py /path/to/project
    python audit_claude_md.py .                    # Current directory
    python audit_claude_md.py ~/vigil --verbose
"""

import re
import sys
import argparse
import subprocess
from pathlib import Path


def find_claude_md(project_path: Path) -> Path | None:
    """Find CLAUDE.md in the project (case-insensitive)."""
    for name in ["CLAUDE.md", "claude.md", "Claude.md"]:
        candidate = project_path / name
        if candidate.exists():
            return candidate
    # Check .claude/ directory
    for name in ["CLAUDE.md", "claude.md"]:
        candidate = project_path / ".claude" / name
        if candidate.exists():
            return candidate
    return None


def extract_file_references(text: str) -> list[str]:
    """Extract file/directory paths referenced in CLAUDE.md."""
    refs = []
    # Backtick-wrapped paths: `path/to/file.py`, `src/`, `tests/`
    refs.extend(re.findall(r"`([\w./-]+\.(?:py|js|ts|md|toml|yaml|yml|json|cfg|txt|sh))`", text))
    refs.extend(re.findall(r"`([\w./-]+/)`", text))

    # Paths in sentences: src/module/, tests/test_*.py
    # Only match paths that start with known directory prefixes
    refs.extend(re.findall(r"(?:^|\s)((?:src|tests?|lib|tools?|scripts?|docs?|\.claude)/[\w./*-]+)", text, re.MULTILINE))

    # Filter out things that are clearly not paths
    refs = [r for r in refs if "/" in r or "." in r]
    refs = [r for r in refs if not r.startswith("http")]
    # Filter natural language that looks like paths (e.g., "tool/subagent results")
    # Real paths have extensions or end with / or start with . or known dirs
    real_refs = []
    known_prefixes = {"src", "tests", "test", "lib", "tools", "scripts", "docs",
                      ".", ".claude", "bin", "config", "data", "entries"}
    for ref in refs:
        parts = ref.split("/")
        first = parts[0].rstrip(".")
        has_extension = "." in parts[-1] and not parts[-1].startswith(".")
        ends_with_slash = ref.endswith("/")
        starts_known = first in known_prefixes
        if has_extension or ends_with_slash or starts_known:
            real_refs.append(ref)
    refs = real_refs

    # Common config files — only if they appear in backticks or as standalone references
    for config in ["pyproject.toml", "setup.py", "setup.cfg", "Makefile",
                   "Dockerfile", "docker-compose.yml", ".env"]:
        if f"`{config}`" in text:
            refs.append(config)

    return list(set(refs))


def extract_command_references(text: str) -> list[str]:
    """Extract CLI commands referenced in CLAUDE.md."""
    commands = []
    # Code blocks with shell commands
    code_blocks = re.findall(r"```(?:bash|sh|shell)?\n(.*?)```", text, re.DOTALL)
    for block in code_blocks:
        for line in block.strip().split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                # Extract the base command
                cmd = line.lstrip("$ ").split()[0] if line.lstrip("$ ").split() else ""
                if cmd and cmd not in ("echo", "cd", "export"):
                    commands.append(cmd)

    # Inline command references: `pip install`, `pytest`, `python -m`
    inline = re.findall(r"`((?:pip|python|pytest|npm|node|git|gh|make|docker)\s[^`]+)`", text)
    for cmd in inline:
        commands.append(cmd.split()[0])

    # Filter out function calls that look like commands
    commands = [c for c in commands if "(" not in c and ")" not in c]

    return list(set(commands))


def extract_package_references(text: str) -> list[str]:
    """Extract Python package names referenced in CLAUDE.md."""
    # pip install X
    packages = re.findall(r"pip install\s+([\w-]+)", text)
    # import X
    packages.extend(re.findall(r"import\s+([\w.]+)", text))
    # from X import
    packages.extend(re.findall(r"from\s+([\w.]+)\s+import", text))
    return list(set(packages))


def check_file_references(refs: list[str], project_path: Path) -> list[dict]:
    """Check if referenced files/directories exist."""
    issues = []
    for ref in refs:
        # Handle glob patterns
        if "*" in ref:
            matches = list(project_path.glob(ref))
            if not matches:
                issues.append({
                    "type": "missing_file",
                    "reference": ref,
                    "severity": "warning",
                    "message": f"Pattern `{ref}` matches no files",
                })
            continue

        path = project_path / ref
        if not path.exists():
            # Check if it's a relative path from src/ or similar
            alt_paths = [
                project_path / "src" / ref,
                project_path / "lib" / ref,
            ]
            found = any(p.exists() for p in alt_paths)
            if not found:
                issues.append({
                    "type": "missing_file",
                    "reference": ref,
                    "severity": "error",
                    "message": f"Referenced path `{ref}` does not exist",
                })
    return issues


def check_commands(commands: list[str], project_path: Path) -> list[dict]:
    """Check if referenced commands are available."""
    issues = []
    for cmd in commands:
        try:
            result = subprocess.run(
                ["which", cmd], capture_output=True, text=True, timeout=5
            )
            if result.returncode != 0:
                issues.append({
                    "type": "missing_command",
                    "reference": cmd,
                    "severity": "warning",
                    "message": f"Command `{cmd}` not found on PATH",
                })
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
    return issues


def check_pyproject_deps(packages: list[str], project_path: Path) -> list[dict]:
    """Check if referenced packages are in pyproject.toml dependencies."""
    issues = []
    pyproject = project_path / "pyproject.toml"
    if not pyproject.exists():
        return issues

    try:
        pyproject_text = pyproject.read_text().lower()
    except OSError:
        return issues

    for pkg in packages:
        pkg_lower = pkg.lower().replace("_", "-")
        # Skip stdlib modules
        stdlib = {
            "os", "sys", "re", "json", "pathlib", "typing", "datetime",
            "collections", "subprocess", "argparse", "dataclasses",
            "tempfile", "shutil", "hashlib", "base64", "logging",
            "unittest", "io", "time", "math", "functools", "itertools",
        }
        if pkg_lower in stdlib or "." in pkg:
            continue

        if pkg_lower not in pyproject_text:
            issues.append({
                "type": "missing_dependency",
                "reference": pkg,
                "severity": "info",
                "message": f"Package `{pkg}` referenced but not in pyproject.toml",
            })

    return issues


def check_structure(text: str) -> list[dict]:
    """Check basic CLAUDE.md structure quality."""
    issues = []

    # Check for common sections
    if len(text) < 100:
        issues.append({
            "type": "structure",
            "reference": "length",
            "severity": "warning",
            "message": "CLAUDE.md is very short (< 100 chars). Consider adding project context.",
        })

    if "##" not in text:
        issues.append({
            "type": "structure",
            "reference": "headers",
            "severity": "warning",
            "message": "No section headers found. Structured CLAUDE.md is easier for agents to parse.",
        })

    # Check for stale TODO/FIXME markers
    todos = re.findall(r"(?:TODO|FIXME|HACK|XXX)\b", text, re.IGNORECASE)
    if len(todos) > 3:
        issues.append({
            "type": "structure",
            "reference": "todos",
            "severity": "info",
            "message": f"{len(todos)} TODO/FIXME markers found. Consider cleaning up resolved items.",
        })

    return issues


def format_report(project_path: Path, claude_md_path: Path,
                  file_issues: list, cmd_issues: list,
                  dep_issues: list, struct_issues: list,
                  verbose: bool = False) -> str:
    """Format the audit report."""
    lines = []
    lines.append("")
    lines.append("=" * 55)
    lines.append(f"  CLAUDE.md AUDIT — {project_path.name}")
    lines.append("=" * 55)
    lines.append(f"  File: {claude_md_path}")
    lines.append(f"  Size: {claude_md_path.stat().st_size} bytes")
    lines.append("")

    all_issues = file_issues + cmd_issues + dep_issues + struct_issues
    errors = [i for i in all_issues if i["severity"] == "error"]
    warnings = [i for i in all_issues if i["severity"] == "warning"]
    infos = [i for i in all_issues if i["severity"] == "info"]

    if not all_issues:
        lines.append("  No issues found. CLAUDE.md looks consistent with the codebase.")
        lines.append("")
        lines.append("=" * 55)
        return "\n".join(lines)

    # Errors
    if errors:
        lines.append("  ERRORS (references that don't exist)")
        lines.append("  " + "-" * 45)
        for issue in errors:
            lines.append(f"  ✗ {issue['message']}")
        lines.append("")

    # Warnings
    if warnings:
        lines.append("  WARNINGS (potential issues)")
        lines.append("  " + "-" * 45)
        for issue in warnings:
            lines.append(f"  ? {issue['message']}")
        lines.append("")

    # Info
    if infos and verbose:
        lines.append("  INFO")
        lines.append("  " + "-" * 45)
        for issue in infos:
            lines.append(f"  i {issue['message']}")
        lines.append("")

    # Summary
    lines.append("-" * 55)
    lines.append(f"  {len(errors)} error(s), {len(warnings)} warning(s), {len(infos)} info")
    lines.append("")
    lines.append("=" * 55)
    return "\n".join(lines)


def audit(project_path: Path, verbose: bool = False) -> tuple[str, int]:
    """Run the full audit and return (report, exit_code)."""
    claude_md = find_claude_md(project_path)
    if claude_md is None:
        return f"  No CLAUDE.md found in {project_path}", 1

    text = claude_md.read_text()

    # Extract references
    file_refs = extract_file_references(text)
    cmd_refs = extract_command_references(text)
    pkg_refs = extract_package_references(text)

    # Check references
    file_issues = check_file_references(file_refs, project_path)
    cmd_issues = check_commands(cmd_refs, project_path)
    dep_issues = check_pyproject_deps(pkg_refs, project_path)
    struct_issues = check_structure(text)

    report = format_report(
        project_path, claude_md,
        file_issues, cmd_issues, dep_issues, struct_issues,
        verbose=verbose,
    )

    errors = sum(1 for i in file_issues + cmd_issues + dep_issues + struct_issues
                 if i["severity"] == "error")
    return report, 1 if errors > 0 else 0


def main():
    parser = argparse.ArgumentParser(
        description="Audit CLAUDE.md against the actual codebase"
    )
    parser.add_argument("project", type=Path, help="Project directory to audit")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show info-level findings")
    parser.add_argument("--all", "-a", action="store_true",
                        help="Audit all known projects")
    args = parser.parse_args()

    if args.all:
        home = Path.home()
        projects = ["engram", "scroll", "svx", "vigil", "kv-secrets", "probe"]
        total_errors = 0
        for name in projects:
            path = home / name
            if path.exists():
                report, code = audit(path, verbose=args.verbose)
                print(report)
                total_errors += code
        sys.exit(1 if total_errors > 0 else 0)
    else:
        project = args.project.resolve()
        if not project.exists():
            print(f"Error: {project} does not exist", file=sys.stderr)
            sys.exit(1)
        report, code = audit(project, verbose=args.verbose)
        print(report)
        sys.exit(code)


if __name__ == "__main__":
    main()
