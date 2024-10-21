"""
This extension defines a custom Sphinx role, `:include_tooltip:`, to create tooltips
that can either contain inline text or load terms from the glossary.
"""

from docutils import nodes
from docutils.parsers.rst import roles
from sphinx.util import logging
from sphinx.transforms.post_transforms import SphinxPostTransform

LOGGER = logging.getLogger(__name__)

class include_tooltip_node(nodes.inline, nodes.Element):
    pass

def visit_include_tooltip_node_html(self, node):
    tooltip_text = node.get('tooltip', '')
    self.body.append(
        f'<span data-tooltip data-tooltip-height="0" tabindex="1" title="{tooltip_text}" class="top">'
    )

def depart_include_tooltip_node_html(self, node):
    self.body.append('</span>')

class TooltipPostTransform(SphinxPostTransform):
    default_priority = 500 

    def apply(self, **kwargs):
        env = self.env
        std_domain = env.get_domain('std')
        glossary_terms = std_domain._terms

        for node in self.document.traverse(include_tooltip_node):
            tooltip_source = node.get('tooltip_source', '').lower()
            tooltip_text = node.get('tooltip_source', '')

            if tooltip_source in glossary_terms:
                docname, labelid = glossary_terms[tooltip_source]
                try:
                    doctree = env.get_doctree(docname)
                    term_node = doctree.ids.get(labelid)

                    if term_node and term_node.parent:
                        for sibling in term_node.parent:
                            if isinstance(sibling, nodes.definition):
                                tooltip_text = sibling.astext()
                                break
                except Exception as e:
                    LOGGER.error(f"Error retrieving tooltip from glossary during post-transform: {e}")
            
            node['tooltip'] = tooltip_text

def include_tooltip_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    if '<' in text and '>' in text:
        start_index = text.index('<')
        end_index = text.rindex('>')
        main_text = text[:start_index].strip()
        tooltip_source = text[start_index + 1:end_index].strip()
    else:
        msg = inliner.reporter.error(
            "Invalid syntax for include_tooltip role. Expected format: 'display text <tooltip text or term>'",
            line=lineno
        )
        return [inliner.problematic(rawtext, rawtext, msg)], [msg]

    node = include_tooltip_node(main_text, main_text)
    node['tooltip_source'] = tooltip_source

    return [node], []

def setup(app):
    roles.register_local_role('include_tooltip', include_tooltip_role)
    app.add_node(include_tooltip_node, html=(visit_include_tooltip_node_html, depart_include_tooltip_node_html))
    app.add_post_transform(TooltipPostTransform)
    
    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

