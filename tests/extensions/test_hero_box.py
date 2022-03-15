import pytest
from bs4 import BeautifulSoup as bs

from sphinx_scylladb_theme.extensions.hero_box import HeroBox

test_data = [
    [
        [],
        {"title": "Lorem Ipsum", "class": "hero_test"},
        ["Content"],
        """
        <div class="hero hero_test">
                <div class="hero-wrapper">
                    <div class="hero__img">
                    </div>
                    <div class="hero-header">
                        <h1 class="hero__title">Lorem Ipsum</h1>
                        <div class="hero__text">
        """,
    ],
    [
        [],
        {"title": "Lorem Ipsum", "class": "hero_test", "image": "image.png"},
        ["Content"],
        """
        <div class="hero hero_test">
                <div class="hero-wrapper">
                    <div class="hero__img">
                        <img src="image.png" />
                    </div>
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
