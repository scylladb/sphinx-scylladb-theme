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
    result = build_redirect_body(path)
    assert "url=/redirect" in result
    assert "zendesk" not in result


def test_build_redirect_body_with_zendesk_tag():
    path = "/redirect"
    zendesk_tag = "test-zendesk-tag"

    # Call the function with a Zendesk tag
    result = build_redirect_body(path, zendesk_tag)

    # Check if the Zendesk meta tag is in the result
    assert zendesk_tag in result
    assert "url=/redirect" in result


def test_is_url_external():
    path = "https://scylladb.com"
    assert is_url(path)


def test_is_url_relative_path():
    path = "/relative_path"
    assert not is_url(path)
