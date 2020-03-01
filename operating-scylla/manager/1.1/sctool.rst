
================
sctool Reference
================

.. versionadded:: 1.1 Scylla Manager

.. contents:: 
    :depth: 1
    :local:

About sctool
============
``sctool`` is a Command Line Interface (CLI) for the Scylla Manager server. The server communicates with multiple Scylla clusters and performs cluster-wide operations such as automatic repair.

**Usage**

.. code-block:: none
                
   sctool command [parameters] [global flags]


Global flags
------------

* ``--api-url URL`` - URL of Scylla Manager server (default "http://localhost:8889/api/v1")
* ``-h``, ``--help`` - Help for commands. Use **sctool [command] --help** for help about a specific command.


List the sctool version
-----------------------

**Definition:** Lists the currently installed sctool version for both the client and the server.

**Syntax:** ``sctool version [flags]``

version parameters
..................

version takes the `Global flags`_.


version example
...............

.. code-block:: none
                
   sctool version

   Client version: 1.0.0_0.20180119.49f4a33
   Server version: 1.0.0_0.20180119.49f4a33


Managing Clusters
=================
The cluster commands allow you to add, delete, list, and update clusters. A Scylla cluster must be added before management tasks can be initiated.

.. code-block:: none
                
   sctool cluster <command> [flags]


cluster add
-----------
**Definition:** Adds the specified cluster(s) to the manager. Once a  Scylla cluster is added, a  Repair unit is automatically created for every keyspace within the cluster, including system keyspaces. In addition, a weekly repair task is added.

**Syntax:** ``$ sctool cluster add --hosts <hostList> --shard-count <int> [--name <alias>] [flags]``

cluster add parameters
......................

In addition to the `Global flags`_, cluster add takes the following parameters:
 
``--hosts``
	The host list parameter is a **mandatory** parameter requiring a list containing a subset of nodes. Each node needs to be separated by a comma. This list is used to learn the cluster topology. When this parameter is set, an initial connection to each host will be attempted in order to validate that all hosts that belong to the same Scylla cluster and reside within the same datacenter.

``-n``, ``--name`` 
	When a Scylla cluster is added, it is assigned a Unique identifier. Use this parameter to identify the cluster by an alias name which is more meaningful. This alias name can be used with all commands. Note that when the name is used in additional commands it is with the -c global flag and not the -n parameter.

``--shard-count <int>`` 
	Number of Scylla shards on each node in the managed cluster. This is a **mandatory** parameter and the value needs to match the actual number of shards that is set in the cluster. **Note:** Each node must have an equal number of shards.

cluster add example
...................

.. code-block:: none
                
   sctool cluster add --hosts=172.16.1.10,172.16.1.2 --name scylla-1 --shard-count=16

   30a538a0-9bdb-4276-a69d-60e19197fd93   


cluster delete
--------------
**Definition:** Deletes the specified cluster(s) from the manager.

**Syntax:** ``$ sctool cluster delete --cluster <clusterName|ID> [flags]``

cluster delete parameters
.........................

In addition to `Global flags`_, cluster delete takes the following parameter:

``-c`` , ``--cluster``
	This is the cluster name is the name you assigned when you created the cluster (`cluster add`_). You can see the cluster name and ID by running the command `cluster list`_. 

cluster delete example
......................

.. code-block:: none
                
   sctool cluster delete -c scylla-1 

cluster list
------------
**Definition:** Lists the managed clusters.

**Syntax:** ``$ sctool cluster list [flags]``

cluster list parameters
.......................

cluster list takes the `Global flags`_.

cluster list example
....................

.. code-block:: none
                
   sctool cluster list 
   ╭──────────────────────────────────────┬──────────┬──────────────────────────┬─────────────╮        
   │ cluster id                           │ name     │ hosts                    │ shard count │         
   ├──────────────────────────────────────┼──────────┼──────────────────────────┼─────────────┤
   │ 30a538a0-9bdb-4276-a69d-60e19197fd93 │ scylla-1 │ [172.16.1.10 172.16.1.2] │ 16          │
   ╰──────────────────────────────────────┴──────────┴──────────────────────────┴─────────────╯ 

cluster update
--------------
**Definition:** Modifies a managed cluster.

**Syntax:** 

.. code-block:: none

   sctool cluster update --cluster <clusterName|ID> [--name <alias>] [--shard-count <int>] [flags]


cluster update parameters
.........................
In addtion to the `Global flags`_, cluster update takes the following parameters:

``-c`` , ``--cluster``
	This is a **mandatory** parameter. The cluster name is the name you assigned when you created the cluser (`cluster add`_). You can see the cluster name and ID by running the command `cluster list`_. 

``-n``, ``--name``
	When a Scylla cluster is added, it is assigned a Unique identifier. Use this parameter to identify the cluster by an alias name which is more meaningful. This alias name can be used with all cluster commands. This alias name can be used with all commands. Note that when the name is used in additional commands it is with the -c global flag and not the -n parameter.

``--shard-count [int]`` 
	Number of Scylla shards on each node in the managed  cluster. It should match the  actual number of shards as closely as possible. **Note:** Each node must have an equal number of shards.

cluster update example
......................

In this example, the cluster named scylla-1 has been renamed to scylla-cluster-a1 and the shard count was reduced from 16 to 14.

.. code-block:: none
                
   sctool cluster update --cluster scylla-1 --name scylla-cluster-a1 --shard-count 14

Scheduling Repairs
==================
The repair commands allow you to schedule and monitor the progress of repairs for a unit. These commands use the `Global Flags`_. 

.. code-block:: none
                
   sctool repair <command> [flags] 

repair progress
---------------
The details of the latest run (or still running) repair task can be displayed with the command sctool repair progress command. This command requires a task has been added and started. When looking at the `task list`_, its status should be 'running'. 

**Definition:** gives details about an active repair task

**Syntax:** 

.. code-block:: none

   sctool repair progress <repair/UUID> --cluster <clusterName|ID>  [--details] [--unit <unitName>] [flags] 

A Repair UUID or task ID is **required** for this command. If you do not know the repair or task ID run the sctool `repair schedule_` command. 

repair progress parameters
..........................


In addition to the `Global flags`_, repair progress takes the following parameters:

``-c`` , ``--cluster``
	This is a **mandatory** parameter. The cluster name is the name you assigned when you created the cluser (`cluster add`_). You can see the cluster name and ID by running the command `cluster list`_. 

``-d``, ``--details`` 
	More detailed progress data. Without the ``--details`` flag specified, each row holds the host’s address, progress percentage and the number of failed segments.

``-r``, ``--repair`` 
	The repair task id, as returned by the sctool `repair schedule`_ command

``-u``, ``--unit``
	The repair unit name as set in the sctool `repair unit add`_ command

Alternatively, without specifying the repair/task-id one can use the `-u` flag to get the details of the latest repair run on the specified unit.
The output returned includes the repair status, overall repair progress percentage and a table listing per-host progress.
A host on which repair on its primary ranges has not started yet, will hold minus (“-”) signs instead of values

repair progress examples
........................

.. code-block:: none

   sctool repair progress   repair/b9a1b304-a51f-4238-871d-e8f2dddd1215 --cluster scylla-cluster2
   Status: running, progress: 68%
   ╭───────────┬──────────┬─────────────────╮
   │ host      │ progress │ failed segments │
   ├───────────┼──────────┼─────────────────┤
   │ 127.0.0.1 │ 68       │ 0               │
   ╰───────────┴──────────┴─────────────────╯
                

The ``--details`` flag shows each host’s shard repair progress, with the shards numbered from zero.


.. code-block:: none

   sctool repair progress repair/b9a1b304-a51f-4238-871d-e8f2dddd1215 --details --cluster scylla-cluster2
   Status: running, progress: 73%
   ╭───────────┬───────┬──────────┬─────────────────╮
   │ host      │ shard │ progress │ failed segments │
   ├───────────┼───────┼──────────┼─────────────────┤
   │ 127.0.0.1 │ 0     │ 73       │ 0               │
   │ 127.0.0.1 │ 1     │ 73       │ 0               │
   │ 127.0.0.1 │ 2     │ 73       │ 0               │
   │ 127.0.0.1 │ 3     │ 73       │ 0               │
   ╰───────────┴───────┴──────────┴─────────────────╯

repair schedule
---------------
**Definition:** Allows you to schedule the unit repair. 

**Syntax:** 

.. code-block:: none

   sctool repair schedule <unit-id> --cluster <clusterName|ID> [--interval <days>] [--num-retries <retries>] [--start-date <date-string>] [flags]
 
This command replies with the task ID. You will need this ID for additional commands. 
When a repair is scheduled, a repair task is created, it is assigned a unique identifier with the “repair” prefix (“repair/UUID”) which is printed to the command line.

repair schedule parameters
..........................

The Unit ID `<unit-id>` is a **mandatory** parameter for this command. The Unit ID can be supplied as a UUID or as an alias name. If you do not know the Unit ID, run the command ``sctool repair unit list`` (see `repair unit list`_). If you do not have a Unit ID see `repair unit add`_. In addition to the `Global Flags`_, repair schedule takes the following parameters:

``-c`` , ``--cluster``
	This is a **mandatory** parameter. The cluster name is the name you assigned when you created the cluser (`cluster add`_). You can see the cluster name and ID by running the command `cluster list`_. 

``-i``, ``--interval``
	Schedule a repair interval in days (default is 7). Every X days a repair will occur. 

``-r``, ``--retries``
	Should the scheduled repair fail, if this parameter is set, the server will retry to run the repair. You need to supply the number of retries (default is 3). Entering a value of 0 disables retries.

``-s``, ``--start-date`` 
	The task start date. in RFC3339 format date (i.e. 2017-12-30T23:00:00Z) form or use the string ``now`` with an optional modifier specifying time units to add. For example **now+2h** to start 2 hours from now, **now+30m** to start in 30 minutes.

repair schedule example
.......................

In this example a repair schedule was made to repair unit b02b418d-1884-43d4-b34f-2ea07d0e10c7 on cluster scylla-cluster 2 to begin two hours from now. It returns the repair task ID.

.. code-block:: none
                
   sctool repair schedule 3650e852-33bf-46b0-9e46-650ea3a07c8e --cluster scylla-cluster2 --start-date now+2h

   repair/b9a1b304-a51f-4238-871d-e8f2dddd1215

Alternatively, you can use the ``--name`` parameter to specify the repair Unit ID's alias name:

.. code-block:: none
                
   sctool repair schedule --name system --cluster scylla-cluster2 --start-date now+2h

   repair/b9a1b304-a51f-4238-871d-e8f2dddd1215


Managing repair units
=====================
The repair unit commands allow you to manage repair units. 

.. code-block:: none

   sctool repair unit <command> [flags]

repair unit add
---------------
**Definition:** Adds a new repair unit

**Syntax:** 

.. code-block:: none

   sctool repair unit add --cluster <clusterName|ID> [--keyspace <name>][--name <alias>][--tables <string>][flags]


Note that once a Scylla cluster is registered, a Repair Unit is automatically created for each existing keyspace in the cluster, including system keyspaces. These units are kept in sync by the automatic repair. Therefore this step is only necessary when keyspaces are added/removed before the auto repair sync had a chance to run and a repair needs to be scheduled on them.

repair unit add parameters
..........................

In addition to the `Global Flags`_, repair unit add takes the following parameters:

``-c`` , ``--cluster``
	This is a **mandatory** parameter. The cluster name is the name you assigned when you created the cluser (`cluster add`_). You can see the cluster name and ID by running the command `cluster list`_. 

``-k``, ``keyspace``
	This is a **mandatory** parameter. Name of the keyspace to be repaired.

``-n``, ``--name``
	When a Scylla cluster is added, it is assigned a Unique identifier. Use this parameter to identify the cluster by an alias name which is more meaningful. This alias name can be used with all cluster commands. This alias name can be used with all commands. Note that when the name is used in additional commands it is with the -c global flag and not the -n parameter.

``-t``, ``--tables``
	Comma-separated list of tables in to repair in the keyspace, if empty or if not used, all tables in the keyspace are repaired.

repair unit add example
.......................

.. code-block:: none
                
   sctool repair unit add --name system --keyspace system --cluster scylla-cluster2

repair unit delete
------------------
**Definition:** Deletes a repair unit

**Syntax:** ``$ sctool repair unit delete --cluster <clusterName|ID> [flags]``
 
repair unit delete parameters
.............................
In addition to the `Global Flags`_, repair unit delete takes the following parameters:
 
``-c`` , ``--cluster``
	This is a **mandatory** parameter. The cluster name is the name you assigned when you created the cluser (`cluster add`_). You can see the cluster name and ID by running the command `cluster list`_.
 
repair unit delete example
..........................

.. code-block:: none
                
   sctool repair unit delete -n repair-unit-name --cluster scylla-1

repair unit list
----------------
**Definition:** Lists the repair units

**Syntax:** ``$ sctool repair unit list --cluster <clusterName|ID> [flags]``
 
repair unit list parameters
...........................
In addition to the `Global Flags`_, repair unit list takes the following parameters:

``-c`` , ``--cluster``
	This is a **mandatory** parameter. The cluster name is the name you assigned when you created the cluser (`cluster add`_). You can see the cluster name and ID by running the command `cluster list`_..  


repair list example
...................

.. code-block:: none
                
   sctool repair unit list --cluster scylla-1        
   ╭──────────────────────────────────────┬────────────────┬────────────────┬────────╮
   │ unit id                              │ name           │ keyspace       │ tables │
   ├──────────────────────────────────────┼────────────────┼────────────────┼────────┤
   │ 3650e852-33bf-46b0-9e46-650ea3a07c8e │ system         │ system         │ []     │
   │ 4c0ab8c6-7e57-41de-b3b5-836f55dab8ff │ system_traces  │ system_traces  │ []     │
   │ 61bee124-6624-43e2-b1bf-4433852865c3 │ scylla_manager │ scylla_manager │ []     │
   ╰──────────────────────────────────────┴────────────────┴────────────────┴────────╯          

repair unit update
------------------
**Definition:** Modifies a repair unit

**Syntax:** 

.. code-block:: none

   sctool repair unit update <unitID> --cluster <clusterName|ID> [--keyspace <name>][--name <alias>][--tables <string>] [flags]


A unit name or ID is **required** for this command. The Unit ID can be supplied as a UUID or as an alias name. If you do not know the Unit ID, it is displayed when you run the command ``sctool repair unit list`` (see `repair unit list`_).

repair unit update parameters
.............................
In addition to the `Global Flags`_, repair unit update takes the following parameters:

``-c`` , ``--cluster``
	This is a **mandatory** parameter. The cluster name is the name you assigned when you created the cluser (`cluster add`_). You can see the cluster name and ID by running the command `cluster list`_.

``-k``, ``keyspace``
	Name of the keyspace to be repaired.

``-n``, ``--name``
	When a repair unit is added, it is assigned a Unique identifier (Unit ID). Use this parameter to identify the cluster by an alias name which is more meaningful.

``-t``, ``--tables``
	Comma-separated list of tables in to repair in the keyspace, if empty or if not used, all tables in the keyspace are repaired.

repair unit update example
..........................
This example updates Unit ID 61bee124-6624-43e2-b1bf-4433852865c3 and changes the name from scylla_manager to repair-unit-name.

.. code-block:: none
                
   sctool repair unit update 61bee124-6624-43e2-b1bf-4433852865c3 --cluster scylla-cluster2 --name repair-unit-name


Managing tasks
==============
The task command set allows you to schedule, start, stop and modify tasks.

.. code-block:: none
                
   sctool task <command> [flags]


task delete
-----------
**Definition:** Deletes a task

**Syntax:** ``$ sctool task delete <taskID> --cluster <clusterName|ID> [flags]``

A task ID is **required** for this command. This is a unique ID which is created when the task was made. To display the ID, run the command ``sctool task list``

task delete parameters
......................

In addition to the `Global Flags`_, task delete takes the following parameters:

``-c`` , ``--cluster``
	This is a **mandatory** parameter. The cluster name is the name you assigned when you created the cluser (`cluster add`_). You can see the cluster name and ID by running the command `cluster list`_.

task delete example
...................

.. code-block:: none
                
   sctool task delete repair/63af310a-8923-4ad0-b60a-426f04a225ea -c scylla-cluster2

task history
------------
**Definition:** Returns a list of runs for a specified task.

**Syntax:** 

.. code-block:: none

   sctool task history <taskID> --cluster <clusterName|ID> [--limit limit]  [flags]

A task ID is **required** for this command. This is a unique ID which is created when the task was made. To display the ID, run the command ``$ sctool task list`` (see `task list`_).

task history parameters
.......................

In addition to the `Global Flags`_, task history takes the following parameters:

``-c`` , ``--cluster``
	This is a **mandatory** parameter. The cluster name is the name you assigned when you created the cluser (`cluster add`_). You can see the cluster name and ID by running the command `cluster list`_.

``--limit``
	Limits the number of returned results. The default limit is 10.

task history example
....................

Using sctool task history a chronological list of past task runs can be displayed. Use the ``--limit`` flag to limit the number of returned results. A missing stop time field for a running task is indicated with a minus (“-”)  as it has not been set yet.

.. code-block:: none
                
   sctool task history repair/3f51284f-6cf2-4fe0-9723-5e6e10ad9992 --cluster scylla-cluster2
   ╭──────────────────────────────────────┬──────────────────────┬──────────────────────────┬─────────╮
   │ id                                   │ start time           │ stop time                │ status  │
   ├──────────────────────────────────────┼──────────────────────┼──────────────────────────┼─────────┤
   │ de9c0b40-17d6-11e8-beda-42010af00037 │ 2018-02-22T13:47:06Z │ 2018-02-22T13:47:20.076Z │ stopped │
   ╰──────────────────────────────────────┴──────────────────────┴──────────────────────────┴─────────╯

task list
-----------
**Definition:** Lists the available tasks and a timestamp for when they were run last. 
This command displays a table with all of the scheduled tasks for the specified cluster. Each row contains the type and Task ID, separated by a slash (“/”). The row also contains the original task schedule as was set with the ``$ sctool repair schedule`` command. This consists of a start date, interval setting and number of retries. Additionally the last run details are displayed which are comprised of the run start & stop dates and the last run status.
Incomplete fields are filled with a minus (“-”). This will happen if the task has not started or in the case of a running task a stop time has not been recorded.

**Syntax:** ``$ sctool task list --cluster <clusterName|ID> [--all] [--status] [flags]``

task list parameters
......................

In addition to the `Global Flags`_, task list takes the following parameters:

``-c`` , ``--cluster``
	This is a **mandatory** parameter. The cluster name is the name you assigned when you created the cluser (`cluster add`_). You can see the cluster name and ID by running the command `cluster list`_.

``--all``
	Lists all tasks, including those which have been disabled.

``--status`` 
	filters tasks according to their last run status. Accepted values include starting, running, stopping, stopped, and error. 

task list example
...................

.. code-block:: none
		
   sctool task list --cluster scylla-cluster2
   ╭───────────────────────────────────────────────────────────┬──────┬──────────────────────┬───────────────┬─────────────┬──────────────────────────┬──────────────────────────┬─────────╮
   │ task id                                                   │ name │ start date           │ interval days │ num retries │ run start                │ run stop                 │ status  │
   ├───────────────────────────────────────────────────────────┼──────┼──────────────────────┼───────────────┼─────────────┼──────────────────────────┼──────────────────────────┼─────────┤
   │ repair/438338ca-bacf-412c-b46f-9c2ecd370353               │      │ 2018-02-22T12:52:46Z │ 7             │ 3           │ 2018-02-22T13:02:46.001Z │ 2018-02-22T13:02:46.001Z │ error   │
   │ repair/97c747a2-c584-4145-99a3-ec9e596e70f1               │      │ 2018-02-22T12:45:52Z │ 7             │ 3           │ 2018-02-22T13:05:52.001Z │ 2018-02-22T13:05:52.001Z │ -       │
   │ repair/b9a1b304-a51f-4238-871d-e8f2dddd1215               │      │ 2018-02-22T12:16:25Z │ 7             │ 3           │ 2018-02-22T12:16:25.001Z │ -                        │ running │
   │ repair/f498329f-1687-48a6-90bf-1fba862746d1               │      │ 2018-02-22T12:57:05Z │ 7             │ 3           │ 2018-02-22T13:07:05.001Z │ 2018-02-22T13:07:05.001Z │ error   │
   │ repair_auto_schedule/aa01977e-437b-4931-885d-78b80152476b │      │ 2018-02-23T00:00:00Z │ 7             │ 6           │ -                        │ -                        │ -       │
   ╰───────────────────────────────────────────────────────────┴──────┴──────────────────────┴───────────────┴─────────────┴──────────────────────────┴──────────────────────────┴─────────╯


Setting the ``--all`` flag will also list disabled tasks which are not shown in the regular view by displaying an additional column “enabled”. A checkmark in the column, indicates that the task is enabled.  


.. code-block:: none

   sctool task list --cluster scylla-cluster2 --all
   ╭─────────┬───────────────────────────────────────────────────────────┬──────┬──────────────────────┬───────────────┬─────────────┬──────────────────────────┬──────────────────────┬─────────╮
   │ enabled │ task id                                                   │ name │ start date           │ interval days │ num retries │ run start                │ run stop             │ status  │
   ├─────────┼───────────────────────────────────────────────────────────┼──────┼──────────────────────┼───────────────┼─────────────┼──────────────────────────┼──────────────────────┼─────────┤
   │ ✓       │ repair/438338ca-bacf-412c-b46f-9c2ecd370353               │      │ 2018-02-22T12:52:46Z │ 7             │ 3           │ -                        │ -                    │ -       │
   │ ✓       │ repair/97c747a2-c584-4145-99a3-ec9e596e70f1               │      │ 2018-02-22T12:45:52Z │ 7             │ 3           │ 2018-02-22T12:45:52Z     │ 2018-02-22T12:45:52Z │ error   │
   │ ✓       │ repair/b9a1b304-a51f-4238-871d-e8f2dddd1215               │      │ 2018-02-22T12:16:25Z │ 7             │ 3           │ 2018-02-22T12:16:25.001Z │ -                    │ running │
   │ ✓       │ repair_auto_schedule/aa01977e-437b-4931-885d-78b80152476b │      │ 2018-02-23T00:00:00Z │ 7             │ 6           │ -                        │ -                    │ -       │
   ╰─────────┴───────────────────────────────────────────────────────────┴──────┴──────────────────────┴───────────────┴─────────────┴──────────────────────────┴──────────────────────┴─────────╯

In this example the task list is filtered to those with an error status. 

.. code-block:: none
		
   sctool task list --cluster scylla-cluster2 --status=error
   ╭───────────────────────────────────────────────────────────┬──────┬──────────────────────┬───────────────┬─────────────┬──────────────────────────┬──────────────────────────┬─────────╮
   │ task id                                                   │ name │ start date           │ interval days │ num retries │ run start                │ run stop                 │ status  │
   ├───────────────────────────────────────────────────────────┼──────┼──────────────────────┼───────────────┼─────────────┼──────────────────────────┼──────────────────────────┼─────────┤
   │ repair/438338ca-bacf-412c-b46f-9c2ecd370353               │      │ 2018-02-22T12:52:46Z │ 7             │ 3           │ 2018-02-22T13:02:46.001Z │ 2018-02-22T13:02:46.001Z │ error   │
   │ repair/f498329f-1687-48a6-90bf-1fba862746d1               │      │ 2018-02-22T12:57:05Z │ 7             │ 3           │ 2018-02-22T13:07:05.001Z │ 2018-02-22T13:07:05.001Z │ error   │
   ╰───────────────────────────────────────────────────────────┴──────┴──────────────────────┴───────────────┴─────────────┴──────────────────────────┴──────────────────────────┴─────────╯

 
task start
----------

**Definition:** starts running a task. Note that if the task is already running (either due to a previous start command or a scheduled task), executing this command cause an error in the task status.

**Syntax:** ``$ sctool task start <taskID> --cluster <clusterName|ID> [flags]``

A task ID is **required** for this command. This is a unique ID which is created when the task was made. To display the ID, run the command ``sctool task list`` (see `task list`_).

task start parameters
.....................

In addition to the `Global Flags`_, task start takes the following parameters:

``-c`` , ``--cluster``
	This is a **mandatory** parameter. The cluster name is the name you assigned when you created the cluser (`cluster add`_). You can see the cluster name and ID by running the command `cluster list`_.

task start example
..................

.. code-block:: none

   sctool task start b509ac5d-c10a-48e7-a9f1-a938cb2d1db7 --cluster scylla-cluster2


task stop
----------

**Definition:** Stops a specified task. Stopping an already stopped task has no effect.

**Syntax:** ``$ sctool task start <taskID> --cluster <clusterName|ID> [flags]``

A task ID is required for this command. This is a unique ID which is created when the task was made. To display the ID, run the command ``sctool task list``


task stop parameters
.....................

In addition to the `Global flags`_, task stop takes the following parameters:

``-c`` , ``--cluster``
	This is a **mandatory** parameter. The cluster name is the name you assigned when you created the cluser (`cluster add`_). You can see the cluster name and ID by running the command `cluster list`_.

task stop example
..................

.. code-block:: none

   sctool task stop b509ac5d-c10a-48e7-a9f1-a938cb2d1db7 --cluster scylla-cluster2


task update
-----------

**Definition:** updates a specified task

**Syntax:**

.. code-block:: none

   sctool task update <taskID> --cluster <clusterName|ID> [--num-retries <int>] [--enabled] [--interval] [--start-date <date>] [--metadata <string>] [--tags <string>] [flags]``


A task ID is **required** for this command. This is a unique ID which is created when the task was made. To display the ID, run the command ``$ sctool task list``


task update parameters
......................

In addition to `Global flags`_, task stop takes the following parameters:

``-c`` , ``--cluster``
	This is a **mandatory** parameter. The cluster name is the name you assigned when you created the cluser (`cluster add`_). You can see the cluster name and ID by running the command `cluster list`_.

``-e``, ``--enabled`` 
	Enables the update. Values are true and false. Default is true.

``-i``, ``--interval``
	Sets the task interval in days. Every X days, the task runs, with X being the interval value you set. Default is 7.

``-m``, ``--metadata``
	Adds a string of metadata to the task.

``-r``, ``--num-retries``
	Sets the number of times a task can be retried on a unit. Default is 3.

``-s``, ``--start-date`` 
	The task start date. in RFC3339 format date (i.e. 2017-12-30T23:00:00Z) form or use the string ``now`` with an optional modifier specifying time units to add. For example **now+2h** to start 2 hours from now, **now+30m** to start in 30 minutes. 

``--tags`` 
	Allows you to tag the task with a text string.


task update example
...................

This example updates the task so that the re-try value is now set to 4 and the interval is 3 days

.. code-block:: none

   sctool task update b509ac5d-c10a-48e7-a9f1-a938cb2d1db7 ---num-retries 4 --interval 3 --cluster scylla-cluster2

Automatic repair scheduling
===========================

Whenever a Scylla cluster is added to the list of managed cluster, a special task of type **repair_auto_schedule** is created. It is set to run every 7 days at midnight UTC.
When the repair_auto_schedule task runs it ensures all available keyspaces in the managed Scylla cluster have a corresponding Repair Unit defined.
It then proceeds to schedule a repair task for each Repair Unit. The scheduled repair tasks are set to run starting at two hours past midnight UTC, with enough retries to last for 6 days.

Environment variables
=====================

The SCYLLA_MANAGER_CLUSTER environment variable can be used instead of specifying the cluster name/ID with the ``--cluster`` flag on command invocations.
The SCYLLA_MANAGER_API_URL environment variable can be used instead of specifying the ``--api-url`` flag to indicate the Scylla Manager server listening endpoint (for example if the default was changed from http://localhost:8889/api/v1). 


