=============
Configuration
=============

Configuration options for this theme.

Template Options
----------------

Template-level settings can be configured via your ``conf.py`` in ``html_theme_options``. 
For example:

.. code:: console

    html_theme_options = {
        'header_links': [
        ('Scylla Theme', 'https://sphinx-theme.scylladb.com/'),
        ('Scylla University', 'https://university.scylladb.com/'),
        ('ScyllaDB Home', 'https://www.scylladb.com/')],
        'site_description': 'Sphinx Theme for ScyllaDB projects.',
        'github_issues_repository': 'scylladb/sphinx-scylladb-theme',
        'show_sidebar_index': 'false',
        'hide_banner': 'true',
    }

* ``header_links``: Links displayed in the top navbar.
* ``site_description``: Short summary describing the site. Metadescriptions are mainly used by search engines.
* ``github_issues_repository``: Repository organization name and project slug, separated by a slash (/). Used by the "Report an Issue on this Page" button.
* ``show_sidebar_index``: Set to ``true`` to display the left sidebar in the index page.
* ``hide_banner``: Set to ``true`` to show the ScyllaDB Summit registration banner at the top of the page.

.. _multiversion:

Multiversion Options
--------------------

The theme supports the extension `sphinx-multiversion <https://github.com/Holzhaus/sphinx-multiversion>`_ for building self-hosted versioned documentation.

.. tip:: Maintaining multiple versions is expensive. Consider building docs for a version only if this introduces relevant breaking changes reflected in the documentation.

Defining supported versions
===========================

The properties ``smv_tag_whitelist`` and ``smv_branch_whitelist`` in ``docs/source/conf.py`` defines regular expressions with the pattern for tags/branches supported.
If you only want to support a subset of versions, modify the regular expression to accept a list of tags. For example, ``smv_tag_whitelist = r'\b(3.22.0-scylla|3.21.0-scylla)\b'`` would only build the documentation for the tags ``3.22.0-scylla`` and ``3.21.0-scylla``.

The environment variable ``LATEST_VERSION`` in ``.github/workflows/pages.yml`` defines which branch or tag is considered the latest.
This is used to redirect users to the latest version of the docs automatically once they open the main project URL.

The extension allows configuring extra parameters.
To know more about them, refer to `sphinx-multiversion documentation <https://holzhaus.github.io/sphinx-multiversion/master/configuration.html>`_.

Disabling multiversion support
==============================

Set the properties ``smv_tag_whitelist`` and ``smv_branch_whitelist`` in ``conf.py`` to ``None``.

.. code:: console

    smv_tag_whitelist = None
    smv_branch_whitelist = None

or:

.. code:: console

    TAGS = []
    smv_tag_whitelist = multiversion_regex_builder(TAGS)
    BRANCHES = []
    smv_branch_whitelist = multiversion_regex_builder(BRANCHES)

Defining a stable URL
=====================

We encourage every project to maintain a ``stable`` tag on git.
The purpose is to have default documentation links that do not change, which is beneficial for SEO purposes and referencing docs on other websites.

Each project maintainer must update the stable tag reference when a new version of the software is released, and this is considered the latest stable version.

To create/update the stable tag:

.. code:: console

    # Creates or updates the tag reference. You can change HEAD for a commit id.
    git tag -f stable HEAD
    # Publishes all local tags to the remote repository.
    git push --tags

Other projects have decided to build docs for the ``master`` branch. Since this branch is used normally to integrate changes, it might be possible that the docs are not aligned with the latest stable version.