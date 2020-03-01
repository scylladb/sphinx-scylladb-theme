=========================================
Add a cluster or a node to Scylla Manager
=========================================

.. contents::
   :depth: 2
   :local:

Scylla Manager manages clusters. A cluster contains one or more nodes / datacenters. When you add a cluster to Scylla Manager, it adds all of the nodes which are:

* associated with it, 
* that are running Scylla Manager Agent, 
* and are accessible   


Port Settings
=============

Confirm all ports required for Scylla Manager and Scylla Manager Agent are open. This includes:

* 9042 CQL
* 9142 SSL CQL
* 10001 Scylla Agent REST API


Add a Cluster
=============

This procedure adds the nodes to Scylla Manager so the cluster can be a managed cluster under Scylla Manager.

Prerequisites
-------------

For each node in the cluster, the **same** `authentication token <../install-agent/#generate-an-authentication-token>`_ needs to be identified in ``/etc/scylla-manager-agent/scylla-manager-agent.yaml``

Create a Managed Cluster
------------------------

.. _name:

**Procedure**

#. From the Scylla Manager Server, provide the broadcast_address of one of the nodes and the generated auth_token (if used) and a custom name if desired.

   Where:

   * ``--host`` is hostname or IP of one of the cluster nodes. You can use an IPv6 or an IPv4 address.
   * ``--name`` is an alias you can give to your cluster. Using an alias means you do not need to use the ID of the cluster in all other operations.  
   * ``--auth-token`` is the authentication `token <../install-agent/#generate-an-authentication-token>`_ you identified in ``/etc/scylla-manager-agent/scylla-manager-agent.yaml``
   * ``--without-repair`` - when cluster is added, Manager schedules repair to repeat every 7 days. To create a cluster without a scheduled repair, use this flag.

   Example (IPv4):

   .. code-block:: none

      sctool cluster add --host 34.203.122.52 --auth-token "6Es3dm24U72NzAu9ANWmU3C4ALyVZhwwPZZPWtK10eYGHJ24wMoh9SQxRZEluWMc0qDrsWCCshvfhk9uewOimQS2x5yNTYUEoIkO1VpSmTFu5fsFyoDgEkmNrCJpXtfM"  --name manager-testcluster 

      c1bbabf3-cad1-4a59-ab8f-84e2a73b623f
       __  
      /  \     Cluster added! You can set it as default, by exporting env variable.
      @  @     $ export SCYLLA_MANAGER_CLUSTER=c1bbabf3-cad1-4a59-ab8f-84e2a73b623f
      |  |     $ export SCYLLA_MANAGER_CLUSTER=manager-testcluster
      || |/    
      || ||    Now run:
      |\_/|    $ sctool status -c manager-testcluster
      \___/    $ sctool task list -c manager-testcluster


   Example (IPv6):

   .. code-block:: none

         sctool cluster add --host 2a05:d018:223:f00:971d:14af:6418:fe2d --auth-token       "6Es3dm24U72NzAu9ANWmU3C4ALyVZhwwPZZPWtK10eYGHJ24wMoh9SQxRZEluWMc0qDrsWCCshvfhk9uewOimQS2x5yNTYUEoIkO1VpSmTFu5fsFyoDgEkmNrCJpXtfM"  --name manager-testcluster

   Each cluster has a unique ID. You will use this ID in all commands where the cluster ID is required.
   Each cluster is automatically registered with a repair task which runs once a week. This can be canceled using ``--without-repair``. To use a different repair schedule, see `Schedule a Repair <../repair-a-cluster/#schedule-a-repair>`_. 

#. Verify that the cluster you added has a registered repair task by running the ``sctool task list -c <cluster-name>`` command, adding the name_  of the cluster you created in step 1 (with the ``--name`` flag).

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

   * Healthcheck - which checks the Scylla CQL, starting immediately, repeating every 15 seconds. See `Scylla Health Check <../health-check>`_
   * Healthcheck API - which checks the Scylla REST API, starting immediately, repeating every hour. See `Scylla Health Check <../health-check>`_
   * Repair - an automated repair task, starting at midnight tonight, repeating every seven days at midnight. See `Run a Repair <../repair-a-cluster/>`_

   .. note:: If you want to change the schedule for the repair, see `Reschedule a repair <../repair-a-cluster/#reschedule-a-repair>`_.

.. _monitorings:

Connect Managed Cluster to Scylla Monitoring
============================================

Connecting your cluster to Scylla Monitoring allows you to see metrics about your cluster and Scylla Manager all within Scylla Monitoring. 

To connect your cluster to Scylla Monitoring it is **required** to use the same cluster name_ as you used when you created the cluster. See `Add a Cluster`_.

**Procedure**

Follow the procedure :monitor_lst:`Scylla Monitoring <monitoring_stack/#procedure>` as directed, remembering to update the Scylla Node IPs and  Cluster name_  as well as the Scylla Manager IP in the relevant Prometheus configuration files. 

If you have any issues connecting to Scylla Monitoring Stack consult the `Troubleshooting Guide </troubleshooting/manager_monitoring_integration/>`_.

Add a Node to a Managed Cluster
===============================

Although Scylla Manager is aware of all topology changes made within every cluster it manages, it cannot properly manage nodes/datacenters without establishing connections with every node/datacenter in the cluster including the Scylla Manager Agent which is on each managed node. 

**Before You Begin**

* Confirm you have a managed cluster running under Scylla Manager. If you do not have a managed cluster, see `Add a cluster`_.
* Confirm the `node </operating-scylla/procedures/cluster-management/add_node_to_cluster/#procedure>`_ or `Datacenter </operating-scylla/procedures/cluster-management/add_dc_to_exist_dc/#procedure>`_ is added to the Scylla Cluster. 

**Procedure**

#. `Add Scylla Manager Agent <../install-agent>`_ to the new node. Use the **same** authentication token as you did for the other nodes in this cluster. Do not generate a new token. 

#. Confirm the node / datacenter was added by checking its `status <../sctool/#status>`_. From the node running Scylla Manager server run the ``sctool status --cluster <cluster-name>`` command, using the name of the managed cluster. 
 
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


#. If you are using the Scylla Monitoring Stack, continue to `monitoring <../add-a-cluster/#monitorings>`_ for more information. 



Remove a Node/Datacenter from Scylla Manager
--------------------------------------------

There is no need to perform any action in Scylla Manager after removing a node or datacenter from a Scylla cluster. 

.. note:: If you are removing the cluster from Scylla Manager and you are using Scylla Monitoring, refer to :monitor_lst:`Prometheus Target List </monitoring_stack/#procedure>` for more information. 

See Also
========

* `sctool Reference <../sctool>`_
* `Remove a node from a Scylla Cluster </operating-scylla/procedures/cluster-management/remove_node>`_ 
* `Scylla Monitoring </operating-scylla/monitoring>`_

