"""
Sphinx role for HTML Label Components.
"""

from docutils import nodes
from sphinx.util.docutils import SphinxRole


class LabelRole(SphinxRole):
    def __init__(self, style):
        super().__init__()
        self.style = style

    def run(self):
        node = nodes.inline(
            self.rawtext,
            self.text,
            classes=["label", self.style],
        )
        self.set_source_info(node)
        return [node], []


def setup(app):
    app.add_role(
        "label-default",
        LabelRole("label--default"),
    )
    app.add_role(
        "label-note",
        LabelRole("label--note"),
    )
    app.add_role(
        "label-tip",
        LabelRole("label--tip"),
    )
    app.add_role(
        "label-caution",
        LabelRole("label--caution"),
    )
    app.add_role(
        "label-warning",
        LabelRole("label--warning"),
    )

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
