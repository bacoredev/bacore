"""Retrieve Functionality Module (the "get" word feels overloaded)."""
import tomllib
from bacore.domain import config
from pathlib import Path
from typing import Protocol, runtime_checkable


def project_information(pyproject_file: Path) -> config.Project:
    """Get project information."""
    info = toml_file_content(pyproject_file)
    project_info = config.Project(name=info["project"]["name"],
                                  version=info["project"]["version"],
                                  description=info["project"]["description"])
    return project_info


def toml_file_content(file: Path) -> dict:
    """Get project information."""
    try:
        with open(file, mode="rb") as f:
            content = tomllib.load(f)
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file}' not found.")


class SupportsRetrieveDict(Protocol):
    """Protocol for retrieval of file content as dict."""

    def data_to_dict(self) -> dict:
        """Content as dictionary."""
        ...


class File:
    """File retrival."""

    def __init__(self, name: SupportsRetrieveDict):
        """Initialize."""
        self.file = name

    @property
    def as_dict(self):
        """Content as dictionary."""
        return self.file.data_to_dict()
