========
Commands
========

Use the command-line interface to run the following commands.

Prerequisites
-------------

To run the following commands, you will need to have installed:

- A Unix-based terminal. For Windows, use `Windows Subsystem for Linux <https://learn.microsoft.com/en-us/windows/wsl/install>`_.
- `Python 3.10 or 3.12 <https://www.python.org/downloads/>`_.
- `Poetry 1.8.1 <https://python-poetry.org/docs/master/>`_.
- `Make <https://www.gnu.org/software/make/>`_.
- `Git <https://git-scm.com/>`_.

Setup commands
--------------

setupenv
========

Installs system dependencies required to build the docs such as Poetry.

.. code:: console

    make setupenv

install
=======

Installs the required Python dependencies to build the documentation.

.. code:: console

    make install

.. note:: The command ``make install`` is called automatically when running build commands.

update
======

Updates Python dependencies to the latest version.

.. code:: console

    make update

As a result, updates the ``poetry.lock`` file.


Build commands
--------------

.. _Make_Preview:

preview
=======

Builds a local instance of the docs site so you can view the rendering in a sandbox environment on your local browser.

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

To fix the error ``pyproject.toml changed significantly since poetry.lock was last generated.``, run the following command:

    .. code:: console

        poetry lock --no-update

    Then, run the preview command again.


multiversionpreview
===================

Generates a local instance of the docs site with all :doc:`specified versions <../configuration/multiversion>` available for navigation.
You can view the rendering in a sandbox environment on your local browser.

To preview multiple versions:

#. Build the docs.

    .. code:: console

        cd docs
        make multiversionpreview

#. Open http://0.0.0.0:5500/ with your preferred browser.

For further guidance on using the ``multiversionpreview command``, see :doc:`Multiversion configuration <../configuration/multiversion>`.

dirhtml
=======

Generates the documentation in HTML version.

.. note:: The command ``make dirhtml`` is aimed to be used by GitHub Actions CI. While documenting new features, it is not advised to run ``make dirhtml``, but ``make preview`` instead.

.. code:: console

    cd docs
    make multiversion

Docs are generated under the ``docs/_build/dirhtml`` directory.

multiversion
============

Generates multiple versions of the docs with all :doc:`specified versions <../configuration/multiversion>` available for navigation.

.. note:: The command ``make multiversion`` is aimed to be used by GitHub Actions CI. While documenting new features, it is not advised to run ``make multiversion``, but ``make preview`` instead.

.. code:: console

    cd docs
    make multiversion

Docs are generated under the ``docs/_build/dirhtml`` directory.

redirects
=========

Generates HTML redirects from the ``_utils/redirects.yaml`` file.

.. note:: The command ``make multiversion`` is aimed to be used by GitHub Actions CI.

.. code:: console

    cd docs
    make multiversion

Redirects are generated under the ``docs/_build/dirhtml`` directory.

Clean commands
--------------

clean
=====

When making changes to the docs, it is helpful to delete the contents of this directory before running ``make preview``.

.. code:: console

    cd docs
    make clean

Test commands
-------------

linkcheck
=========

Checks for broken links on the documentation site.

.. code:: console

    cd docs
    make dirhtml
    make linkcheck
