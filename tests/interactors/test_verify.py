"""Tests for interactors.verify module."""

import pytest
from bacore.domain.system import CLIProgram
from bacore.interactors.verify import command_on_path
from bacore.interactors.retrieve import system_information_os

pytestmark = pytest.mark.interactors


@pytest.fixture
def fixture_test_command_on_path():
    """Fixture for command_on_path."""
    match system_information_os().os:
        case "Darwin":
            return "ls"
        case "Linux":
            return "ls"
        case "Windows":
            return "dir"
        case _:
            raise ValueError("OS is not supported.")


def test_command_on_path(fixture_test_command_on_path):
    """Test command_on_path."""
    assert command_on_path(CLIProgram(name=fixture_test_command_on_path)) is True
    assert command_on_path(CLIProgram(name="bogus_does_not_exist")) is False
