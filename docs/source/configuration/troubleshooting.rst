===============
Troubleshooting
===============

Installation
------------

.. _Windows_Installation:

How to use the toolchain in Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run the toolchain on **Windows**:

#. Make sure you have `Make <https://www.gnu.org/software/make/>`_ installed.

    The easiest way to install it is using Chocolatey.
    First, you need to `install this package manager <https://chocolatey.org/install>`_.
    Then, install Make with the command ``choco install make``.

   .. tip:: If you get an error when installing make, try to run the command in a console prompt with elevated permissions.

#. You must run ``make`` commands from a Unix-based terminal such as `Git Bash <https://www.atlassian.com/git/tutorials/git-bash>`_.

Multiversion
------------

.. _Sync_Fork:

How to preview latest local changes with multiversion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, the command builds the documentation that is available on GitHub (remote repository).

To build multiversion docs for the local branches:

1. In ``conf.py``, set ``smv_remote_whitelist`` to ``None``:

.. code:: console

    smv_remote_whitelist = None

2. Follow `Syncing a Fork <https://docs.github.com/es/github/collaborating-with-pull-requests/working-with-forks/syncing-a-fork>`_ for every branch not updated in your fork.

3. Run ``make multiversionpreview`` again.

.. _Preview_Production:

How to preview locally the documentation published in production
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Follow `these steps <https://docs.github.com/es/github/collaborating-with-pull-requests/working-with-forks/syncing-a-fork>`_ to configure a remote that points to the upstream repository in Git.

2. Download the latest tags and branches from upstream:

.. code:: console

    git fetch --all

3. Edit the setting ``smv_remote_whitelist`` in the file `conf.py` to build the docs from upstream as follows:

.. code:: console

    smv_remote_whitelist = r"^upstream$"

4. Run the command ``make multiversionpreview`` again.

.. _No_Matching_Refs_Found:

How to fix the error "No matching refs found!"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the console raises the error "No matching refs found!", most likely your fork is not updated with the upstream repository.

In this case, you can:

* Build multiversion docs for the upstream repository. See :ref:`Preview documentation published in production <Preview_Production>` (recommended).
* Sync the fork with the upstream repository. See :ref:`Preview latest local changes <Sync_Fork>`.

Another frequent mistake that raises the error message is to have typos in the configuration file. Make sure that the version names listed in ``TAGS`` and ``BRANCHES`` settings from ``conf.py`` match the repository's branch and tags names on Git.
