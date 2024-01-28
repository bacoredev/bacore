"""Tests for domain.config module."""
import pytest
from bacore.domain import info

pytestmark = pytest.mark.domain


class TestProject:
    """Tests for ProjectInfo entity."""

    def test_name(self):
        """Test name."""
        p = info.Project(name="bacore")
        assert p.name == "bacore"

    def test_name_must_not_contain_spaces(self):
        """Test name_must_not_contain_spaces."""
        with pytest.raises(ValueError):
            info.Project(name="ba core")


class TestSystem:
    """Test for SystemInfo."""

    def test_os(self):
        """Test os. (Darwin is macOS.)"""
        system_info = info.System(os="Darwin")
        assert system_info.os in ["Darwin", "Linux", "Windows"]

    def test_os_must_be_supported(self):
        """Test os_must_be_supported."""
        with pytest.raises(ValueError):
            info.System(os="AS/400")
