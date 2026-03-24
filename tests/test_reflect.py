"""Tests for the reflection pattern analyzer."""

import sys
from pathlib import Path
from textwrap import dedent

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.reflect import parse_entries, trap_frequency, verdict_distribution


def write_temp(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "REFLECT.md"
    p.write_text(dedent(content))
    return p


# --- Parsing ---

def test_parse_basic_entry(tmp_path):
    """Parse a single reflection entry."""
    p = write_temp(tmp_path, """\
        ### 2026-03-24 — Confidence Trap (testing)

        **Trigger:** Something happened
        **What it caught:** A problem
        **What changed:** My approach shifted
        **Verdict:** useful
    """)
    entries = parse_entries(p)
    assert len(entries) == 1
    assert entries[0]["date"] == "2026-03-24"
    assert entries[0]["trap"] == "confidence"
    assert entries[0]["verdict"] == "useful"


def test_parse_missed_verdict(tmp_path):
    """Parse entry with missed verdict."""
    p = write_temp(tmp_path, """\
        ### 2026-03-24 — Pattern-Matching Trap (test)

        **Trigger:** Failed to catch something
        **What it caught:** Nothing
        **What changed:** Realized after the fact
        **Verdict:** missed
    """)
    entries = parse_entries(p)
    assert len(entries) == 1
    assert entries[0]["verdict"] == "missed"
    assert entries[0]["trap"] == "pattern-matching"


def test_parse_meta_interrupt(tmp_path):
    """Parse meta-interrupt entry."""
    p = write_temp(tmp_path, """\
        ### 2026-03-24 — Meta-Interrupt (autopilot check)

        **Trigger:** Everything felt smooth
        **What it caught:** Was on autopilot
        **What changed:** Paused and reconsidered
        **Verdict:** useful
    """)
    entries = parse_entries(p)
    assert len(entries) == 1
    assert entries[0]["trap"] == "meta-interrupt"


def test_parse_multiple_entries(tmp_path):
    """Parse multiple entries."""
    p = write_temp(tmp_path, """\
        ### 2026-03-24 — Delegation Trap (test 1)

        **Trigger:** A
        **What it caught:** B
        **What changed:** C
        **Verdict:** useful

        ### 2026-03-24 — Scope Trap (test 2)

        **Trigger:** D
        **What it caught:** E
        **What changed:** F
        **Verdict:** performative
    """)
    entries = parse_entries(p)
    assert len(entries) == 2
    assert entries[0]["trap"] == "delegation"
    assert entries[1]["trap"] == "scope"


def test_parse_empty_file(tmp_path):
    """Empty file returns no entries."""
    p = write_temp(tmp_path, "# REFLECT.md\n\nNo entries.\n")
    entries = parse_entries(p)
    assert len(entries) == 0


# --- Reports ---

def test_trap_frequency_counts(tmp_path):
    """Trap frequency report counts correctly."""
    p = write_temp(tmp_path, """\
        ### 2026-03-24 — Confidence Trap (a)

        **Trigger:** A
        **What it caught:** B
        **What changed:** C
        **Verdict:** useful

        ### 2026-03-24 — Confidence Trap (b)

        **Trigger:** D
        **What it caught:** E
        **What changed:** F
        **Verdict:** missed

        ### 2026-03-24 — Scope Trap (c)

        **Trigger:** G
        **What it caught:** H
        **What changed:** I
        **Verdict:** useful
    """)
    entries = parse_entries(p)
    report = trap_frequency(entries)
    assert "confidence" in report
    assert "scope" in report


def test_verdict_distribution(tmp_path):
    """Verdict distribution includes all types."""
    p = write_temp(tmp_path, """\
        ### 2026-03-24 — Meta-Interrupt (a)

        **Trigger:** A
        **What it caught:** B
        **What changed:** C
        **Verdict:** useful

        ### 2026-03-24 — Delegation Trap (b)

        **Trigger:** D
        **What it caught:** E
        **What changed:** F
        **Verdict:** performative
    """)
    entries = parse_entries(p)
    report = verdict_distribution(entries)
    assert "useful" in report
    assert "performative" in report


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
