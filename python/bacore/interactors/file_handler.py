"""File handling interactors."""

import subprocess as sup
from bacore.domain.files import DeletedFiles
from bacore.domain.protocols import SupportsRetrieveDict
from datetime import datetime, timedelta
from pathlib import Path
from pydantic import Field, validate_call
from typing import Annotated, Optional


def get_files_in_dir(dir: Path, recursive: bool, pattern: str = "*") -> list[Path]:
    """Get list of files as path objects from a directory matching a pattern.

    Args:
        dir (Path): The directory to search in.
        recursive (bool): Whether to search recursively.
        pattern (str): The pattern to match files against.

    Returns:
        List[Path]: A list of Path objects for each file found.
    """
    if isinstance(dir, str):
        dir = Path(dir)
    find_function = dir.rglob if recursive else dir.glob

    return [file_path for file_path in find_function(pattern) if file_path.is_file()]



@validate_call
def delete_files(
    path: Path,
    pattern: str = "*",
    older_than_days: Annotated[int, Field(ge=0)] = 0,
    recursive: bool = False,
) -> DeletedFiles:
    """Delete files older than x days.

    Args:
        path (`Path`): Path to search for files.
        pattern (`str`): Pattern to search for files.
        older_than_days (`int`): Delete files older than x dyas. Default is `0`. Negative values are not allowed.
        recursive (`bool`): Optionally delete files recursively. Default is `False`.
    """
    number_of_deleted_files = 0
    deleted_files = []
    now = datetime.now()
    files_matching_pattern = get_files_in_dir(dir=path, recursive=recursive, pattern=pattern)

    for file in files_matching_pattern:
        if file.stat().st_mtime < (now - timedelta(days=older_than_days)).timestamp():
            file.unlink()
            deleted_files.append(file)
            number_of_deleted_files += 1

    return DeletedFiles(path=path,
                        pattern=pattern,
                        older_than_days=older_than_days,
                        recursive=recursive,
                        number_of_deleted_files=number_of_deleted_files,
                        deleted_files=deleted_files)


def file_as_dict(file: SupportsRetrieveDict) -> dict:
    """Content as dictionary."""
    return file.data_to_dict()


def read_markdown_file(file: Path, skip_title: bool) -> str:
    """Read a file in markdown format.

    Parameters:
        `file`: File path
        `skip_title`: Will skip the first line of the markdown file if it starts with the '#' character

    Returns:
        String of complete text or the text without the title.
    """
    if not isinstance(file, Path):
        file = Path(file)

    if file.suffix not in ['.md', '.markdown']:
        raise ValueError("File should be in markdown format")

    try:
        text = file.read_text()
    except FileNotFoundError:
        raise FileNotFoundError(f'Unable to find file: {file}')
    except IsADirectoryError:
        raise IsADirectoryError(f'Path is a directory, {file}')
    except PermissionError:
        raise PermissionError(f'Insuffient permissions to read {file}')

    title, body = text.split('\n', 1)
    if skip_title and title.strip().startswith('#'):
        return body
    else:
        return text


def rsync_copy(source: Path, destination: Path, file_filter: Optional[str]):
    """Use rsync to mirror files and folders from src to dest."""
    try:
        sup.run(f"rsync -av --delete {source}/{file_filter} {destination}", shell=True)
    except FileNotFoundError:
        raise FileNotFoundError("Unable to find file or directory to copy.")
