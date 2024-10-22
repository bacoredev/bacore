"""FastHTML web interface."""
from bacore.domain.source_code import ModuleModel
from bacore.interactors.file_handler import read_markdown_file
from fasthtml.common import A, Div, Li, P, Ul, Titled
from pathlib import Path


def div_from_markdown(file: Path, skip_title: bool = True) -> Div:
    return Div(read_markdown_file(file=file, skip_title=skip_title), cls='marked')
