
Remove a Node from a Scylla Cluster (Down Scale)
************************************************

Use these instructions when you want to remove nodes in-order to reduce the size of your cluster. 

-----------------
Procedure
-----------------

1. Run the :doc:`nodetool status </operating-scylla/nodetool-commands/status>` command to check the status of the nodes in your cluster

.. code-block:: shell

   Datacenter: DC1
   Status=Up/Down
   State=Normal/Leaving/Joining/Moving
   --  Address        Load       Tokens  Owns (effective)                         Host ID         Rack
   UN  192.168.1.201  112.82 KB  256     32.7%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   B1
   UN  192.168.1.202  91.11 KB   256     32.9%             125ed9f4-7777-1dbn-mac8-43fddce9123e   B1
   DN  192.168.1.203  124.42 KB  256     32.6%             675ed9f4-6564-6dbd-can8-43fddce952gy   B1

2. If the node status is Up Normal (UN), use the ``nodetool decommission`` command.

Using ``nodetool decommission`` guarantees that the node streams its own data to the remaining nodes, so there is no possibility
of data loss. Aside from hard node failures, ``nodetool decommission`` is always preferred.

.. include:: /operating-scylla/_common/decommission_warning.rst

Use the ``nodetool netstats`` command to monitor the progress of the token reallocation.
             
3. If the node status is Down Normal (DN) and cannot be restored, use the ``nodetool removenode`` command

**Attention** When using ``nodetool removenode``, the data in the node is not streamed. For this reason,
in order to be able to keep quorum consistencies it is extremely advisable to run a full cluster repair before
``nodetool removenode`` so all existing replicas have the most up to date data.

When using ``nodetool removenode`` we need to use the Host ID of the node

**For Example:**

``nodetool removenode 675ed9f4-6564-6dbd-can8-43fddce952gy``

Use the ``nodetool netstats`` command to monitor the progress of the token reallocation

4. If the node status is Up Joining (UJ) and does not chenge to Up Normal,  see this procedure on how to `remove the node <../safely-removing-joining-node>`_.

5. Verify that the node removed by using the ``nodetool status`` command

.. code-block:: shell

   Datacenter: DC1
   Status=Up/Down
   State=Normal/Leaving/Joining/Moving
   --  Address        Load       Tokens  Owns (effective)                         Host ID         Rack
   UN  192.168.1.201  112.82 KB  256     32.7%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   B1
   UN  192.168.1.202  91.11 KB   256     32.9%             125ed9f4-7777-1dbn-mac8-43fddce9123e   B1

6. When a node was removed from the cluster his data doesn't removed automatically. The data and commitlog stored on that node need to be removed manually.
If you do not do this the old data will still be counted against the load on that node.

To delete the data use

.. include:: /rst_include/clean-data-code.rst
