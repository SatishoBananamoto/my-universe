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


def test_onboarding_trial_records_caliber_continuation_result():
    """The onboarding continuation should record the connected-project result."""
    text = (BASE / "ONBOARDING-TRIAL.md").read_text()
    assert "Continuation Result: caliber multi-agent workflow hardening" in text
    assert "caliber:45ea13d" in text
    assert "101 tests" in text
    assert "No-deletion check" in text


def test_onboarding_trial_records_caliber_import_cleanup_result():
    """The import cleanup continuation should record archive evidence."""
    text = (BASE / "ONBOARDING-TRIAL.md").read_text()
    assert "Continuation Result: caliber CALIBRATE import cleanup" in text
    assert "caliber:102b294" in text
    assert "103 tests" in text
    assert ".archive/2026-05-11/extract-calibrate-standalone-parser/" in text


def test_onboarding_trial_records_caliber_mcp_config_result():
    """The MCP config continuation should record trust-boundary evidence."""
    text = (BASE / "ONBOARDING-TRIAL.md").read_text()
    assert "Continuation Result: caliber MCP config helper" in text
    assert "caliber:4c4a781" in text
    assert "105 tests" in text
    assert "Trust-boundary check" in text


def test_onboarding_trial_records_caliber_tutorial_result():
    """The tutorial continuation should record adoption-boundary evidence."""
    text = (BASE / "ONBOARDING-TRIAL.md").read_text()
    assert "Continuation Result: caliber first-user tutorial" in text
    assert "caliber:64464ad" in text
    assert "GETTING_STARTED.md" in text
    assert "Account-boundary check" in text


def test_onboarding_trial_records_analysis_readme_result():
    """The analysis continuation should record repo-selection evidence."""
    text = (BASE / "ONBOARDING-TRIAL.md").read_text()
    assert "Continuation Result: analysis README orientation" in text
    assert "analysis:fe6e352" in text
    assert "AI-agent dependency-risk reports" in text
    assert "Repo-selection and verification-boundary check" in text


def test_onboarding_trial_records_kvsecure_readme_result():
    """The kvsecure continuation should record product-boundary evidence."""
    text = (BASE / "ONBOARDING-TRIAL.md").read_text()
    assert "Continuation Result: kvsecure.com README orientation" in text
    assert "kvsecure.com:5e3f0b0" in text
    assert "stale-claim search" in text
    assert "Product-boundary and visual-verification check" in text


def test_onboarding_trial_records_profile_stats_result():
    """The profile continuation should record portfolio evidence."""
    text = (BASE / "ONBOARDING-TRIAL.md").read_text()
    assert "Continuation Result: profile README stats refresh" in text
    assert "SatishoBananamoto:db4da6b" in text
    assert "34k+ source lines" in text
    assert "Source-of-truth check" in text


def test_onboarding_trial_records_kvsecure_live_qa_result():
    """The kvsecure live QA continuation should record browser evidence."""
    text = (BASE / "ONBOARDING-TRIAL.md").read_text()
    assert "Continuation Result: kvsecure.com live browser QA" in text
    assert "kvsecure.com:4b58ba5" in text
    assert "denied-clipboard fallback" in text
    assert "node /tmp/codex-kvsecure-live-qa/interaction-qa.js" in text


def test_onboarding_trial_records_ai_agents_api_test_result():
    """The AI-Agents continuation should record transport-boundary evidence."""
    text = (BASE / "ONBOARDING-TRIAL.md").read_text()
    assert "Continuation Result: AI-Agents-Failure-Modes API test hardening" in text
    assert "AI-Agents-Failure-Modes:a1ac245" in text
    assert "transport-independent" in text
    assert "32 tests" in text


def test_onboarding_trial_records_portfolio_registry_result():
    """The portfolio continuation should record source-of-truth evidence."""
    text = (BASE / "ONBOARDING-TRIAL.md").read_text()
    assert "Continuation Result: portfolio registry/profile consistency" in text
    assert "SatishoBananamoto:ff3dc84" in text
    assert "35,815 source lines" in text
    assert "ai-agents-failure-modes" in text
