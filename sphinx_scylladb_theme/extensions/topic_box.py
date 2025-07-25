"""
Sphinx directive for HTML Topic Box Components.
"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives
import os

from .utils import generate_template, is_url, resolve_link


class TopicBox(Directive):
    has_content = True
    option_spec = {
        "title": directives.unchanged_required,
        "link": directives.path,
        "link_target": directives.path,
        "anchor": directives.path,
        "icon": directives.path,
        "icon_color": directives.path, # unused, left for compatibility
        "image": directives.path,
        "class": directives.unchanged,
    }

    def run(self):
        class_name = "topic-box"
        container_class_name = self.options.get("class", "").replace(",", " ")

        link = self.options.get("link")
        link_target = self.options.get("link_target", "auto")
        target_attr = ""
        
        if link:
            env = self.state.document.settings.env
            link = resolve_link(link, env)
            if link_target == "_blank":
                target_attr = 'target="_blank"'
            elif link_target == "auto" and is_url(link):
                target_attr = 'target="_blank"'

        link_template = """
            <div class="{class_name} {container_class_name}">
                <div class="card">
            """
        if link:
            link_template = f"""
                <div class="cell {class_name} {container_class_name}">
                    <a class="card" href="{link}" {target_attr}>
                """

        html_tag_open = generate_template(
            link_template,
            class_name=class_name,
            container_class_name=container_class_name,
            link=link,
        )
        html_tag_close = "</a></div>" if link else "</div></div>"

        icon = self.options.get("icon")
        icon_color = self.options.get("icon_color", "#23263b")
        image = self.options.get("image")

        html_icon = (
            generate_template(
                """
            <div class="{class_name}__icon">
                <i class="{icon}"></i>
            </div>
            """,
                class_name=class_name,
                icon=icon,
                icon_color=icon_color,
            )
            if icon
            else generate_template(
                """
            <div class="{class_name}__icon"">
                <img src="{image}"/>
            </div>
            """,
                class_name=class_name,
                image=image,
            )
            if image
            else ""
        )

        anchor = self.options.get("anchor")
        anchor = (
            generate_template(
                """
                <div class="{class_name}__anchor">{anchor}
                 <i class="icon-newtab" aria-hidden="true"></i>
                </div>
                """
                if target_attr == 'target="_blank"'
                else """
                <div class="{class_name}__anchor">{anchor}</div>
                """,
                class_name=class_name,
                anchor=anchor,
            )
            if anchor
            else ""
        )

        html0 = generate_template(
            """
            {html_tag_open}
                <div class="{class_name}__head">
                {html_icon}
                <h3 class="{class_name}__title">{title}</h3>
                </div>
                <div class="{class_name}__body">
            """,
            class_name=class_name,
            html_tag_open=html_tag_open,
            html_icon=html_icon,
            title=self.options.get("title", ""),
        )
        html1 = generate_template(
            """
            {anchor}
            </div>
            {html_tag_close}
            """,
            anchor=anchor,
            class_name=class_name,
            html_tag_close=html_tag_close,
        )

        description_node = nodes.container()
        if self.state:
            self.state.nested_parse(self.content, 0, description_node)

        return [
            nodes.raw(text=html0, format="html"),
            description_node,
            nodes.raw(text=html1, format="html"),
        ]


def setup(app):
    app.add_directive("topic-box", TopicBox)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
