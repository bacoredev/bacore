"""Tests for delete.py interactors."""
import pytest
from bacore.interactors import delete


@pytest.fixture
def create_file(tmp_path):
    """Create a file."""
    file = tmp_path / "test.txt"
    file.write_text("test")
    return file


def test_delete_files(create_file):
    """Test delete_files."""
    file = create_file
    assert file.exists()
    delete.files(path=file.parent, pattern="*.txt", recursive=False)
    assert not file.exists()
