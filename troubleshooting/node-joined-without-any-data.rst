Node Joined With No Data
========================
When a Scylla node joins the ring, it is visible by the other nodes in the cluster in the ``UJ`` (Up Joining) state. Its data steadily grows until it has its share of the data and then switches to the ``UN`` (Up Normal) state. This troubleshooting guide describes what to do in cases where the node joins the cluster directly into the ``UN`` state -  without any data.

.. note:: This procedure only covers the situation in which a new node joins the cluster. Nodes that are replacing existing nodes following the :doc:`Replace A Dead Node </operating-scylla/procedures/cluster-management/replace_dead_node/>` procedure are expected to be in ``UN`` state from the start.

The Problem
^^^^^^^^^^^

There are two possible causes for a new node not acquiring data from its peers:

* The new node's configuration file (scylla.yml) lists only itself as the seed node and doesn't use the same seed address as the other nodes in the cluster do.
* The node was added with the ``auto_bootstrap`` flag set to *False*

Both scenarios constitute user error and are the incorrect way of adding new nodes to the cluster. See :doc:`Adding New Node </operating-scylla/procedures/cluster-management/add_node_to_cluster/>` for more details.
In this article, we will discuss what can be done to safely restore your cluster in case this situation happens.

.. warning:: It is important that you **do not** run nodetool cleanup in any of the other nodes in the cluster until this is fixed. Otherwise, data may have already been deleted from the existing nodes.

Solution
^^^^^^^^

Steps to fix:

#. For every node that joined the cluster directly in UN state, run nodetool decommission serially. Do not decommission more than one node at the same time.
#. Make sure to clean the data from the decommissioned node

   .. include:: /rst_include/clean-data-code.rst

   Actual directories might be different than above, check your ``scylla.yaml`` to validate.   
   
#. Once all new nodes are decommissioned, add them again with the :doc:`correct procedure </operating-scylla/procedures/cluster-management/add_node_to_cluster/>`. Do not add nodes as seeds. Do not add nodes with the ``auto_bootstrap`` flag set to *False*.


Other important considerations:

* Avoid running ``nodetool removenode`` for the new nodes. Running ``nodetool removenode`` instead of ``nodetool decommission`` will cause the new writes that were sent to the new nodes to be lost. In all cases, you should always prefer decommission over removenode. Use removenode **only** cases where there is no other way to restart the node.
* While running a repair in the cluster will bring some data back to the new node and may be a way of restoring its data, it will take much longer than the procedure suggested. It is also important to keep in mind that one copy is lost per each node that was inserted directly into the UN state. In the extreme case in which N nodes were added where N is your replication factor, some data may have been permanently lost and repairs will not be able to restore it. Therefore, repair is not recommended to fix this issue, except in situations where the user is aware and their consistency model can tolerate missing data points.
  

