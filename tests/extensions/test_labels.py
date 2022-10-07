import pytest
from bs4 import BeautifulSoup as bs

from sphinx_scylladb_theme.extensions.panel_box import Label

test_data = [
    [
        [],
        {"class": "abc"},
        ["Label"],
        """
        <span class="abc">
        """,
    ],
]


@pytest.mark.parametrize("arguments, options, content, expected", test_data)
def test(arguments, options, content, expected):
    directive = Label("component", arguments, options, content, 0, 0, "", None, None)
    result = directive.run()
    assert (
        bs(result[0].astext(), "html.parser").prettify()
        == bs(expected, "html.parser").prettify()
    )
