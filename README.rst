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

1. Add the dependency to the new Sphinx documentation project.
You can use either poetry, pip, or any other equivalent package manager.

.. code:: console

    poetry add sphinx-scylla-theme

2. Add the following configuration in the documentation's ``conf.py`` file.

.. code:: console

    html_theme = 'sphinx_scylla_theme'
    extensions = [
        ...,
        'sphinx_scylla_theme'
    ]

3. In the same ``conf.py`` file, comment out the static paths to use the assets already included in the theme.

.. code:: console

    # templates_path = ['_templates']
    # html_theme_path = ['theme']
    # html_static_path = ['_static']

Preview the theme locally
-------------------------

1. Open a new console prompt and clone the theme project.

.. code:: console

    git clone https://github.com/scylladb/sphinx-scylla-theme.git

2. Install the project's dependencies with poetry.

.. code:: console

    poetry install

3. To build the sample docs, run the following command.

.. code:: console

    potery run sphinx-build -a -b html docs/source _build/dirhtml

If everything goes well, the previous command should generate a ``_build/dirhtml`` directory.

4. Open the ``index.html`` that you will find inside ``_build/dirhtml`` with your preferred browser.