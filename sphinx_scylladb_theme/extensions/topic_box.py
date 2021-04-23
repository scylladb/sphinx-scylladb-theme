"""
Sphinx directive for creating cards in a grid layout.
"""
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from .utils import generate_template, generate_styles, generate_content

class TopicBox(Directive):
    has_content = True
    option_spec = {
        'title': directives.unchanged_required,
        'link': directives.path,
        'icon': directives.path,
        'icon_color': directives.path,
        'icon_bg': directives.path,
        'image': directives.path,
        'last_updated': directives.unchanged_required,
        'class': directives.unchanged,
    }

    def run(self):
        class_name = 'topic-box'
        container_class_name = self.options.get('class', 'small-6 large-3').replace(',', ' ')

        link = self.options.get('link')
        html_tag_open = generate_template('''
            <div class="cell {container_class_name}">
            <a class="{class_name}" href="{link}">
            ''' if link else '''
            <div class="{container_class_name}">
            <div class="{class_name}">
            ''',
            container_class_name=container_class_name,
            class_name=class_name,
            link=link,
        )
        html_tag_close = '</a></div>' if link else '</div></div>'
        
        icon = self.options.get('icon')
        icon_color = self.options.get('icon_color', '#23263b')
        icon_bg = self.options.get('icon_bg', 'transparent')
        image = self.options.get('image')

        html_icon = generate_template('''
            <div class="{class_name}__icon" style="background-color: {icon_bg}">
                <i class="{icon}" style="color:{icon_color}"></i>
            </div>
            ''',
            class_name=class_name,
            icon=icon,
            icon_color= icon_color,
            icon_bg = icon_bg,
        ) if icon else generate_template('''
            <div class="{class_name}__icon"">
                <img src="/_static/{image}"/>
            </div>
            ''',
            class_name=class_name,
            image=image,
        ) if image else ''

        last_updated = self.options.get('last_updated')
        html_last_updated = generate_template('''
            <div class="{class_name}__subtitle">Last updated: {last_updated}</div>
            ''',
            class_name=class_name,
            last_updated=last_updated,
        ) if last_updated else ''

        html0 = generate_template('''
            {html_tag_open}
                <div class="{class_name}__head">
                    {html_icon}
                    <div class="{class_name}-head-content">
                        <h3 class="{class_name}__title">{title}</h3>
                        {html_last_updated}
                    </div>
                </div>
                <div class="{class_name}__body">
            ''',
            class_name=class_name,
            html_tag_open=html_tag_open,
            html_icon=html_icon,
            html_last_updated=html_last_updated,
            title=self.options.get('title', ''),
        )
        html1 = generate_template('''
                </div>
            {html_tag_close}
            ''',
            class_name=class_name,
            html_tag_close=html_tag_close,
        )

        description_node = nodes.container()
        self.state.nested_parse(self.content, 0, description_node)

        return [
            nodes.raw(text=html0, format='html'),
            description_node,
            nodes.raw(text=html1, format='html'),
        ]


def setup(app):
    app.add_directive("topic-box", TopicBox)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
