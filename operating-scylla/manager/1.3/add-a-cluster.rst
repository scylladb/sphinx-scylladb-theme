=========================================
Add a cluster or a node to Scylla Manager
=========================================

.. contents::
   :depth: 2
   :local:

Scylla Manager manages clusters. A cluster contains one or more nodes / datacenters. When you add a cluster to Scylla Manager, it adds all of the nodes which are associated to it.   

Prepare a cluster
=================

Scylla Manager communicates with a Scylla cluster using REST API.
It's required that the REST API is accessible by Scylla Manager on all the cluster nodes.
By default Scylla binds REST API to localhost, which prevents from accessing if from other hosts.
To overcome this limitation Scylla Manager can work with Scylla nodes over SSH.

Communication over SSH
----------------------

This is a preferred way of Scylla Manager interacting with Scylla nodes.
We recommend adding a dedicated system user to every node in a cluster and enabling SSH connectivity using key based authentication.

Scylla Manager comes with ``scyllamgr_ssh_setup`` script that helps you with the user creation, key generation and distribution.
It requires that you have SSH access to to all the nodes with a ``sudo`` enabled user.

Configure SSH connectivity using scyllamgr_ssh_setup
....................................................

.. note:: Once you generate an SSH key pair with scyllamgr_ssh_setup the key should be safely stored. In addition, ``scyllamgr_ssh_setup`` may be invoked many times on a host without effecting already setup hosts.

**Procedure**

1. Run ``scyllamgr_ssh_setup`` to configure SSH access to the cluster.

.. code-block:: none

   scyllamgr_ssh_setup --user ec2-user --identity-file ec2-user.pem \
   --manager-user scylla-manager --manager-identity-file scylla-manager.pem \
   --discover ec2-198-100-51-11.compute-1.amazonaws.com
   198.100.51.12	OK
   198.100.51.13	OK
   198.100.51.22	OK
   198.100.51.23	OK
   198.100.51.11	OK
   198.100.51.21	OK

* ``--user`` is SSH user name used to connect to the cluster nodes
* ``--identity-file`` path is path to identity file containing SSH private key
* ``--manager-user`` is a user name that will be created and configured on cluster nodes, by default it's scylla-manager
* ``--manager-identity-file`` is a path to identity file containing SSH private key for manager user, if there is no such file it will be created
* ``--discover`` enables cluster node discovery, the command would take a single host and setup every node in the cluster

In cases where different hosts require different credentials use the ``--config-file`` option to specify host to identity file mapping using SSH configuration file.

Given an SSH configuration file named *config*:

.. code-block:: none

   Host 198.100.51.*
       User ec2-user
       IdentityFile /path/to/ec2-user.pem

   Host 10.2.*
       User centos
       IdentityFile /path/to/centos.pem

Replace ``--user`` and ``--identity-file`` flags with ``--config-file`` flag.

.. code-block:: none

   scyllamgr_ssh_setup --config-file config
   --manager-user scylla-manager --manager-identity-file scylla-manager.pem \
   --discover ec2-198-100-51-11.compute-1.amazonaws.com
   198.100.51.12	OK
   198.100.51.13	OK
   198.100.51.11	OK
   10.2.72.22		OK
   10.2.72.23		OK
   10.2.72.21		OK

The SSH configuration file parameter may always be used to specify additional SSH options.
Check ``man ssh_config`` for information on file format and available options.

2. Continue to `Add a cluster`_.

**Troubleshooting**

If you encounter troubles setting up SSH connectivity to a node use ``scyllamgr_ssh_setup`` command with ``-v`` flag to show debug information.

Direct communication
--------------------

If you have setup SSH communication with the cluster as described in the previous section please continue to `Add a cluster`_.
If you have not used the script to establish SSH, you will need to create a connection manually.
Note that exposing Scylla REST API may have a security consequences, if in doubt go to previous section.

Scylla Manager can interact with Scylla REST API on cluster nodes directly.
For that configuration of all the cluster nodes must be adjusted and the nodes must be restarted.

**Procedure**

For every node in the cluster repeat the procedure below.

1. SSH to a node.

2. Edit Scylla config file ``/etc/scylla/scylla.yaml``, set ``api_address`` to the broadcast address.

3. Drain the node (stop accepting writes and flush all tables).

.. code-block:: none

   nodetool drain

4. Restart Scylla

.. code-block:: none

   sudo systemctl restart scylla-server.service

5. Verify the Scylla server is running.

Add a cluster
=============

**Before you begin**

Confirm you have established SSH connectivity as explained in `Configure SSH connectivity using scyllamgr_ssh_setup`_ or `Direct communication`_.

**Procedure**

1. From the Scylla Manager Server, run: ``sctool cluster add``

.. code-block:: none

   sctool cluster add --host=198.100.51.11 --name=prod-cluster \
   --ssh-user=scylla-manager --ssh-identity-file=scylla-manager.pem
   db7faf98-7cc4-4a08-b707-2bc59d65551e
    __
   /  \     Cluster added, to set it as a default run:
   @  @     export SCYLLA_MANAGER_CLUSTER=db7faf98-7cc4-4a08-b707-2bc59d65551e
   |  |
   || |/    Repair will run on 01 Sep 18 00:00 UTC and will be repeated every 7 days.
   || ||    To see the currently scheduled tasks: sctool task list -c db7faf98-7cc4-4a08-b707-2bc59d65551e
   |\_/|
   \___/

* ``--host`` is hostname or IP of one of the cluster nodes
* ``--name`` is an alias you can give to your cluster
* ``--ssh-user`` is SSH user name used to connect to the cluster nodes
* ``--ssh-identity-file`` path is path to identity file containing SSH private key

If you exposed the REST API directly to establish SSH connectivity (`Direct Communication`_), the ``--ssh-user`` and ``--ssh-identity-file`` parameters should be omitted.

Each cluster has a unique ID. You will use this ID in all commands where the cluster ID is required.
Each cluster is automatically registered with a repair task which runs once a week.

2. Verify that the cluster you added has a registered repair task.

.. code-block:: none

   sctool task list -c db7faf98-7cc4-4a08-b707-2bc59d65551e
   ╭─────────────────────────────────────────────┬───────────────────────────────┬──────┬────────────┬────────╮
   │ task                                        │ next run                      │ ret. │ properties │ status │
   ├─────────────────────────────────────────────┼───────────────────────────────┼──────┼────────────┼────────┤
   │ repair/730a134a-4792-4139-bc6c-75d2ba7a1e62 │ 01 Sep 18 00:00 UTC (+7 days) │ 3    │            │ NEW    │
   ╰─────────────────────────────────────────────┴───────────────────────────────┴──────┴────────────┴────────╯

Add a Node to a Managed Cluster
===============================

Although Scylla Manager is aware of all topology changes made within every cluster it manages, it cannot properly manage nodes/datacenters without establishing SSH connections with every node/datacenter in the cluster. Keys cannot be automatically distributed so to make sure this connection is established, you need to run the scyllamgr_ssh_setup.

**Before You Begin**

* Confirm you have a managed cluster running under Scylla Manager. If you do not have a managed cluster, see `Add a cluster`_.
* Confirm the `node </operating-scylla/procedures/cluster-management/add_node_to_cluster/#procedure>`_ or `Datacenter </operating-scylla/procedures/cluster-management/add_dc_to_exist_dc/#adding-a-new-data-center-into-an-existing-scylla-cluster>`_ is added to the Scylla Cluster. 

**Procedure**

1. Run the proceddure as described in `Configure SSH connectivity using scyllamgr_ssh_setup`_ above. If you are adding a single node you can leave out the ``--discover`` flag. If you are adding multiple nodes (or a Datacenter) you may either specify them all individually or use the ``--discover`` flag. Make sure you receive a confirmation, with the IP address of the new node. For example:

   .. code-block:: none
 
      198.100.51.12	OK

2. Confirm the node / datacenter was added by checking its `status </operating-scylla/manager/1.3/sctool/#status>`_. From the node running Scylla Manager server run the ``sctool status --cluster <cluster-name>`` command, using the name of the managed cluster. 
 
   .. code-block:: none
   
      sctool status --cluster prod-cluster
      Datacenter: dc1
   
      ╭──────────┬─────┬────────────────╮
      │ CQL      │ SSL │ Host           │
      ├──────────┼─────┼────────────────┤
      │ UP (2ms) │ OFF │ 192.168.100.11 │
      │ UP (3ms) │ OFF │ 192.168.100.12 │
      │ UP (5ms) │ OFF │ 192.168.100.13 │
      │ UP (5ms) │ OFF │ 192.100.51.24  │
      ╰──────────┴─────┴────────────────╯

3. If you are using the Scylla Monitoring Stack, continue to `Prometheus Target list </operating-scylla/monitoring/monitoring_stack/#procedure>`_ for more information. 



Remove a Node/Datacenter from Scylla Manager
--------------------------------------------

There is no need to perform any action in Scylla Manager after removing a node or datacenter from a Scylla cluster. 

.. note:: If you are removing the cluster from Scylla Manager and you are using Scylla Monitoring, refer to `Prometheus Target list </operating-scylla/monitoring/monitoring_stack/#procedure>`_ for more information. 

Retreive a deleted SSH key file
-------------------------------

If you deleted the SSH key files they can be restored. 

From an existing node search the ``/var/lib/scylla-manager/.ssh/authorized_keys`` directory and look for lines under the comment ``# Added by Scylla Manager``. There you will find a copy of the public key. You can copy this key to connect to the private key held by Scylla Manager.

See Also
========

* `sctool Reference <../sctool>`_
* `Remove a node from a Scylla Cluster </operating-scylla/procedures/cluster-management/remove_node/#remove-a-node-from-a-scylla-cluster-down-scale>`_ 

