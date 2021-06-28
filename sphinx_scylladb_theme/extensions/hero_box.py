"""
Sphinx directive for HTML Hero Components.
"""
from docutils import nodes
from docutils.parsers.rst import Directive, directives

from .utils import generate_template


class HeroBox(Directive):
    has_content = True
    option_spec = {
        "title": directives.unchanged_required,
        "text": directives.unchanged_required,
        "image": directives.path,
    }

    def run(self):
        class_name = "hero"

        image = self.options.get("image")
        image = (
            generate_template(
                """
            <img class="{class_name}__img" src="{image}" />
            """,
                image=image,
                class_name=class_name,
            )
            if image
            else ""
        )

        html_tag_open = generate_template(
            """
            <div class="hero">
                <div class="hero-wrapper">
                    <h1 class="{class_name}__title">{title}</h1>
                    {image}
                    <div class="{class_name}__text">
            """,
            title=self.options.get("title", ""),
            image=image,
            class_name=class_name,
        )
        html_tag_close = "</div></div></div>"

        description_node = nodes.container()
        if self.state:
            self.state.nested_parse(self.content, 0, description_node)

        return [
            nodes.raw(text=html_tag_open, format="html"),
            description_node,
            nodes.raw(text=html_tag_close, format="html"),
        ]


def setup(app):
    app.add_directive("hero-box", HeroBox)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
