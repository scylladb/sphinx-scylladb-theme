================
Template Options
================

Configuration options for this theme.

Template Options
----------------

Template-level settings can be configured via your ``conf.py`` in ``html_theme_options``. 
For example:

.. code:: python

    html_theme_options = {
        'header_links': [
        ('Scylla Theme', 'https://sphinx-theme.scylladb.com/'),
        ('Scylla University', 'https://university.scylladb.com/'),
        ('ScyllaDB Home', 'https://www.scylladb.com/')],
        'site_description': 'Sphinx Theme for ScyllaDB projects.',
        'github_issues_repository': 'scylladb/sphinx-scylladb-theme',
        'show_sidebar_index': 'false',
        'hide_banner': 'true',
        'default_branch': 'master',
        'branch_substring_removed': 'branch-',
        'tag_substring_removed': '-scylla'
    }

* ``header_links``: Links displayed in the top navbar.
* ``site_description``: Short summary describing the site. Metadescriptions are mainly used by search engines.
* ``github_issues_repository``: Repository organization name and project slug, separated by a slash (/). Used by the "Report an Issue on this Page" button.
* ``show_sidebar_index``: Set to ``true`` to display the left sidebar in the index page.
* ``hide_banner``: Set to ``true`` to show the ScyllaDB Summit registration banner at the top of the page.
* ``default_branch``: Name of the default branch where changes are integrated. Defaults to ``master``.
* ``branch_substring_removed``: Part of the branch name to skip. When the project does not set this option, the theme removes the prefix ``branch-`` for all releases listed in the multiversion dropdown.
* ``tag_substring_removed``: Part of the tag name to skip. When the project does not set this option, the theme removes the suffix ``-scylla`` for all releases listed in the multiversion dropdown.
