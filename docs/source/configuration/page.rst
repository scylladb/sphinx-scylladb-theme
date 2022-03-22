Page options
============

Add the following annotations at the beggining of ``.rst`` files to customize the layout of a specific page.

Description
-----------

Adds a description to a document.
This description displayed in search engines results page.

For example:

.. code-block:: none

   .. meta::
      :description: The reStructuredText plaintext markup language
      :keywords: plaintext, markup language

Results in the following HTML:

.. code-block:: html

   <meta name="description"
      content="The reStructuredText plaintext markup language">
   <meta name="keywords" content="plaintext, markup language">

Full width
----------

If set, makes the content full-width.

.. code-block:: none

   :full-width:

Landing page
------------

If set, makes the content within the div with class ``landing_content`` float on top of the hero box.

.. code-block:: none

   :landing:

Hide pre content
----------------

If set, hides the breadcrumbs from the page.

.. code-block:: none

   :hide-pre-content:

Hide post content
-----------------

If set, hides the prev / next navigation buttons from the page.

.. code-block:: none

   :hide-post-content:

Hide sidebar
------------

If set, hides the primary sidebar from the page.

.. code-block:: none

   :hide-sidebar:

Hide secondary sidebar
----------------------

If set, hides the secondary sidebar from the page.

.. code-block:: none

   :hide-secondary-sidebar:

Hide version warning
--------------------

If set, hides the version warning from the page.

.. code-block:: none

   :hide-version-warning:
