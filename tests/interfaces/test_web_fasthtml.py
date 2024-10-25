"""FastHTML web interface tests."""
from bacore.domain.source_code import ModuleModel
from bacore.interfaces.web_fasthtml import Documentation, readme_page
from starlette.requests import Request
from pathlib import Path
from random import choice


def test_readme_page():
    assert isinstance(readme_page(title="BACore", readme_file=Path('README.md')), tuple)


class TestDocumentation:
    docs = Documentation(path=Path('python/bacore'),
                         package_root='bacore',
                         base_url='docs')

    def test_docs_tree(self):
        url = choice(list(self.docs.docs_tree().keys()))
        assert isinstance(url, str), url
        assert isinstance(self.docs.docs_tree().get(url), ModuleModel), self.docs.docs_tree()
