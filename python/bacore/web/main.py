"""BACore documentation with FastHTML.

# App:
- `live`: Start the app with `live=True`, to reload the webpage in the browser on any code change.

# Resources:
- FastHTML uses [Pico CSS](https://picocss.com).
"""

from bacore.interfaces.web_fasthtml import (
    Documentation,
    FuncFT,
    MarkdownFT,
    ModuleFT,
    doc_page,
    flexboxgrid,
)
from fasthtml.common import (
    A,
    FastHTML,
    HighlightJS,
    Li,
    MarkdownJS,
    Nav,
    Titled,
    Ul,
    picolink,
    serve,
)
from pathlib import Path

readme_file = MarkdownFT(path=Path("readme.md"), skip_title=True)
src_docs = Documentation(path=Path("python/bacore"), package_root="bacore")
tests_docs = Documentation(path=Path("tests"), package_root="tests")

headers = (
    flexboxgrid,
    HighlightJS(langs=["python", "html", "css"]),
    MarkdownJS(),
    picolink,
)
app = FastHTML(hdrs=headers, htmx=True, live=True)


def nav_main():
    """Main navigation menu, could also be called top nav."""
    return Nav(
        Ul(Li(A("Home", href="/"))),
        Ul(
            Li(A("Documentation", href="/docs")),
            Li(A("Github", href="https://github.com/bacoredev/bacore/")),
            Li(A("PyPi", href="https://pypi.org/project/bacore/")),
        ),
    )


@app.get("/")
def home():
    """The homepage for BACore."""
    return Titled(
        "BACore",
        nav_main(),
        readme_file,
        FuncFT(func=nav_main),
        ModuleFT(path=Path("python/bacore/web/main.py"), package_root="bacore"),
    )


@app.route("/docs/{path:path}", methods="get")
def docs(path: str):
    """Documentation pages."""
    return doc_page(doc_source=src_docs, url=path)


@app.route("/tests/{path:path}", methods="get")
def tests(path: str):
    """Test case pages."""
    return doc_page(doc_source=tests_docs, url=path)


serve(port=7001)
