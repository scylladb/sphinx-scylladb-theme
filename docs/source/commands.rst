========
Commands
========

Use the command-line interface to run the following commands.

.. note:: Make sure you meet the necessary prerequisites before running these commands. For details, see :ref:`Prerequisites <prerequisites>`.

Setup commands
--------------

setupenv
========

Installs system dependencies required to build the docs, such as Poetry.

.. code:: console

    make setupenv

setup
=====

Installs the required Python dependencies to build the documentation.

.. code:: console

    make setup

.. note:: ``make setup`` is called automatically before running build commands.

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


Troubleshooting
...............

Issue: pyproject.toml changed significantly since poetry.lock was last generated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Solution:**

#. Run the following command:

    .. code:: console

        poetry lock --no-update

#. Run the `make preview` command again.

Issue: Keyring asks for a password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This issue is due to a known problem with Poetry that primarily affects GNOME users. For more details, see `poetry/poetry#8761 <https://github.com/python-poetry/poetry/issues/8761>`_.

**Solution:**

#. Edit `docs/Makefile` to add the `POETRY` variable as follows:

    .. code::

        POETRY = PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring poetry

#. Run the `make preview` command again.

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

Generates the documentation in HTML format.

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

Before making changes to the docs, it's helpful to clear the previous build by deleting the contents of the ``build`` directory.
This ensures that the changes you make are reflected correctly.

.. code:: console

    cd docs
    make clean

Test commands
-------------

linkcheck
=========

Checks the documentation site for broken links.

.. code:: console

    cd docs
    make dirhtml
    make linkcheck
