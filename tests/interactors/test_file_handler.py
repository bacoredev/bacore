"""File handler tests."""
import pytest
from bacore.interactors import file_handler

pytestmark = pytest.mark.interactors


@pytest.fixture(scope="function")
def fixt_dir_with_files(tmp_path):
    dir = tmp_path
    (dir / "first_file.txt").write_text("Some text", encoding="utf-8")
    (dir / "sub_directory").mkdir()
    (dir / "sub_directory" / "second_file.py").write_text("Some python text", encoding="utf-8")

    return dir


def test_get_files_in_dir(fixt_dir_with_files):
    """Get files in directory."""
    files = file_handler.get_files_in_dir(dir=fixt_dir_with_files, recursive=True)
    file_names = [file.name for file in files]
    assert file_names == ["first_file.txt", "second_file.py"], f"Expected ['first_file.txt', 'second_file.py'], but got {file_names}"


def test_delete_files(fixt_dir_with_files):
    deleted_files_response = file_handler.delete_files(path=fixt_dir_with_files, older_than_days=0, recursive=True)
    deleted_files = [file.name for file in deleted_files_response.deleted_files]
    assert deleted_files == ["first_file.txt", "second_file.py"], f"Expected ['first_file.txt', 'second_file.py'], but got {deleted_files}"
