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

Landing page
------------

If set, removes all internal paddings from the page.

.. code-block:: none

   :landing:

Hide version warning
--------------------

If set, hides the version warning from the page.

.. code-block:: none

   :hide-version-warning:

Hide pre content
----------------

If set, hides the breadcrumbs and contribute button from the page.

.. code-block:: none

   :hide-pre-content:

Hide post content
-----------------

If set, hides the prev / next navigation buttons from the page.

.. code-block:: none

   :hide-post-content:
