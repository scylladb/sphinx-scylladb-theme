from sphinx_scylladb_theme.extensions.utils import (
    build_redirect_body,
    generate_template,
    is_url,
)


def test_generate_content():
    expected = "<div>Hello World!</div>"
    result = generate_template(
        """
            <div>{value_a} {value_b}!</div>
            """,
        value_a="Hello",
        value_b="World",
    )
    assert result.split() == expected.split()


def test_build_redirect_body():
    path = "/redirect"
    expected_output = """
    <html>
    <head>
    <meta http-equiv="refresh" content="0; url=/redirect">
    </head>
    </html>
    """
    assert build_redirect_body(path) == expected_output


def test_is_url_external():
    path = "https://scylladb.com"
    assert is_url(path)


def test_is_url_relative_path():
    path = "/relative_path"
    assert not is_url(path)
