Admonitions
===========

At ScyllaDB, we limit the admonitions. Although |rst| will allow for more, use the following:

* Note_
* Caution_
* Warning_
* Tip_

Note
----

Use a note to point out something to the reader. This action does not have any risk.

.. code-block:: rst

   .. note:: 
      
      text follows here

      * Option a
      * Option b

Renders as:

.. note::
   
   text follows here

   * Option a
   * Option b


Caution
-------

Use caution if there is any potential risk to data loss or lower performance.

.. code-block:: rst

   .. caution::
      
      look out

      1. Step a
      2. Step b

Renders as

.. caution::

   look out

   1. Step a
   2. Step b


Warning
-------

Use warning if there is any potential risk to total data loss or physical danger.

.. code-block:: rst

   .. warning:: take care

Renders as:

.. warning:: take care

Tip
---

This is a time-saving or performance enhancing option.

.. code-block:: rst

   .. tip:: here's a tip

Renders as:

.. tip:: here's a tip
