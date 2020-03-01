Remove a Seed Node from Seed List
*********************************

This procedure describes how to remove a seed node from the seed list.

-------------
Prerequisites
-------------

Verify that the seed node you want to remove is listed as a seed node in the ``scylla.yaml`` file by running ``cat /etc/scylla/scylla.yaml | grep seeds:``

---------
Procedure
---------

1. Update the Scylla configuration file, scylla.yaml which can be found under ``/etc/scylla/``. For example:

Seed list before removing the node:

.. code-block:: shell

   - seeds: "10.240.0.83,10.240.0.93,10.240.0.103" 

Seed list after removing the node:

.. code-block:: shell

   - seeds: "10.240.0.83,10.240.0.93" 

2. Scylla will read the updated seed list the next time it starts. You can force Scylla to read the list immediately by restarting Scylla as follows:

.. include:: /rst_include/scylla-commands-restart-index.rst
