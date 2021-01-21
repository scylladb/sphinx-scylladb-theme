"""
Overrides CommonMarkParser implementation to avoid checking if relative links exist.
The repositories java-driver and cpp-driver contain links that do not point to the specific index file but its root folder.
This change prevents the error thrown by CommonMarkParser from being raised.
"""
import re
from docutils import nodes
from recommonmark.parser import CommonMarkParser, splitext, urlparse

class CustomCommonMarkParser(CommonMarkParser):
    
    def visit_document(self, node):
        pass
    
    def visit_link(self, mdnode):
        # Override to avoid checking if relative links exists
        ref_node = nodes.reference()
        destination = mdnode.destination
        _, ext = splitext(destination)

        url_check = urlparse(destination)
        scheme_known = bool(url_check.scheme)

        if not scheme_known and ext.replace('.', '') in self.supported:
            destination = destination.replace(ext, '')
        ref_node['refuri'] = destination
        ref_node.line = self._get_line(mdnode)
        if mdnode.title:
            ref_node['title'] = mdnode.title
        next_node = ref_node

        self.current_node.append(next_node)
        self.current_node = ref_node

def replace_relative_links(app, docname, source):
    result = source[0]
    for key in app.config.replacements:
        result = re.sub(key, app.config.replacements[key], result)
    source[0] = result
