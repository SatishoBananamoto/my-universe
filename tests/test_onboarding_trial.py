"""Tests for fresh-agent onboarding trial artifacts."""

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools import brief

next_tool = importlib.import_module("tools.next")

BASE = Path(__file__).parent.parent


def test_onboarding_trial_file_exists():
    """The transfer-validation protocol should be a first-class artifact."""
    assert (BASE / "ONBOARDING-TRIAL.md").exists()


def test_onboarding_trial_has_required_sections():
    """The protocol should be runnable without hidden context."""
    text = (BASE / "ONBOARDING-TRIAL.md").read_text()
    required = [
        "## Purpose",
        "## Hard Constraints",
        "## Trial Setup",
        "## Required Run",
        "## Pass / Fail Rubric",
        "## Trial Record Template",
        "## Trial Records",
        "## Continue",
    ]
    for section in required:
        assert section in text


def test_onboarding_trial_preserves_no_deletion_rule():
    """The user's no-deletion constraint should be explicit and inspectable."""
    text = (BASE / "ONBOARDING-TRIAL.md").read_text().lower()
    assert "no deletion" in text
    assert ".archive/yyyy-mm-dd/<reason>/" in text
    assert "manifest.md" in text


def test_onboarding_trial_names_required_runtime_files():
    """The trial must route participants through the core practice files."""
    text = (BASE / "ONBOARDING-TRIAL.md").read_text()
    for name in ["MANIFEST.md", "PRISM.md", "WARMUP.md", "THINK.md"]:
        assert name in text


def test_continuation_gate_file_exists():
    """Recursive continuation should have an explicit protocol."""
    assert (BASE / "CONTINUATION-GATE.md").exists()


def test_continuation_gate_preserves_recursive_continue_rule():
    """The protocol should make Continue a loop trigger, not a stop signal."""
    text = (BASE / "CONTINUATION-GATE.md").read_text()
    assert "`Continue` is not a normal task" in text
    assert "append Continue again" in text
    assert "Optional xhigh reviewer" in text
    assert text.strip().endswith("as the final item.")


def test_next_actions_end_with_continue():
    """Generated task lists should keep the continuation task last."""
    actions = next_tool.suggest_actions()
    assert actions[-1] == "Continue"


def test_short_brief_points_to_onboarding_trial():
    """Fresh-session briefs should surface the transfer-validation path."""
    text = brief.generate_short()
    assert "ONBOARDING-TRIAL.md" in text
    assert "continue" in text.lower()


def test_full_brief_respects_reflection_lane_boundary():
    """Session briefs should not nudge Codex/Kai work into Claude REFLECT.md."""
    text = brief.generate_brief()
    assert "REFLECT.md or CODEX-REFLECT.md only for the owning lane" in text


def test_onboarding_trial_records_first_fresh_agent_trial():
    """The first fresh-agent trial should be recorded with evidence."""
    text = (BASE / "ONBOARDING-TRIAL.md").read_text()
    assert "Fresh-Agent Trial: caliber CLAUDE snapshot drift" in text
    assert "caliber:439b4b8" in text
    assert "Next continuation task:" in text
    assert "Continue" in text
