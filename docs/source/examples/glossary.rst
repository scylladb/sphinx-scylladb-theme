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

      Long description
         Lorem ipsum dolor sit amet, ``consectetur`` adipiscing elit. Ut tincidunt orci non pellentesque hendrerit. Sed vitae sem convallis, porta felis ut, varius libero. Suspendisse eget auctor felis. Sed sit amet sapien posuere, eleifend urna ut, interdum nisi.
         Donec porta nibh leo, vitae convallis risus ornare sit amet. Mauris porttitor ipsum in mi dignissim, vel volutpat massa placerat.
         
         Vivamus et cursus turpis, id luctus lectus.

This will result in:

.. glossary::

   Term 1
      Definition

   Term 2
      Definition
   
   Long description
      Lorem ipsum dolor sit amet, ``consectetur`` adipiscing elit. Ut tincidunt orci non pellentesque hendrerit. Sed vitae sem convallis, porta felis ut, varius libero. Suspendisse eget auctor felis. Sed sit amet sapien posuere, eleifend urna ut, interdum nisi.
      Donec porta nibh leo, vitae convallis risus ornare sit amet. Mauris porttitor ipsum in mi dignissim, vel volutpat massa placerat.
      
      Vivamus et cursus turpis, id luctus lectus.



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
