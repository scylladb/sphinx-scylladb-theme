"""
Sphinx directive for HTML Grid Components.
"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from .utils import generate_template


class Grid(Directive):
    has_content = True
    option_spec = {
        "class": directives.unchanged,
        "type": directives.unchanged,  # 'default', 'scrollable', 'products'
        "title": directives.unchanged,
        "text": directives.unchanged,
    }

    def run(self):
        class_name = "topics-grid"
        container_class_name = self.options.get("class", "")

        # Add type modifier
        grid_type = self.options.get("type", "default")
        if grid_type in ["scrollable", "products"]:
            container_class_name = f"{container_class_name} topics-grid--{grid_type}".strip()

        # Generate title and text if provided
        title = self.options.get("title", "")
        text = self.options.get("text", "")
        
        header = ""
        if title or text:
            header = generate_template(
                """
                <h2 class="topics-grid__title">{title}</h2>
                <p class="topics-grid__text">{text}</p>
                """,
                title=title,
                text=text,
            )

        html_tag_open = generate_template(
            """
            <div class="{class_name} {container_class_name}">
                {header}
                <div class="grid-container full">
                    <div class="grid-x grid-margin-x{scrollable_class}">
            """,
            class_name=class_name,
            container_class_name=container_class_name,
            header=header,
            scrollable_class=" hs" if grid_type == "scrollable" else "",
        )
        html_tag_close = "</div></div></div>"

        # Parse content directly without container wrapper
        content_nodes = []
        if self.state:
            self.state.nested_parse(self.content, 0, content_nodes)

        return [
            nodes.raw(text=html_tag_open, format="html"),
            *content_nodes,
            nodes.raw(text=html_tag_close, format="html"),
        ]


def setup(app):
    app.add_directive("grid", Grid)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    } 