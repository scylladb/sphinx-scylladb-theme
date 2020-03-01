
Scylla Repair
=============

Scylla Repair is a process which runs in the background and synchronizes the data between nodes, so that eventually, all the replicas hold the same data.
Data stored on nodes can become inconsistent with other replicas over time which is why repairs are a necessary part of database maintenance.
Using Scylla repair, makes data on the node consistent with the other nodes in the cluster. The best use of Scylla repair is to have Scylla Manager schedule and run the repairs for you. 

.. note:: Run the :doc:`nodetool repair </operating-scylla/nodetool-commands/repair/>` command regularly. If you delete data frequently, it should be more often than the value of ``gc_grace_seconds`` (by default: 10 days), for example, every week. Use the **nodetool repair -pr** on each node in the cluster, sequentially.

                                                                       

See also

:doc:`Scylla  Manager</operating-scylla/manager/index/>`





