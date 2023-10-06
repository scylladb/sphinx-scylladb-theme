================
Template options
================

The following options can be defined in the file ``conf.py`` per project, using ``html_theme_options`` setting.

General options
---------------

General configuration options.

.. list-table::
  :widths: 20 20 20 40
  :header-rows: 1

  * - Option
    - Type
    - Default Value
    - Description
  * - ``scylladb_scripts``
    - string
    - true
    - Set to ``true`` to load ScyllaDB JS specific scripts, including Google Tag Manager, Expertrec, and Zendesk configuration.
  * - ``skip_warnings``
    - string
    -
    - List of custom warnings implemented by the theme to exclude, separated by commas. Available values are: ``document_has_underscores``.

Example:

.. code:: python

  html_theme_options = {
      'scylladb_scripts': 'true',
  }


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
    - ScyllaDB University Live | Free Virtual Training Event
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
      'banner_title_text': 'ScyllaDB University Live | Free Virtual Training Event',
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
  * - ``hide_version_dropdown``
    -  list of strings
    -  []
    -  List of tags and branches names to hide from the multiversion dropdown.
  * - ``hide_versions_dropdown``
    - string
    - true
    -  Set to `true` to remove completely the multiversion dropdown.
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

Version warning options
-----------------------

Configuration options for version warning.

.. list-table::
  :widths: 20 20 20 40
  :header-rows: 1

  * - Option
    - Type
    - Default Value
    - Description
  * - ``versions_unstable``
    -  list of strings
    -  []
    -  List of versions (branches or tags) that are not released yet.
  * - ``versions_deprecated``
    -  list of strings
    -  []
    -  List of deprecated versions (branches or tags).

Example:

.. code:: python

  html_theme_options = {
      'versions_unstable': ['master'],
      'versions_deprecated': [],
  }


Edit on this page button options
--------------------------------

Configuration options for the Edit on this page button.

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
  * - ``default_branch``
    - string
    - master
    - Name of the default branch where changes are integrated. Used to create the URL for the "Edit on this page" button.
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
    - ScyllaDB is an Apache Cassandra-compatible NoSQL data store that can handle 1 million transactions per second on a single server.
    - Short summary describing the site.

Example:

.. code:: python

  html_theme_options = {
      'site_description': 'Documentation toolchain for ScyllaDB projects.',
  }

Feedback buttons options
------------------------

Configuration options for the like and dislike buttons shown at the bottom of the page.

.. list-table::
  :widths: 20 20 20 40
  :header-rows: 1

  * - Option
    - Type
    - Default Value
    - Description
  * - ``hide_feedback_buttons``
    - string
    - true
    - Set to `true` to display the like and dislike buttons at the bottom of the page.

.. code:: python

  html_theme_options = {
      'hide_feedback_buttons': 'true',
  }
