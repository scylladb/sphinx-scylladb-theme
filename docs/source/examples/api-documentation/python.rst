:toc-depth: 4

Python
======

The `sphinx.ext.autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_ extension generates documentation from Python docstrings.

Basic usage
-----------

Document a module
~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. automodule:: examples._sample_module
      :members:

.. automodule:: examples._sample_module
   :members:

Document a class
~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. autoclass:: examples._sample_module.DatabaseConnection
      :members:

.. autoclass:: examples._sample_module.DatabaseConnection
   :members:
   :no-index:

Document a function
~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. autofunction:: examples._sample_module.format_query

.. autofunction:: examples._sample_module.format_query
   :no-index:

Common options
--------------

Select specific members
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. autoclass:: examples._sample_module.DatabaseConnection
      :members: connect, disconnect

Include special methods
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. autoclass:: examples._sample_module.DatabaseConnection
      :members:
      :special-members: __init__

Include private members
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. autoclass:: examples._sample_module.DatabaseConnection
      :members:
      :private-members:

Include undocumented members
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. automodule:: examples._sample_module
      :members:
      :undoc-members:

Exclude members
~~~~~~~~~~~~~~~

.. code-block:: rst

   .. autoclass:: examples._sample_module.DatabaseConnection
      :members:
      :exclude-members: disconnect

Configuration
-------------

Set defaults in ``conf.py``:

.. code-block:: python

   autodoc_default_options = {
       'members': True,
       'member-order': 'bysource',
       'special-members': '__init__',
   }

   autodoc_typehints = 'signature'  # 'signature', 'description', 'none', 'both'
   autodoc_member_order = 'bysource'  # 'alphabetical', 'bysource', 'groupwise'

Related extensions
------------------

* ``sphinx.ext.napoleon`` - Google and NumPy docstring styles
* ``sphinx.ext.autosummary`` - Summary tables
* ``sphinx.ext.viewcode`` - Source code links
