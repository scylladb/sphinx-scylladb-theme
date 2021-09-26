=========
Topic Box
=========

Default Topic
-------------

With Icon
=========

Using:

.. code-block:: rst

    .. topic-box::
        :title: Lorem Ipsum
        :icon: fa fa-github
        :link: #
        :anchor: Lorem ipsum

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Results in:

.. topic-box::
    :title: Lorem Ipsum
    :icon: fa fa-github
    :link: #
    :anchor: Lorem ipsum

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

With Image
==========

Using:

.. code-block:: rst

    .. topic-box::
        :title: Lorem Ipsum
        ::image: /_static/img/mascots/scylla-enterprise.svg
        :link: #
        :anchor: Lorem ipsum

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Results in:

.. topic-box::
    :title: Lorem Ipsum
    :image: /_static/img/mascots/scylla-enterprise.svg
    :link: #
    :anchor: Lorem ipsum

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

With Horizontal Scroll (Mobile)
===============================

Using:

.. code-block::

    .. raw:: html

        <div class="topics-grid topics-grid--scrollable grid-container full">

        <div class="grid-x grid-margin-x hs">

    .. topic-box::
        :title: Lorem ipsum
        :link: scylla-cloud
        :class: large-4
        :anchor: Lorem ipsum

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    .. topic-box::
        :title: Lorem ipsum
        :link: scylla-cloud
        :class: large-4
        :anchor: Lorem ipsum

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    .. topic-box::
        :title: Lorem ipsum
        :link: scylla-cloud
        :class: large-4
        :anchor: Lorem ipsum

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    .. raw:: html

        </div></div>


Results in:

.. raw:: html

    <div class="topics-grid topics-grid--scrollable grid-container full">

    <div class="grid-x grid-margin-x hs">

.. topic-box::
    :title: Lorem ipsum
    :link: scylla-cloud
    :class: large-4
    :anchor: Lorem ipsum

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. topic-box::
    :title: Lorem ipsum
    :link: scylla-cloud
    :class: large-4
    :anchor: Lorem ipsum

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. topic-box::
    :title: Lorem ipsum
    :link: scylla-cloud
    :class: large-4
    :anchor: Lorem ipsum

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. raw:: html

    </div></div>

Product Topic
-------------

Using:

.. code-block:: rst

    .. topic-box::
        :title: Lorem Ipsum
        :link: #
        :image: /_static/img/mascots/scylla-enterprise.svg
        :class: topic-box--product

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Results in:

.. topic-box::
    :title: Lorem Ipsum
    :link: #
    :image: /_static/img/mascots/scylla-enterprise.svg
    :class: topic-box--product

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.


Topic Grid
----------

Using:

.. code-block:: rst

    .. raw:: html

        <div class="topics-grid topics-grid--products">

            <h2 class="topics-grid__title">Lorem Ipsum</h2>
            <p class="topics-grid__text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>

            <div class="grid-container full">
                <div class="grid-x grid-margin-x">

    .. topic-box::
        :title: Lorem Ipsum
        :link: #
        :image: /_static/img/mascots/scylla-enterprise.svg
        :class: topic-box--product,large-3,small-6

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    .. topic-box::
        :title: Lorem Ipsum
        :link: #
        :image: /_static/img/mascots/scylla-enterprise.svg
        :class: topic-box--product,large-3,small-6

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    .. topic-box::
        :title: Lorem Ipsum
        :link: #
        :image: /_static/img/mascots/scylla-enterprise.svg
        :class: topic-box--product,large-3,small-6

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    .. topic-box::
        :title: Lorem Ipsum
        :link: #
        :image: /_static/img/mascots/scylla-enterprise.svg
        :class: topic-box--product,large-3,small-6

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    .. topic-box::
        :title: Lorem Ipsum
        :link: #
        :image: /_static/img/mascots/scylla-enterprise.svg
        :class: topic-box--product,large-3,small-6

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    .. topic-box::
        :title: Lorem Ipsum
        :link: #
        :image: /_static/img/mascots/scylla-enterprise.svg
        :class: topic-box--product,large-3,small-6

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    .. topic-box::
        :title: Lorem Ipsum
        :link: #
        :image: /_static/img/mascots/scylla-enterprise.svg
        :class: topic-box--product,large-3,small-6

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    .. topic-box::
        :title: Lorem Ipsum
        :link: #
        :image: /_static/img/mascots/scylla-enterprise.svg
        :class: topic-box--product,large-3,small-6

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    .. raw:: html

        </div></div></div>


Results in:

.. raw:: html

    <div class="topics-grid topics-grid--products">

        <h2 class="topics-grid__title">Lorem Ipsum</h2>
        <p class="topics-grid__text">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>

        <div class="grid-container full">
            <div class="grid-x grid-margin-x">

.. topic-box::
    :title: Lorem Ipsum
    :link: #
    :image: /_static/img/mascots/scylla-enterprise.svg
    :class: topic-box--product,large-3,small-6

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. topic-box::
    :title: Lorem Ipsum
    :link: #
    :image: /_static/img/mascots/scylla-enterprise.svg
    :class: topic-box--product,large-3,small-6

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. topic-box::
    :title: Lorem Ipsum
    :link: #
    :image: /_static/img/mascots/scylla-enterprise.svg
    :class: topic-box--product,large-3,small-6

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. topic-box::
    :title: Lorem Ipsum
    :link: #
    :image: /_static/img/mascots/scylla-enterprise.svg
    :class: topic-box--product,large-3,small-6

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. topic-box::
    :title: Lorem Ipsum
    :link: #
    :image: /_static/img/mascots/scylla-enterprise.svg
    :class: topic-box--product,large-3,small-6

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. topic-box::
    :title: Lorem Ipsum
    :link: #
    :image: /_static/img/mascots/scylla-enterprise.svg
    :class: topic-box--product,large-3,small-6

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. topic-box::
    :title: Lorem Ipsum
    :link: #
    :image: /_static/img/mascots/scylla-enterprise.svg
    :class: topic-box--product,large-3,small-6

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. topic-box::
    :title: Lorem Ipsum
    :link: #
    :image: /_static/img/mascots/scylla-enterprise.svg
    :class: topic-box--product,large-3,small-6

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

.. raw:: html

    </div></div></div>
