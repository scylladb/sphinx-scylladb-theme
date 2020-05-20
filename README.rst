==========================
Scylla Documentation Theme
==========================

The base Sphinx theme for ScyllaDB documentation projects.

Requirements
------------

The theme is available on `PyPI <https://pypi.org/project/sphinx-scylla-theme/>`_ and has been tested with Sphinx 1.8.0.
To build and preview the project locally, you will need to install the following software:

- `Git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_
- `Poetry 1.0.5 <https://python-poetry.org/docs/basic-usage/>`_
- `Python 3.7 <https://www.python.org/downloads/>`_

Installation
------------

To install the theme in a new Sphinx project, follow the next steps:

1. Add the dependency to the new Sphinx documentation project.
Open a console prompt and run the following command in the root documentation folder.

.. code:: console

    poetry add sphinx-scylla-theme


2. Add the following configuration in the documentation's ``conf.py`` file.

.. code:: console

    html_theme = 'sphinx_scylla_theme'
    extensions = [
        ...,
        'sphinx_scylla_theme'
    ]

3. In the same ``conf.py`` file, overwrite the ``html_theme_options`` property to customize the navigation bar.

.. code:: console

    html_theme_options = {
        'header_links': [
        ('Scylla Cloud', 'https://docs.scylladb.com/scylla-cloud/'),
        ('Scylla University', 'https://university.scylladb.com/'),
        ('ScyllaDB Home', 'https://www.scylladb.com/')]
    }

4. Finally, comment out the static paths to use the assets already included in the theme.

.. code:: console

    # templates_path = ['_templates']
    # html_theme_path = ['theme']
    # html_static_path = ['_static']

Preview the theme locally
-------------------------

The ``docs`` folder contains a sample project with the Sphinx theme already installed.

To preview the theme locally, follow the next steps:

1. Open a new console prompt and clone the theme project.

.. code:: console

    git clone https://github.com/scylladb/sphinx-scylla-theme.git

2. Run the following command to build the docs.

.. code:: console

    ./docs/_utils/preview.sh 

If everything goes well, the previous command should generate a ``docs/_build/dirhtml`` directory.

3. Open http://127.0.0.1:8000/ with your preferred browser and preview the docs.
