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
        'hide_version_dropdown': ['master'],
        'default_branch': 'master',
        'branch_substring_removed': 'branch-',
        'tag_substring_removed': '-scylla'
    }

.. list-table::
    :widths: 33 33 33
    :header-rows: 1

    * - Option
      - Description
      - Default Value
    * - ``header_links``
      - Links displayed in the top navbar.
      - []
    * - ``site_description``
      - Short summary describing the site. Metadescriptions are mainly used by search engines.
      - Scylla is an Apache Cassandra-compatible NoSQL data store that can handle 1 million transactions per second on a single server.
    * - ``github_issues_repository``
      - Repository organization name and project slug, separated by a slash (/). Used by the "Report an Issue on this Page" button.
      -  scylladb/sphinx-scylladb-theme
    * - ``show_sidebar_index``
      -  Set to ``true`` to display the left sidebar on the index page.
      -  false
    * - ``hide_banner``
      -  Set to ``true`` to hide the ScyllaDB Summit registration banner at the top of the page.
      -  true
    * - ``hide_version_dropdown``
      -  List of tags and branches names to hide from the multiversion dropdown.
      -  []
    * - ``default_branch``
      -  Name of the default branch where changes are integrated. Used to display the "You are not reading the most current version of the documentation" warning. 
      -  master
    * - ``branch_substring_removed``
      -  Part of the branch name to skip from the multiversion dropdown.
      -  branch-
    * - ``tag_substring_removed``
      -  Part of the tag name to skip from the multiversion dropdown.
      -  -scylla
