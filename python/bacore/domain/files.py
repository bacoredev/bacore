"""Module domain files for handling of files and directories."""
from pathlib import Path

try:
    import tomllib
except ImportError:
    import toml as tomllib


class TOML:
    """TOML file class."""

    def __init__(self, path: Path):
        """Initialize."""
        self.path = path

    @property
    def path(self):
        """Get file path."""
        return self._path

    @path.setter
    def path(self, value):
        """Set file path as pathlib.Path object."""
        if not isinstance(value, Path):
            raise TypeError("Path must be a pathlib.Path object.")
        self._path = value

    def data_to_dict(self) -> dict:
        """Content as dictionary."""
        with open(self.path, mode="rb") as file:
            file_content = file if isinstance(file, str) else file.read()
            content_as_dict = tomllib.load(file_content)
        return content_as_dict
