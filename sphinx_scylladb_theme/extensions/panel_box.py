"""
Sphinx directive that renders a group of links together in a panel box.
"""
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from .utils import generate_template, generate_styles, generate_content

class PanelBox(Directive):
    has_content = True
    option_spec = {
        'title': directives.unchanged_required,
        'id': directives.unchanged,
        'class': directives.unchanged
    }

    def run(self):
        class_name = 'panel-box'
        container_class_name = self.options.get('class', '')

        html0 = generate_template('''
        <div class="cell {container_class_name}">
                <div class="{class_name}">
                <h5 id={id} class="{class_name}__title">{title}</h5>
            ''',
            container_class_name = container_class_name,
            class_name=class_name,
            title=self.options.get('title', ''),
            id=self.options.get('id', '')
        )

        html1 = '</div></div>'

        description_node = nodes.container()
        self.state.nested_parse(self.content, 0, description_node)

        return [
            nodes.raw(text=html0, format='html'),
            description_node,
            nodes.raw(text=html1, format='html'),
        ]


def setup(app):
    app.add_directive("panel-box", PanelBox)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
