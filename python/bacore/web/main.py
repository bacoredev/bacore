"""BACore documentation with FastHTML.

# App:
- `live`: Start the app with `live=True`, to reload the webpage in the browser on any code change.

# Resources:
- FastHTML uses [Pico CSS](https://picocss.com).
"""

from bacore.interfaces.web_fasthtml import (
    Documentation,
    doc_page,
    flexboxgrid,
    readme_page,
)
from fasthtml.common import FastHTML, HighlightJS, MarkdownJS, picolink, serve
from pathlib import Path

src_docs = Documentation(path=Path("python/bacore"), package_root="bacore")
tests_docs = Documentation(path=Path("tests"), package_root="tests")


headers = (
    flexboxgrid,
    HighlightJS(langs=["python", "html", "css"]),
    MarkdownJS(),
    picolink,
)
app = FastHTML(hdrs=headers, htmx=True, live=True)


@app.get("/")
def home():
    """The homepage for BACore."""
    return readme_page(title="BACore", readme_file=Path("README.md"))


@app.route("/docs/{path:path}", methods="get")
def docs(path: str):
    """Documentation pages."""
    return doc_page(doc_source=src_docs, url=path)


@app.route("/tests/{path:path}", methods="get")
def tests(path: str):
    """Test case pages."""
    return doc_page(doc_source=tests_docs, url=path)


serve(port=7001)
