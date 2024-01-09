"""Tests for domain.config module."""
import pytest
from bacore.domain import config

pytestmark = pytest.mark.domain


class TestProject:
    """Tests for Project entity."""

    def test_name(self):
        """Test name."""
        p = config.Project(name="bacore")
        assert p.name == "bacore"

    def test_name_must_not_contain_spaces(self):
        """Test name_must_not_contain_spaces."""
        with pytest.raises(ValueError):
            config.Project(name="ba core")


class TestSystem:
    """Tests for System entity."""

    def test_os(self):
        """Test os."""
        os = config.System.os
        assert os in ["Darwin", "Linux", "Windows"]

    def test_os_must_be_supported(self):
        """Test os_must_be_supported."""
        with pytest.raises(ValueError):
            config.System(os="MacOS")
