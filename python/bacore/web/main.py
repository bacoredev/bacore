"""BACore documentation with FastHTML.

# App:

- `live`: Start the app with `live=True`, to reload the webpage in the browser on any code change.

# Resources:

- FastHTML uses [Pico CSS](https://picocss.com).
"""
# from fasthtml.common import *
import bacore
import inspect
from fasthtml.common import A, Div, HighlightJS, Li, P, Ul, MarkdownJS, Titled, fast_app, serve
from types import ModuleType

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


def NumList(up_to_and_including: int):
    return Ul(*[Li(num) for num in range(up_to_and_including + 1) if num != 0], id='num_list', title='Very cool list')


def module_doc(module: ModuleType):
    return Div(inspect.getdoc(module), cls='marked')


@rt('/')
def home():
    return Titled("BACore",
                  module_doc(bacore),
                  module_doc(config),
                  # Div(bacore, cls='marked'),
                  todos.insert(Todo(title="Fifth todo", done=False)),
                  Div(P('I am alive more alive, even more.')),
                  NumList(5),
                  P(A('Link', href='/change')),
                  P(A('Google', href='https://google.com')),
                  P(A('Todos', hx_get='/todos')),  # Does not have to be a link, but could be anything.
                  P(A('See the docs', hx_get='/docs')),
                  P(A('Config docs', href='/config')),
                  id=1)


@rt('/change')
def change():
    return Titled('Some change',
                  Div(P('Change is good')),
                  P(A('Link', href='/')),
              )


@rt('/config')
def get():
    return Titled('Config',
                  module_doc(config),
                  P(A('Back', href='/')),
                  id='config')

@rt('/todos')
def get():
    return Titled('Todos',
                  Ul(*todos()))


@rt('/docs')
def get():
    """The documentation information."""
    return Titled('Docs',
                  Div(__doc__, cls='marked'))

serve()
