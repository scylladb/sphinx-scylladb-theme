
==================
Cluster Management
==================

.. versionadded:: 1.1 Scylla Manager

A *managed cluster* is a cluster which is under management by Scylla Manager. 

Scylla Manager is is a centralized cluster administration and recurrent tasks automation tool which includes automation of repairs. Using *sctool*, you will be able to add and remove clusters from Scylla Manager.


.. contents:: 
   :depth: 1
   :local:


Add a new managed cluster
-------------------------

Using sctool you add the specified cluster(s) to the manager. Once a  Scylla cluster is added, a  Repair unit is automatically created for every keyspace within the cluster, including system keyspaces. In addition, a weekly repair task is added.

You can add multiple clusters to Scylla Manager, but each one needs to be added separately. 

**Procedure**

1. From the Scylla Manager Server, run:

.. code-block:: shell

   sctool cluster add --hosts <hostList> --shard-count <int> [--name <alias>] [flags]

For parameter definitions refer to `cluster add parameters <../sctool/#cluster-add-parameters>`_.


Once added, the command returns a repair unit / cluster ID. This ID can be retrieved using `cluster list <../sctool/#cluster-list>`_. 

Add a new cluster example
.........................

In this example, a 16 shard cluster named **scylla-1** containing 2 nodes (172.16.1.10 and 172.16.1.2) is created. Once added, the command replies with **30a538a0-9bdb-4276-a69d-60e19197fd93**, the repair unit (cluster ID) ID.

.. code-block:: shell
                
   sctool cluster add --hosts=172.16.1.10,172.16.1.2 --name scylla-1 --shard-count=16 

     30a538a0-9bdb-4276-a69d-60e19197fd93   

Delete a managed cluster
------------------------

This action does **not** decommission the cluster, which will continue to serve requests, rather it removes it from the scope of Scylla Manager.


1. From the Scylla Manager Server, run:

.. code-block:: shell

   sctool cluster delete --cluster <clusterName|ID> [flags]
 

For parameter definitions refer to `cluster delete parameters <../sctool/#cluster-delete-parameters>`_.


Delete a cluster example
........................

In this example, you will delete the cluster you created in `Add a new managed cluster`_, using the alias name scylla-1. The same procedure could have been done using the UUID 30a538a0-9bdb-4276-a69d-60e19197fd93.

.. code-block:: shell
                
   sctool cluster delete -c scylla-1 
        
