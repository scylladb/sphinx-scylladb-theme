Labels
======

A custom directive that lets you add labels to your text.

For example, you could use the label directive to promote experimental features or highlight that a feature is only available in a specific software version.

Syntax
------

.. code-block:: rst

   .. labels::
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
  * - ``class``
    - string
    -
    -
    - Custom CSS class.
  * - ``style``
    - string
    -
    -
    - Label style. Available values are ``default``, ``note``, ``tip``, ``caution``, ``warning``.

Usage
-----

Default
.......

Using:

.. code-block:: rst

   .. label::
      :text: Default

   .. label::
      :style: note
      :text: Note

   .. label::
      :style: tip
      :text: Tip

   .. label::
      :style: caution
      :text: Caution

   .. label::
      :style: warning
      :text: Warning


Results in:

   .. label::
      :text: Default

   .. label::
      :style: note
      :text: Note

   .. label::
      :style: tip
      :text: Tip

   .. label::
      :style: caution
      :text: Caution

   .. label::
      :style: warning
      :text: Warning
