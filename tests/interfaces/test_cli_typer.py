"""Tests for interactors.retrieve module."""
import pytest
from bacore.interfaces import cli_typer

pytestmark = pytest.mark.interfaces


def test_project_info(fixture_pyproject_file):
    """Test project_info."""
    project = cli_typer.ProjectInfo(pyproject_file=fixture_pyproject_file)
    assert project.name == "bacore"
    assert project.version == "1.0.0"
    assert project.description == "BACore is a framework for business analysis and test automation."
