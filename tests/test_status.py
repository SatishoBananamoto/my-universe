"""Tests for the system health check."""

import sys
from pathlib import Path
from textwrap import dedent

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.status import calibration_summary, reflection_summary, file_health, count_traps


def write_file(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(dedent(content))
    return p


# --- Calibration summary ---

def test_calibration_summary_with_data(tmp_path):
    """Parse calibration data correctly."""
    write_file(tmp_path, "CALIBRATE.md", """\
        ### [P-001] 2026-03-24 — facts

        **Prediction:** A
        **Confidence:** 80%
        **Actual:** Yes
        **Result:** correct

        ### [P-002] 2026-03-24 — facts

        **Prediction:** B
        **Confidence:** 70%
        **Actual:** No
        **Result:** incorrect
    """)
    stats = calibration_summary(tmp_path / "CALIBRATE.md")
    assert stats["resolved"] == 2
    assert stats["correct"] == 1


def test_calibration_summary_empty(tmp_path):
    """Handle missing file."""
    stats = calibration_summary(tmp_path / "CALIBRATE.md")
    assert stats["total"] == 0


def test_calibration_template_not_counted(tmp_path):
    """Template line should not be counted as a result."""
    write_file(tmp_path, "CALIBRATE.md", """\
        **Result:** correct | incorrect

        ### [P-001] 2026-03-24 — facts

        **Prediction:** A
        **Confidence:** 80%
        **Actual:** Yes
        **Result:** correct
    """)
    stats = calibration_summary(tmp_path / "CALIBRATE.md")
    assert stats["correct"] == 1  # Not 2


# --- Reflection summary ---

def test_reflection_summary_with_data(tmp_path):
    """Parse reflection verdicts correctly."""
    write_file(tmp_path, "REFLECT.md", """\
        ### 2026-03-24 — Test

        **Trigger:** A
        **What it caught:** B
        **What changed:** C
        **Verdict:** useful

        ### 2026-03-24 — Test 2

        **Trigger:** D
        **What it caught:** E
        **What changed:** F
        **Verdict:** missed
    """)
    stats = reflection_summary(tmp_path / "REFLECT.md")
    assert stats["total"] == 2
    assert stats["useful"] == 1
    assert stats["missed"] == 1


def test_reflection_summary_empty(tmp_path):
    """Handle missing file."""
    stats = reflection_summary(tmp_path / "REFLECT.md")
    assert stats["total"] == 0


# --- Trap count ---

def test_count_traps(tmp_path):
    """Count named traps in THINK.md."""
    write_file(tmp_path, "THINK.md", """\
        ### The Completion Trap
        Some text.

        ### The Confidence Trap
        More text.

        **The category trap (variant):**
        Even more text.
    """)
    count = count_traps(tmp_path / "THINK.md")
    assert count == 3


# --- File health ---

def test_file_health_all_present(tmp_path):
    """All expected files present."""
    for name in ["MANIFEST.md", "THINK.md", "REFLECT.md", "CALIBRATE.md",
                 "REASON.md", "WARMUP.md", "PORTFOLIO-THESIS.md"]:
        (tmp_path / name).write_text(f"# {name}")

    health = file_health(tmp_path)
    assert all(exists for _, exists, _ in health)


def test_file_health_missing(tmp_path):
    """Some files missing."""
    (tmp_path / "THINK.md").write_text("# THINK")
    health = file_health(tmp_path)
    present = [name for name, exists, _ in health if exists]
    missing = [name for name, exists, _ in health if not exists]
    assert "THINK.md" in present
    assert len(missing) > 0


if __name__ == "__main__":
    import tempfile
    import inspect
    passed = 0
    failed = 0
    for name, func in sorted(globals().items()):
        if name.startswith("test_"):
            try:
                sig = inspect.signature(func)
                if sig.parameters:
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
