========
Commands
========

Use the command-line interface to run the following commands.

Prerequisites
-------------

To run the following commands, you will need to have installed:

- A Unix-based terminal. For Windows, use `Windows Subsystem for Linux <https://learn.microsoft.com/en-us/windows/wsl/install>`_.
- `Python 3.7 <https://www.python.org/downloads/>`_ or later.
- `Poetry #.12 <https://python-poetry.org/docs/master/>`_ or later.
- `Make <https://www.gnu.org/software/make/>`_.
- `Git <https://git-scm.com/>`_.

.. _Make_Preview:

Preview current branch
----------------------

The preview command builds a local instance of the docs site so you can view the rendering in a sandbox environment on your local browser.

To preview the docs:

#. Build the docs.

    .. code:: console

        cd docs
        make preview

#. Open http://127.0.0.1:5500/ with your preferred browser.

.. tip:: You can pass custom options to increase or decrease verbosity. For a list with all the available options, refer to the `Sphinx documentation <https://www.sphinx-doc.org/en/master/man/sphinx-build.html>`_.

To increase verbosity, use the option ``-v``:

    .. code:: console

        make preview SPHINXOPTS=-v

To decrease verbosity, use the option ``-Q``:

    .. code:: console

        make preview SPHINXOPTS=-Q


Preview multiversion
--------------------

The multiversionpreview command generates a local instance of the docs site with all :doc:`specified versions <../configuration/multiversion>` available for navigation.
You can view the rendering in a sandbox environment on your local browser.

To preview multiple versions:

#. Build the docs.

    .. code:: console

        cd docs
        make multiversionpreview

#. Open http://0.0.0.0:5500/ with your preferred browser.

For further guidance on using the `multiversionpreview command`, see :doc:`Multiversion configuration <../configuration/multiversion>`.

Build HTML for multiple versions
--------------------------------

.. note:: The command ``make multiversion`` is aimed to be used by GitHub Actions CI. While documenting new features, it is not advised to run ``make multiversion``, but ``make preview`` instead.

.. code:: console

    cd docs
    make multiversion

The previous command generates HTML docs under the ``docs/_build/dirhtml`` directory.

Clean all builds
----------------

The ``make preview`` operation creates content in the ``_build`` directory. When making changes to the docs, it is helpful to delete the contents of this directory before running ``make preview``.

.. code:: console

    cd docs
    make clean

Check for broken links
----------------------

Check for broken links on the documentation site.

.. code:: console

    cd docs
    make dirhtml
    make linkcheck
