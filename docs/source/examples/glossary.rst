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
   
   Long description
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sed lorem quis dui mattis suscipit sit amet id dui. Suspendisse elementum rutrum vulputate. Cras in velit sapien. Etiam egestas turpis eget arcu feugiat semper. Ut blandit sagittis cursus. Maecenas at varius ex, et porttitor mi. Nullam tortor elit, tincidunt et nulla id, porta vestibulum nibh. Quisque tellus elit, maximus at congue quis, molestie eget urna. Donec odio lorem, semper sed pharetra eu, sodales eget velit. Donec dignissim quam mi, nec vehicula magna gravida in. Vestibulum consectetur, sem a tristique porta, risus est laoreet nibh, sed cursus nibh est vel massa. Vestibulum aliquet varius tellus eu pulvinar. Integer a lorem sollicitudin, placerat orci eu, lobortis velit. Pellentesque sit amet magna porta augue iaculis egestas dapibus sed dui.


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
