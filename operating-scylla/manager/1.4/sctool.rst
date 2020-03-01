================
sctool Reference
================

.. contents::
   :depth: 2
   :local:

About sctool
============

``sctool`` is a Command Line Interface (CLI) for the Scylla Manager server. The server communicates with multiple Scylla clusters and performs cluster-wide operations such as automatic repair.

**Usage**

.. code-block:: none

   sctool command [flags] [global flags]


Global flags
------------

* ``--api-url URL`` - URL of Scylla Manager server (default "http://localhost:8889/api/v1")
* ``-h``, ``--help`` - Help for commands. Use **sctool [command] --help** for help about a specific command.

Environment variables
---------------------

Sctool uses the following environment variables:

* `SCYLLA_MANAGER_CLUSTER` - if set specifies default value for ``-c, --cluster`` flag in commands that support it
* `SCYLLA_MANAGER_API_URL` - if set specifies default value for ``--api-url`` flag, it can be useful when using sctool with a remote Scylla Manager server

The environment variables may be saved in  your ``~/.bashrc`` file so that the variables are set after login.

Show version
------------

This command shows the currently installed sctool version and the Scylla Manager server version.

**Syntax:**

.. code-block:: none

   sctool version [flags] [global flags]

version parameters
..................

version takes the `Global flags`_.

Example: version 
................

.. code-block:: none

   sctool version
   Client version: 1.4-0.20190417.95c4bffd
   Server version: 1.4-0.20190417.95c4bffd

Managing clusters
=================

The cluster commands allow you to add, delete, list, and update clusters. A Scylla cluster must be added before management tasks can be initiated.

.. code-block:: none

   sctool cluster <command> [flags] [global flags]

**Subcommands**

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Subcommand
     - Usage
   * - `cluster add`_
     - Add a cluster to manager.
   * - `cluster delete`_
     - Delete a cluster from manager.
   * - `cluster list`_
     - Show managed clusters.
   * - `cluster update`_
     - Modify a cluster.

cluster add
-----------

This command adds the specified cluster to the manager.
Once a Scylla cluster is added, a weekly repair task is also added.

Before continuing make sure the cluster that you want to add is prepared for it,
see `Add a cluster to Scylla Manager <../add-a-cluster>`_ for instructions.

**Syntax:**

.. code-block:: none

   sctool cluster add --host <node IP> [--name <alias>]
   [--ssh-identity-file <path to private key> --ssh-user <username>] [global flags]

cluster add parameters
......................

In addition to the `Global flags`_, cluster add takes the following parameters:

=====

.. include:: _common/cluster-params.rst

=====

Example: cluster add 
....................

This example is only the command that you use to add the cluster to Scylla Manager, not the entire procedure for adding a cluster. The procedure is detailed in `Add a cluster to Scylla Manager <../add-a-cluster>`_.

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

cluster delete
--------------

This command deletes the specified cluster from the manager.
Note that there is no confirmation or warning to confirm.
If you deleted the cluster by mistake, you will need to add it again.

**Syntax:**

.. code-block:: none

   sctool cluster delete --cluster <id|name> [global flags]

.. note:: If you are removing the cluster from Scylla Manager and you are using Scylla Monitoring, remove the target from Prometheus Target list </operating-scylla/monitoring/monitoring_stack/#procedure>`_ in the prometheus/scylla_manager_servers.yml file.


cluster delete parameters
.........................

In addition to `Global flags`_, cluster delete takes the following parameter:

=====

.. include:: _common/param-cluster.rst

=====

Example: cluster delete
.......................

.. code-block:: none

   sctool cluster delete -c manager-testcluster

cluster list
------------

Lists the managed clusters.

**Syntax:**

.. code-block:: none

   sctool cluster list [global flags]

cluster list parameters
.......................

cluster list takes the `Global flags`_.

Example: cluster list
.....................

.. code-block:: none

   sctool cluster list
   ╭──────────────────────────────────────┬─────────────────────┬────────────────╮
   │ cluster id                           │ name                │ ssh user       │
   ├──────────────────────────────────────┼─────────────────────┼────────────────┤
   │ db7faf98-7cc4-4a08-b707-2bc59d65551e │ manager-testcluster │ scylla-manager │
   ╰──────────────────────────────────────┴─────────────────────┴────────────────╯

cluster update
--------------

This command modifies managed cluster parameters.

**Syntax:** 

.. code-block:: none

   sctool cluster update --cluster <id|name> [--host <node IP>] [--name <alias>]
   [--ssh-identity-file <path to private key> --ssh-user <username>] [global flags]


cluster update parameters
.........................

In addition to the `Global flags`_, cluster update takes all the `cluster add parameters`_.

=====

.. include:: _common/param-cluster.rst

=====

.. include:: _common/cluster-params.rst

=====

Example: cluster update 
.......................

In this example, the cluster named cluster has been renamed to prod-cluster and the SSH username was changed to scylla.

.. code-block:: none

   sctool cluster update --cluster cluster --name prod-cluster --ssh-user scylla

Scheduling repairs
==================

repair
------

The repair commands allow you to schedule repairs for a specified cluster.

.. code-block:: none

   sctool repair --cluster <id|name> [--dc <list of glob patterns>] [--dry-run]
   [--fail-fast] [--force] [--host <node IP>] [--interval <time between task runs>]
   [--keyspace <list of glob patterns>] [--num-retries <times to rerun a failed task>]
   [--start-date <now+duration|RFC3339>]
   [--token-ranges <pr|npr|all>] [--with-hosts <list of node IPs>][global flags]

repair parameters
.................

In addition to `Global flags`_, repair takes the following parameters:

=====

.. include:: _common/param-cluster.rst

=====

``--dc <list of glob patterns>``

List of data centers to be repaired, separated by a comma. This can also include glob patterns.

.. include:: _common/glob.rst

**Example**

Given the following data centers: *us-east-1*, *us-east-2*, *us-west-1*, *us-west-2*.

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Parameter
     - Selects
   * - ``--dc us-east-1,us-west-2``
     - *us-east-1*, *us-west-2*
   * - ``--dc 'us-east-*'``
     - *us-east-1*, *us-east-2*
   * - ``--dc '*','!us-east-'``
     - *us-west-1*, *us-west-2*

**Default:** everything - all data centers

=====

``--dry-run``

Validates and displays repair information without actually scheduling the repair. This allows you to display what will happen should the repair run with the parameters you set.

**Example**

Given the following keyspaces: 

* system_auth 
* system_distributed
* system_traces
* test_keyspace_dc1_rf2, test_keyspace_dc1_rf3, and test_keyspace_dc2_rf2
* keyspace_dc2_rf3
* test_keyspace_rf2 and test_keyspace_rf3

The following command will run a repair on all keyspaces **except** for test_keyspace_dc1_rf2 in dry-run mode.


.. code-block:: none

   sctool repair --dry-run -K '*,!test_keyspace_dc1_rf2'

   NOTICE: dry run mode, repair is not scheduled

   Data Centers:
     - dc1
     - dc2
   Keyspace: system_auth
     (all tables)
   Keyspace: system_distributed
     (all tables)
   Keyspace: system_traces
     (all tables)
   Keyspace: test_keyspace_dc1_rf3
     (all tables)
   Keyspace: test_keyspace_dc2_rf2
     (all tables)
   Keyspace: test_keyspace_dc2_rf3
     (all tables)
   Keyspace: test_keyspace_rf2
     (all tables)
   Keyspace: test_keyspace_rf3
     (all tables)

**Example with error**

.. code-block:: none

   sctool repair -K 'system*.bla' --dry-run -c bla

   NOTICE: dry run mode, repair is not scheduled

   Error: API error (status 400)
   {
     "message": "no matching units found for filters, ks=[system*.*bla*]",
     "trace_id": "b_mSOUoOSyqSnDtk9EANyg"
   }

=====

``--fail-fast``

Stops the repair process on the first error.

**Default:** False

=====

``--force``

Forces the repair to skip database validation and schedules a repair even if there aren't any matching keyspaces/tables. This means that if the glob patterns matches nothing, a repair will still run.

Default: False

=====

``--host <node IP>``

Host to repair, you may use that to repair given host with other hosts (--with-hosts), you may also want to specify token ranges to repair (--token-ranges).

=====

``-K, --keyspace <list of glob patterns>``

A list of glob patterns separated by a comma.
The patterns match keyspaces and tables, when you write the pattern,
separate the keyspace name from the table name with a dot (*KEYSPACE.TABLE*).

.. include:: _common/glob.rst

**Example**

Given the following tables:

* *shopping_cart.cart*
* *orders.orders_by_date_2018_11_01*
* *orders.orders_by_date_2018_11_15*
* *orders.orders_by_date_2018_11_29*
* *orders.orders_by_date_2018_12_06*

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Parameter
     - Selects
   * - ``-K '*'``
     - *everything - all tables in all keyspaces*
   * - ``-K shopping_cart``
     - *shopping_cart.cart*
   * - ``-K '*,!orders'``
     - *shopping_cart.cart*
   * - ``-K orders.'orders.2018_11_'``
     - *orders.orders_by_date_2018_11_01*
       *orders.orders_by_date_2018_11_15*
       *orders.orders_by_date_2018_11_29*
   * - ``-K 'orders.*2018_1?_2?'``
     - *orders.orders_by_date_2018_11_29*
   * - ``-K 'orders.*2018_11?[19]'``
     - *orders.orders_by_date_2018_11_01*
       *orders.orders_by_date_2018_11_29*

**Default:** everything - all tables in all keyspaces

=====

``--token-ranges <pr|npr|all>``

Dictates which token range is used for the repair. There are three to choose from:

* ``pr``- restricts the repair to the Primary token Range. This is a token range where the node is the first replica in the ring. It is important that if you choose this option to make sure it runs on **every** node in the cluster in order to repair the entire ring.
* ``npr``-  runs the repair on the non-primary token range.
* ``all``- repairs all ranges, primary and non-primary.

**Default:** pr

.. note:: ``--token-ranges`` requires ``--host`` or ``--with-hosts`` to also be used.

=====

``--with-hosts <list of node IPs>``

List of hosts to repair with separated by a comma. When the repair runs the repair compares the ``--host`` with the ``--with-hosts``.

Use **caution** with this flag. It disables the built-in Scylla mechanism for repair and instead, uses only the IP or hostname you set here. If there is a situation where there is missing data in the --with-host cluster, it will be deleted from the subsequent clusters.

=====

.. include:: _common/task-params.rst

=====

Example: Schedule a repair
..........................

Repairs can be scheduled to run on selected keyspaces/tables, nodes, or datacenters. Scheduled repairs run every *n* days depending on the frequency you set. A scheduled repair runs at the time you set it to run at. If no time is given, the repair runs immediately. Repairs can run once, or can run at a set schedule based on a time interval. 

Repair cluster weekly
^^^^^^^^^^^^^^^^^^^^^
 
In this example, you create a repair task for a cluster named *prod-cluster*. The task begins on May 2, 2019 at 3:04 PM. It repeats every week at this time. As there are no datacenters or keyspaces listed, all datacenters and all data in the specified cluster are repaired.

.. code-block:: none
   
   sctool repair -c prod-cluster -s 2019-05-02T15:04:05Z07:00 --interval 7d

The system replies with a repair task ID. You can use this ID to change the start time, stop the repair, or cancel the repair. 

.. code-block:: none

   repair/3208ff15-6e8f-48b2-875c-d3c73f545410

Repair datacenters in a region weekly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
This example repairs all datacenters starting with the name *dc-asia-*, such as *dc-asia-1*. The repair begins on September 15, 2018 at 7:00 PM (JST, for example) and runs every week.

.. code-block:: none

   sctool repair -c prod-cluster --dc 'asia-*' -s 2018-09-15T19:00:05Z07:00 --interval 7d

Repair selected keyspaces/tables weekly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
Using glob patterns gives you additional flexibility in selecting both keyspaces and tables. This example repairs all tables in the *orders* keyspace starting with *2018_11_* prefix. The repair is scheduled to run on December 4, 2018 at 8:00 AM and will run after that point every week.

.. code-block:: none

   sctool repair -c prod-cluster -K 'orders.2018_12_' -s 2018-12-04T08:00:05Z07:00 --interval 7d

Repair a specific host once
^^^^^^^^^^^^^^^^^^^^^^^^^^^

By listing the host IP address, you run a repair only on the the specified host. The argument ``--token-ranges all`` specifies that the repair will run on all token ranges (primary and secondary).

.. code-block:: none

   sctool repair -c prod-cluster --host 198.100.51.11    --token-ranges all

Monitoring clusters
===================

status
------

This command displays the live status of each node in the cluster.
The CQL status is used for healthcheck
The SSL status can be `ON` if SSL is enabled or `OFF` if it is disabled. If you are using an SSH to connect to the clusters, the SSL status will be `OFF`.
The REST API status can be `UP` or `DOWN`. If it is `DOWN`, it means that the connection to the nodes over the REST API has been lost. 

For each node, in parallel, Scylla Manager opens a connection to a CQL port and asks for server options.
If there is no response or the response takes longer than 250 milliseconds, the node is considered to be `DOWN` otherwise the node is considered to be `UP`.
Each host's response time in milliseconds is also shown in the status report.

The status information is also available as a metric in Scylla Monitoring Manager dashboard.
The `healthcheck` task checks nodes every 15 seconds, the interval can be changed using `task update`_ command.

**Syntax:**

.. code-block:: none

   sctool status [global flags]

status parameters
..................

status takes the `Global flags`_. The `SCYLLA_MANAGER_CLUSTER` must also be included. See `Environment variables`_.

Example: status
................

.. code-block:: none

   sctool status -c prod-cluster2
   Datacenter: dc1
   ╭──────────┬─────┬──────────┬────────────────╮
   │ CQL      │ SSL │ REST     │ Host           │
   ├──────────┼─────┼──────────┼────────────────┤
   │ UP (2ms) │ OFF │ UP (1ms) │ 192.168.100.11 │
   │ UP (1ms) │ OFF │ UP (0ms) │ 192.168.100.12 │
   │ UP (2ms) │ OFF │ UP (0ms) │ 192.168.100.13 │
   ╰──────────┴─────┴──────────┴────────────────╯
   Datacenter: dc2
   ╭──────────┬─────┬──────────┬────────────────╮
   │ CQL      │ SSL │ REST     │ Host           │
   ├──────────┼─────┼──────────┼────────────────┤
   │ UP (2ms) │ OFF │ UP (1ms) │ 192.168.100.21 │
   │ UP (1ms) │ OFF │ UP (1ms) │ 192.168.100.22 │
   │ UP (1ms) │ OFF │ UP (1ms) │ 192.168.100.23 │
   ╰──────────┴─────┴──────────┴────────────────╯
  
Managing tasks
==============

The task command set allows you to schedule, start, stop and modify tasks.

.. code-block:: none

   sctool task <command> [flags] [global flags]

**Subcommands**

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Subcommand
     - Usage
   * - `task delete`_
     - Delete a task.
   * - `task history`_
     - Show run history of a task.
   * - `task list`_
     - Show available tasks and their last run status.
   * - `task progress`_
     - Show the task progress.
   * - `task start`_
     - Start executing a task.
   * - `task stop`_
     - Stop executing a task.
   * - `task update`_
     - Modify a task.

task delete
-----------

This command deletes a task from manager.
Note that a task can be disabled if you want to temporarily turn it off (see `task update`_).

**Syntax:**

.. code-block:: none

   sctool task delete <task type/id> --cluster <id|name> [global flags]

.. include:: _common/task-id-note.rst

task delete parameters
......................

In addition to the `Global Flags`_, task delete takes the following parameter:

=====

.. include:: _common/param-cluster.rst

=====

Example: task delete
....................

This example deletes the repair from the task list. You need the task ID for this action. This can be retrieved using the command ``sctool task list``. Once the repair is removed, you cannot resume the repair. You will have to create a new one.

.. code-block:: none 
   
   sctool task delete --cluster prod-cluster repair/143d160f-e53c-4890-a9e7-149561376cfd


task history
------------

This command shows a details about task run history for a give task.

**Syntax:** 

.. code-block:: none

   sctool task history <task type/id> --cluster <id|name>
   [--limit <number of results>] [global flags]

.. include:: _common/task-id-note.rst

task history parameters
.......................

In addition to the `Global Flags`_, task history takes the following parameters:

=====

.. include:: _common/param-cluster.rst

=====

``--limit <number of results>``

Limits the number of returned results.

**Default** 10

=====

Example: task history
.....................

.. code-block:: none

   sctool task history repair/730a134a-4792-4139-bc6c-75d2ba7a1e62 -c prod-cluster

   ╭──────────────────────────────────────┬────────────────────────┬────────────────────────┬──────────┬────────────────────────────────────────────────╮
   │ id                                   │ start time             │ end time               │ duration │ status                                         │ 
   ├──────────────────────────────────────┼────────────────────────┼────────────────────────┼──────────┼────────────────────────────────────────────────┤ 
   │ f81ba8ad-ad79-11e8-915f-42010af000a9 │ 01 Jan 18 00:00:00 UTC │ 01 Jan 18 00:00:30 UTC │ 30s      │ STOPPED                                        │
   │ e02d2caf-ad2a-11e8-915e-42010af000a9 │ 31 Feb 18 14:33:05 UTC │ 31 Feb 18 14:34:35 UTC │ 90s      │ SUCCESS                                        │
   │ 7a8c6fe2-ad29-11e8-915d-42010af000a9 │ 31 Mar 18 14:23:20 UTC │ 31 Mar 18 14:23:20 UTC │ 0s       │ ERROR failed to load units …                   │  
   │ 08f75324-610d-11e9-9aac-42010af000a9 │ 05 Apr 19 12:33:42 UTC │ 05 Apr 19 12:33:43 UTC │ 1s       │ DONE                                           │
   │ 000681e1-610d-11e9-9aab-42010af000a9 │ 09 Apr 19 12:33:27 UTC │ 09 Apr 19 12:33:28 UTC │ 1s       │ DONE                                           │
   │ f715fb82-610c-11e9-9aaa-42010af000a9 │ 11 Apr 19 12:33:12 UTC │ 11 Apr 19 12:33:13 UTC │ 1s       │ DONE                                           │
   │ ee251fc0-610c-11e9-9aa9-42010af000a9 │ 13 Apr 19 12:32:57 UTC │ 13 Apr 19 12:32:58 UTC │ 1s       │ DONE                                           │
   │ e5343b52-610c-11e9-9aa8-42010af000a9 │ 15 Apr 19 15:32:42 UTC │ 15 Apr 19 15:32:43 UTC │ 1s       │ DONE                                           │
   │ dc435562-610c-11e9-9aa7-42010af000a9 │ 17 Apr 19 12:32:27 UTC │ 17 Apr 19 12:32:28 UTC │ 1s       │ DONE                                           │
   ╰──────────────────────────────────────┴────────────────────────┴────────────────────────┴──────────┴────────────────────────────────────────────────╯

task list
---------

This command shows all of the scheduled tasks for the specified cluster.
If cluster is not set this would output a table for every cluster.
Each row contains task type and ID, separated by a slash, task properties, next activation and last status information.
For more information on a task consult `task history`_ and `task progress`_.

**Syntax:**

.. code-block:: none

   sctool task list [--cluster <id|name>] [--all]
   [--status <status>] [--type <task type>] [global flags]

task list parameters
....................

In addition to the `Global Flags`_, task list takes the following parameters:

=====

.. include:: _common/param-cluster.rst

=====

``--all``

Lists all tasks, including those which have been disabled. Disabled tasks are prefixed with ``*``. For example ``*repair/afe9a610-e4c7-4d05-860e-5a0ddf14d7aa``.

=====

``--status <status>``

Filters tasks according to their last run status. Accepted values are NEW, STARTING, RUNNING, STOPPING, STOPPED, DONE, ERROR, ABORTED.

=====

``-t, --type <task type>``

Display only tasks of a given type.

=====

Example: task list
..................

.. code-block:: none


   sctool task list -c prod-cluster --all

   ╭──────────────────────────────────────────────────────┬───────────────────────────────┬──────┬───────────────────────────┬──────────╮
   │ task                                                 │ next run                      │ ret. │ arguments                 │ status   │
   ├──────────────────────────────────────────────────────┼───────────────────────────────┼──────┼───────────────────────────┼──────────┤
   │ healthcheck/43242be1-c78f-43fd-ac24-7c95e3c369ba     │ 22 Mar 19 14:31:41 CET (+15s) │ 0    │                           │ DONE     │
   │ repair/953b8f67-ac5e-411d-8964-47488964deaf          │ 22 Mar 19 14:31:56 CET        │ 3/3  │ -K foo,bar,zoo,!zoo.horse │ ERROR    │
   │ healthcheck_api/3dff7987-c42d-4a3c-a36f-de3494c76c78 │ 22 Mar 19 15:25:26 CET (+1h)  │ 0    │                           │ STARTING │
   │ repair/12e88c37-e1d8-423f-8d23-f2d5da5ce988          │ 23 Mar 19 00:00:00 CET (+7d)  │ 3/3  │                           │ NEW      │
   ╰──────────────────────────────────────────────────────┴───────────────────────────────┴──────┴───────────────────────────┴──────────╯

Setting the ``--all`` flag will also list disabled tasks which are not shown in the regular view. Disabled tasks are prefixed with a ``*``.

task progress
-------------

This command shows details of the latest run (or still running) task.

**Syntax:**

.. code-block:: none

   sctool task progress <task type/id> --cluster <id|name> [--details] [global flags]

.. include:: _common/task-id-note.rst

progress parameters
...................


In addition to the `Global flags`_, repair progress takes the following parameters:

=====

.. include:: _common/param-cluster.rst

=====

``--details``

More detailed progress data, depending on task type.

====

Example: task progress 
......................

This example displays the progress of a running repair. 

.. code-block:: none

   sctool task progress repair/dff91fd1-f430-4f98-8932-373644fe647e -c test-cluster
   Status:         RUNNING
   Start time:     17 Apr 19 12:55:57 UTC
   Duration:       46s
   Progress:       0.45%
   Datacenters:
     - dc1
     - dc2
   ╭───────────────────────┬───────╮
   │ system_auth           │ 3.85% │
   │ system_distributed    │ 0.00% │
   │ system_traces         │ 0.00% │
   │ test_keyspace_dc1_rf2 │ 0.00% │
   │ test_keyspace_dc1_rf3 │ 0.00% │
   │ test_keyspace_dc2_rf2 │ 0.00% │
   │ test_keyspace_dc2_rf3 │ 0.00% │
   │ test_keyspace_rf2     │ 0.00% │
   │ test_keyspace_rf3     │ 0.00% │
   ╰───────────────────────┴───────╯

The ``--details`` flag shows each host’s shard repair progress, with the shards numbered from zero.

.. code-block:: none

   Status:         RUNNING
   Start time:     17 Apr 19 12:55:57 UTC
   Duration:       3m0s
   Progress:       1.91%
   Datacenters:
     - dc1
     - dc2
   ╭───────────────────────┬────────╮
   │ system_auth           │ 16.30% │
   │ system_distributed    │ 0.00%  │
   │ system_traces         │ 0.00%  │
   │ test_keyspace_dc1_rf2 │ 0.00%  │
   │ test_keyspace_dc1_rf3 │ 0.00%  │
   │ test_keyspace_dc2_rf2 │ 0.00%  │
   │ test_keyspace_dc2_rf3 │ 0.00%  │
   │ test_keyspace_rf2     │ 0.00%  │
   │ test_keyspace_rf3     │ 0.00%  │
   ╰───────────────────────┴────────╯
   ╭───────────────────────┬───────┬──────────┬───────────────┬─────────────────┬───────────────╮
   │ system_auth           │ shard │ progress │ segment_count │ segment_success │ segment_error │
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ 192.168.100.11        │ 0     │ 100.00%  │ 748           │ 748             │ 0             │
   │ 192.168.100.11        │ 1     │ 100.00%  │ 757           │ 757             │ 0             │
   │ 192.168.100.22        │ 0     │ 2.40%    │ 791           │ 19              │ 0             │
   │ 192.168.100.22        │ 1     │ 2.35%    │ 807           │ 19              │ 0             │
   │ 192.168.100.12        │ 0     │ 0.00%    │ 740           │ 0               │ 0             │
   │ 192.168.100.12        │ 1     │ 0.00%    │ 740           │ 0               │ 0             │
   │ 192.168.100.13        │ 0     │ 0.00%    │ 922           │ 0               │ 0             │
   │ 192.168.100.13        │ 1     │ 0.00%    │ 930           │ 0               │ 0             │
   │ 192.168.100.21        │ 0     │ 0.00%    │ 765           │ 0               │ 0             │
   │ 192.168.100.21        │ 1     │ 0.00%    │ 767           │ 0               │ 0             │
   │ 192.168.100.23        │ 0     │ 0.00%    │ 752           │ 0               │ 0             │
   │ 192.168.100.23        │ 1     │ 0.00%    │ 747           │ 0               │ 0             │   
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ system_distributed    │ shard │ progress │ segment_count │ segment_success │ segment_error │
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ 192.168.100.11        │ 0     │ 0.00%    │ 748           │ 0               │ 0             │
   │ 192.168.100.11        │ 1     │ 0.00%    │ 757           │ 0               │ 0             │
   │ 192.168.100.12        │ 0     │ 0.00%    │ 740           │ 0               │ 0             │
   │ 192.168.100.12        │ 1     │ 0.00%    │ 740           │ 0               │ 0             │
   │ 192.168.100.13        │ 0     │ 0.00%    │ 922           │ 0               │ 0             │
   │ 192.168.100.13        │ 1     │ 0.00%    │ 930           │ 0               │ 0             │
   │ 192.168.100.21        │ 0     │ 0.00%    │ 765           │ 0               │ 0             │
   │ 192.168.100.21        │ 1     │ 0.00%    │ 767           │ 0               │ 0             │
   │ 192.168.100.22        │ 0     │ 0.00%    │ 791           │ 0               │ 0             │
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ system_traces         │ shard │ progress │ segment_count │ segment_success │ segment_error │
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ 192.168.100.11        │ 0     │ 0.00%    │ 748           │ 0               │ 0             │
   │ 192.168.100.11        │ 1     │ 0.00%    │ 757           │ 0               │ 0             │
   │ 192.168.100.12        │ 0     │ 0.00%    │ 740           │ 0               │ 0             │
   │ 192.168.100.12        │ 1     │ 0.00%    │ 740           │ 0               │ 0             │
   │ 192.168.100.13        │ 0     │ 0.00%    │ 922           │ 0               │ 0             │
   │ 192.168.100.13        │ 1     │ 0.00%    │ 930           │ 0               │ 0             │
   │ 192.168.100.21        │ 0     │ 0.00%    │ 765           │ 0               │ 0             │
   │ 192.168.100.21        │ 1     │ 0.00%    │ 767           │ 0               │ 0             │
   │ 192.168.100.22        │ 0     │ 0.00%    │ 791           │ 0               │ 0             │
   │ 192.168.100.22        │ 1     │ 0.00%    │ 807           │ 0               │ 0             │
   │ 192.168.100.23        │ 0     │ 0.00%    │ 752           │ 0               │ 0             │
   │ 192.168.100.23        │ 1     │ 0.00%    │ 747           │ 0               │ 0             │
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ test_keyspace_dc1_rf2 │ shard │ progress │ segment_count │ segment_success │ segment_error │
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ 192.168.100.11        │ 0     │ 0.00%    │ 1339          │ 0               │ 0             │
   │ 192.168.100.11        │ 1     │ 0.00%    │ 1339          │ 0               │ 0             │
   │ 192.168.100.12        │ 0     │ 0.00%    │ 1482          │ 0               │ 0             │
   │ 192.168.100.12        │ 1     │ 0.00%    │ 1480          │ 0               │ 0             │
   │ 192.168.100.13        │ 0     │ 0.00%    │ 1523          │ 0               │ 0             │
   │ 192.168.100.13        │ 1     │ 0.00%    │ 1528          │ 0               │ 0             │
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ test_keyspace_dc1_rf3 │ shard │ progress │ segment_count │ segment_success │ segment_error │
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ 192.168.100.11        │ 0     │ 0.00%    │ 1339          │ 0               │ 0             │
   │ 192.168.100.11        │ 1     │ 0.00%    │ 1339          │ 0               │ 0             │
   │ 192.168.100.12        │ 0     │ 0.00%    │ 1482          │ 0               │ 0             │
   │ 192.168.100.12        │ 1     │ 0.00%    │ 1480          │ 0               │ 0             │
   │ 192.168.100.13        │ 0     │ 0.00%    │ 1523          │ 0               │ 0             │
   │ 192.168.100.13        │ 1     │ 0.00%    │ 1528          │ 0               │ 0             │   
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ test_keyspace_dc2_rf2 │ shard │ progress │ segment_count │ segment_success │ segment_error │
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ 192.168.100.21        │ 0     │ 0.00%    │ 1349          │ 0               │ 0             │
   │ 192.168.100.21        │ 1     │ 0.00%    │ 1343          │ 0               │ 0             │
   │ 192.168.100.22        │ 0     │ 0.00%    │ 1550          │ 0               │ 0             │
   │ 192.168.100.22        │ 1     │ 0.00%    │ 1561          │ 0               │ 0             │
   │ 192.168.100.23        │ 0     │ 0.00%    │ 1450          │ 0               │ 0             │
   │ 192.168.100.23        │ 1     │ 0.00%    │ 1465          │ 0               │ 0             │
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ test_keyspace_dc2_rf3 │ shard │ progress │ segment_count │ segment_success │ segment_error │
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ 192.168.100.21        │ 0     │ 0.00%    │ 1349          │ 0               │ 0             │
   │ 192.168.100.21        │ 1     │ 0.00%    │ 1343          │ 0               │ 0             │
   │ 192.168.100.22        │ 0     │ 0.00%    │ 1550          │ 0               │ 0             │
   │ 192.168.100.22        │ 1     │ 0.00%    │ 1561          │ 0               │ 0             │
   │ 192.168.100.23        │ 0     │ 0.00%    │ 1450          │ 0               │ 0             │
   │ 192.168.100.23        │ 1     │ 0.00%    │ 1465          │ 0               │ 0             │
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ test_keyspace_rf2     │ shard │ progress │ segment_count │ segment_success │ segment_error │
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ 192.168.100.21        │ 0     │ 0.00%    │ 1349          │ 0               │ 0             │
   │ 192.168.100.21        │ 1     │ 0.00%    │ 1343          │ 0               │ 0             │
   │ 192.168.100.22        │ 0     │ 0.00%    │ 1550          │ 0               │ 0             │
   │ 192.168.100.22        │ 1     │ 0.00%    │ 1561          │ 0               │ 0             │
   │ 192.168.100.23        │ 0     │ 0.00%    │ 1450          │ 0               │ 0             │
   │ 192.168.100.23        │ 1     │ 0.00%    │ 1465          │ 0               │ 0             │
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ test_keyspace_rf3     │ shard │ progress │ segment_count │ segment_success │ segment_error │
   ├───────────────────────┼───────┼──────────┼───────────────┼─────────────────┼───────────────┤
   │ 192.168.100.11        │ 0     │ 0.00%    │ 1339          │ 0               │ 0             │
   │ 192.168.100.11        │ 1     │ 0.00%    │ 1339          │ 0               │ 0             │
   │ 192.168.100.12        │ 0     │ 0.00%    │ 1482          │ 0               │ 0             │
   │ 192.168.100.12        │ 1     │ 0.00%    │ 1480          │ 0               │ 0             │
   │ 192.168.100.13        │ 0     │ 0.00%    │ 1523          │ 0               │ 0             │
   │ 192.168.100.13        │ 1     │ 0.00%    │ 1528          │ 0               │ 0             │
   ╰───────────────────────┴───────┴──────────┴───────────────┴─────────────────┴───────────────╯
   


task start
----------

This command initiates a task run.
Note that if a repair task is already running on a cluster, other repair tasks runs on that cluster will fail.

**Syntax:**

.. code-block:: none

   sctool task start <task type/id> --cluster <id|name> [global flags]

.. include:: _common/task-id-note.rst

task start parameters
.....................

In addition to the `Global Flags`_, task start takes the following parameters:

=====

.. include:: _common/param-cluster.rst

=====

``--continue``

Try to resume the last run.

**Default** true

=====

Example: task start
...................

This example resumes running which was previously stopped. To start a repair which is scheduled, but is currently not running use the ``task update`` command making sure to set the start time to ``now``. See `Example: task update`_.


If you have stopped a repair you can resume it by running the following command. You will need the task ID for this action. This can be retrieved using the command ``sctool task list``.

.. code-block:: none 
   
   sctool task start --cluster a_cluster_name repair/143d160f-e53c-4890-a9e7-149561376cfd

task stop
---------

Stops a specified task, stopping an already stopped task has no effect.

**Syntax:**

.. code-block:: none

   sctool task stop <task type/id> --cluster <id|name> [global flags]

.. include:: _common/task-id-note.rst

task stop parameters
.....................

In addition to the `Global flags`_, task stop takes the following parameter:

=====

.. include:: _common/param-cluster.rst

=====

Example: task stop
..................

This example immediately stops a running repair. 
The task is not deleted and can be resumed at a later time. 
You will need the task ID for this action. This can be retrieved using the command ``sctool task list``.

.. code-block:: none 
   
   sctool task stop --cluster a_cluster_name repair/143d160f-e53c-4890-a9e7-149561376cfd 

task update
-----------

This command changes generic task parameters such as schedule.

**Syntax:**

.. code-block:: none

   sctool task update <task type/id> --cluster <id|name> [--enabled <bool>]
   [--name <alias>] [--tags <list of tags>]
   [--interval <time between task runs>]
   [--start-date <now+duration|RFC3339>]
   [--num-retries <times to rerun a failed task>] [global flags]

.. include:: _common/task-id-note.rst

task update parameters
......................

In addition to `Global flags`_, task stop takes the following parameters:

=====

.. include:: _common/param-cluster.rst

=====

``-e``, ``--enabled``

Setting enabled to false disables the task.
Disabled task is not executed and hidden from task list.
To show disabled tasks invoke ``sctool task list --all`` (see `task list`_).

**Default** true

=====

``-n``, ``--name <alias>``

Adds a name to a task.

=====

``--tags <list of tags>``

Allows you to tag the task with a list of text.

=====

.. include:: _common/task-params.rst

=====

Example: task update
....................

This example disables the task

.. code-block:: none

   sctool task update -c prod-cluster repair/4d79ee63-7721-4105-8c6a-5b98c65c3e21 --enabled false


This example reschedules the repair to run in 3 hours from now instead of whatever time it was supposed to run and sets the repair to run every two days. 
The new time you set replaces the time which was previously set. 

.. code-block:: none 
   
   sctool task update -c prod-cluster repair/143d160f-e53c-4890-a9e7-149561376cfd -s now+3h --interval 2d


