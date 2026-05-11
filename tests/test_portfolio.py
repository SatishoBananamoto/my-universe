"""Tests for the cross-project portfolio registry."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools import portfolio


def test_portfolio_registry_includes_ai_agents_failure_modes():
    """The active ICIF-AES verifier should be counted in portfolio health."""
    project = portfolio.PROJECTS["ai-agents-failure-modes"]
    assert project["path"].name == "AI-Agents-Failure-Modes"
    assert project["type"] == "api-and-cli"


def test_portfolio_quick_width_covers_long_project_names():
    """The quick status table should not collapse long names into branches."""
    assert portfolio.PROJECT_NAME_WIDTH >= len("ai-agents-failure-modes")


def test_portfolio_quick_width_covers_long_branch_names():
    """The quick status table should not collapse long branches into state."""
    assert portfolio.BRANCH_WIDTH >= len("wip/2026-04-22-codex-snapshot")
