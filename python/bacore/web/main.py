"""BACore documentation with FastHTML.

# App:
- `live`: Start the app with `live=True`, to reload the webpage in the browser on any code change.

# Resources:
- FastHTML uses [Pico CSS](https://picocss.com).


class DocsRouter:
    def __init__(self, docs_tree: Dict[str, ModuleModel]):
        self.docs_tree = docs_tree

    def create_sidebar(self) -> Nav:
        ""Create navigation sidebar from docs tree""
        nav_items = []

        # Group items by their top-level section
        sections = {}
        for path, module in self.docs_tree.items():
            if path.startswith('docs/'):
                parts = path[5:].split('/')  # Remove 'docs/' prefix
                section = parts[0] if len(parts) > 1 else 'root'
                if section not in sections:
                    sections[section] = []
                sections[section].append((path, module))

        # Create navigation structure
        for section, items in sorted(sections.items()):
            if section != 'root':
                section_items = [
                    Li(A(m.name, href=f"/{p}"))
                    for p, m in sorted(items, key=lambda x: x[1].name)
                ]
                nav_items.append(Li([
                    H1(section.title(), cls='nav-section'),
                    Ul(section_items, cls='nav-items')
                ]))

        return Nav(Ul(nav_items, cls='nav-list'), cls='docs-nav')

    def render_module(self, module: ModuleModel) -> Article:
        ""Render a module's documentation""
        return Article([
            H1(module.name.title()),
            P(f"Package: {module.package_root}"),
            Div(module.doc(), cls='marked')
        ])

    def render_404(self, path: str) -> Article:
        ""Render 404 page""
        return Article([
            H1("404 Not Found"),
            P(f"Documentation for '{path}' not found.")
        ])

@rt('/docs')
def docs_root():
    ""Render documentation home page""
    return Titled("Documentation", [
        docs_router.create_sidebar(),
        Article([
            H1("Documentation"),
            P("Select a module from the sidebar to view its documentation.")
        ])
    ])

@rt('/docs/{path:path}')
def docs_page(path: str):
    ""Render documentation for a specific path""
    # Normalize the path
    docs_path = f"docs/{path}"

    # Try to find the module
    module = docs_router.docs_tree.get(docs_path)

    # If not found directly, try with different casing or dash/underscore
    if module is None:
        normalized_path = docs_path.replace('-', '_').lower()
        for key in docs_router.docs_tree:
            if key.replace('-', '_').lower() == normalized_path:
                # Found a match with different formatting
                return Titled("Redirecting...",
                    A(f"Click here if not redirected automatically",
                      href=f"/docs/{key[5:]}",
                      cls="button"))

    # Render the page
    return Titled(
        f"Documentation - {path.title()}" if module else "404 Not Found",
        [
            docs_router.create_sidebar(),
            docs_router.render_module(module) if module else docs_router.render_404(path)
        ]
    )
"""
from bacore.interfaces.web_fasthtml import Documentation, readme_page
from fasthtml.common import A, Div, HighlightJS, H1, H2, H3, H4, Li, P, Ul, MarkdownJS, Titled, fast_app, serve
from pathlib import Path


hdrs = (MarkdownJS(), HighlightJS(langs=['python', 'html', 'css']), )
docu = Documentation(path=Path('python/bacore'), package_root='bacore', base_url='docs')


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


def non_wrapped_function():
    """lite text"""
    return "hi"


@rt('/{path:path}')
def docs(path: str):
    """Dirty implementation of the Documentation (future) component.

    The **Module Classes** function has to be recursive in the same way as
    `map_path_to_module` in `interfaces/web_fasthtml` is.

    """

    module = docu.docs_tree().get(path)
    if module is None:
        raise ValueError(f'404 module "{path}" does not exist')

    funcs = module.functions()
    classes = module.classes()

    return Titled(module.name.title(),
                  Div(module.doc(), cls='marked'),
                  Div(
                      H1('Module Functions'),
                      Ul(*[Li(func.name.title()) for func in funcs]),
                      Div(*[(H2(func.name.title()), P(func.doc, cls='marked')) for func in funcs])
                  ) if funcs else '',
                  Div(
                      H1('Module Classes'),
                      Ul(*[Li(klass.name.title()) for klass in classes]),
                      Div(*[(H2(klass.name.title()), P(klass.doc, cls='marked'),
                          Div(
                              H3('Class Functions'),
                              Ul(*[Li(class_func.name.title()) for class_func in klass.functions()]),
                              Div(*[(H4(class_func.name.title()), P(class_func.doc, cls='marked')) for class_func in klass.functions()])
                              ) if klass.functions() else "",
                          Div(
                              H3('Sub-Classes'),
                              Ul(*[Li(sub_class.name.title()) for sub_class in klass.classes()]),
                              Div(*[(H4(sub_class.name.title()), P(sub_class.doc, cls='marked')) for sub_class in klass.classes()])
                              ) if klass.classes() else "",
                          ) for klass in classes]),
                  ) if classes else ''
                  )

serve(port=7001)
