Panel Box
=========

This is a custom directive which creates boxes on the index screens. Do not use the panel-box on the root ``index.rst``.

For example, using:

.. code-block:: rst

   .. panel-box::
      :title: Admin
      :id: "admin"
      :class: my-panel

      Test

Results in:

.. panel-box::
    :title: Admin
    :id: "admin"
    :class: my-panel

    Test
