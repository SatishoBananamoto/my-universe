"""Tests for the CLAUDE.md auditor."""

import sys
from pathlib import Path
from textwrap import dedent

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.audit_claude_md import (
    extract_file_references,
    extract_command_references,
    extract_package_references,
    check_file_references,
    check_structure,
    find_claude_md,
)


# --- File reference extraction ---

def test_extract_backtick_paths():
    """Extract paths wrapped in backticks."""
    text = "Check `src/main.py` and `tests/test_core.py` for details."
    refs = extract_file_references(text)
    assert "src/main.py" in refs
    assert "tests/test_core.py" in refs


def test_extract_directory_refs():
    """Extract directory references ending with /."""
    text = "Files are in `src/` and `tests/`."
    refs = extract_file_references(text)
    assert "src/" in refs
    assert "tests/" in refs


def test_no_natural_language_paths():
    """Don't extract natural language that looks like paths."""
    text = "After receiving tool/subagent results, check the output."
    refs = extract_file_references(text)
    assert "tool/subagent" not in refs


def test_extract_dotted_paths():
    """Extract paths starting with dots."""
    text = "See `.claude/skills/think/SKILL.md` for details."
    refs = extract_file_references(text)
    assert ".claude/skills/think/SKILL.md" in refs


# --- Command extraction ---

def test_extract_code_block_commands():
    """Extract commands from code blocks."""
    text = '```bash\npython3 tools/calibrate.py\npytest tests/\n```'
    cmds = extract_command_references(text)
    assert "python3" in cmds or "pytest" in cmds


def test_no_function_calls_as_commands():
    """Don't treat function calls as commands."""
    text = '```\nengram_search(query="test")\n```'
    cmds = extract_command_references(text)
    for cmd in cmds:
        assert "(" not in cmd


# --- File reference checking ---

def test_check_existing_file(tmp_path):
    """Existing files should not be flagged."""
    (tmp_path / "README.md").write_text("# Hello")
    issues = check_file_references(["README.md"], tmp_path)
    assert len(issues) == 0


def test_check_missing_file(tmp_path):
    """Missing files should be flagged as errors."""
    issues = check_file_references(["nonexistent.py"], tmp_path)
    assert len(issues) == 1
    assert issues[0]["severity"] == "error"


def test_check_glob_pattern(tmp_path):
    """Glob patterns that match should not be flagged."""
    (tmp_path / "test_foo.py").write_text("pass")
    issues = check_file_references(["test_*.py"], tmp_path)
    assert len(issues) == 0


def test_check_glob_no_match(tmp_path):
    """Glob patterns that don't match should be flagged."""
    issues = check_file_references(["test_*.py"], tmp_path)
    assert len(issues) == 1
    assert issues[0]["severity"] == "warning"


# --- Structure checks ---

def test_structure_very_short():
    """Very short CLAUDE.md should get a warning."""
    issues = check_structure("Short file")
    assert any(i["reference"] == "length" for i in issues)


def test_structure_no_headers():
    """Missing headers should get a warning."""
    issues = check_structure("No headers here, just a bunch of text " * 10)
    assert any(i["reference"] == "headers" for i in issues)


def test_structure_good():
    """Well-structured CLAUDE.md should have no structure issues."""
    text = "# Project\n\n## Overview\n\nSome detailed content here.\n" * 5
    issues = check_structure(text)
    # May have 0 issues or only minor ones
    assert not any(i["reference"] in ("length", "headers") for i in issues)


# --- Find CLAUDE.md ---

def test_find_claude_md(tmp_path):
    """Find CLAUDE.md in project root."""
    (tmp_path / "CLAUDE.md").write_text("# Test")
    result = find_claude_md(tmp_path)
    assert result is not None
    assert result.name == "CLAUDE.md"


def test_find_claude_md_missing(tmp_path):
    """Return None when no CLAUDE.md exists."""
    result = find_claude_md(tmp_path)
    assert result is None


if __name__ == "__main__":
    import tempfile
    passed = 0
    failed = 0
    for name, func in sorted(globals().items()):
        if name.startswith("test_"):
            try:
                if "tmp_path" in func.__code__.co_varnames:
                    with tempfile.TemporaryDirectory() as td:
                        func(Path(td))
                else:
                    func()
                print(f"  PASS  {name}")
                passed += 1
            except Exception as e:
                print(f"  FAIL  {name}: {e}")
                failed += 1

    print(f"\n{passed} passed, {failed} failed")
