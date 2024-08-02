"""
This extension defines a custom Sphinx role, `:include_tooltip:`, to create tooltips
that can either contain inline text or load terms from the glossary.
"""

from docutils import nodes
from docutils.parsers.rst import roles
from sphinx.util import logging

LOGGER = logging.getLogger(__name__)

class include_tooltip_node(nodes.inline, nodes.Element):
    pass

def visit_include_tooltip_node_html(self, node):
    tooltip_text = node['tooltip']
    self.body.append(
        f'<span data-tooltip tabindex="1" title="{tooltip_text}">'
    )

def depart_include_tooltip_node_html(self, node):
    self.body.append(' <i class="scylla-icon scylla-icon--help"></i></span>')

def get_tooltip_from_glossary(tooltip_source, inliner):
    try:
        env = inliner.document.settings.env
        glossary = env.domains['std'].data['terms']
        if tooltip_source in glossary:
            return ''.join([term.astext() for term in glossary[tooltip_source]])
    except KeyError:
        LOGGER.warning(f"Glossary term '{tooltip_source}' not found.")
    return None

def get_tooltip_from_text(tooltip_source):
    return tooltip_source

def include_tooltip_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    if '<' in text and '>' in text:
        start_index = text.index('<')
        end_index = text.rindex('>')
        main_text = text[:start_index].strip()
        tooltip_source = text[start_index + 1:end_index].strip()
    else:
        msg = inliner.reporter.error(
            "Invalid syntax for include_tooltip role. Expected format: 'display text <tooltip text or term or file>'",
            line=lineno
        )
        return [inliner.problematic(rawtext, rawtext, msg)], [msg]

    tooltip_text = (
        get_tooltip_from_glossary(tooltip_source, inliner) or
        get_tooltip_from_text(tooltip_source)
    )

    tooltip_text = tooltip_text.replace('\n', '<br>')
    
    node = include_tooltip_node(main_text, main_text)
    node['tooltip'] = tooltip_text
    
    return [node], []

def setup(app):
    roles.register_local_role('include_tooltip', include_tooltip_role)
    app.add_node(include_tooltip_node, html=(visit_include_tooltip_node_html, depart_include_tooltip_node_html))
    
    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
