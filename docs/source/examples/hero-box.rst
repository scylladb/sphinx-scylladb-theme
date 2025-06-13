Hero box
========

A custom directive that creates prominent header sections at the top of landing.

Syntax
------

.. code-block:: rst

   .. hero-box::
      <options>

      <text>

Options
-------

The ``hero-box`` directive supports the following options:

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
    - Hero box title.
  * - ``class``
    - string
    -
    -
    - Custom CSS class.
  * - ``cta``
    - string
    - 
    - Learn more
    - Call to action text.
  * - ``image``
    - string
    -
    - /_static/img/mascots-2/enterprise.svg
    - Path to the image. The image should be located in the project's ``_static`` folder.
  * - ``button_style``
    - string
    -
    - bold
    - Button style. Available values: `bold`.
  * - ``button_icon``
    - string
    -
    - icon-github
    - A list of CSS classes to render icons, separated by comma or space.
  * - ``button_icon_position``
    - string
    -
    - right
    - Icon position. Available values: `left`, `right`.
  * - ``button_icon_link``
    - flag
    -
    -
    - If present, the icon will be rendered as a link.
  * - ``button_url``
    - string
    -
    - getting-started
    - Relative link or external URL for the call to action.
  * - ``button_text``
    - string
    -
    - Learn more
    - Button text.
  * - ``search_box``
    - flag
    -
    -
    - If present, a search box will be rendered.
  * - ``content_page``
    - flag
    -
    -
    - If present, adds vertical padding suitable for content pages. By default (without this flag), the hero box is optimized for landing pages.

Link resolution
---------------

The hero-box directive handles different types of links:

1. External links (e.g. https://example.com)
2. Internal links with different path formats:
   * Absolute paths (e.g. /getting-started/installation)
   * Relative paths (e.g. code-blocks)
   * Parent directory references (e.g. ../getting-started)
   * Index files (e.g. index)

Examples:

.. code-block:: rst

    # External link
    .. hero-box::
        :title: External Resources
        :text: Visit our website for more information
        :button_text: Learn more
        :button_url: https://scylladb.com
        :button_icon: icon-external-link
        :button_icon_position: right

    # Internal link (absolute)
    .. hero-box::
        :title: Getting Started
        :text: Learn how to install and configure ScyllaDB
        :button_text: Learn more
        :button_url: /getting-started/installation
        :button_icon: icon-arrow-right
        :button_icon_position: right

    # Internal link (relative)
    .. hero-box::
        :title: Code blocks
        :text: Learn how to install and configure ScyllaDB
        :button_text: Learn more
        :button_url:code-blocks
        :button_icon: icon-arrow-right
        :button_icon_position: right

    # Internal link (relative)
    .. hero-box::
        :title: Related Topics
        :text: Check out these related guides
        :button_text: Learn more
        :button_url: ../getting-started/installation
        :button_icon: icon-folder
        :button_icon_position: left

Usage
-----

Basic usage
...........

Using:

.. code-block:: rst

    .. hero-box::
        :title: Lorem Ipsum
        :text: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        :button_text: Learn more
        :button_url: #
        :button_icon: icon-arrow-right
        :button_icon_position: right
        :content_page:

Results in:

.. hero-box::
    :title: Lorem Ipsum
    :text: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    :button_text: Learn more
    :button_url: #
    :button_icon: icon-arrow-right
    :button_icon_position: right
    :content_page:

With image
..........

Using:

.. code-block:: rst

    .. hero-box::
        :title: Lorem Ipsum
        :text: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        :image: /_static/img/mascots-2/enterprise.svg
        :button_text: Learn more
        :button_url: #
        :button_icon: icon-arrow-right
        :button_icon_position: right
        :content_page:

Results in:

.. hero-box::
    :title: Lorem Ipsum
    :text: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    :image: /_static/img/mascots-2/enterprise.svg
    :button_text: Learn more
    :button_url: #
    :button_icon: icon-arrow-right
    :button_icon_position: right
    :content_page:

With search box
...............

Using:

.. code-block:: rst

    .. hero-box::
        :title: Lorem Ipsum
        :text: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        :search_box:
        :content_page:

Results in:

.. hero-box::
    :title: Lorem Ipsum
    :text: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    :search_box:
    :content_page:

With bold button
.................

Using:

.. code-block:: rst

    .. hero-box::
        :title: Lorem Ipsum
        :text: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        :button_text: Learn more
        :button_url: #
        :button_icon: icon-arrow-right
        :button_icon_position: right
        :button_style: bold
        :content_page:

Results in:

.. hero-box::
    :title: Lorem Ipsum
    :text: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    :button_text: Learn more
    :button_url: #
    :button_icon: icon-arrow-right
    :button_icon_position: right
    :button_style: bold
    :content_page:

With icon as link
.................

Using:

.. code-block:: rst

    .. hero-box::
        :title: Lorem Ipsum
        :text: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        :button_text: Learn more
        :button_url: #
        :button_icon: icon-arrow-right
        :button_icon_position: right
        :button_icon_link:
        :content_page:

Results in:

.. hero-box::
    :title: Lorem Ipsum
    :text: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    :button_text: Learn more
    :button_url: #
    :button_icon: icon-arrow-right
    :button_icon_position: right
    :button_icon_link:
    :content_page:
