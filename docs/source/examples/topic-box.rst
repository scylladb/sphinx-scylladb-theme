Topic box
=========

A custom directive that creates graphical boxes (cards) for navigation and content organization. 

Syntax
------

.. code-block:: rst

   .. topic-box::
      <options>

      <text>

Options
-------

The ``topic-box`` directive supports the following options:

.. list-table::
  :widths: 20 20 10 20 30
  :header-rows: 1

  * - Option
    - Type
    - Required
    - Example Value
    - Description
  * - ``title``
    - string
    - |v|
    - Lorem ipsum
    - Topic box title.
  * - ``class``
    - string
    -
    -
    - Custom CSS class.
  * - ``icon``
    - string
    -
    - icon-home
    - A list of CSS classes to render icons, separated by comma or space.
  * - ``image``
    - string
    -
    - /_static/img/mascots-2/enterprise.svg
    - Path to the image. The image should be located in the project's ``_static`` folder.
  * - ``link``
    - string
    -
    - getting-started
    - Relative link or external URL for the call to action. Do not use leading and trailing ("/") symbols to define relative links. (e.g. instead of ``/getting-started/``, use ``getting-started``).
  * - ``link_target``
    - string
    -
    - auto
    - Defines if the link should be opened in a new tab or not. Available values: `auto`, `_blank`, `_self`. Defaults to `auto`. When set to `auto`, external links will open in a new tab while internal links will open in the same tab.
  * - ``anchor``
    - string
    -
    - Getting Started >
    - Text for the call to action.

Link resolution
---------------

The topic-box directive handles different types of links:

1. External links (e.g. https://example.com)
2. Internal links with different path formats:
   * Absolute paths (e.g. /getting-started/installation)
   * Relative paths (e.g. code-blocks)
   * Parent directory references (e.g. ../getting-started)
   * Index files (e.g. index)

Examples:

.. code-block:: rst

    # External link
    .. topic-box::
        :title: ScyllaDB
        :link: https://scylladb.com
        :anchor: Learn more

    # Absolute path (from project root)
    .. topic-box::
        :title: Getting Started
        :link: /getting-started/installation
        :anchor: Learn more

    # Relative path (same directory)
    .. topic-box::
        :title: Code Blocks
        :link: code-blocks
        :anchor: Learn more

    # Relative path (subdirectory)
    .. topic-box::
        :title: Subdirectory Example
        :link: subdir/example
        :anchor: Learn more

    # Parent directory
    .. topic-box::
        :title: Parent Section
        :link: ../getting-started/installation
        :anchor: Learn more

    # Index file
    .. topic-box::
        :title: Examples
        :link: index
        :anchor: Learn more

Grid support
------------

To display topic boxes in responsive grid layouts, use the :doc:`grid` directive. The grid directive is specifically designed to work with topic boxes and supports Foundation's grid system for responsive layouts.

Usage
-----

Topic with icon
...............

Using:

.. code-block:: rst

    .. topic-box::
        :title: Lorem Ipsum
        :icon: icon-github
        :link: #
        :anchor: Lorem ipsum

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Results in:

.. topic-box::
    :title: Lorem Ipsum
    :icon: icon-github
    :link: #
    :anchor: Lorem ipsum

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Topic with image
................

Using:

.. code-block:: rst

    .. topic-box::
        :title: Lorem Ipsum
        :image: /_static/img/mascots-2/enterprise.svg
        :link: #
        :anchor: Lorem ipsum

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Results in:

.. topic-box::
    :title: Lorem Ipsum
    :image: /_static/img/mascots-2/enterprise.svg
    :link: #
    :anchor: Lorem ipsum

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Topic with external link
........................

Using:

.. code-block:: rst

    .. topic-box::
        :title: Lorem Ipsum
        :link: https://scylladb.com
        :anchor: Lorem ipsum

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Results in:

.. topic-box::
    :title: Lorem Ipsum
    :link: https://scylladb.com
    :anchor: Lorem ipsum

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.


Topic with external link (same tab)
...................................

Using:

.. code-block:: rst

    .. topic-box::
        :title: Lorem Ipsum
        :link: https://scylladb.com
        :link_target: _self
        :anchor: Lorem ipsum

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Results in:

.. topic-box::
    :title: Lorem Ipsum
    :link: https://scylladb.com
    :link_target: _self
    :anchor: Lorem ipsum

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Product topic
.............

Using:

.. code-block:: rst

    .. topic-box::
        :title: Lorem Ipsum
        :link: #
        :image: /_static/img/mascots-2/enterprise.svg
        :class: topic-box--product

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Results in:

.. topic-box::
    :title: Lorem Ipsum
    :link: #
    :image: /_static/img/mascots-2/enterprise.svg
    :class: topic-box--product

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

