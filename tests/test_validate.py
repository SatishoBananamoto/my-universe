"""Tests for entry validation."""

import sys
from pathlib import Path
from textwrap import dedent

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.validate import validate_calibrate, validate_reflect


def write_temp(tmp_path: Path, content: str) -> Path:
    """Write content to a temp CALIBRATE.md and return path."""
    p = tmp_path / "CALIBRATE.md"
    p.write_text(dedent(content))
    return p


def entry(num: int, domain: str = "facts") -> str:
    """Return a minimal valid calibration entry."""
    return f"""\
        ### [P-{num:03d}] 2026-03-24 — {domain}

        **Prediction:** Prediction {num}
        **Confidence:** 70%
        **Actual:** Actual {num}
        **Result:** correct
    """


def test_validate_allows_out_of_order_ids(tmp_path):
    """Topic-grouped entries can be out of numeric order without being invalid."""
    p = write_temp(
        tmp_path,
        entry(1) + "\n" + entry(3) + "\n" + entry(2),
    )
    issues = validate_calibrate(p)
    assert not issues


def test_validate_allows_missing_ids_by_default(tmp_path):
    """Normal validation checks entries, not historical numbering gaps."""
    p = write_temp(
        tmp_path,
        entry(1) + "\n" + entry(3),
    )
    issues = validate_calibrate(p)
    assert not issues


def test_validate_strict_ids_reports_missing_ids(tmp_path):
    """Strict ID validation reports gaps when requested."""
    p = write_temp(
        tmp_path,
        entry(1) + "\n" + entry(3),
    )
    issues = validate_calibrate(p, strict_ids=True)
    assert "CALIBRATE [P-002]: Missing entry ID" in issues


def test_validate_reports_duplicate_ids(tmp_path):
    """Duplicate IDs should still be rejected."""
    p = write_temp(
        tmp_path,
        entry(1) + "\n" + entry(1),
    )
    issues = validate_calibrate(p)
    assert "CALIBRATE [P-001]: Duplicate entry ID" in issues


def test_validate_reflect_accepts_codex_reflect_format(tmp_path):
    """The shared reflection validator should work for CODEX-REFLECT.md."""
    p = tmp_path / "CODEX-REFLECT.md"
    p.write_text(dedent("""\
        ### 2026-05-10 — Binary Trap (test)

        **Trigger:** A
        **What it caught:** B
        **What changed:** C
        **Verdict:** useful
    """))
    issues = validate_reflect(p)
    assert not issues
