import pytest
from bs4 import BeautifulSoup as bs

from sphinx_scylladb_theme.extensions.hero_box import HeroBox

test_data = [
    [
        [],
        {"title": "Lorem Ipsum", "class": "abc"},
        ["Content"],
        """
        <div class="hero">
                <div class="hero-wrapper">
                    <div class="hero-header">
                        <h1 class="hero__title">Lorem Ipsum</h1>
                        <div class="hero__text">
        """,
    ],
    [
        [],
        {"title": "Lorem Ipsum", "image": "image.png"},
        ["Content"],
        """
        <div class="hero">
                <div class="hero-wrapper">
                    <img class="hero__img" src="image.png" />
                    <div class="hero-header">
                        <h1 class="hero__title">Lorem Ipsum</h1>
                        <div class="hero__text">
        """,
    ],
]


@pytest.mark.parametrize("arguments, options, content, expected", test_data)
def test(arguments, options, content, expected):
    directive = HeroBox("component", arguments, options, content, 0, 0, "", None, None)
    result = directive.run()
    assert bs(result[0].astext(), "html.parser") == bs(expected, "html.parser")
