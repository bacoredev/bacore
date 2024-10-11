"""FastHTML web interface tests."""
import pytest
from bacore.interfaces import web_fasthtml


@pytest.mark.skip
def test_module_doc():
    doc_text = web_fasthtml.module_doc(module_name="bacore.domain.settings", doc_title="Settings")
    assert doc_text == ""
