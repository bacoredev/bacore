"""Settings module for settings of BACore and its components."""
from bacore.domain import files
from pathlib import Path
from pydantic import Field, computed_field, field_validator, SecretStr
from pydantic_settings import BaseSettings


class Credential(BaseSettings):
    """Credential details."""

    username: str
    password: SecretStr

    @field_validator("username")
    @classmethod
    def username_must_not_contain_spaces(cls, v: str) -> str:
        """Validate that the username does not contain spaces."""
        if " " in v:
            raise ValueError("No spaces allowed in username.")
        return v


class Project(BaseSettings):
    """Project settings assumes that the project will use a pyproject.toml file."""

    path: Path = Field(default=Path("."), alias="project_root_dir")

    @field_validator("path")
    def path_must_be_directory(cls, v: Path) -> Path:
        """Validate that the path is a directory."""
        if v.is_dir() is False:
            raise ValueError(f"Path '{v}' is not a directory.")
        if (v / "pyproject.toml").is_file() is False:
            raise FileNotFoundError(f"Unable to find pyproject.toml file at path '{v}")
        return v

    @computed_field
    @property
    def _pyproject_file(self) -> Path:
        project_file = self.path / "pyproject.toml"
        if project_file.is_file() is False:
            raise FileNotFoundError(f"Unable to find pyproject.toml file, got '{project_file}'")
        return project_file

    @computed_field
    @property
    def _project_info(self) -> dict:
        """pyproject.toml file as dictionary."""
        return files.TOML(path=self._pyproject_file).data_to_dict()

    @computed_field
    @property
    def name(self) -> str:
        """Project name."""
        project_name = self._project_info["project"]["name"]
        if " " in project_name:
            raise ValueError("No spaces allowed in project name.")
        return project_name

    @computed_field
    @property
    def version(self) -> str:
        """Project name."""
        project_version = self._project_info["project"]["version"]
        return project_version if project_version is not None else "No project version set."

    @computed_field
    @property
    def description(self) -> str:
        """Project description."""
        project_description = self._project_info["project"]["description"]
        return project_description if project_description is not None else "No project description given."


class Token(BaseSettings):
    """Credential details."""

    id: SecretStr
