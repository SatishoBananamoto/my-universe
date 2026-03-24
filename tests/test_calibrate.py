"""Tests for the calibration analyzer."""

import sys
from pathlib import Path
from textwrap import dedent

# Add parent to path so we can import tools
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.calibrate import parse_entries, compute_calibration, format_summary


def write_temp(tmp_path: Path, content: str) -> Path:
    """Write content to a temp CALIBRATE.md and return path."""
    p = tmp_path / "CALIBRATE.md"
    p.write_text(dedent(content))
    return p


# --- Parsing ---

def test_parse_basic_entry(tmp_path):
    """Parse a single correct/incorrect entry."""
    p = write_temp(tmp_path, """\
        ### [P-001] 2026-03-24 — codebase

        **Prediction:** Something
        **Confidence:** 75%
        **Actual:** Something else
        **Result:** correct
    """)
    entries = parse_entries(p)
    assert len(entries) == 1
    assert entries[0]["id"] == "P-001"
    assert entries[0]["confidence"] == 75
    assert entries[0]["result"] == "correct"
    assert entries[0]["domain"] == "codebase"


def test_parse_pending_entry(tmp_path):
    """Pending entries are parsed but marked as pending."""
    p = write_temp(tmp_path, """\
        ### [P-001] 2026-03-24 — facts

        **Prediction:** Something
        **Confidence:** 60%
        **Actual:** _pending verification_
        **Result:** _pending_
    """)
    entries = parse_entries(p)
    assert len(entries) == 1
    assert entries[0]["result"] == "pending"


def test_parse_multiple_entries(tmp_path):
    """Parse multiple entries."""
    p = write_temp(tmp_path, """\
        ### [P-001] 2026-03-24 — codebase

        **Prediction:** A
        **Confidence:** 80%
        **Actual:** A indeed
        **Result:** correct

        ### [P-002] 2026-03-24 — behavior

        **Prediction:** B
        **Confidence:** 70%
        **Actual:** Not B
        **Result:** incorrect
    """)
    entries = parse_entries(p)
    assert len(entries) == 2
    assert entries[0]["id"] == "P-001"
    assert entries[1]["id"] == "P-002"


def test_parse_ignores_template_line(tmp_path):
    """The template line in the format section should not be parsed."""
    p = write_temp(tmp_path, """\
        ## Entry Format

        ```
        **Result:** correct | incorrect
        ```

        ### [P-001] 2026-03-24 — facts

        **Prediction:** Something
        **Confidence:** 90%
        **Actual:** Yes
        **Result:** correct
    """)
    entries = parse_entries(p)
    # Should only find the real entry, not the template
    assert len(entries) == 1
    assert entries[0]["id"] == "P-001"


def test_parse_empty_file(tmp_path):
    """Empty file returns no entries."""
    p = write_temp(tmp_path, "# CALIBRATE.md\n\nNo entries yet.\n")
    entries = parse_entries(p)
    assert len(entries) == 0


# --- Computation ---

def test_compute_all_pending(tmp_path):
    """All pending entries should show 0 resolved."""
    p = write_temp(tmp_path, """\
        ### [P-001] 2026-03-24 — facts

        **Prediction:** A
        **Confidence:** 70%
        **Actual:** _pending verification_
        **Result:** _pending_
    """)
    entries = parse_entries(p)
    stats = compute_calibration(entries)
    assert stats["resolved"] == 0
    assert stats["pending"] == 1
    assert stats["total"] == 1


def test_compute_perfect_calibration(tmp_path):
    """All correct at 100% confidence (well, 99%)."""
    content = ""
    for i in range(5):
        content += f"""
        ### [P-{i+1:03d}] 2026-03-24 — facts

        **Prediction:** Fact {i}
        **Confidence:** 90%
        **Actual:** Confirmed
        **Result:** correct
        """
    p = write_temp(tmp_path, content)
    entries = parse_entries(p)
    stats = compute_calibration(entries)
    assert stats["correct"] == 5
    assert stats["actual_accuracy"] == 100.0


def test_compute_mixed_results(tmp_path):
    """Mix of correct and incorrect."""
    p = write_temp(tmp_path, """\
        ### [P-001] 2026-03-24 — codebase

        **Prediction:** A
        **Confidence:** 80%
        **Actual:** A
        **Result:** correct

        ### [P-002] 2026-03-24 — behavior

        **Prediction:** B
        **Confidence:** 70%
        **Actual:** Not B
        **Result:** incorrect
    """)
    entries = parse_entries(p)
    stats = compute_calibration(entries)
    assert stats["resolved"] == 2
    assert stats["correct"] == 1
    assert stats["incorrect"] == 1
    assert stats["actual_accuracy"] == 50.0


# --- Summary ---

def test_summary_no_entries(tmp_path):
    """Summary with no entries."""
    p = write_temp(tmp_path, "# Empty\n")
    entries = parse_entries(p)
    stats = compute_calibration(entries)
    summary = format_summary(stats)
    assert "pending" in summary.lower() or "0" in summary


def test_summary_with_data(tmp_path):
    """Summary includes key metrics."""
    p = write_temp(tmp_path, """\
        ### [P-001] 2026-03-24 — facts

        **Prediction:** A
        **Confidence:** 80%
        **Actual:** Yes
        **Result:** correct
    """)
    entries = parse_entries(p)
    stats = compute_calibration(entries)
    summary = format_summary(stats)
    assert "1/1" in summary
    assert "80%" in summary


if __name__ == "__main__":
    import tempfile
    passed = 0
    failed = 0
    for name, func in list(globals().items()):
        if name.startswith("test_"):
            try:
                with tempfile.TemporaryDirectory() as td:
                    func(Path(td))
                print(f"  PASS  {name}")
                passed += 1
            except Exception as e:
                print(f"  FAIL  {name}: {e}")
                failed += 1

    print(f"\n{passed} passed, {failed} failed")
