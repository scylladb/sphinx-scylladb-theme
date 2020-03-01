
Replace a Dead Node in a Scylla Cluster 
***************************************

Replace dead node operation will cause the other nodes in the cluster to stream data to the node that was replaced. This operation can take some time (depending on the data size and network bandwidth).

This procedure is for replacing one dead node. To replace more than one dead node, run the full procedure to completion one node at a time.

-------------
Prerequisites
-------------

* Verify the status of the node using :doc:`nodetool status </operating-scylla/nodetool-commands/status>` command, the node with status DN is down and need to be replaced

.. code-block:: shell

   Datacenter: DC1
   Status=Up/Down
   State=Normal/Leaving/Joining/Moving
   --  Address        Load       Tokens  Owns (effective)                         Host ID         Rack
   UN  192.168.1.201  112.82 KB  256     32.7%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   B1
   UN  192.168.1.202  91.11 KB   256     32.9%             125ed9f4-7777-1dbn-mac8-43fddce9123e   B1
   DN  192.168.1.203  124.42 KB  256     32.6%             675ed9f4-6564-6dbd-can8-43fddce952gy   B1

Login to one of the nodes in the cluster with (UN) status. Collect the following info from the node:

* cluster_name - ``cat /etc/scylla/scylla.yaml | grep cluster_name``
* seeds - ``cat /etc/scylla/scylla.yaml | grep seeds:``
* endpoint_snitch - ``cat /etc/scylla/scylla.yaml | grep endpoint_snitch``
* Scylla version - ``scylla --version``

---------
Procedure
---------

1. Check that the dead node isn't a seed node using ``cat /etc/scylla/scylla.yaml | grep seeds:``. If the dead node IP is in the list it needs to be :doc:`replaced</operating-scylla/procedures/cluster-management/replace_seed_node>`. 

2. Install Scylla on a new node, see :doc:`Getting Started</getting-started/index>` for further instructions.
Follow the Scylla install procedure up to ``scylla.yaml`` configuration phase. Make sure that Scylla version of the new node is identical to the other nodes in the cluster. 

.. include:: /operating-scylla/procedures/cluster-management/_common/match_version.rst

3. In the ``scylla.yaml`` file edit the parameters listed below.
The file can be found under ``/etc/scylla/``

- **cluster_name** - Set the selected cluster_name
 
- **listen_address** - IP address that Scylla uses to connect to other Scylla nodes in the cluster

- **seeds** - Set the selected seed nodes

- **auto_bootstrap** - By default, this parameter is set to true, it allow new nodes to migrate data to themselves automatically

- **endpoint_snitch** - Set the selected snitch

- **rpc_address** - Address for client connection (Thrift, CQL)

4. Add the ``replace_address_first_boot`` parameter to the ``scylla.yaml`` file.
This line can be added in any place in the file for the first start only. After a successful node replacement, there is no need to remove it from the ``scylla.yaml`` file unlike the ``replace_address`` parameter. 

The correct format is:

``replace_address_first_boot: 192.168.1.203``   

5. Start Scylla node.

.. include:: /rst_include/scylla-commands-start-index.rst

6. Verify that the node has been added to the cluster using ``nodetool status`` command.

**For Example:**

.. code-block:: shell

   Datacenter: DC1
   Status=Up/Down
   State=Normal/Leaving/Joining/Moving
   --  Address        Load       Tokens  Owns (effective)                         Host ID         Rack
   UN  192.168.1.201  112.82 KB  256     32.7%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   B1
   UN  192.168.1.202  91.11 KB   256     32.9%             125ed9f4-7777-1dbn-mac8-43fddce9123e   B1
   DN  192.168.1.203  124.42 KB  256     32.6%             675ed9f4-6564-6dbd-can8-43fddce952gy   B1

``192.168.1.203`` is the dead node.

The replacing node ``192.168.1.204`` will be bootstrapping data.
We will not see ``192.168.1.204`` during the bootstrap.

.. code-block:: shell

   Datacenter: dc1
   ===============
   Status=Up/Down
   |/ State=Normal/Leaving/Joining/Moving
   --  Address    Load       Tokens       Owns    Host ID                               Rack
   UN  192.168.1.201  112.82 KB  256     32.7%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   B1
   UN  192.168.1.202  91.11 KB   256     32.9%             125ed9f4-7777-1dbn-mac8-43fddce9123e   B1

Use ``nodetool gossipinfo`` to see ``192.168.1.204`` is in HIBERNATE status.

.. code-block:: shell
                         
   /192.168.1.204
     generation:1553759984                                                                                            
     heartbeat:104                      
     HOST_ID:655ae64d-e3fb-45cc-9792-2b648b151b67
     STATUS:hibernate,true
     RELEASE_VERSION:3.0.8
     X3:3                                        
     X5:                                                                                    
     NET_VERSION:0
     DC:DC1
     X4:0
     SCHEMA:2790c24e-39ff-3c0a-bf1c-cd61895b6ea1
     RPC_ADDRESS:192.168.1.204
     X2:
     RACK:B1
     INTERNAL_IP:192.168.1.204

   /192.168.1.203
     generation:1553759866
     heartbeat:2147483647
     HOST_ID:655ae64d-e3fb-45cc-9792-2b648b151b67
     STATUS:shutdown,true
     RELEASE_VERSION:3.0.8
     X3:3
     X5:0:18446744073709551615:1553759941343
     NET_VERSION:0
     DC:DC1
     X4:1
     SCHEMA:2790c24e-39ff-3c0a-bf1c-cd61895b6ea1
     RPC_ADDRESS:192.168.1.203
     RACK:B1
     LOAD:1.09776e+09
     INTERNAL_IP:192.168.1.203

After the bootstrapping is over ``nodetool status`` will show:

.. code-block:: shell

   Datacenter: DC1
   Status=Up/Down
   State=Normal/Leaving/Joining/Moving
   --  Address        Load       Tokens  Owns (effective)                         Host ID         Rack
   UN  192.168.1.201  112.82 KB  256     32.7%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   B1
   UN  192.168.1.202  91.11 KB   256     32.9%             125ed9f4-7777-1dbn-mac8-43fddce9123e   B1
   UN  192.168.1.204  124.42 KB  256     32.6%             675ed9f4-6564-6dbd-can8-43fddce952gy   B1 

7. Run the ``nodetool repair`` command on the node that was replaced to make sure that the data is synced with the other nodes in the cluster.
You can use `Scylla Manager`_ to run the repair.
 
..  _`Scylla Manager`: /operating-scylla/manager/
