

===============================
Add a cluster to Scylla Manager
===============================

.. contents::
   :depth: 2
   :local:

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

2. Continue to `Add a cluster`_.

**Troubleshooting**

If you encounter troubles setting up SSH connectivity to a node use ``scyllamgr_ssh_test`` command with ``-v`` flag to show debug information.

.. code-block:: none

   scyllamgr_ssh_test --user scylla-manager --identity-file scylla-manager.pem\
   -v 198.100.51.11
   OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017
   debug1: Reading configuration data /etc/ssh/ssh_config
   debug1: /etc/ssh/ssh_config line 58: Applying options for *
   debug1: Connecting to 198.100.51.11 [198.100.51.11] port 22.
   debug1: fd 3 clearing O_NONBLOCK
   debug1: Connection established.
   debug1: identity file scylla-manager.pem type 1
   debug1: key_load_public: No such file or directory

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

Before you begin, confirm you have established SSH connectivity as explained in `Configure SSH connectivity using scyllamgr_ssh_setup`_ or `Direct communication`_.

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

See Also
========

* `sctool Reference <../sctool>`_

