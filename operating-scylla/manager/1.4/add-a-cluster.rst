=========================================
Add a cluster or a node to Scylla Manager
=========================================

.. contents::
   :depth: 2
   :local:

Scylla Manager manages clusters. A cluster contains one or more nodes / datacenters. When you add a cluster to Scylla Manager, it adds all of the nodes which are associated with it.   


Port Settings
=============

For all Scylla Nodes, confirm that port :9042 and port :22 are open. Port 9042 is vital for Healthcheck and port 22 is necessary for Repair. 

Enable SSH Communication
========================

Scylla Manager communicates with a Scylla cluster using REST API.
It's required that the REST API is accessible by Scylla Manager on all of the cluster nodes.
By default Scylla binds REST API to the localhost, preventing other hosts from having access to it.
Scylla Manager communicates with Scylla nodes over SSH, ensuring a secure connection for Scylla Management.

Prerequisites
-------------

Verify that you have SSH access to **all** nodes in the cluster as well as Scylla Manager Server.
Verify that the user attached to the SSH key is a ``sudo`` enabled user.
Make sure that you know the path to the private key (which is saved on the Scylla Manager Server).

If you cannot establish an SSH connection, you will need to make sure that:

* You have created an SSH key pair
* The Private Key is on Scylla Manager
* The Public Key is on each Scylla Node

.. _scyllamgr_ssh_setup:

Configure Scylla Manager connectivity using scyllamgr_ssh_setup
---------------------------------------------------------------

Scylla Manager comes with ``scyllamgr_ssh_setup`` script that helps you with the user creation, key generation and distribution.

There are three stages to the script:

* Stage 1 - The SSH connection to the nodes from Scylla Manager is tested using the key which you used to test connectivity (`Prerequisites`_). 
* Stage 2 - A new SSH key is made, the private key is stored on Scylla Manager Server and the Public Key is distributed to each Scylla node in the cluster. A new user (``scylla-manager`` by default), is created and listed in the SSH key. 
* Stage 3 - Using the new SSH key, connectivity is tested again and connectivity to the Scylla REST API is tested as well. Upon completion, a confirmation message is displayed. 

.. note:: ``scyllamgr_ssh_setup`` may be invoked many times without affecting Scylla Manager or the nodes. If you generate a new key the old key is overwritten.

**Procedure**

1. From Scylla Manager server, run ``scyllamgr_ssh_setup`` to configure SSH access to the cluster.

.. code-block:: none

     scyllamgr_ssh_setup [--ssh-user <username>] [--ssh-identity-file <path to private key/filename>] [--ssh-config-file <path to SSH config file>] [--create-user <username>] [--single-node] [--debug] SCYLLA_NODE_IP 

Where:

* ``-u <username>`` ``--ssh-user <username>``  is the SSH username listed in the public key located on the Scylla nodes. This user must be a sudo enabled user.
* ``-i <file>`` ``--ssh-identity-file <file>`` is the path to the Private key located on Scylla Manager server.
* ``--create-user <username>`` is the **new** username which will be listed in the new public key when it is placed on the Scylla nodes, default user is ``scylla-manager``
* ``-c <file>`` ``--ssh-config-file <file>`` is the path to an alternate configuration file. See `Configure connectivity with a configuration file`_ for an example.
* ``--single-node`` is used to setup only the given node, skipping discovery of any other cluster nodes
* ``--debug`` is used to display debug information

2. Confirm a ``Done!`` message displays. Make sure that the new keys which scyllamgr_ssh_setup creates are safely stored. 
3. Proceed to `Add a cluster`_.

**Example**

In this example, the SSH Private Key is located on Scylla Manager Server in /home/centos/.ssh directory and is named key.pem. The username in the SSH Private Key is centos. When the script runs to connect to Scylla Node 192.0.2.14 (a seed node, but not required), a new SSH key is created with the default user (as --create-user is not used) attached to the key.

.. code-block:: none

   scyllamgr_ssh_setup --ssh-user centos --ssh-identity-file /home/centos/.ssh/key.pem 192.0.2.14

   > Discovering all the cluster nodes
   > Creating user 'scylla-manager'
   192.0.2.14   OK
   192.0.2.15  	OK
   192.0.2.16  	OK
   > Testing Scylla API connectivity
   192.0.2.14  	OK
   192.0.2.15  	OK
   192.0.2.16	OK

   > Done!
   > To add the cluster to Scylla Manager run: sctool cluster add --host 192.0.2.14 --ssh-user 'scylla-manager' --ssh-identity-file '/home/centos/.ssh/scylla-manager.pem'

Configure connectivity with a configuration file
------------------------------------------------

In cases where different clusters require different credentials use the ``--config-file`` option to specify host to identity file mapping using SSH configuration file.

For example, there are two datacenters. Each datacenter is running with its own identity configuration (different SSH keys and users). In order for the scyllamgr_ssh_setup  script to connect to each datacenter, you can use a configuration file which will map the credentials to the correct machines. This configuration file can be placed in any location, but by default it is read from ~/.ssh/config.

.. note:: If the configuration file is saved in ~/.ssh/config it will be used by every SSH command. If you want to use this configuration only for Scylla, consider saving the file in another location. 

**Example**

1. Given an SSH configuration file named *config*, saved in ~/.ssh/scylla_config:

.. code-block:: none

   Host 198.100.51.*
       User ec2-user
       IdentityFile /path/to/ec2-user.pem

   Host 10.2.*
       User centos
       IdentityFile /path/to/centos.pem

2. Replace ``--user`` and ``--identity-file`` flags with ``--config-file`` flag.

.. code-block:: none
 
   scyllamgr_ssh_setup --ssh-config-file ~/.ssh/scylla_config config 192.0.2.14

   > Discovering all the cluster nodes
   > Creating user 'scylla-manager'
   192.0.2.14   OK
   192.0.2.15  	OK
   192.0.2.16  	OK
   > Testing Scylla API connectivity
   192.0.2.14  	OK
   192.0.2.15  	OK
   192.0.2.16	OK
   > Done!
   > To add the cluster to Scylla Manager run: sctool cluster add --host 192.0.2.14 --ssh-user 'scylla-manager' --ssh-identity-file '/home/centos/.ssh/scylla-manager.pem'

The SSH configuration file parameter may always be used to specify additional SSH options.
Check ``man ssh_config`` for information on file format and available options.

2. Continue to `Add a cluster`_.

Troubleshooting
===============

If you encounter trouble setting up SSH connectivity to a node use the ``scyllamgr_ssh_setup`` command with ``--debug`` flag to show debug information.

Direct communication
====================

If you have setup SSH communication with the cluster as described in the previous section please continue to `Add a cluster`_.
If you have not used the procedure in `Enable SSH Communication`_ to establish SSH, you will need to create a connection manually.

.. caution:: exposing Scylla REST API may have a security consequences. This procedure is not recommended.

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


Add a Cluster
=============

**Before you begin**

Confirm you have established SSH connectivity as explained in `scyllamgr_ssh_setup`_ or `Direct communication`_.

**Procedure**

1. From the Scylla Manager Server, you can copy and paste the confirmation message you received when you connected your cluster with `scyllamgr_ssh_setup`_ , which instructs you to run: ``sctool cluster add``. 

.. code-block:: none

   sctool cluster add --host 192.0.2.14 --ssh-user 'scylla-manager' --ssh-identity-file '/home/centos/.ssh/scylla-manager.pem' --name manager-testcluster
   085bdfe2-91c7-4f6c-aeb0-cfea107ff9f0
    __
   /  \     Cluster added, to set it as a default run:
   @  @     export SCYLLA_MANAGER_CLUSTER=085bdfe2-91c7-4f6c-aeb0-cfea107ff9f0
   |  |
   || |/    Repair will run on 03 Apr 19 00:00:00 UTC and will be repeated every 7d.
   || ||    To see the currently scheduled tasks: sctool task list -c 085bdfe2-91c7-4f6c-aeb0-cfea107ff9f0
   |\_/|
   \___/


.. _name:

Where:

* ``--host`` is hostname or IP of one of the cluster nodes
* ``--name`` is an alias you can give to your cluster. Using an alias means you do not need to use the ID of the cluster in all other operations.  
* ``--ssh-user`` is SSH user name used in the ``--create-user <username>`` field when you ran the `scyllamgr_ssh_setup`_
* ``--ssh-identity-file`` path is path to identity file containing SSH private key

If you exposed the REST API directly to establish SSH connectivity (`Direct Communication`_), the ``--ssh-user`` and ``--ssh-identity-file`` parameters should be omitted.

Each cluster has a unique ID. You will use this ID in all commands where the cluster ID is required.
Each cluster is automatically registered with a repair task which runs once a week.

2. Verify that the cluster you added has a registered repair task by running the ``sctool task list`` command, adding the name_ of the cluster (using the parameter ``-c manager-testcluster``) you created in step 1.

.. code-block:: none

   sctool task list -c manager-testcluster
   Cluster: manager-testcluster
   ╭──────────────────────────────────────────────────────┬───────────────────────────────┬──────┬───────────┬────────╮
   │ task                                                 │ next run                      │ ret. │ arguments │ status │
   ├──────────────────────────────────────────────────────┼───────────────────────────────┼──────┼───────────┼────────┤
   │ healthcheck/018da854-b9ff-4e0a-bae7-ca65c677c559     │ 02 Apr 19 18:06:31 UTC (+15s) │ 0    │           │ NEW    │
   │ healthcheck_api/597f237f-103d-4994-8167-3ff591150b7e │ 02 Apr 19 18:07:01 UTC (+1h)  │ 0    │           │ NEW    │
   │ repair/21006f88-0c8c-4e11-9e84-83c319f80d0c          │ 03 Apr 19 00:00:00 UTC (+7d)  │ 3/3  │           │ NEW    │
   ╰──────────────────────────────────────────────────────┴───────────────────────────────┴──────┴───────────┴────────╯

You will see 3 tasks which are created by adding the cluster:

* Healthcheck - which checks the Scylla CQL, starting immediately, repeating every 15 seconds. See `Scylla Health Check <../overview/#scylla-health-check>`_
* Healthcheck API - which checks the Scylla REST API, starting immediately, repeating every hour. See `Scylla Health Check <../overview/#scylla-health-check>`_
* Repair - an automated repair task, starting at midnight tonight, repeating every seven days at midnight. See `Run a Repair <../repair-a-cluster/>`_

.. note:: If you want to change the schedule for the repair, see `Reschedule a repair <../repair-a-cluster/#reschedule-a-repair>`_.

.. _monitoring:

Connect Managed Cluster to Scylla Monitoring
============================================

Connecting your cluster to Scylla Monitoring allows you to see metrics about your cluster and Scylla Manager all within Scylla Monitoring. 

To connect your cluster to Scylla Monitoring it is **required** to use the same cluster name_ as you used when you created the cluster. See `Add a Cluster`_.

**Procedure**

Follow the procedure :monitor_lst:`Scylla Monitoring <monitoring_stack/#procedure>` as directed, remembering to update the Scylla Node IPs and  Cluster name_  as well as the Scylla Manager IP in the relevant Prometheus configuration files. 
  
If you have any issues connecting to Scylla Monitoring Stack consult the `Troubleshooting Guide </troubleshooting/manager_monitoring_integration/>`_.

Add a Node to a Managed Cluster
===============================

Although Scylla Manager is aware of all topology changes made within every cluster it manages, it cannot properly manage nodes/datacenters without establishing SSH connections with every node/datacenter in the cluster. Keys cannot be automatically distributed so to make sure this connection is established, you need to run the scyllamgr_ssh_setup.

**Before You Begin**

* Confirm you have a managed cluster running under Scylla Manager. If you do not have a managed cluster, see `Add a cluster`_.
* Confirm the `node </operating-scylla/procedures/cluster-management/add_node_to_cluster/#procedure>`_ or `Datacenter </operating-scylla/procedures/cluster-management/add_dc_to_exist_dc/#procedure>`_ is added to the Scylla Cluster. 

**Procedure**

1. Run the procedure as described in `Configure Scylla Manager connectivity using scyllamgr_ssh_setup`_ above. If you are adding a single node you can leave out the ``--discover`` flag. If you are adding multiple nodes (or a Datacenter) you may either specify them all individually or use the ``--discover`` flag. Make sure you receive a confirmation, with the IP address of the new node. For example:

   .. code-block:: none
 
      198.100.51.12	OK

2. Confirm the node / datacenter was added by checking its `status <../sctool>`_. From the node running Scylla Manager server run the ``sctool status --cluster <cluster-name>`` command, using the name of the managed cluster. 
 
   .. code-block:: none
   
      sctool status -c manager-testcluster
      Datacenter: us-east
      ╭──────────┬──────────┬─────┬──────────────╮
      │ CQL      │ API      │ SSL │ Host         │
      ├──────────┼──────────┼─────┼──────────────┤
      │ UP (0ms) │ UP (0ms) │ OFF │ 198.0.2.14   │
      │ UP (0ms) │ UP (0ms) │ OFF │ 198.0.2.15   │
      │ UP (0ms) │ UP (0ms) │ OFF │ 198.0.2.16   │ 
      │ UP (0ms) │ UP (0ms) │ OFF │ 198.0.2.18   │
      ╰──────────┴──────────┴─────┴──────────────╯


3. If you are using the Scylla Monitoring Stack, continue to :ref:`monitoring` for more information. 



Remove a Node/Datacenter from Scylla Manager
--------------------------------------------

There is no need to perform any action in Scylla Manager after removing a node or datacenter from a Scylla cluster. 

.. note:: If you are removing the cluster from Scylla Manager and you are using Scylla Monitoring, refer to :monitor_lst:`Prometheus Target List </monitoring_stack/#procedure>` for more information. 

Retrieve a deleted SSH key file
-------------------------------

If you deleted the SSH key files they can be restored. 

From an existing node search the ``/var/lib/scylla-manager/.ssh/authorized_keys`` directory and look for lines under the comment ``# Added by Scylla Manager``. There you will find a copy of the public key. You can copy this key to connect to the private key held by Scylla Manager.

See Also
========

* `sctool Reference <../sctool>`_
* `Remove a node from a Scylla Cluster </operating-scylla/procedures/cluster-management/remove_node>`_ 
* `Scylla Monitoring <operating-scylla/monitoring/>`_

