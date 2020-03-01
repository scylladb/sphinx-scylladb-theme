Adding a New Node Into an Existing Scylla Cluster (Out Scale)
*************************************************************

The add a new node operation causes the other nodes in the cluster to stream data to the new node. This operation can take some time (depending on the data size and network bandwidth). If using multi-availability-zone_ make sure they are balanced - see here for more info.

.. _multi-availability-zone: /faq/#what-is-the-best-scenario-to-add-a-node-to-a-multi-availability-zone-az

-------------
Prerequisites
-------------

Before adding the new node check the nodes status in the cluster using :doc:`nodetool status </operating-scylla/nodetool-commands/status>` command.
If one (or more), of the nodes is down, a new node can not be added to the cluster

For Example:

.. code-block:: shell

   Datacenter: DC1
   Status=Up/Down
   State=Normal/Leaving/Joining/Moving
   --  Address        Load       Tokens  Owns (effective)                         Host ID         Rack
   UN  192.168.1.201  112.82 KB  256     32.7%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   B1
   DN  192.168.1.202  91.11 KB   256     32.9%             125ed9f4-7777-1dbn-mac8-43fddce9123e   B1

In order to proceed, start the node or :doc:`remove it from the cluster </operating-scylla/procedures/cluster-management/remove_node/>`

Login to one of the nodes in the cluster, collect the following info from the node:

.. include:: /operating-scylla/procedures/cluster-management/_common/prereq.rst

---------
Procedure
---------

1. Install Scylla on a new node, see :doc:`Getting Started</getting-started/index>` for further instructions.
Follow the Scylla install procedure up to ``scylla.yaml`` configuration phase. Make sure that the Scylla version of the new node is identical to the other nodes in the cluster 

In the case that the node starts during the process follow :doc:`these instructions </operating-scylla/procedures/cluster-management/clear_data>` 

.. include:: /operating-scylla/procedures/cluster-management/_common/match_version.rst


2. In the ``scylla.yaml`` file edit the parameters listed below,
the file can be found under ``/etc/scylla/``

- **cluster_name** - Set the selected cluster_name

- **listen_address** - IP address that Scylla used to connect to the other Scylla nodes in the cluster

- **auto_bootstrap** - By default, this parameter is set to true, it allow new nodes to migrate data to themselves automatically

- **endpoint_snitch** - Set the selected snitch

- **rpc_address** - Address for client connections (Thrift, CQL)

- **seeds** - Set the selected seed nodes

.. Note:: 

   The added node should not be a seed node.

3. Start Scylla node using

.. include:: /rst_include/scylla-commands-start-index.rst

4. Verify that the node was added to the cluster using :doc:`nodetool status </operating-scylla/nodetool-commands/status>` command.
Since the other nodes in the cluster streams data to the new node, the new node will be in Up Joining (UJ) status.
It may take some time (Depending on the data size and network bandwidth) until the node status will become Up Normal (UN) status

**For Example:**

The nodes in the cluster streams data to the new node

.. code-block:: shell

   Datacenter: DC1
   Status=Up/Down
   State=Normal/Leaving/Joining/Moving
   --  Address        Load       Tokens  Owns (effective)                         Host ID         Rack
   UN  192.168.1.201  112.82 KB  256     32.7%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   B1
   UN  192.168.1.202  91.11 KB   256     32.9%             125ed9f4-7777-1dbn-mac8-43fddce9123e   B1
   UJ  192.168.1.203  124.42 KB  256     32.6%             675ed9f4-6564-6dbd-can8-43fddce952gy   B1

The nodes in the cluster finish streaming data to the new node

.. code-block:: shell

   Datacenter: DC1
   Status=Up/Down
   State=Normal/Leaving/Joining/Moving
   --  Address        Load       Tokens  Owns (effective)                         Host ID         Rack
   UN  192.168.1.201  112.82 KB  256     32.7%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   B1
   UN  192.168.1.202  91.11 KB   256     32.9%             125ed9f4-7777-1dbn-mac8-43fddce9123e   B1
   UN  192.168.1.203  124.42 KB  256     32.6%             675ed9f4-6564-6dbd-can8-43fddce952gy   B1

5. When the new node status is Up Normal (UN), use :doc:`nodetool cleanup </operating-scylla/nodetool-commands/cleanup>` cleanup command on all the nodes in the cluster except the new node that has just been added.
It will remove keys that are no longer belong to the node. Run this command one node at a time.
It is possible to postpone this step to low demand hours.

.. note::

   If using Scylls Enterprise 2018.1.5, Scylla Open Source 2.2.0, 2.3.0 or lower version **Do not** run the ``nodetool cleanup`` command before upgrading to the latest release of your branch, see this issue_ for further information.

.. _issue: https://github.com/scylladb/scylla/issues/3872

6. If you are using Scylla Monitoring, update the `monitoring stack </operating-scylla/monitoring/monitoring_stack/#procedure>`_ to monitor it. If you are using Scylla Manager, make sure :manager_lst:`Manager <add-a-cluster/#add-a-node-to-a-managed-cluster>` can connect to the new node.
