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
        "class": directives.path,
        "text": directives.unchanged_required,
        "cta": directives.unchanged_required,
        "image": directives.path,
        "button_style": directives.path,
        "button_icon": directives.path,
        "button_icon_position": directives.path,
        "button_icon_link": directives.flag,
        "button_url": directives.path,
        "button_text": directives.path,
        "search_box": directives.flag,
    }

    def run(self):
        class_name = "hero"
        container_class_name = self.options.get("class", "")

        image = self.options.get("image")
        image = (
            generate_template(
                """
                <img src="{image}" />
                """,
                image=image,
            )
            if image
            else ""
        )

        cta = self.options.get("cta")
        button_icon_position = self.options.get("button_icon_position")
        button_style = self.options.get("button_style")
        button_icon = self.options.get("button_icon")
        button_icon_link = "button_icon_link" in self.options
        button_url = self.options.get("button_url")
        button_text = self.options.get("button_text")

        button_content = f"{button_text}"
        if cta:
            button_content += f" <span class='{class_name}__cta'>{cta}</span>"
        icon_link_class = "icon--link" if button_icon_link else ""
        if button_icon_position == "right":
            button_content = f"{button_content}<i class='icon icon--right {icon_link_class} {button_icon}' aria-hidden='true'></i>"
        else:
            button_content = f"<i class='icon icon--left {icon_link_class} {button_icon}' aria-hidden='true'></i>{button_content}"

        button_class = f"{class_name}__button button"

        if button_style == "bold":
            button_class += f" {class_name}__button--bold"

        button = (
            generate_template(
                """
                <a href="{button_url}">
                <button class="{button_class}">
                {button_content}
                </button>
                </a>
                """,
                button_content=button_content,
                button_url=button_url,
                button_class=button_class,
            )
            if button_text
            else ""
        )

        has_search_box = "search_box" in self.options
        search_box = (
            generate_template(
                """
                <div class="{class_name}__search-box search-box search-box--hero">
                <ci-search></ci-search>
                </div>
                """,
                class_name=class_name,
            )
            if has_search_box
            else ""
        )

        html_tag_open = generate_template(
            """
            <div class="{class_name} {container_class_name}">
                <div class="{class_name}-wrapper">
                    <div class="{class_name}__img">
                    {image}
                    </div>
                    <div class="{class_name}-header">
                        <h1 class="{class_name}__title">{title}</h1>
                        <div class="{class_name}__text">
            """,
            title=self.options.get("title", ""),
            image=image,
            class_name=class_name,
            container_class_name=container_class_name,
        )
        html_tag_close = generate_template(
            """</div>{button}{search_box}</div></div></div>""",
            button=button,
            search_box=search_box,
        )
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
