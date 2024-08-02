Glossary
========

You can create a glossary using a paged named `glossary.rst` page. 

Syntax
------

The glossary has the following format:

.. code-block:: rst

   .. glossary::

      Term 1
         Definition

      Term 2
         Definition

This will result in:

.. glossary::

   Term 1
      Definition

   Term 2
      Definition

The terms in the glossary are automatically organized in alphabetical order.

Citing a glossary term
----------------------

To reference a term from the glossary within other parts of your documentation, use the following convention:

.. code-block:: rst

   :term:`term <term as written in Glossary>`

For exmaple:

.. code-block:: rst

   :term:`Size-tiered Compaction Strategy (STCS)<Size-tiered Compaction Strategy>`

Abbreviations and acronyms
--------------------------

Abbreviations and acronyms are defined in-line, with the abbreviation followed by the full term in parentheses.
Use the `abbr` role for this purpose:

.. code-block:: rst

   :abbr:`LIFO (last-in, first-out)`

You can also use it for longer phrases:

.. code-block:: rst

   :abbr:`Overwrite (Same data cells overwritten many times)`
