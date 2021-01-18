========
Commands
========

Preview current branch
----------------------

To preview the docs:

1. Build the docs.

.. code:: console

    cd docs
    make preview

2. Open http://127.0.0.1:5500/ with your preferred browser.

You can pass custom options to increase or decrease verbosity. For a list of all the available options, refer to the `Sphinx documentation <https://www.sphinx-doc.org/en/master/man/sphinx-build.html>`_.
For example:

.. code:: console

    make preview SPHINXOPTS=-v

Preview multiversion 
--------------------

To preview multiple versions:

1. Build the docs.

.. code:: console

    cd docs
    make previewmultiversion

2. Open http://0.0.0.0:5500/ with your preferred browser.

If you don't see docs for all listed versions, try to run ``git fetch --tags`` to download the latest tags from remote.

Build HTML for the current branch
---------------------------------

To generate an HTML version:

1. Build the docs.

.. code:: console

    cd docs
    make dirhtml

2. The previous command should generate HTML docs under the ``docs/_build/dirhtml`` directory.

Build HTML for multiple versions
--------------------------------

.. note:: The command ``make multiversion`` is aimed to be used by GitHub Actions CI. While documenting new features, it is not advised to run ``make multiversion``, but ``make preview`` instead.

To generate multiple versions of the documentation:

1. Build the docs.

.. code:: console

    cd docs
    make multiversion

2. The previous command should generate HTML docs under the ``docs/_build/dirhtml`` directory.

Clean all builds
----------------

Remove all the documentation builds previously generated:

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