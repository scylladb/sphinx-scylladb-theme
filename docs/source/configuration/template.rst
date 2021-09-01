================
Template Options
================

The following options can be defined in the file ``conf.py`` per project, using ``html_theme_options`` setting.

Banner options
--------------

Configuration options for the banner shown at the top of the page.

.. list-table::
  :widths: 20 20 20 40
  :header-rows: 1

  * - Option
    - Type
    - Default Value
    - Description
  * - ``banner_button_text``
    - string
    - Learn more
    - Caption for the promotional banner call to action.
  * - ``banner_button_url``
    - string
    - #
    - Link for the promotional banner call to action.
  * - ``banner_button_icon``
    - string
    -
    - Relative path to icon for the promotional banner.
  * - ``banner_title_text``
    - string
    - Scylla University Live | Free Virtual Training Event
    - Leading text shown in the promotional banner.
  * - ``hide_banner``
    - string
    - true
    - Set to ``true`` to hide the promotional banner.

Example:

.. code:: python

  html_theme_options = {
      'banner_button_text': 'Learn more',
      'banner_button_url': '#',
      'banner_icon_path': '_static/mascots/scylla-opensource.svg',
      'banner_title_text': 'Scylla University Live | Free Virtual Training Event',
      'hide_banner': 'true',
  }

Version dropdown options
------------------------

Configuration options for version dropdown.

.. list-table::
  :widths: 20 20 20 40
  :header-rows: 1

  * - Option
    - Type
    - Default Value
    - Description
  * - ``branch_substring_removed``
    -  string
    -  branch-
    -  Part of the branch name to skip from the multiversion dropdown.
  * - ``default_branch``
    - string
    - master
    - Name of the default branch where changes are integrated. Used to display the "You are not reading the most current version of the documentation" warning.
  * - ``hide_version_dropdown``
    -  list of strings
    -  []
    -  List of tags and branches names to hide from the multiversion dropdown.
  * - ``tag_substring_removed``
    -  string
    -  -scylla
    -  Part of the tag name to skip from the multiversion dropdown.

Example:

.. code:: python

  html_theme_options = {
      'branch_substring_removed': 'branch-',
      'default_branch': 'master',
      'hide_version_dropdown': ['master'],
      'tag_substring_removed': '-scylla',
  }

Contribute button options
-------------------------

Configuration options for the Contribute button.

.. list-table::
  :widths: 20 20 20 40
  :header-rows: 1

  * - Option
    - Type
    - Default Value
    - Description
  * - ``conf_py_path``
    - string
    - docs/source
    - Relative path to conf.py file.
  * - ``github_issues_repository``
    - string
    - scylladb/scylla-doc-issues
    - Repository organization name and project slug to report issues, separated by a slash (/).
  * - ``github_repository``
    - string
    -
    - Repository organization name and project slug where docs are hosted, separated by a slash (/).
  * - ``hide_edit_this_page_button``
    - string
    - true
    -  Set to ``true`` to hide the contribute button.

Example:

.. code:: python

  html_theme_options = {
      'conf_py_path': 'docs/source/',
      'github_issues_repository': 'scylladb/sphinx-scylladb-theme',
      'hide_edit_this_page_button': 'true',
  }

Sidebar options
---------------

Configuration options for the left sidebar.

.. list-table::
  :widths: 20 20 20 40
  :header-rows: 1

  * - Option
    - Type
    - Default Value
    - Description
  * - ``hide_sidebar_index``
    -  string
    -  true
    -  Set to ``true`` to hide the sidebars on the index page.
  * - ``collapse_navigation``
    - string
    - false
    - Set to `true` to remove the ">" icon next to each sidebar entry.
  * - ``navigation_depth``
    - number
    - -1
    - The maximum depth of the sidebar nested entries. Set to `-1` to allow unlimited depth.

Example:

.. code:: python

  html_theme_options = {
      'hide_sidebar_index': 'true',
      'collapse_navigation': 'false',
      'navigation_depth': '-1'
  }

SEO options
-----------

Configuration options for Search Engine Optimization.

.. list-table::
  :widths: 20 20 20 40
  :header-rows: 1

  * - Option
    - Type
    - Default Value
    - Description
  * - ``site_description``
    - string
    - Scylla is an Apache Cassandra-compatible NoSQL data store that can handle 1 million transactions per second on a single server.
    - Short summary describing the site.

Example:

.. code:: python

  html_theme_options = {
      'site_description': 'Documentation toolchain for Scylla projects.',
  }
