"""BACore documentation with FastHTML.

# App:
- `live`: Start the app with `live=True`, to reload the webpage in the browser on any code change.

# Resources:
- FastHTML uses [Pico CSS](https://picocss.com).
"""
from bacore.interactors.source_code_reader import SrcDir, SrcFile, package_init_file
from bacore.interfaces.web_fasthtml import div_from_markdown
from fasthtml.common import A, Div, HighlightJS, Li, P, Ul, MarkdownJS, Titled, fast_app, serve
from pathlib import Path
from typing import Optional


hdrs = (MarkdownJS(), HighlightJS(langs=['python', 'html', 'css']), )


app, rt, todos, Todo = fast_app(db_file='data/todos.db',
                                live=True,
                                hdrs=hdrs,
                                id=int,
                                title=str,
                                done=bool,
                                pk='id')


def num_list(up_to_and_including: int):
    return Ul(*[Li(num) for num in range(up_to_and_including + 1) if num != 0], id='num_list', title='Very cool list')


NumList = num_list

bacore_pkg = SrcDir(path=Path('python/bacore'), package_root='bacore')


@rt('/')
def home():
    return Titled("BACore",
                  div_from_markdown(file=Path('README.md')),
                  P(A('See the docs', href='/docs')),
                  id=1)


@rt('/docs')
def docs():
    bacore_init = package_init_file(package_path=Path('python/bacore'), package_root='bacore')
    return Titled('Documentation',
                  P(A('Back', href='/')),
                  Div(Ul(*[Li(A(src_file.name.title(), href=f'/docs/{src_file.name}')) for src_file in bacore_pkg.src_files])),
                  Div(P(bacore_init.doc(), cls='marked'))
                  )


@rt('/docs/{doc_page}')
def docs_file(doc_page: str):
    src_dir = SrcDir(path=Path('python/bacore'), package_root='bacore')
    pages = src_dir.src_files
    found_page = None

    for page in pages:
        if page.name == doc_page:
            found_page = page
            break

    if not found_page:
        raise FileNotFoundError(f"404 file not found {doc_page} {page}")

    return Titled(page.name.title(),
                  P(A('Back', href='/')),
                  Div(P(page.path, cls='marked')),
                  Div(P(page.doc(), cls='marked'))
                 )


serve(port=7001)
