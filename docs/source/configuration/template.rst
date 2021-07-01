================
Template Options
================

The following options can be defined in the file ``conf.py`` per project, using ``html_theme_options`` setting.

.. code:: python

    html_theme_options = {
        'banner_button_text': 'Learn More >',
        'banner_button_url': '#',
        'banner_icon_path': '_static/mascots/scylla-opensource.svg',
        'banner_title_text': 'Scylla University Live | Free Virtual Training Event',
        'branch_substring_removed': 'branch-',
        'default_branch': 'master',
        'github_issues_repository': 'scylladb/sphinx-scylladb-theme',
        'hide_banner': 'true',
        'hide_sidebar_index': 'true',
        'hide_version_dropdown': ['master'],
        'site_description': 'Documentation toolchain for Scylla projects.',
        'tag_substring_removed': '-scylla',
    }

.. list-table::
    :widths: 33 33 33
    :header-rows: 1

    * - Option
      - Description
      - Default Value
    * - ``banner_button_text``
      - Caption for the promotional banner call to action.
      - Learn More >
    * - ``banner_button_url``
      - Link for the promotional banner call to action.
      - #
    * - ``banner_button_icon``
      - Icon for the promotional banner.
      -
    * - ``banner_title_text``
      - Leading text shown in the promotional banner.
      - Scylla University Live | Free Virtual Training Event
    * - ``branch_substring_removed``
      -  Part of the branch name to skip from the multiversion dropdown.
      -  branch-
    * - ``default_branch``
      -  Name of the default branch where changes are integrated. Used to display the "You are not reading the most current version of the documentation" warning.
      -  master
    * - ``github_issues_repository``
      - Repository organization name and project slug, separated by a slash (/). Used by the "Report an Issue on this Page" button.
      -  scylladb/scylla-doc-issues
    * - ``hide_banner``
      -  Set to ``true`` to hide the promotional banner. This banner is mainly used to promote events and new features, and is located at the top of every page.
      -  true
    * - ``hide_sidebar_index``
      -  Set to ``true`` to hide the sidebars on the index page.
      -  true
    * - ``hide_version_dropdown``
      -  List of tags and branches names to hide from the multiversion dropdown.
      -  []
    * - ``site_description``
      - Short summary describing the site. Metadescriptions are mainly used by search engines.
      - Scylla is an Apache Cassandra-compatible NoSQL data store that can handle 1 million transactions per second on a single server.
    * - ``tag_substring_removed``
      -  Part of the tag name to skip from the multiversion dropdown.
      -  -scylla
