=============
Configuration
=============

Configuration options for this theme.

Template Options
----------------

Template-level settings can be configured via your ``conf.py`` in ``html_theme_options``. 
For example:

.. code:: python

    html_theme_options = {
        'site_description': 'Sphinx Theme for ScyllaDB projects.',
        'github_issues_repository': 'scylladb/sphinx-scylladb-theme',
        'hide_right_sidebar_index': 'true',
        'hide_banner': 'true',
        'default_branch': 'master',
        'branch_substring_removed': 'branch-',
        'tag_substring_removed': '-scylla'
    }

* ``site_description``: Short summary describing the site. Metadescriptions are mainly used by search engines.
* ``github_issues_repository``: Repository organization name and project slug, separated by a slash (/). Used by the "Report an Issue on this Page" button.
* ``hide_right_sidebar_index``: Set to ``true`` to hide the right sidebar on the index page.
* ``hide_banner``: Set to ``true`` to show the ScyllaDB Summit registration banner at the top of the page.
* ``default_branch``: Name of the default branch where changes are integrated. Defaults to ``master``.
* ``branch_substring_removed``: Part of the branch name to skip. When the project does not set this option, the theme removes the prefix ``branch-`` for all releases listed in the multiversion dropdown.
* ``tag_substring_removed``: Part of the tag name to skip. When the project does not set this option, the theme removes the suffix ``-scylla`` for all releases listed in the multiversion dropdown.

.. _multiversion:

Multiversion Options
--------------------

The theme supports the extension `sphinx-multiversion <https://github.com/dgarcia360/sphinx-multiversion>`_ for building self-hosted versioned documentation.

.. tip:: Maintaining multiple versions is expensive. Consider building docs for a version only if this introduces relevant breaking changes reflected in the documentation.

Defining supported versions
===========================

The properties ``smv_tag_whitelist`` and ``smv_branch_whitelist`` in ``docs/source/conf.py`` defines regular expressions with the pattern for tags/branches supported.
If you only want to support a subset of versions, modify the regular expression to accept a list of tags. For example, ``smv_tag_whitelist = r'\b(3.22.0-scylla|3.21.0-scylla)\b'`` would only build the documentation for the tags ``3.22.0-scylla`` and ``3.21.0-scylla``.

The  variable ``smv_latest_version`` in ``conf.py`` defines which branch or tag is considered the latest.
This is used to redirect users to the latest version of the docs automatically once they open the main project URL.

The extension allows configuring extra parameters.
To know more about them, refer to `sphinx-multiversion documentation <https://holzhaus.github.io/sphinx-multiversion/master/configuration.html>`_.

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

2. On ``.github/workflows/pages.yaml``, change the command ``make multiversion`` for ``make dirhtml``.

Defining a stable URL
=====================

We encourage every project to rename the latest version output directory to ``stable``.
The purpose is to have default documentation links that do not change, which is beneficial for SEO purposes and referencing docs on other websites.

You can override the latest version output directory via your ``conf.py`` with the setting ``smv_rename_latest_version``.

Here's an example:

.. code:: python


    smv_latest_version = 'x.y.z'        # Use the branch/tag name
    smv_rename_latest_version = 'latest' # Use the commit hash

.. note:: Other projects have decided to build docs for the ``master`` branch. Since this branch is used commonly to integrate changes, it might be possible that the docs are not aligned with the latest stable version.
