Tooltips
========

A custom role to create tooltips in your documentation. The tooltip text can be provided inline or loaded from a glossary entry.

.. warning:: Ensure that the included content is appropriate for display as a tooltip, as long text or complex formatting may not render well.

Syntax
------

.. code-block:: rst

   :include_tooltip:`display text <tooltip text or term name>`

Usage
-----

Tooltip with text
.................

Using:

.. code-block:: rst

   Here is a :include_tooltip:`word <This is the tooltip text>`.

Results in:

Here is a :include_tooltip:`word <This is the tooltip text>`.

Tooltip from a glossary entry
.............................

Using:

.. code-block:: rst

   Here is a :include_tooltip:`term <Term 1>`.

This will load the definition of `term-name` from your project's glossary and use it as the tooltip text for "term".


Results in:

Here is a :include_tooltip:`term <Term 1>`.

