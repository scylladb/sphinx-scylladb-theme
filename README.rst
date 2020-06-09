==========================
Scylla Documentation Theme
==========================

The base Sphinx theme for ScyllaDB documentation projects.

Requirements
------------

The theme is available on `PyPI <https://pypi.org/project/sphinx-scylladb-theme/>`_ and has been tested with Sphinx 1.8.0.
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

    poetry add sphinx-scylladb-theme


2. Add the following configuration in the documentation's ``conf.py`` file.

.. code:: console

    html_theme = 'sphinx_scylladb_theme'
    extensions = [
        ...,
        'sphinx_scylladb_theme'
    ]

3. In the same ``conf.py`` file, overwrite the ``html_theme_options`` property.
You can customize the navigation  bar and set the GitHub repository to report documentation issues.

.. code:: console

    html_theme_options = {
        'header_links': [
        ('Scylla Cloud', 'https://docs.scylladb.com/scylla-cloud/'),
        ('Scylla University', 'https://university.scylladb.com/'),
        ('ScyllaDB Home', 'https://www.scylladb.com/')],
        'github_issues_repository': 'scylladb/scylla-doc-issues'
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

    git clone https://github.com/scylladb/sphinx-scylladb-theme.git

2. Run the following command to build the docs.

.. code:: console

    cd docs
    make preview

If everything goes well, the previous command should generate a ``docs/_build/dirhtml`` directory.

3. Open http://127.0.0.1:5500/ with your preferred browser and preview the docs.

Publish to PyPi
---------------

To upload a new version of the package to PyPi, follow the next steps:

1. Open the file ``pyproject.toml`` with a text editor and increase the project's version number.

.. code:: console

    [tool.poetry]
    name = "sphinx-scylladb-theme"
    version = "0.1.1"
    ...

2. After saving your changes, run the command to build the package in a command prompt. The current directory should be the ``sphinx-scylla-theme`` project source code.

.. code:: console

    poetry build

3. Publish the package to PyPi. The command prompt will ask you for the PyPi username and password.

.. code:: console

    poetry publish

After publishing the package, you should see the new release listed on  `PyPI <https://pypi.org/project/sphinx-scylladb-theme/#history>`_.
