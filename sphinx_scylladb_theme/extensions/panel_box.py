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

        html0 = generate_template('''
                <div class="panel callout radius animated">
                   <div class="row">
                      <div class="medium-3 columns">
                         <h5 id={id}>{title}</h5>
              </div>
              <div class="medium-9 columns">
            ''',
            class_name=class_name,
                                  title=self.options.get('title', ''),
            id=self.options.get('id', '')
        )

        html1 = generate_template('''
        </div></div></div>
            ''',
        class_name=class_name
        )

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
