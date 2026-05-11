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
