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

Tooltip with inline text
........................

Using:

.. code-block:: rst

   Here is a :include_tooltip:`word <This is the tooltip text>`.
   
   Here is another :include_tooltip:`term with long description <Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut tincidunt orci non pellentesque hendrerit. Sed vitae sem convallis, porta felis ut, varius libero. Suspendisse eget auctor felis. Sed sit amet sapien posuere, eleifend urna ut, interdum nisi.>`.

Results in:

Here is a :include_tooltip:`word <This is the tooltip text>`.

Here is another :include_tooltip:`term with long description <Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut tincidunt orci non pellentesque hendrerit. Sed vitae sem convallis, porta felis ut, varius libero. Suspendisse eget auctor felis. Sed sit amet sapien posuere, eleifend urna ut, interdum nisi.>`.

Tooltip from a glossary entry
.............................

You can also create a tooltip by referencing a glossary term. The tooltip will automatically pull the term's definition from the glossary.

Using:

.. code-block:: rst

   Here is a :include_tooltip:`term <Term 1>`.
   
   Here is another :include_tooltip:`term loading a long description <Long description>` from the glossary.

Results in:

Here is a :include_tooltip:`term <Term 1>` loading the description from the glossary.

Here is another :include_tooltip:`term loading a long description <Long description>` from the glossary.
