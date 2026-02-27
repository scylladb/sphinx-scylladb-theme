=======================
Contribute to the theme
=======================

If you are reading this guide because you have decided to contribute to the ScyllaDB Sphinx Theme, thank you!
We appreciate your contribution and hope that this handbook will answer any questions you may have.

Configuring a Python environment
--------------------------------

This project's Python side is managed with `uv <https://docs.astral.sh/uv/>`_.
It combines several things in one tool:

*   Keeping track of Python dependencies, including ones required only for development and tests.
*   Initializing and managing a virtual environment.
*   Packaging the theme into a package for PyPI (Python Package Index).
    Such package can be installed with ``pip install`` and other tools.

To initialize a Python development environment for this project:

#.  Make sure you have Python 3.11 or later installed (Python 3.12+ recommended).
#.  `Install uv <https://docs.astral.sh/uv/getting-started/installation/>`_.

Previewing the theme locally
----------------------------

The ``docs`` folder contains a sample project with the Sphinx theme already installed.

To preview the theme locally:

#. Open a new console prompt and clone the project.

   .. code:: console

      git clone https://github.com/scylladb/sphinx-scylladb-theme.git

#. Build the docs.

   .. code:: console

      cd docs
      make preview

#. The previous command should generate a ``docs/_build/dirhtml`` directory. To preview the docs, open http://127.0.0.1:5500/ with your preferred browser.

Building the frontend
---------------------

The frontend static files of this project are managed with `webpack <https://webpack.js.org/>`_.
It combines several things in one tool:

*   Installing third-party node modules.
*   Combining JavaScript and CSS in a single file.
*   Minifying CSS and JavaScript files.

The original static files are located under the folder ``src``.

To build the minimized static files for this project:

#.  Make sure you have Node.js 18 or later installed.
#.  Build the static files with:

.. code:: console

    npm run build

This will create minified static files under the ``sphinx_scylladb_theme/static``.


Running unit tests
------------------

Run:

.. code:: console

    uv run pytest tests

Publishing the theme to PyPi
----------------------------

.. note:: You need a PyPi account and be a project maintainer to release new theme versions.

To publish a new version of the theme to PyPi, run the following script:

.. code:: console

    ./deploy.sh

To increase the **minor version**, run ``uv version --bump minor`` before  ``./deploy``.

To increase the **major version**, run ``uv version --bump major`` before  ``./deploy``.

Behind the scenes, ``deploy.sh`` executes the following logic:

1. Checks if the local git URL matches the original repository to prevent you from releasing from a personal fork.
2. Checks if the local contents differ from the remote master branch.
3. Increases the package's version **patch** with the command ``uv version --bump patch``.
4. Builds the package with the command ``uv build``.
5. Publishes the package to PyPI with ``uv publish``.

After publishing the package, you should see the new release listed on `PyPI <https://pypi.org/project/sphinx-scylladb-theme/#history>`_.
