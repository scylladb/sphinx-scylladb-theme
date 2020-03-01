Nodetool repair
===============

**repair** - A process which runs in the background and synchronizes the data between nodes, so that eventually, all the replicas hold the same data.

The repair command needs to be performed on **all** the nodes in the cluster.

.. note:: Run the :doc:`nodetool repair </operating-scylla/nodetool-commands/repair/>` command regularly. If you delete data frequently, it should be more often than the value of ``gc_grace_seconds`` (by default: 10 days), for example, every week. Use the **nodetool repair -pr** on each node in the cluster, sequentially.

  

Scylla nodetool repair command supports the following options:
                                                                                                         

- ``-dc`` ``--in-dc`` executes a repair on all nodes in the specified named datacenter. The datacenter must be a local datacenter.                

  For example: 

  ::

     nodetool repair -dc US_DC
     nodetool repair --in-dc US_DC

- ``-et`` ``--end-token`` executes a repair on the specified node/s starting with the first token and ending with the specified UUID token. 

  For example: 

  ::

     nodetool repair -et 90874935784
     nodetool repair --end-token 90874935784

- ``-hosts`` ``--in-hosts`` executes a repair on a specific hosts, using host ID or Address.

  For example: 

  ::

     nodetool repair -hosts cdc295d7-c076-4b07-af69-1385fefdb40b
     nodetool repair --in-hosts cdc295d7-c076-4b07-af69-1385fefdb40b
     nodetool repair --in-hosts 172.17.0.2

- ``-local`` ``--in-local-dc`` executes a repair on the nodes in the local datacenter only .                                                                                    

  For example: 

  ::

     nodetool repair -local
     nodetool repair --in-local-dc

- ``-pr`` ``--partitioner-range`` executes a repair only on the primary replica returned by the partitioner.                                                                          

  For example: 
  
  ::

     nodetool repair -pr
     nodetool repair --partitioner-range

- ``-st`` ``--start-token`` executes a repair on a range of node/s starting with the start token (the token specified).                                                               

  For example: 

  ::

     nodetool repair -st 10474535988
     nodetool repair --start-token

- ``keyspace`` executes a repair on a specific keyspace. The default is all keyspaces.   

  For example: 

  ::

     nodetool repair <my_keyspace>


- ``table`` executes a repair on a specific table or a list of space-delimited table names. The default is all tables.


  For example: 

  
  ::

     nodetool repair <my_keyspace> <my_table>

See also

:doc:`Scylla  Manager</operating-scylla/manager/index/>` 

.. include:: nodetool-index.rst
