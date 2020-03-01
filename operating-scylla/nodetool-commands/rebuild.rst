Nodetool rebuild
================

| **rebuild** ``[<src-dc-name>]`` - This command rebuilds a node's data by streaming data from other nodes in the cluster (similarly to bootstrap).
| Rebuild operates on multiple nodes in a Scylla cluster, it streams data from a single source replica when rebuilding a token range, when executing the command Scylla first figures out which ranges the local node (the one we want to rebuild) is responsible for. Then which node in the cluster contains the same ranges. Finally, Scylla streams the data to the local node.
 
| When :doc:`adding a new data-center into an existing Scylla cluster </operating-scylla/procedures/cluster-management/add_dc_to_exist_dc/>` use the rebuild command.

|
| **Note**: Scylla rebuild process continues to run in the background, even if the nodetool command is killed or the process is interrupted.

| For example, when nodetool command is killed 

.. code-block:: shell

   nodetool rebuild <src-dc-name>

.. include:: nodetool-index.rst
