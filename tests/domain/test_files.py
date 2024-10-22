"""Tests for domain.files module."""

import pytest
from bacore.domain import files
from pathlib import Path

pytestmark = pytest.mark.domain


class TestTOML:
    """Tests for TOML entity."""

    def test_path(self, fixt_dir_with_files):
        """Test path."""
        toml_file = files.TOML(path=fixt_dir_with_files / "pyproject.toml")
        assert isinstance(toml_file.path, Path)

    def test_path_fail_with_string(self):
        """Test path."""
        with pytest.raises(TypeError):
            files.TOML(path="pyproject.toml")

    def test_data_to_dict(self, fixt_dir_with_files):
        """Test toml_file_content."""
        content = files.TOML(path=fixt_dir_with_files / "pyproject.toml")
        assert isinstance(content.data_to_dict(), dict)
