=======================
Contribute to the Theme
=======================

If you are reading this guide because you have decided to contribute to the Scylla Sphinx Theme, thank you!
We appreciate your contribution and hope that this handbook will answer any questions you may have.

Configuring a Python environment
--------------------------------

This project's Python side is managed with `Poetry <https://python-poetry.org/docs/>`_.
It combines several things in one tool:

*   Keeping track of Python dependencies, including ones required only for development and tests.
*   Initializing and managing a virtual environment.
*   Packaging the theme into a package for PyPI (Python Package Index).
    Such package can be installed with ``pip install`` and other tools.

To initialize a Python development environment for this project:

#.  Make sure you have Python version 3.7 or later installed.
#.  `Install Poetry <https://python-poetry.org/docs/>`_.

#.  Initialize a virtual environment with:

    ..  code-block:: bash

        poetry install

    This will create an environment outside of the project directory, somewhere under ``~/Library/Caches/pypoetry/virtualenvs/``.
    You'll see the path in installation logs.

#.  Activate the virtual environment for current shell session:

    ..  code-block:: bash

        poetry shell

    Alternatively, if you use PyCharm, you can configure the project to use this environment as the default Python interpreter.
    PyCharm doesn't detect Poetry (yet), so just use the "virtualenv" option and
    provide the full path to the environment.

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


Publishing the theme to PyPi
----------------------------

.. note:: You need a PyPi account and be a project maintainer to release new theme versions.

All the documentation projects receives new patches when the theme is released on PyPi.
The script automatically increases the package's version and will ask you for the PyPi username and password.

.. code:: console

    ./deploy.sh

The script automatically increases the package's version and will ask you for the PyPi username and password.

After publishing the package, you should see the new release listed on `PyPI <https://pypi.org/project/sphinx-scylladb-theme/#history>`_.

.. toctree::
   :hidden:

   api/sphinx_scylladb_theme