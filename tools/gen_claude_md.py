#!/usr/bin/env python3
"""
CLAUDE.md generator — creates project-specific CLAUDE.md from codebase analysis.

Reads pyproject.toml, code structure, test patterns, and README to generate
a CLAUDE.md that gives AI agents useful project context.

Does NOT write the file automatically — outputs to stdout for review.

Usage:
    python gen_claude_md.py /path/to/project           # Print to stdout
    python gen_claude_md.py /path/to/project -o FILE    # Write to file
    python gen_claude_md.py --all                        # Generate for all projects
"""

import re
import sys
import argparse
from pathlib import Path


HOME = Path.home()

PROJECTS = {
    "engram": HOME / "engram",
    "scroll": HOME / "scroll",
    "svx": HOME / "svx",
    "vigil": HOME / "vigil",
    "kv-secrets": HOME / "kv-secrets",
    "probe": HOME / "probe",
}


def read_pyproject(path: Path) -> dict:
    """Extract metadata from pyproject.toml."""
    pyproject = path / "pyproject.toml"
    if not pyproject.exists():
        return {}

    text = pyproject.read_text()
    meta = {}

    # Name
    m = re.search(r'name\s*=\s*"([^"]+)"', text)
    if m:
        meta["name"] = m.group(1)

    # Version
    m = re.search(r'version\s*=\s*"([^"]+)"', text)
    if m:
        meta["version"] = m.group(1)

    # Description
    m = re.search(r'description\s*=\s*"([^"]+)"', text)
    if m:
        meta["description"] = m.group(1)

    # Python version
    m = re.search(r'requires-python\s*=\s*"([^"]+)"', text)
    if m:
        meta["python"] = m.group(1)

    # Dependencies
    deps = re.findall(r'"([\w-]+)(?:[><=!].*?)?"', text)
    # Filter to actual package names (skip metadata)
    dep_section = re.search(r'dependencies\s*=\s*\[(.*?)\]', text, re.DOTALL)
    if dep_section:
        meta["deps"] = re.findall(r'"([\w-]+)', dep_section.group(1))
    else:
        meta["deps"] = []

    # Entry points
    m = re.search(r'\[project\.scripts\](.*?)(?:\[|$)', text, re.DOTALL)
    if m:
        scripts = re.findall(r'(\w+)\s*=\s*"([^"]+)"', m.group(1))
        meta["scripts"] = scripts

    return meta


def analyze_structure(path: Path) -> dict:
    """Analyze project file structure."""
    info = {}

    # Source files
    src_files = list(path.rglob("*.py"))
    src_files = [f for f in src_files
                 if "__pycache__" not in str(f)
                 and ".venv" not in str(f)
                 and "test" not in f.name.lower()]
    info["source_files"] = len(src_files)

    # Test files
    test_files = list(path.rglob("test_*.py"))
    test_files = [f for f in test_files if "__pycache__" not in str(f)]
    info["test_files"] = len(test_files)
    info["test_dir"] = None
    if test_files:
        test_dirs = set(f.parent.name for f in test_files)
        if "tests" in test_dirs:
            info["test_dir"] = "tests/"
        elif "test" in test_dirs:
            info["test_dir"] = "test/"

    # Source directory
    if (path / "src").exists():
        info["src_dir"] = "src/"
    elif any(f.parent == path for f in src_files):
        info["src_dir"] = "./"
    else:
        # Find the most common parent
        parents = [f.parent.relative_to(path) for f in src_files if f.is_relative_to(path)]
        if parents:
            info["src_dir"] = str(parents[0]) + "/"
        else:
            info["src_dir"] = "./"

    # Key directories
    info["dirs"] = []
    for d in sorted(path.iterdir()):
        if d.is_dir() and not d.name.startswith(".") and d.name not in (
            "__pycache__", ".venv", "node_modules", ".git",
            ".mypy_cache", ".pytest_cache", ".ruff_cache",
        ):
            info["dirs"].append(d.name)

    # Has MCP server
    info["has_mcp"] = False
    for f in src_files:
        try:
            content = f.read_text()
            if "FastMCP" in content or "mcp.server" in content:
                info["has_mcp"] = True
                break
        except (OSError, UnicodeDecodeError):
            pass

    # Has CLI
    info["has_cli"] = False
    for f in src_files:
        try:
            content = f.read_text()
            if "@click" in content or "argparse" in content:
                info["has_cli"] = True
                break
        except (OSError, UnicodeDecodeError):
            pass

    # Git info
    info["is_git"] = (path / ".git").exists()

    return info


def read_readme(path: Path) -> str | None:
    """Read README content if available."""
    for name in ["README.md", "readme.md", "README.rst", "README"]:
        f = path / name
        if f.exists():
            try:
                return f.read_text()[:2000]  # First 2000 chars
            except OSError:
                pass
    return None


def generate(project_path: Path) -> str:
    """Generate CLAUDE.md content for a project."""
    meta = read_pyproject(project_path)
    structure = analyze_structure(project_path)
    readme = read_readme(project_path)

    name = meta.get("name", project_path.name)
    desc = meta.get("description", "")
    version = meta.get("version", "unknown")
    python_req = meta.get("python", ">=3.10")

    lines = []
    lines.append(f"# {name} — Project Instructions")
    lines.append("")

    # Description
    if desc:
        lines.append(f"> {desc}")
        lines.append("")

    # Overview
    lines.append("## Overview")
    lines.append("")
    lines.append(f"- **Version**: {version}")
    lines.append(f"- **Python**: {python_req}")
    if meta.get("deps"):
        lines.append(f"- **Dependencies**: {', '.join(meta['deps'])}")
    lines.append(f"- **Source files**: {structure['source_files']}")
    lines.append(f"- **Test files**: {structure['test_files']}")
    if structure.get("has_mcp"):
        lines.append("- **Type**: MCP Server")
    if structure.get("has_cli"):
        lines.append("- **Type**: CLI Tool")
    lines.append("")

    # Structure
    lines.append("## Project Structure")
    lines.append("")
    lines.append(f"- Source code: `{structure['src_dir']}`")
    if structure["test_dir"]:
        lines.append(f"- Tests: `{structure['test_dir']}`")
    if structure["dirs"]:
        lines.append(f"- Key directories: {', '.join(f'`{d}/`' for d in structure['dirs'][:8])}")
    lines.append("")

    # Working conventions
    lines.append("## Working Conventions")
    lines.append("")
    lines.append("- Read existing code before modifying")
    lines.append("- Run tests after making changes")
    if structure["test_dir"]:
        lines.append(f"- Tests are in `{structure['test_dir']}` — run with `pytest {structure['test_dir']}`")
    lines.append("- Never auto-commit — only commit when explicitly asked")
    lines.append("- Never push without asking")
    lines.append("")

    # Entry points
    if meta.get("scripts"):
        lines.append("## CLI Commands")
        lines.append("")
        for script_name, entry in meta["scripts"]:
            lines.append(f"- `{script_name}` → `{entry}`")
        lines.append("")

    # MCP server info
    if structure.get("has_mcp"):
        lines.append("## MCP Server")
        lines.append("")
        lines.append("This project includes an MCP server. When modifying server tools:")
        lines.append("- Update tool descriptions if behavior changes")
        lines.append("- Test tool responses with realistic inputs")
        lines.append("- Keep tool names stable (changing names breaks client configs)")
        lines.append("")

    # Generated notice
    lines.append("---")
    lines.append("")
    lines.append("*Generated by MY UNIVERSE audit_claude_md.py. Review and customize before use.*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate CLAUDE.md from codebase analysis")
    parser.add_argument("project", type=Path, nargs="?", help="Project directory")
    parser.add_argument("-o", "--output", type=Path, help="Write to file instead of stdout")
    parser.add_argument("--all", action="store_true", help="Generate for all known projects")
    args = parser.parse_args()

    if args.all:
        for name, path in PROJECTS.items():
            if not path.exists():
                continue
            print(f"\n{'=' * 55}")
            print(f"  {name}")
            print(f"{'=' * 55}\n")
            print(generate(path))
            print()
        return

    if not args.project:
        parser.error("Either specify a project path or use --all")

    project = args.project.resolve()
    if not project.exists():
        print(f"Error: {project} does not exist", file=sys.stderr)
        sys.exit(1)

    content = generate(project)

    if args.output:
        args.output.write_text(content)
        print(f"Written to {args.output}")
    else:
        print(content)


if __name__ == "__main__":
    main()
