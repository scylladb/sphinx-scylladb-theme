Grid
====

A custom directive that creates responsive grid layouts using Foundation's grid system.
Perfect for organizing topic boxes in rows and columns.

.. note::
   The grid directive currently supports only :doc:`topic-box` directives as content.
   Other content types are not supported within grids.

Syntax
------

.. code-block:: rst

   .. grid::
      <options>

      .. topic-box::
         <topic-box options>

         <content>

Options
-------

The ``grid`` directive supports the following options:

.. list-table::
  :widths: 20 20 10 20 30
  :header-rows: 1

  * - Option
    - Type
    - Required
    - Example Value
    - Description
  * - ``class``
    - string
    -
    - large-3
    - Custom CSS class.
  * - ``type``
    - string
    -
    - scrollable
    - Grid type. Available values: ``default``, ``scrollable``, ``products``.
  * - ``title``
    - string
    -
    - Lorem Ipsum
    - Grid title.
  * - ``text``
    - string
    -
    - Lorem ipsum dolor sit amet
    - Grid description.

Supported Content
-----------------

The grid directive works exclusively with **topic-box** directives. Each topic-box within a grid should include Foundation grid classes in its ``:class:`` option to control layout:

- ``large-3`` - 4 columns per row on desktop
- ``large-4`` - 3 columns per row on desktop
- ``large-6`` - 2 columns per row on desktop
- ``large-12`` - 1 column per row (full width)
- ``small-6`` - 2 columns per row on mobile

For more information about topic-box options and usage, see :doc:`topic-box`.

Usage
-----

Basic grid
..........

Using:

.. code-block:: rst

    .. grid::
        :type: default

        .. topic-box::
            :title: Quick Start
            :link: #
            :class: large-6
            :anchor: Get Started

            Learn how to get started with ScyllaDB.

        .. topic-box::
            :title: Architecture
            :link: #
            :class: large-6
            :anchor: Learn More

            Understand ScyllaDB's architecture and design principles.

Results in:

.. grid::
    :type: default

    .. topic-box::
        :title: Quick Start
        :link: /getting-started
        :class: large-6
        :anchor: Get Started

        Learn how to get started with ScyllaDB.

    .. topic-box::
        :title: Architecture
        :link: /architecture
        :class: large-6
        :anchor: Learn More

        Understand ScyllaDB's architecture and design principles.

Scrollable grid
.................

Using:

.. code-block:: rst

    .. grid::
        :type: scrollable

        .. topic-box::
            :title: Installation
            :link: #
            :class: large-3
            :anchor: Install

            Install ScyllaDB on your system.

        .. topic-box::
            :title: Configuration
            :link: #
            :class: large-3
            :anchor: Configure

            Configure ScyllaDB for your needs.

        .. topic-box::
            :title: Security
            :link: #
            :class: large-3
            :anchor: Secure

            Secure your ScyllaDB deployment.

        .. topic-box::
            :title: Monitoring
            :link: #
            :class: large-3
            :anchor: Monitor

            Monitor your ScyllaDB cluster.

Results in:

.. grid::
    :type: scrollable

    .. topic-box::
        :title: Installation
        :link: #
        :class: large-3
        :anchor: Install

        Install ScyllaDB on your system.

    .. topic-box::
        :title: Configuration
        :link: #
        :class: large-3
        :anchor: Configure

        Configure ScyllaDB for your needs.

    .. topic-box::
        :title: Security
        :link: #
        :class: large-3
        :anchor: Secure

        Secure your ScyllaDB deployment.

    .. topic-box::
        :title: Monitoring
        :link: /monitoring
        :class: large-3
        :anchor: Monitor

        Monitor your ScyllaDB cluster.

Products grid
.............

Using:

.. code-block:: rst

    .. grid::
        :type: products
        :title: ScyllaDB Products
        :text: Choose the right ScyllaDB product for your needs

        .. topic-box::
            :title: ScyllaDB Enterprise
            :link: #
            :image: /_static/img/mascots-2/enterprise.svg
            :class: topic-box--product,large-4,small-6

            Enterprise-grade NoSQL database with advanced features and support.

        .. topic-box::
            :title: ScyllaDB Cloud
            :link: #
            :image: /_static/img/mascots-2/cloud.svg
            :class: topic-box--product,large-4,small-6

            Fully managed NoSQL database as a service.

        .. topic-box::
            :title: ScyllaDB Open Source
            :link: #
            :image: /_static/img/mascots-2/opensource.svg
            :class: topic-box--product,large-4,small-6

            Free and open-source NoSQL database.

Results in:

.. grid::
    :type: products
    :title: ScyllaDB Products
    :text: Choose the right ScyllaDB product for your needs

    .. topic-box::
        :title: ScyllaDB Enterprise
        :link: #
        :image: /_static/img/mascots-2/enterprise.svg
        :class: topic-box--product,large-4,small-6

        Enterprise-grade NoSQL database with advanced features and support.

    .. topic-box::
        :title: ScyllaDB Cloud
        :link: #
        :image: /_static/img/mascots-2/cloud.svg
        :class: topic-box--product,large-4,small-6

        Fully managed NoSQL database as a service.

    .. topic-box::
        :title: ScyllaDB Docs
        :link: #
        :image: /_static/img/mascots-2/docs.svg
        :class: topic-box--product,large-4,small-6

        Documentation for ScyllaDB.
