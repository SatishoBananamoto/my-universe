"""Tests for next-action suggestions."""

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

next_tool = importlib.import_module("tools.next")


def test_unfired_traps_respects_binary_entries():
    """Binary trap entries should remove binary from the unfired set."""
    entries = [
        {"trap": "binary"},
        {"trap": "confidence"},
    ]
    unfired = next_tool.get_unfired_traps(entries)
    assert "binary" not in unfired
    assert "performance" in unfired


def test_unfired_traps_respects_multi_trap_entries():
    """Entries with multiple traps should count every named trap."""
    entries = [
        {"trap": "completion", "traps": ["completion", "performance"]},
    ]
    unfired = next_tool.get_unfired_traps(entries)
    assert "completion" not in unfired
    assert "performance" not in unfired


def test_reflection_entries_include_codex_lane():
    """Active reflection inputs should include CODEX-REFLECT.md when present."""
    entries = next_tool.get_reflection_entries()
    headers = {entry["header"] for entry in entries}
    assert any("Binary Trap" in header for header in headers)


def test_task_list_has_review_gate_and_continue_last():
    """Continuation task lists should review first and keep Continue last."""
    actions = next_tool.suggest_task_list()
    assert actions[0].startswith("Review previous slice")
    assert any("xhigh reviewer" in action for action in actions)
    assert actions[-1] == "Continue"


def test_review_gate_mentions_required_state_surfaces():
    """The review gate should route through the active Codex/Kai surfaces."""
    actions = next_tool.review_gate_actions()
    joined = " ".join(actions)
    assert "PRISM.md" in joined
    assert "CODEX-PRISM.md" in joined
    assert "CODEX-REFLECT.md" in joined
