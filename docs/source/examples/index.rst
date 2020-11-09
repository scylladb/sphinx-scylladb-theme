.. toctree::
   :hidden:

   example-topic

Examples
========

Code block with substitutions
-----------------------------

Using a code block with the ``:substitutions:`` directive and then a substitution such as ``|mon_version|``

renders

.. code-block:: bash
   :substitutions:

   |mon_version|

.. _link-format-examples:

Link Format Examples
--------------------

* This is an example of an `External Link <https://docs.scylladb.com/some-doc>`_.
* This is an example of an :ref:`Internal Link <link-format-examples>`.
* This is an example of an :doc:`Internal Doc <../index>`.
* This is an example of an :download:`download <index.rst>`.
* This is an example of an `Internal Doc </contributing>`_ using the external link directive.
