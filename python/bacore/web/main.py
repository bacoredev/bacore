"""BACore documentation with FastHTML.

# App:
- `live`: Start the app with `live=True`, to reload the webpage in the browser on any code change.

# Resources:
- FastHTML uses [Pico CSS](https://picocss.com).
"""
from bacore.interfaces.web_fasthtml import div_from_markdown, module_doc
from fasthtml.common import A, Div, HighlightJS, Li, P, Ul, MarkdownJS, Titled, fast_app, serve
from pathlib import Path


hdrs = (MarkdownJS(), HighlightJS(langs=['python', 'html', 'css']), )


def todo_renderer(todo):
    return Li(todo.title + (' ✅' if todo.done else ''))


app, rt, todos, Todo = fast_app(db_file='data/todos.db',
                                live=True,
                                render=todo_renderer,
                                hdrs=hdrs,
                                id=int,
                                title=str,
                                done=bool,
                                pk='id')


def num_list(up_to_and_including: int):
    return Ul(*[Li(num) for num in range(up_to_and_including + 1) if num != 0], id='num_list', title='Very cool list')


NumList = num_list


@rt('/')
def home():
    return Titled("BACore",
                  div_from_markdown(file=Path('README.md')),
                  P(A('See the docs', href='/docs')),
                  P(A('Todos', href='/todos')),  # Does not have to be a link, but could be anything.
                  id=1)


@rt('/docs')
def docs():
    """The documentation information."""
    return Titled('Docs',
                  P(
                      A('Back', href='/')),
                  P('Docs section:',
                    Ul(
                        Li('Domains',
                           Ul(
                               Li(A('Errors', href="/docs/domain/errors")),
                               Li(A('Files', href="/docs/domain/files")),
                               Li(A('Settings', href="/docs/domain/settings"))
                           )),
                        Li('Interactors',
                            Ul(
                                 Li(A('Source Code Reader', href="/docs/interactors/source_code_reader"))
                            ))
                    ))
                  )


@rt('/docs/domain/errors')
def docs_domain_errors():
    return module_doc(module_name='bacore.domain.errors', doc_title="Errors")


@rt('/docs/domain/files')
def docs_domain_files():
    return module_doc(module_name='bacore.domain.files', doc_title="Files")


@rt('/docs/domain/settings')
def docs_domain_settings():
    return module_doc(module_name='bacore.domain.settings', doc_title="Settings")


@rt('/docs/interactors/source_code_reader')
def docs_interactors_source_code_reader():
    return module_doc(module_name='bacore.interactors.source_code_reader', doc_title="Source Code Reader")


@rt('/todos')
def todos_():
    return Titled('Todos',
                  P(A('Add Todo', hx_get='/todos/add'),
                    Div(' '),  # Would like to ad some space here
                    A('Back', href='/')),
                  Ul(*todos()))


@rt('/todos/add')
def todos_add():
    return Titled('Todos Add',
                  todos.insert(Todo(title="Sixth todo", done=False)),
                  P(A('Back', href='/todos'))
                  )


serve()
