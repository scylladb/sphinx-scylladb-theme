from unittest.mock import Mock

from bs4 import BeautifulSoup

from sphinx_scylladb_theme.extensions.navigation import relativize_and_mark_current


def _run(html, docname, target_uri):
    builder = Mock()
    builder.get_target_uri = Mock(return_value=target_uri)
    soup = BeautifulSoup(html, "html.parser")
    relativize_and_mark_current(soup, docname, builder)
    return soup


def test_html_target_is_not_suffixed_again():
    # multiversion builder already yields rendered URLs ending in .html
    soup = _run(
        '<ul><li><a href="installation.html">i</a></li></ul>',
        "getting-started/index",
        "getting-started/index.html",
    )
    assert soup.a["href"] == "../installation.html"


def test_trailing_slash_and_fragment_preserved():
    soup = _run(
        '<a href="guide/#sec">g</a>', "index", "index/"
    )
    assert soup.a["href"] == "../guide/#sec"


def test_current_page_marked():
    soup = _run(
        '<ul><li><a href="a.html">a</a></li></ul>', "a", "a.html"
    )
    assert soup.a["href"] == "#"
    assert "current" in soup.a["class"] and "current" in soup.li["class"]
