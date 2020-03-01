Adding a New Data Center Into an Existing Scylla Cluster
********************************************************

.. contents::
   :depth: 2
   :local:

The following procedure specifies how to add a Data Center (DC) to a live Scylla Cluster, in a single data center, `multi-availability zone`_, or multi-data center. Adding a DC out-scales the cluster and provides higher availability (HA).

The procedure includes:

* Install nodes on the new DC.
* Add the new nodes to the cluster.
* Update the replication strategy of selected keyspace to use the new DC.
* Rebuild new nodes
* Run full cluster repair
* Update the Moniotring stack  

..  _`multi-availability zone`: /faq/#what-is-the-best-scenario-to-add-a-node-to-a-multi-availability-zone-az

.. note::

   Make sure to complete the full procedure **before** starting to read from the new Data Center

.. warning::

   The node/nodes you add **must** be clean (no data), otherwise you risk data loss. See `Clean Data from Nodes`_ below.

Prerequisites
-------------

1. Login to one of the nodes in the cluster, collect the following info from the node:

.. include:: /operating-scylla/procedures/cluster-management/_common/prereq.rst

2. Install the new **clean** Scylla nodes (See `Clean Data from Nodes`_ below) on the new data-center, see :doc:`Getting Started</getting-started/index>` for further instructions, create as many nodes that you need.
Follow the Scylla install procedure up to ``scylla.yaml`` configuration phase.
In the case that the node starts during the installation process follow :doc:`these instructions </operating-scylla/procedures/cluster-management/clear_data>`.

3. Select a couple of nodes in the **new data-center** to be seed nodes.

Clean Data from Nodes
---------------------

.. include:: /rst_include/clean-data-code.rst


Add New DC
----------

**Procedure**

1. In the **existing data-center(s)** alter each Keyspace replication to use ``class : NetworkTopologyStrategy`` and set the new DC replication factor to zero. This will prevent writing to the new DC until explicitly enabled.

Alter the following:

* Keyspace created by the user.
* System: ``system_auth``, ``system_distributed``, ``system_traces``.

For example:

Before

.. code-block:: cql

   DESCRIBE KEYSPACE mykeyspace; 
   CREATE KEYSPACE mykespace WITH replication = { 'class' : 'SimpleStrategy', 'replication_factor': '3'};

ALTER Command

.. code-block:: cql
   
   ALTER KEYSPACE mykespace WITH replication = { 'class' : 'NetworkTopologyStrategy', '<exiting_dc>' : 3, '<new_dc>' : 0};

After

.. code-block:: cql

   DESCRIBE KEYSPACE mykeyspace;
   CREATE KEYSPACE mykespace WITH replication = { 'class' : 'NetworkTopologyStrategy', '<exiting_dc>' : 3, <new_dc> : 0};

2. For each node in the **existing data-center(s)** edit the ``scylla.yaml`` file to use either

* ``Ec2MultiRegionSnitch`` - for AWS cloud-based, multi-data-center deployments.

* ``GossipingPropertyFileSnitch`` - for bare metal and cloud (other than AWS) deployments. 

3. Set the DC and Rack Names.
In the ``cassandra-rackdc.properties`` file edit the parameters listed below.
The file can be found under ``/etc/scylla/``.

``Ec2MultiRegionSnitch`` 

Ec2MultiRegionSnitch give each DC and rack default names, the region name defined as datacenter name and `availability zones`_ are defined as racks within a datacenter. 

.. _`availability zones`: /faq/#what-is-the-best-scenario-to-add-a-node-to-a-multi-availability-zone-az

For example:

A node in the ``us-east-1`` region, 
us-east is the data center name and 1 is the rack location. 

To change the DC names do the following:

Edit the ``cassandra-rackdc.properties`` file with the prefered data-center name.
The file can be found under ``/etc/scylla/``

The dc_suffix defines a suffix added to the data-center name as described below.

For example:

Region us-east

``dc_suffix=_1_scylla`` will be ``us-east_1_scylla``

Or

Region us-west

``dc_suffix=_1_scylla`` will be ``us-west_1_scylla``

``GossipingPropertyFileSnitch``

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

4. In the **existing data-center(s)** retart Scylla nodes one by one.

.. include:: /rst_include/scylla-commands-restart-index.rst

5. For each node in the **new data-center** edit the ``scylla.yaml`` file parameters listed below,
the file can be found under ``/etc/scylla/``.

- **cluster_name** - Set the selected cluster_name.

- **listen_address** - IP address that Scylla used to connect to the other Scylla nodes in the cluster.

- **auto_bootstrap** - By default, this parameter is set to true, it allow new nodes to migrate data to themselves automatically.

- **endpoint_snitch** - Set the selected snitch.

- **rpc_address** - Address for client connections (Thrift, CQL).

* The parameters ``seeds``, ``cluster_name`` and ``endpoint_snitch`` need to match the existing cluster.

6. In the **new data-center**, set the DC and Rack Names (see step number **three** for more details).

7. In the **new data-center**, start Scylla nodes one by one using.

.. include:: /rst_include/scylla-commands-start-index.rst

8. Verify that the nodes were added to the cluster using ``nodetool status``.

For example:

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
   
9. When all nodes are up and running ``ALTER`` the following Keyspaces in the new nodes:

* Keyspace created by the user (which needed to replicate to the new DC).
* System: ``system_auth``, ``system_distributed``, ``system_traces`` For example, replicate the data to three nodes in the new DC.

For example:

Before

.. code-block:: cql

   DESCRIBE KEYSPACE mykeyspace; 

   CREATE KEYSPACE mykespace WITH replication = { 'class' : 'NetworkTopologyStrategy', '<exiting_dc>' : 3};

ALTER Command

.. code-block:: cql

   ALTER KEYSPACE mykespace WITH replication = { 'class' : 'NetworkTopologyStrategy', '<exiting_dc>' : 3, <new_dc> : 3};
   ALTER KEYSPACE system_auth WITH replication = { 'class' : 'NetworkTopologyStrategy', '<exiting_dc>' : 3, <new_dc> : 3};
   ALTER KEYSPACE system_distributed WITH replication = { 'class' : 'NetworkTopologyStrategy', '<exiting_dc>' : 3, <new_dc> : 3};
   ALTER KEYSPACE system_traces WITH replication = { 'class' : 'NetworkTopologyStrategy', '<exiting_dc>' : 3, <new_dc> : 3};

After

.. code-block:: cql

   DESCRIBE KEYSPACE mykeyspace; 
   CREATE KEYSPACE mykespace WITH REPLICATION = {'class’: 'NetworkTopologyStrategy', <exiting_dc>:3, <new_dc>: 3};
   CREATE KEYSPACE system_auth WITH replication = { 'class' : 'NetworkTopologyStrategy', '<exiting_dc>' : 3, <new_dc> : 3};
   CREATE KEYSPACE system_distributed WITH replication = { 'class' : 'NetworkTopologyStrategy', '<exiting_dc>' : 3, <new_dc> : 3};
   CREATE KEYSPACE system_traces WITH replication = { 'class' : 'NetworkTopologyStrategy', '<exiting_dc>' : 3, <new_dc> : 3};

10. Run ``nodetool rebuild`` on each node in the new data-center, specify the existing data-center name in the rebuild command.

For example:

``nodetool rebuild -- <existing_data_center_name>``

The rebuild ensures that the new nodes that were just added to the cluster will recognize the existing data-centers in the cluster.

11. Run a full cluster repair, using `nodetool repair -pr </operating-scylla/nodetool-commands/repair>`_ on each node, or using :manager_lst:`Scylla Manager ad-hoc repair<repair-a-cluster>`

12. Update ``scylla.yaml`` file in the **existing data-center(s)** and the **new data-center** with the newly promoted seed nodes.

Retart Scylla node one by one using.

.. include:: /rst_include/scylla-commands-restart-index.rst

13. If you are using Scylla Monitoring, update the `monitoring stack </operating-scylla/monitoring/monitoring_stack/#procedure>`_ to monitor it. If you are using Scylla Manager, make sure :manager_lst:`Manager <add-a-cluster/#add-a-node-or-datacenter-to-a-managed-cluster>` can connect to the new datacenter.
