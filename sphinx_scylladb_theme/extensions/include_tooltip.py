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
        f'<span data-tooltip data-tooltip-height="0" tabindex="1" title="{tooltip_text}" class="top">'
    )

def depart_include_tooltip_node_html(self, node):
    self.body.append('</span>')

def get_tooltip_from_glossary(tooltip_source, inliner):
    env = inliner.document.settings.env
    std_domain = env.get_domain('std')
    glossary_terms = std_domain._terms
    term_info = glossary_terms.get(tooltip_source.lower(), None)
    if term_info:
        docname, labelid = term_info
        try:
            doctree = env.get_doctree(docname)
            term_node = doctree.ids.get(labelid)

            if term_node and term_node.parent:
                definition_node = None
                for sibling in term_node.parent:
                    if isinstance(sibling, nodes.definition):
                        definition_node = sibling
                        break

                if definition_node:
                    return definition_node.astext()
        except Exception as e:
            pass
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

