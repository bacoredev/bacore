"""FastHTML web interface."""
import inspect
from bacore.interactors.file_handler import read_markdown_file
from bacore.interactors.source_code_reader import get_module_from_name, is_member_of_module
from fasthtml.common import A, Div, Li, P, Ul, Titled
from pathlib import Path


def div_from_markdown(file: Path, skip_title: bool = True) -> Div:
    return Div(read_markdown_file(file=file, skip_title=skip_title), cls='marked')


def module_doc(module_name: str, doc_title: str):
    module = get_module_from_name(module_name=module_name)

    all_members = inspect.getmembers(module)

    my_members = [
        member for name, member in all_members
        # if (inspect.isclass(member) or inspect.isfunction(member)) and is_member_of_module(member, module_name)
        if is_member_of_module(member, module_name)
    ]

    return Titled(doc_title,
                  P(A('Back', href="/docs")),
                  Div(module.__doc__, cls='marked'),
                  Div(P('Here comes more information:'),
                      Ul(*[Li(member.__name__) for member in my_members]))
                  )
