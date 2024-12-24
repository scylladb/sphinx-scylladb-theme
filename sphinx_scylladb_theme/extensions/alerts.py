"""
Sphinx directive for HTML Alert Components with target option.
"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from .utils import generate_template


class Alert(Directive):
    has_content = True
    option_spec = {
        "link": directives.unchanged_required,
        "link_text": directives.unchanged_required,
        "icon": directives.unchanged,
        "target": directives.unchanged,
    }

    def run(self):
        class_name = "alert"
        icon_class = self.options.get("icon", "logs")
        link = self.options.get("link", "")
        link_text = self.options.get("link_text", "")
        target = self.options.get("target", "_self")

        if target == "_blank":
            target_attr = 'target="_blank"'
        else:
            target_attr = ''

        html0 = generate_template(
            """
            <div class="{class_name}">
                <div><i class="icon-{icon_class}"></i> {content}</div>
                <div><a href="{link}" {target_attr}>{link_text} <i class="icon-arrow-right"></i></a></div>
            </div>
            """,
            class_name=class_name,
            icon_class=icon_class,
            link=link,
            link_text=link_text,
            target_attr=target_attr,
            content=self.content[0] if self.content else "",
        )

        alert_node = nodes.raw(text=html0, format="html")
        
        return [alert_node]


def setup(app):
    app.add_directive("alert", Alert)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
