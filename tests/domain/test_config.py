"""Tests for domain.config module."""
import pytest
from bacore.domain import config


@pytest.mark.domain
def test_system():
    """Test System."""
    assert config.System.os is not None
