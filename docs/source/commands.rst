========
Commands
========

To run the next commands you will need to have installed Python 3.7 and PIP.

Preview current branch
----------------------

The preview command builds a local instance of the docs site so you can view the rendering in a sandbox environment on your local browser.

To preview the docs:

1. Build the docs.

.. code:: console

    cd docs
    make preview

2. Open http://127.0.0.1:5500/ with your preferred browser.

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

1. Build the docs.

.. code:: console

    cd docs
    make multiversionpreview

2. Open http://0.0.0.0:5500/ with your preferred browser.


Build HTML for multiple versions
--------------------------------

.. note:: The command ``make multiversion`` is aimed to be used by GitHub Actions CI. While documenting new features, it is not advised to run ``make multiversion``, but ``make preview`` instead.

To generate multiple versions of the documentation:

1. Build the docs.

.. code:: console

    cd docs
    make multiversion

2. The previous command should generate HTML docs under the ``docs/_build/dirhtml`` directory.

.. tip:: If the command raises an error, see :doc:`Troubleshooting <configuration/troubleshooting>` for help.

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
