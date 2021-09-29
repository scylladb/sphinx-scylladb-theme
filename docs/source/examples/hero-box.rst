Hero Box
========

This is a custom directive which creates a header on home pages. Do not use the topic-box on the subordinate `index.rst` files.

Default
-------

Using:

.. code-block:: rst

    .. hero-box::
        :title: Lorem Ipsum

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Results in:

.. hero-box::
    :title: Lorem Ipsum

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

With Image
----------


Using:

.. code-block:: rst

    .. hero-box::
        :title: Lorem Ipsum
        :image: /_static/img/mascots/scylla-enterprise.svg

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Results in:

.. hero-box::
    :title: Lorem Ipsum
    :image: /_static/img/mascots/scylla-enterprise.svg

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

With Button
-----------

Using:

.. code-block:: rst

    .. hero-box::
        :title: Lorem Ipsum
        :image: /_static/img/mascots/scylla-enterprise.svg
        :button_icon: fa fa-github
        :button_url: #
        :button_text: Project Name

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Results in:

.. hero-box::
    :title: Lorem Ipsum
    :image: /_static/img/mascots/scylla-enterprise.svg
    :button_icon: fa fa-github
    :button_url: #
    :button_text: Project Name

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
