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

You can pass custom options to increase or decrease verbosity. For example, use ``-v`` to increase verbosity:

.. code:: console

    make preview SPHINXOPTS=-v

For a list with all the available options, refer to the `Sphinx documentation <https://www.sphinx-doc.org/en/master/man/sphinx-build.html>`_.

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

Troubleshooting
===============

.. _Sync_Fork:

I cannot see my latest local changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, the command builds the documentation that is available on GitHub (remote repository).

To build multiversion docs for the local branches:

1. In ``conf.py``, set ``smv_remote_whitelist`` to ``None``:

.. code:: console

    smv_remote_whitelist = None

2. Follow `Syncing a Fork <https://docs.github.com/es/github/collaborating-with-pull-requests/working-with-forks/syncing-a-fork>`_ for every branch not updated in your fork.

3. Run ``make multiversionpreview`` again.

.. _Preview_Production:

I want to preview the documentation published in production
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Follow `these steps <https://docs.github.com/es/github/collaborating-with-pull-requests/working-with-forks/syncing-a-fork>`_ to configure a remote that points to the upstream repository in Git.

2. Download the latest tags and branches from upstream:

.. code:: console

    git fetch --all

3. Edit the setting ``smv_remote_whitelist`` in the file `conf.py` to build the docs from upstream as follows:

.. code:: console

    smv_remote_whitelist = r"^upstream$"

4. Run the command ``make multiversionpreview`` again.

No matching refs found!
^^^^^^^^^^^^^^^^^^^^^^^

If the console raises the error "No matching refs found!", most likely your fork is not updated with the upstream repository.

In this case, you can:

* Build multiversion docs for the upstream repository. See :ref:`Preview documentation published in production <Preview_Production>` (recommended)
* Sync the fork with the upstream repository. See :ref:`Preview latest local changes <Sync_Fork>`

Another frequent mistake that raises the error message is to have typos in the configuration file. Make sure that the version names listed in ``TAGS`` and ``BRANCHES`` settings from ``conf.py`` match the repository's branch and tags names on Git.

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
