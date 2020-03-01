Create a Scylla Cluster - Single Data Center (DC)
*************************************************

-------------
Prerequisites
-------------

.. include:: /operating-scylla/procedures/_common/create_cluster_prerequisites_include.rst

---------
Procedure
---------

These steps need to be done for each of the nodes in the new cluster.

1. Install Scylla on a node, see :doc:`Getting Started</getting-started/index>` for further instructions.
Follow the Scylla install procedure up to ``scylla.yaml`` configuration phase.

In case that the node starts during the process follow :doc:`these instructions </operating-scylla/procedures/cluster-management/clear_data>` 

2. In the ``scylla.yaml`` file edit the parameters listed below.
The file can be found under ``/etc/scylla/``

- **cluster_name** - Set the selected cluster_name
- **seeds** - Set the selected seed nodes
- **listen_address** - IP address that Scylla used to connect to other Scylla nodes in the cluster
- **auto_bootstrap** - By default, this parameter is set to **true**, it allows new nodes to migrate data to themselves automatically.
- **endpoint_snitch** - Set the selected snitch
- **rpc_address** - Address for client connection (Thrift, CQL)

3. This step needs to be done only if using **GossipingPropertyFileSnitch**.
In the ``cassandra-rackdc.properties`` file edit the parameters listed below.
The file can be found under ``/etc/scylla/``

- **dc** - Set the datacenter name
- **rack** - Set the rack name

For example:

.. code-block:: shell
   
   # cassandra-rackdc.properties
   #
   # The lines may include white spaces at the beginning and the end.
   # The rack and data center names may also include white spaces.
   # All trailing and leading white spaces will be trimmed.
   #
   dc=thedatacentername
   rack=therackname
   # prefer_local=<false | true>
   # dc_suffix=<Data Center name suffix, used by EC2SnitchXXX snitches>
   
4. After Scylla has been installed and configured edit ``scylla.yaml`` file on all the nodes, start the seed nodes one at a time, and then start the rest of the nodes in the cluster using

.. include:: /rst_include/scylla-commands-start-index.rst

5. Verify that the node has been added to the cluster using
``nodetool status``

-------
Example
-------

This example shows how to install and configure a three nodes cluster, using two seed nodes, and using GossipingPropertyFileSnitch as the endpoint_snitch, each node on a different rack.

1. Installing Three Scylla nodes the IP's are:

.. code-block:: shell

   192.168.1.201 (seed)
   192.168.1.202 
   192.168.1.203 (seed)

2. In each Scylla node, edit the ``scylla.yaml`` file

**192.168.1.201**

.. code-block:: shell

   cluster_name: 'Scylla_cluster_demo'
   seeds: "192.168.1.201,192.168.1.203"
   endpoint_snitch: GossipingPropertyFileSnitch
   rpc_address: "192.168.1.201"
   listen_address: "192.168.1.201"

**192.168.1.202**

.. code-block:: shell

   cluster_name: 'Scylla_cluster_demo'
   seeds: "192.168.1.201,192.168.1.203"
   endpoint_snitch: GossipingPropertyFileSnitch
   rpc_address: "192.168.1.202"
   listen_address: "192.168.1.202"

**192.168.1.203**

.. code-block:: shell

   cluster_name: 'Scylla_cluster_demo'
   seeds: "192.168.1.201,192.168.1.203"
   endpoint_snitch: GossipingPropertyFileSnitch
   rpc_address: "192.168.1.203"
   listen_address: "192.168.1.203"

3. This step needs to be done only if using **GossipingPropertyFileSnitch**.
In each Scylla node, edit the ``cassandra-rackdc.properties`` file

**192.168.1.201**

.. code-block:: shell

   # cassandra-rackdc.properties
   #
   # The lines may include white spaces at the beginning and the end.
   # The rack and data center names may also include white spaces.
   # All trailing and leading white spaces will be trimmed.
   #
   dc=datacenter1
   rack=rack43
   # prefer_local=<false | true>
   # dc_suffix=<Data Center name suffix, used by EC2SnitchXXX snitches>

**192.168.1.202**

.. code-block:: shell

   # cassandra-rackdc.properties
   #
   # The lines may include white spaces at the beginning and the end.
   # The rack and data center names may also include white spaces.
   # All trailing and leading white spaces will be trimmed.
   #
   dc=datacenter1
   rack=rack44
   # prefer_local=<false | true>
   # dc_suffix=<Data Center name suffix, used by EC2SnitchXXX snitches>


**192.168.1.203**

.. code-block:: shell

   # cassandra-rackdc.properties
   #
   # The lines may include white spaces at the beginning and the end.
   # The rack and data center names may also include white spaces.
   # All trailing and leading white spaces will be trimmed.
   #
   dc=datacenter1
   rack=rack45
   # prefer_local=<false | true>
   # dc_suffix=<Data Center name suffix, used by EC2SnitchXXX snitches>

4. Starting Scylla nodes, since our seeds nodes are ``192.168.1.201`` and ``192.168.1.203`` we will start them first, after that we can start ``192.168.1.202`` 

.. include:: /rst_include/scylla-commands-start-index.rst

5. Verify that the node has been added to the cluster by using the ``nodetool status`` command

.. code-block:: shell

   Datacenter: datacenter1
   Status=Up/Down
   State=Normal/Leaving/Joining/Moving
   --  Address        Load       Tokens  Owns (effective)                         Host ID         Rack
   UN  192.168.1.201  112.82 KB  256     32.7%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   43
   UN  192.168.1.202  91.11 KB   256     32.9%             125ed9f4-7777-1dbn-mac8-43fddce9123e   44
   UN  192.168.1.203  124.42 KB  256     32.6%             675ed9f4-6564-6dbd-can8-43fddce952gy   45
