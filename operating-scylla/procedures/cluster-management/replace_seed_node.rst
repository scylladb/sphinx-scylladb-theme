
Replacing a dead seed node
**************************

In Scylla it is not possible to bootstrap a seed node. The following steps describe how to replace a dead seed node

-------------
Prerequisites
-------------

Verify that the node is a seed node. Use the command below.
``cat /etc/scylla/scylla.yaml | grep seeds:``
If the dead node's IP is in the seeds list it needa to be replaced.

---------
Procedure
---------

* Perform steps 1-3 for all the nodes in the cluster:

1. Promote an existing node from the cluster to be a seed node by adding the node IP to the seed list in the ``scylla.yaml`` file. It can be found under ``/etc/scylla/`` 
2. Remove the dead node IP from the seeds providers list
3. Restart the node in the cluster using 

.. include:: /rst_include/scylla-commands-restart-index.rst

* Replace the dead node using the :doc:`Replace a dead node procedure </operating-scylla/procedures/cluster-management/replace_dead_node/>`

It is recommended to have more than one seed node in your cluster (it's not allowed to define all the node in the cluster as seed node).


