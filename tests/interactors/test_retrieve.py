"""Tests for interactors.retrieve module."""
import pytest
from bacore.domain import info
from bacore.interactors import retrieve


@pytest.fixture
def fixture_test_system_information():
    """Fixture for system_information."""
    return "Darwin"


def test_system_information(fixture_test_system_information):
    """Test system_information."""
    information = retrieve.system_information(func=fixture_test_system_information)
    assert isinstance(information, info.System)
    assert information.os == "Darwin"
