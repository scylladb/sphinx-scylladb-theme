====================
Multiversion Options
====================

The theme supports the extension `sphinx-multiversion <https://github.com/dgarcia360/sphinx-multiversion>`_ for building self-hosted versioned documentation.

.. note:: Maintaining multiple versions is expensive. Consider building docs for a version only if this introduces relevant breaking changes reflected in the documentation.

Supported versions
==================

The settings ``TAGS`` and ``BRANCHES`` in ``conf.py`` defines which versions are supported:

* ``BRANCHES``:  List of `git branches <https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging>`_, separated by a comma. For example, ``BRANCHES= ['master']`` builds docs for the ``master`` branch.
* ``TAGS``:  List of `git tags <https://git-scm.com/book/en/v2/Git-Basics-Tagging>`_, separated by a comma. For example, ``TAGS = ['3.22.0-scylla', '3.21.0-scylla']`` builds docs for the tags ``3.22.0-scylla`` and ``3.21.0-scylla``.

.. tip:: If you maintain a branch for each minor release (e.g. ``branch-3.22``), we recommended building docs for the **branch** and not for tags. This will allow you to backport documentation changes if needed without having to update the tag reference.

The setting ``smv_latest_version`` in ``conf.py`` defines which branch or tag is considered the latest.
This is used to redirect users to the latest version of the docs automatically once they open the main project URL.

This is how the configuration file looks like:

.. code:: python

    TAGS = ['3.22.0-scylla', '3.21.0-scylla']
    smv_tag_whitelist = multiversion_regex_builder(TAGS)
    BRANCHES = ['master']
    smv_branch_whitelist = multiversion_regex_builder(BRANCHES)

    smv_latest_version = '3.22.0-scylla'


The extension allows configuring extra settings.
To know more about them, refer to `sphinx-multiversion documentation <https://holzhaus.github.io/sphinx-multiversion/master/configuration.html>`_.

Stable URL
==========

We encourage every project to rename the latest version output directory to ``stable``.
The purpose is to have default documentation links that do not change, which is beneficial for SEO purposes and referencing docs on other websites.

You can override the latest version output directory via your ``conf.py`` with the setting ``smv_rename_latest_version``.

Here's an example:

.. code:: python


    smv_latest_version = 'x.y.z'        # Use the branch/tag name
    smv_rename_latest_version = 'stable' # Use the commit hash

Disabling multiversion support
==============================

1. Set the properties ``smv_tag_whitelist`` and ``smv_branch_whitelist`` in ``conf.py`` to ``None``.

.. code:: python

    smv_tag_whitelist = None
    smv_branch_whitelist = None

or:

.. code:: python

    TAGS = []
    smv_tag_whitelist = multiversion_regex_builder(TAGS)
    BRANCHES = []
    smv_branch_whitelist = multiversion_regex_builder(BRANCHES)

2. On ``.github/workflows/pages.yml``, change the command ``make multiversion`` for ``make dirhtml``.
