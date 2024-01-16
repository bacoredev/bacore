"""BACore CLI entrypoint module."""
from bacore.cli import create, serve
from bacore.domain import files
from bacore.interfaces import cli_typer
from typer import Typer

pyproject_file = files.TOML(path=files.Path("pyproject.toml"))
project_info = cli_typer.ProjectInfo(pyproject_file=pyproject_file)

app = Typer(rich_markup_mode="rich", add_completion=False)
app.add_typer(create.app, name="create", help="Create a project")
app.add_typer(serve.app, name="serve", help="Serve documentation")

if __name__ == "__main__":
    print(f"{project_info.name} v.{project_info.version}")