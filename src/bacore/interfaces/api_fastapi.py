"""Web API with FastAPI."""
from bacore.domain import files
from bacore.interactors import retrieve
from pathlib import Path


class ProjectInfo:
    """Project information."""

    def __init__(self, pyproject_file: Path):
        """Initialize."""
        self._pyproject_file_toml_object = files.TOML(path=pyproject_file)
        self._project_info = retrieve.file_as_dict(file=self._pyproject_file_toml_object)

    @property
    def name(self) -> str:
        """Project name."""
        return self._project_info["project"]["name"]

    @property
    def version(self) -> str:
        """Project version."""
        return self._project_info["project"]["version"]

    @property
    def description(self) -> str:
        """Project description."""
        return self._project_info["project"]["description"]
