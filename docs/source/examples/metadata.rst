Metadata
========

Add the following annotations at the beggining of ``.rst`` files to customize the layout of a specific page.

Description
-----------

Adds a description to a document. This description is mainly used for Search Engine Optimization.

.. code-block:: none

   .. meta::
      :description: The reStructuredText plaintext markup language
      :keywords: plaintext, markup language

This would be converted to the following HTML:

.. code-block:: html

   <meta name="description"
      content="The reStructuredText plaintext markup language">
   <meta name="keywords" content="plaintext, markup language">


Full width
----------

If set, hides boths sidenavs and makes the content full-width. 

.. code-block:: none

   :full-width:
