===============
Troubleshooting
===============

Multiversion
------------

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
