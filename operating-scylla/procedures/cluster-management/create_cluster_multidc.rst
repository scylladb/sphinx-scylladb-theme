
Create a Scylla Cluster - Multi Data Centers (DC)
*************************************************

Consult with the table below if each node in the cluster has internal IP for internal DC communication and external IP for cross DC communication.

Single Multi Data Centers Configuration Table
---------------------------------------------

=====================  ===========================
Parameter                    Multi DC 
=====================  ===========================
seeds	               External IP address                
---------------------  ---------------------------
listen_address         Internal IP address          
---------------------  ---------------------------
rpc_address            Internal IP address      
---------------------  ---------------------------
broadcast_address      External IP address
---------------------  ---------------------------
broadcast_rpc_address  External IP address
---------------------  ---------------------------
endpoint_snitch        GossipingPropertyFileSnitch
=====================  ===========================

**Important**

If the node have two physical network interfaces in a multi-datacenter installation.
Set ``listen_address`` to this node's private IP or hostname.
Set ``broadcast_address`` to the second IP or hostname (for communication between datacenters).
Set ``listen_on_broadcast_address`` to true.
Open the storage_port or ssl_storage_port on the public IP firewall.

-------------
Prerequisites
-------------

.. include:: /operating-scylla/procedures/_common/create_cluster_prerequisites_include.rst

* Decide the name of the rack, for example:  RACK1, RACK2 or RC1, RC2.  
* Decide the name of the data-center, for example: DC1, DC2 or US-DC, ASIA-DC.

**Choose the data-center name carefully, it is not possible to rename a data-center later**

When working with production environments you must choose one of the snitches below:

* Ec2MultiRegionSnitch_ - for AWS cloud-based, multi-data-center deployments.

* GossipingPropertyFileSnitch_ - for bare metal and cloud (other than AWS) deployments. 

.. _Ec2MultiRegionSnitch: /operating-scylla/system-configuration/snitch/#ec2multiregionsnitch
.. _GossipingPropertyFileSnitch: /operating-scylla/system-configuration/snitch/#gossipingpropertyfilesnitch

---------
Procedure
---------

These steps need to be done for each of the nodes in the new cluster.

1. Install Scylla on a node, see :doc:`Getting Started</getting-started/index>` for further instructions, create as many nodes that you need
Follow the Scylla install procedure up to scylla.yaml configuration phase.

In case that your node starts during the process follow :doc:`these instructions </operating-scylla/procedures/cluster-management/clear_data>` 

2. In the ``scylla.yaml`` file edit the parameters listed below,
the file can be found under ``/etc/scylla/``

- **cluster_name** - Set the selected cluster_name
- **seeds** - Set the selected seed nodes
- **listen_address** - IP address that the Scylla use to connect to other Scylla nodes in the cluster
- **auto_bootstrap** - By default, this parameter is set to true, it allow new nodes to migrate data to themselves automatically
- **endpoint_snitch** - Set the selected snitch
- **rpc_address** - Address for client connection (Thrift, CQLSH)

3. In the ``cassandra-rackdc.properties`` file, edit the rack and data-center information. 
The file can be found under ``/etc/scylla/``.

To save bandwidth, add the ``prefer_local=true`` parameter. Scylla will use the node private (local) IP address when the nodes are in the same data-center.

4. After you have installed and configured Scylla and edit ``scylla.yaml`` on all nodes, start the seeds nodes one at a time, and then start the rest of the nodes in your cluster

.. include:: /rst_include/scylla-commands-start-index.rst

5. Verify that the node added to the cluster
``nodetool status``

**For Example:**

In this example we will show how to install a nine nodes cluster, we will have six seed nodes 

1. Installing nine Scylla nodes, three nodes in each data-center (U.S, ASIA, EUROPE) and two seed nodes in each data-center, the IP's are:

.. code-block:: shell

   U.S Data-center 
   Node# Private IP    Public IP
   Node1 192.168.1.201 54.187.36.59 (seed)
   Node2 192.168.1.202 54.187.142.201 (seed)
   Node3 192.168.1.203 54.187.168.20 
   
   ASIA Data-center 
   Node# Private IP    Public IP
   Node4 192.168.1.204 54.191.72.56 (seed)
   Node5 192.168.1.205 54.187.25.99 (seed)
   Node6 192.168.1.206 54.191.2.121 
   
   EUROPE Data-center 
   Node# Private IP    Public IP       
   Node7 192.168.1.207 54.160.174.243 (seed)
   Node8 192.168.1.208 54.235.9.159 (seed)
   Node9 192.168.1.209 54.146.228.25
 
2. In each Scylla node, edit the ``scylla.yaml`` file (example of one node per DC below)

**U.S Data-center - 192.168.1.201**

.. code-block:: shell

   cluster_name: 'multi_dc_demo'
   seeds: "54.187.36.59,54.187.142.201,54.191.72.56,54.187.25.99,54.160.174.243,54.235.9.159"
   endpoint_snitch: GossipingPropertyFileSnitch
   rpc_address: "192.168.1.201"
   listen_address: "192.168.1.201"
   broadcast_address: "54.187.36.59"
   broadcast_rpc_address: "54.187.36.59"
   listen_on_broadcast_address: true (optional)

**ASIA Data-center - 192.168.1.204**

.. code-block:: shell

   cluster_name: 'multi_dc_demo'
   seeds: "54.187.36.59,54.187.142.201,54.191.72.56,54.187.25.99,54.160.174.243,54.235.9.159"
   endpoint_snitch: GossipingPropertyFileSnitch
   rpc_address: "192.168.1.204"
   listen_address: "192.168.1.204"
   broadcast_address: "54.191.72.56"
   broadcast_rpc_address: "54.191.72.56"
   listen_on_broadcast_address: true (optional)

**EUROPE Data-center - 192.168.1.207**

.. code-block:: shell

   cluster_name: 'multi_dc_demo'
   seeds: "54.187.36.59,54.187.142.201,54.191.72.56,54.187.25.99,54.160.174.243,54.235.9.159"
   endpoint_snitch: GossipingPropertyFileSnitch
   rpc_address: "192.168.1.207"
   listen_address: "192.168.1.207"
   broadcast_address: "54.160.174.243"
   broadcast_rpc_address: "54.160.174.243"
   listen_on_broadcast_address: true (optional)

3. In each Scylla node, edit the ``cassandra-rackdc.properties`` file with the relevant rack and data-center information 

**Nodes 1-3**

.. code-block:: shell

   dc=US-DC
   rack=RACK1


**Nodes 4-6**

.. code-block:: shell

   dc=ASIA-DC
   rack=RACK1

**Nodes 7-9**

.. code-block:: shell

   dc=EUROPE-DC
   rack=RACK1

4. Starting Scylla nodes, starting with the seed nodes. 

.. include:: /rst_include/scylla-commands-start-index.rst

.. code-block:: shell

   192.168.1.201 
   192.168.1.202
   192.168.1.204
   192.168.1.205
   192.168.1.207
   192.168.1.208

And than we will start the remaining of the nodes

.. code-block:: shell

   192.168.1.203
   192.168.1.206
   192.168.1.209

5. Verify that the node added to the cluster by using the ``nodetool status`` command

.. code-block:: shell

   nodetool status

   Datacenter: US-DC
   =========================
   Status=Up/Down
   |/ State=Normal/Leaving/Joining/Moving
   --   Address         Load            Tokens  Owns            Host ID                                 Rack
   UN   54.191.2.121    120.97 KB       256     ?               c84b80ea-cb60-422b-bc72-fa86ede4ac2e    RACK1
   UN   54.191.72.56    109.54 KB       256     ?               129087eb-9aea-4af6-92c6-99fdadb39c33    RACK1
   UN   54.187.25.99    104.94 KB       256     ?               0540c7d7-2622-4f1f-a3f0-acb39282e0fc    RACK1
   
   Datacenter: ASIA-DC
   =======================
   Status=Up/Down
   |/ State=Normal/Leaving/Joining/Moving
   --   Address         Load            Tokens  Owns            Host ID                                 Rack
   UN   54.160.174.243  109.54 KB       256     ?               c7686ffd-7a5b-4124-858e-df2e61130aaa    RACK1
   UN   54.235.9.159    109.75 KB       256     ?               39798227-9f6f-4868-8193-08570856c09a    RACK1
   UN   54.146.228.25   128.33 KB       256     ?               7a4957a1-9590-4434-9746-9c8a6f796a0c    RACK1
  
   Datacenter: EUROPE-DC
   =========================
   Status=Up/Down
   |/ State=Normal/Leaving/Joining/Moving
   --   Address         Load            Tokens  Owns            Host ID                                 Rack
   UN   54.187.36.59    114.35 KB       256     ?               4c3e1533-1b78-45bf-8bd4-818090f019ab    RACK1
   UN   54.187.142.201  109.54 KB       256     ?               d99967d6-987c-4a54-829d-86d1b921470f    RACK1
   UN   54.187.168.20   109.54 KB       256     ?               2329c2e0-64e1-41dc-8202-74403a40f851    RACK1


See also:

:doc:`Create a Scylla Cluster - Single Data Center (DC) </operating-scylla/procedures/cluster-management/create_cluster>`


