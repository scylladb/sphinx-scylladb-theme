Panel box
=========

A custom directive to creates boxes on subordinate ``index.rst`` files.

.. warning:: Do not use the panel-box on the root ``index.rst``.

Syntax
------

.. code-block:: rst

   .. panel-box::
      <options>

      <text>

Options
-------

The ``panel-box`` directive supports the following options:

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

Usage
-----

For example, using:

.. code-block:: rst

   .. panel-box::
      :title: Title

      Body

Results in:

.. panel-box::
    :title: Title

    Body

Compatibility with previous versions
------------------------------------

Some panel boxes in the open-source project where defined with raw html as follows:

.. code-block:: rst

  .. raw:: html

    <div class="panel callout radius animated">
        <div class="row">
          <div class="medium-3 columns">
            <h5 id="getting-started">Title</h5>
          </div>
          <div class="medium-9 columns">
            Body
          </div>
        </div>
    </div>

This example tests how the previous panel box is rendered:

.. raw:: html

  <div class="panel callout radius animated">
      <div class="row">
        <div class="medium-3 columns">
          <h5 id="getting-started">Title</h5>
        </div>
        <div class="medium-9 columns">
          Body
        </div>
      </div>
  </div>
