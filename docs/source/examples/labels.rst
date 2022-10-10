Labels
======

A custom role that lets you add labels to your text.

For example, you could use the label role to promote experimental features or highlight that a feature is only available in a specific software version.

Syntax
------

.. code-block:: rst

   :label-<style>:`Text`


Where:

* **style:** Available values are ``default``, ``note``, ``tip``, ``caution``, ``warning``.

Usage
-----

Default
.......

Using:

.. code-block:: rst

   :label-default:`Default`, :label-note:`Note`, :label-tip:`Tip`, :label-caution:`Caution`, :label-warning:`Warning`, :label-note:`Note`


Results in:

:label-default:`Default`, :label-note:`Note`, :label-tip:`Tip`, :label-caution:`Caution`, :label-warning:`Warning`, :label-note:`Note`

Inlined with text
.................

Using:

.. code-block:: rst

   Heading :label-caution:`Beta`
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Results in:

Heading :label-caution:`Beta`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
