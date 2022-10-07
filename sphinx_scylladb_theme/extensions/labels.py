"""
Sphinx directive for HTML Label Components.
"""
from docutils import nodes
from docutils.parsers.rst import Directive, directives

from .utils import generate_template


class Label(Directive):
    has_content = True
    option_spec = {
        "class": directives.unchanged,
        "style": directives.unchanged,
        "text": directives.unchanged,
    }

    def run(self):
        class_name = "label"
        container_class_name = self.options.get("class", "")
        style_name = "label--" + self.options.get("style", "")
        text = self.options.get("text", "")

        html0 = generate_template(
            """
            <span class="{container_class_name}">
            """,
            container_class_name=container_class_name,
            class_name=class_name,
            text=self.options.get("text", ""),
        )

        html1 = "</span>"

        text_node = nodes.inline(text=text, classes=["label", style_name])

        return [
            nodes.raw(text=html0, format="html"),
            text_node,
            nodes.raw(text=html1, format="html"),
        ]


def setup(app):
    app.add_directive("label", Label)
    app.add_role("label", Label)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
