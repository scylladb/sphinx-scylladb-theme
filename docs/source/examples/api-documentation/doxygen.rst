:toc-depth: 4

Doxygen
=======

The `Breathe <https://breathe.readthedocs.io/>`_ extension integrates Doxygen-generated documentation into Sphinx.

Supported languages
-------------------

Breathe supports any language that Doxygen can parse:

* C
* C++
* C#
* Objective-C
* PHP
* Java
* Python (limited)
* Fortran
* VHDL

Setup
-----

Install Breathe:

.. code-block:: bash

   pip install breathe

Configure Doxygen to generate XML output in your ``Doxyfile``:

.. code-block:: text

   GENERATE_XML = YES
   XML_OUTPUT = xml

Add Breathe to your ``conf.py``:

.. code-block:: python

   extensions = ['breathe']

   breathe_projects = {
       'myproject': './doxygen/xml/'
   }
   breathe_default_project = 'myproject'

Basic usage
-----------

Document a class
~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. doxygenclass:: DatabaseConnection
      :members:

.. doxygenclass:: DatabaseConnection
   :members:

Document a function
~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. doxygenfunction:: format_query

.. doxygenfunction:: format_query

Common options
--------------

Select specific members
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. doxygenclass:: DatabaseConnection
      :members: connect, disconnect

Include private members
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. doxygenclass:: DatabaseConnection
      :members:
      :private-members:

Include undocumented members
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   .. doxygenclass:: DatabaseConnection
      :members:
      :undoc-members:

Doxygen comment syntax
----------------------

C++ example
~~~~~~~~~~~

.. code-block:: cpp

   /**
    * @brief Establishes a connection
    * @param host The database host address
    * @param port The database port number
    * @return true if connection successful
    * @throw ConnectionError if connection fails
    */
   bool connect(const std::string& host, int port);

C example
~~~~~~~~~

.. code-block:: c

   /**
    * @brief Connect to database
    * @param[in] config Connection configuration
    * @return Connection handle or NULL on failure
    */
   connection_t* db_connect(const connection_config_t* config);

Configuration
-------------

Common settings in ``conf.py``:

.. code-block:: python

   breathe_default_members = ('members', 'undoc-members')
   breathe_show_define_initializer = True

Automatic API generation
-------------------------

For large projects, use `Exhale <https://exhale.readthedocs.io/>`_ to automatically generate API documentation pages:

.. code-block:: bash

   pip install exhale

Configure in ``conf.py``:

.. code-block:: python

   extensions = ['breathe', 'exhale']

   exhale_args = {
       'containmentFolder': './api',
       'rootFileName': 'library_root.rst',
       'rootFileTitle': 'API Reference',
       'doxygenStripFromPath': '..',
   }

Exhale will automatically create a page for each class, function, and file in your project.
