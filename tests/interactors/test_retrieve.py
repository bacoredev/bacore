"""Tests for interactors.retrieve module."""
import pytest
from bacore.domain import config
from bacore.interactors import retrieve

pytestmark = pytest.mark.interactors


@pytest.fixture
def fixture_test_system_information():
    """Fixture for system_information."""
    return "Darwin"


def test_system_information(fixture_test_system_information):
    """Test system_information."""
    info = retrieve.system_information(func=fixture_test_system_information)
    assert isinstance(info, config.SystemInfo)
    assert info.os == "Darwin"
