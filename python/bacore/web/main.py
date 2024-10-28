"""BACore documentation with FastHTML.

# App:
- `live`: Start the app with `live=True`, to reload the webpage in the browser on any code change.

# Resources:
- FastHTML uses [Pico CSS](https://picocss.com).
"""
from bacore.interfaces.web_fasthtml import Documentation, doc_page, readme_page
from fasthtml.common import HighlightJS, MarkdownJS, fast_app, serve
from pathlib import Path

hdrs = (MarkdownJS(), HighlightJS(langs=['python', 'html', 'css']), )
documentation = Documentation(path=Path('python/bacore'), package_root='bacore', base_url='docs')


app, rt, todos, Todo = fast_app(db_file='data/todos.db',
                                live=True,
                                hdrs=hdrs,
                                id=int,
                                title=str,
                                done=bool,
                                pk='id')


@rt('/')
def home():
    """The homepage for BACore."""
    return readme_page(title="BACore", readme_file=Path('README.md'))


@rt('/{path:path}')
def docs(path: str):
    """Documentation pages."""
    return doc_page(doc_source=documentation, url=path)


serve(port=7001)
