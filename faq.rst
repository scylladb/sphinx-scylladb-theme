Scylla FAQ
==========

.. contents::
   :local:

Performance
-----------

I’m not getting the level of performance I expected. What’s wrong?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Lower than expected performance can be a result of many factors, from HW (storage, CPU, network) to data modeling to the application layer.
As a first step, make sure to have |mon_root| in place. Looking at the Scylla dashboard is the best way to look for bottlenecks.
If you need our help, please follow :doc:`How to Report a Performance Problem </troubleshooting/report_scylla_problem/>` to share data securely.

Scylla is using all of my memory! Why is that? What if the server runs out of memory?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Scylla uses available memory to cache your data. Scylla knows how to dynamically manage memory for optimal performance; for example, if many clients connect to Scylla, it will evict some data from the cache to make room for these connections; when the connection count drops again, this memory is returned to the cache.

Can I limit Scylla to use less CPU and memory?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The :code:`--smp` option (for instance, :code:`--smp 2`) will restrict Scylla to a smaller number of CPUs. It will still use 100 % of those CPUs, but at least won’t take your system out completely. An analogous option exists for memory: :code:`-m`.

Do I ever need to disable the Scylla cache to use less memory?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It is not possible to turn off the Scylla cache. But cache problems do not arise in normal operation. Scylla can use up to 50% of memory for cache, and will dynamically evict rows from the cache if they are too large. So the only possibility of getting an out of memory error is if a single row is bigger than 50% of the memory for a shard. This is (total_machine_memory / (number_of_lcores * 2)).

For a 64GB machine with 16 cores and hyperthreading enabled, you have 2GB per shard, of which the cache can use 1GB per shard. With such large rows, you will have other problems. We recommend staying with rows that are less than a few megabytes maximum size.

What are some of the techniques Scylla uses to achieve its performance?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Scylla tries to utilize all available resources (processor cores, memory, storage, and networking) by always operations in parallel and never blocking. If Scylla needs to read a disk block, it initiates the read and immediately moves on to another task. Later, when the read completes Scylla resumes the original task from where it left off. By never blocking, a high degree of concurrency is achieved, allowing all resources to be utilized to their limit.
Read more on Scylla Architecture:

* `Scylla Technology <http://www.scylladb.com/product/technology/>`_
* `Scylla Memory Management <http://www.scylladb.com/product/technology/memory-management/>`_

I understood Scylla underline `Seastar framework <https://github.com/scylladb/seastar>`_ use one thread per core, but I see more than two threads per core
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Seastar creates an extra thread per core for blocking syscalls (like :code:`open()`/ :code:`fsync()` / :code:`close()` ); this allows the Seastar reactor to continue executing while a blocking operation takes place. Those threads are usually idle, so they don’t contribute to significant context switching activity.

I’m seeing X compaction running in parallel on a single Scylla node. Is it normal?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Yes, for more than one reason:

* each shard (core) will run its compactions independently, often at the same time,
* each table will run its compactions independently, often at the same time
* depending on the compaction strategy, more than one compaction can run in parallel. For example in Sized Tier Compaction Strategy (STCS), large sstable compaction can take time, allowing smaller sstable to be compacted at the same time

Setting io.conf configuration for HDD storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
As part of the Scylla setup process, **iotune** runs a short benchmark of your storage. When completed, it generates the `/etc/scylla.d/io.conf` configuration file. Note that iotune has known issues benchmarking HDD storage.

.. note:: This section is not relevant in 2.3

Therefore, when using Scylla with HDD storage, it is recommended to use RAID0 on all of your available disks, and manually update the `io.conf` configuration file `max-io-request` parameter. This parameter sets the number of concurrent requests sent to the storage. The value for this parameter should be 3X (3 times) the number of your disks. For example, if you have 3 disks, you would set `max-io-request=9`.

How many connections is it recommended to open from each Scylla client application?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a rule of thumb, for Scylla's best performance, each client needs at least 1-3 connection per Scylla core.
For example, a cluster with three nodes, each node with 16 cores, each client application should open 32 (2x16) connections to each Scylla node.

Do I need to configure ``swap`` on a Scylla node?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes, configure ``swap`` on a Scylla node is recommended.
``swap`` size should be set to either ``total_mem``/3 or 16GB - lower of the two.

``total_mem`` is the total size of the nodes memory.

For example:

* If the node ``total_mem`` is 18GB ``swap`` size should be set to 6GB.

* If the node ``total_mem`` is 240GB ``swap`` size should be set to 16GB.

After upgrade from Scylla 2.1 and older, scylla_reactor_utilization metrics is at high percentage (high CPU utilization is observed). Why does this happen?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Scylla 2.2 enables the compaction automatic controller which was not present prior to version 2.2. What this means is that in Scylla 2.1 (and earlier) the system waits for 4 SSTables to be present in the same tier before starting a compaction. In Scylla 2.2 (and later), compactions can be controlled to not impact the workload. This means that workloads which have been considered as backlog in Scylla 2.1 and earlier, in Scylla 2.2 and later are not.

My query does not return any or some of the data? What happened?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you are using a time range in the query, refer to the solution in the troubleshooting document, :doc:`Time Range Queries Do Not Return Some or All of the Data </troubleshooting/time-zone>`.


DESC SCHEMA shows that I am using many materialized views (MVs) when I know I only added Secondary Indexes (SI). Why are there MVs in my schema?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As SI is built ontop of MV, you can expect to see MV in your schema. There is nothing wrong with your system. More information on `Global Secondary Indexes </using-scylla/secondary-indexes/>`_.


Disk Space
-----------

Dropping a table does not reduce storage used by Scylla, how can I clean the disk from dropped tables?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
scylla.yaml includes an ``auto_snapshot`` parameter; when true (it is by default), Scylla creates a snapshot for a table just before dropping it, as a safety measure.
You can find the snapshot in the ``snapshots`` directory, under the table SSTable. For example, for dropped table ``users`` in keyspace ``mykeyspace``:

:code:`/var/lib/scylla/data/mykeyspace/users-bdba4e60f6d511e7a2ab000000000000/snapshots/1515678531438-users`


As the snapshot take the same space as the dropped table, disk usage will remain the same.
You can clean snapshots by using `nodetool clearsnapshot </operating-scylla/nodetool-commands/clearsnapshot>`_. Read more on :doc:`snapshot and snapshotclean </operating-scylla/procedures/backup-restore/delete_snapshot/>`
  
Features
--------
Will Scylla have a certain feature in an upcoming release?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Check the `Roadmap <http://www.scylladb.com/technology/status/>`_ page for features scheduled for our GA release.

I want to try out new features.  How do I enable experimental mode?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You need to add the line :code:`experimental: true`  to your :code:`scylla.yaml` file.

1. Launch the file in a text editor: :code:`$ vi /etc/scylla/scylla.yaml`. (Alternately, on docker, it's :code:`$ docker exec -it your_node vi /etc/scylla/scylla.yaml`);
2. Add the line :code:`experimental: true`;
3. Save the file and exit.
4. Stop and restart the node. 

   On RedHat Enterprise Linux, CentOS or Ubuntu:
   
   :code:`$ sudo systemctl restart scylla-server`
   
   On Docker:  
   
   :code:`$ docker stop <your_node> && docker start <your_node>`

   Alternately, starting from Scylla 2.0, you can start Scylla for Docker with the :code:`experimental` flag as follows:

   :code:`$ docker run --name <your_node> -d scylladb/scylla --experimental 1`

You should now be able to use the experimental features available in your version of Scylla.

How do I check the current version of Scylla that I am running?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* On a regular system or VM (running Ubuntu, CentOS, or RedHat Enterprise): :code:`$ scylla --version`

Check the `Operating System Support Guide </kb/os-support/>`_ for a list of supported operating systems and versions.

* On a docker node: :code:`$ docker exec -it Node_Z scylla --version`


Is Scylla Apache Cassandra compatible? Does API / interface X compatible?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Check the `Cassandra Compatibility <http://www.scylladb.com/technology/status/#cassandra-compatibility>`_ section for compatibility matrix.

Which version(s) of Apache Cassandra is Scylla compatible with? Will Scylla be compatible with future Cassandra versions?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Check the `Cassandra Compatibility <http://www.scylladb.com/technology/status/#cassandra-compatibility>`_ section for current and future Apache Cassandra release compatibility.

We plan to support the 2.2 series features and 3.0 as well, including materialized views.

Beyond 3.0, we will look at the features and see if they make sense for Scylla, but the general plan is to keep compatibility.

We plan to introduce extensions and enhancements. We’ll try to work with the Apache Cassandra community on new features. So that we don’t fragment the ecosystem, and will support switching back and forth between the two implementations while using the same drivers and application code.

I am upgrading my nodes to a version that uses a newer SSTable format, when will the nodes start using the new SSTable format?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :doc:`new "mc" SSTable format</architecture/sstable/sstable3/index>` is supported in Scylla 3.0 and later.
Scylla only starts using the newer format when every node in the cluster is capable to generate it.
Therefore, only when all nodes in the cluster are upgraded the new format is used.

Ubuntu
------

.. _faq-check-update-kernel:

Check and update Ubuntu 14.04 kernel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Running Scylla on Ubuntu 14.04 requires kernel 3.15 or later

* To check your kernel version: :code:`$ uname -a`
* If your kernel is older than 3.15 then:

  * Check for available kernels: :code:`$ sudo apt-cache search linux-image`
  * Install: :code:`$ sudo apt-get install linux-image-your_version_choice`, for example *linux-image-3.16.0*
  * restart: :code:`$ sudo reboot now`

Installation
------------
Can I install Scylla on an Apache Cassandra server?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Scylla comes with its own version of the Apache Cassandra client tools, in the package :code:`scylla-tools`. Trying to install it on a server with Cassandra already installed may result in something like:

.. code-block:: console

   Unpacking scylla-tools (1.0.1-20160411.b9fe89b-ubuntu1) ...
   dpkg: error processing archive /var/cache/apt/archives/scylla-tools_1.0.1-20160411.b9fe89b-ubuntu1_all.deb (--unpack):
   trying to overwrite '/usr/bin/nodetool', which is also in package cassandra 2.1.4

We recommend uninstalling Apache Cassandra before installing :code:`scylla-tools`.

Which snitch or replication strategy should I use?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you are creating a production cluster or if your cluster is going to have more than one data center you need to use a **DC-aware** snitch, e.g. :code:`GossipingPropertyFileSnitch` or :code:`Ec2MutliRegionSnitch`. You will also need to use a **DC-aware** replication strategy, e.g. :code:`NetworkTopologyStrategy`.

However, if you are going to create your first cluster or want to try something simple, if your cluster is going to have a single data center then you may use a :code:`SimpleSnitch` and then use a :code:`SimpleStrategy` for your keyspaces.

Our general recommendation is to always use a :code:`NetworkTopologyStrategy` and use :code:`Ec2XXX` snitches on AWS based clusters and :code:`GossipingPropertyFileSnitch` in all other cases.

A description of all snitch options we support may be found here: `Snitches <https://github.com/scylladb/scylla/wiki/Snitches>`_.

Note: trying to mix a :code:`SimpleSnitch` with a :code:`DC-aware strategy` or a :code:`DC-aware snitch` with a :code:`SimpleStrategy` may cause your cluster not to work as intended therefore we **strongly discourage** these types of configurations in general.

Not using a proper snitch-strategy combination may cause different types of errors.

For instance:

.. code-block:: console

   Unavailable: code=1000 [Unavailable exception] message="Cannot achieve consistency level for cl LOCAL_ONE. Requires 1, alive 0" info={'required_replicas': 1, 'alive_replicas': 0, 'consistency': 'LOCAL_ONE'}

While all Nodes are alive and are shown in a :code:`nodetool status` report.

If you see this error you should always check that you are not using a :code:`SimpleSnitch` in your cluster configuration in conjunction with some :code:`DC-aware replication strategy` for a keyspace of a table you are failing to query.

When working with ``GossipingPropertyFileSnitch`` or ``Ec2MutliRegionSnitch`` you should edit the ``cassandra-rackdc.properties``

For node using ``GossipingPropertyFileSnitch``, the file should look like the following:

.. code-block:: cql

   dc=asia_datacenter
   rack=rack1
   prefer_local= true

When the node is the Asia data center, on rack1 and to minimize BW usage
for inter-datacenter, use the prefer_local

For ``Ec2MultiRegion`` the file should include the following information

.. code-block:: cql
   
   dc_suffix=my_dc

This will create a suffix for the node location for example:

.. code-block:: cql

   us-east1_my_dc


The problem may also arise if you are using some :code:`DC-aware snitch`, e.g. :code:`Ec2MultiRegionSnitch`, and a :code:`SimpleStrategy` in a multi-DC cluster.

Please, make sure that both a snitch and a replication strategy of a keyspace are either both of a :code:`Simple` kind or both are :code:`DC-aware`.

After that, if you are using a :code:`DC-aware` configuration, make sure that the replication strategy uses the proper data centers names. Verify the data centers names in your cluster using a :code:`nodetool status` command.

Can I change the replication factor (a keyspace) on a live cluster?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes, but it will require running a full repair (or cleanup) to change the replica count of existing data:

- :ref:`Alter <alter-keyspace-statement>` the replication factor for desired keyspace (using cqlsh for instance).
- If you're reducing the replication factor, run ``nodetool cleanup`` on the cluster to remove surplus replicated data.
  Cleanup runs on a per-node basis.
- If you're increasing the replication factor, run ``nodetool repair -pr`` on all the nodes in the cluster one node at a time to ensure data is replicated according to the new
  configuration. Repair runs on a per-replica set basis. This is an intensive process that may result in adverse cluster
  performance. It's highly recommended to do rolling repairs, as an attempt to repair the entire cluster at once will
  most likely swamp it. 

Why can't I set ``listen_address`` to listen to 0.0.0.0 (all my addresses)?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Scylla is a gossip-based distributed system and ``listen_address`` is the address a node tells other nodes to reach
it at. Telling other nodes "contact me on any of my addresses" is a bad idea; if different nodes in the cluster pick
different addresses for you, Bad Things happen.

If you don't want to manually specify an IP to ``listen_address`` for each node in your cluster (understandable!), leave
it blank and Scylla will use ``InetAddress.getLocalHost()`` to pick an address. Then it's up to you or your ops team
to make things resolve correctly (``/etc/hosts/``, dns, etc).

What is the best scenario to add a node to a multi availability zone (AZ)?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If using three node cluster, with RF=3, each node located on a different availability zone (AZ).

For example:

.. code-block:: shell

   Datacenter: DC1
   Status=Up/Down
   State=Normal/Leaving/Joining/Moving
   --  Address        Load       Tokens  Owns (effective)                         Host ID         Rack
   UN  192.168.1.201  118.82 KB  256     33.6%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   A1
   UN  192.168.1.202  111.82 KB  256     33.1%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   B1
   UN  192.168.1.203  114.82 KB  256     33.3%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   C1

All nodes holds 100% of the data.
If needed to add a single node to the cluster (scale out), the cluster will become imbalance.
Because the single additional node will split the tokens only with the existing node in the same AZ.

.. Note:: 

   This is only an example, if having more nodes or different RF the number of nodes may be different.


The token distribution will be:

.. code-block:: shell

   AZ A1 node A: 100% of the data
   AZ B1 node B: 100% of the data
   AZ C1 node C: 50% of the data
   AZ C1 node D: 50% of the data

The solution is to add a node in each AZ.

.. code-block:: shell

   Datacenter: DC1
   Status=Up/Down
   State=Normal/Leaving/Joining/Moving
   --  Address        Load       Tokens  Owns (effective)                         Host ID         Rack
   UN  192.168.1.201  118.82 KB  256     16.6%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   A1
   UN  192.168.1.202  111.82 KB  256     16.1%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   B1
   UN  192.168.1.203  114.82 KB  256     16.3%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   C1
   UN  192.168.1.204  118.82 KB  256     16.6%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   A1
   UN  192.168.1.205  111.82 KB  256     16.1%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   B1
   UN  192.168.1.206  114.82 KB  256     16.3%             8d5ed9f4-7764-4dbd-bad8-43fddce94b7c   C1

More info
---------
Where can I ask a question not covered here?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Two mailing lists.

* `scylladb-dev <https://groups.google.com/d/forum/scylladb-dev>`_: Discuss the development of Scylla itself.
* `scylladb-users <https://groups.google.com/d/forum/scylladb-users>`_: Discuss using Scylla and developing client applications.

I delete data from Scylla, but disk usage stays the same. What gives?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Data you write to Scylla gets persisted to SSTables. Since SSTables are immutable, the data can't actually be removed
when you perform a delete, instead, a marker (also called a "tombstone") is written to indicate the value's new status.
Never fear though, on the first compaction that occurs between the data and the tombstone, the data will be expunged
completely and the corresponding disk space recovered. 

What are seeds?
^^^^^^^^^^^^^^^

Seeds are used during startup to discover the cluster.

If you configure your nodes to refer some node as seed, nodes in your ring tend to send Gossip message to seeds more
often than to non-seeds. In other words, seeds are worked as hubs of
Gossip network. With seeds, each node can detect status changes of other nodes quickly.

Seeds are also referred by new nodes on bootstrap to learn about other nodes in the ring. When you add a new node to ring, you
need to specify at least one live seed to contact. Once a node joins the ring, it learns about the other nodes so it doesn't need seed on subsequent boot.

You can make a seed a node at any time. There is nothing special about seed nodes. If you list the node in seed list it
is a seed

Seeds do not auto bootstrap (i.e. if a node has itself in its seed list it will not automatically transfer data to itself)
If you want a node to do that, bootstrap it first and then add it to seeds later. If you have no data (new install) you
do not have to worry about bootstrap at all.

Recommended usage of seeds:

- Pick two (or more) nodes per data center as seed nodes.
- Sync the seed list to all your nodes

Does single seed mean single point of failure?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ring can operate or boot without a seed; however, you will not be able to add new nodes to the cluster. It is recommended to configure multiple seeds in production systems.

Is RAID0 required for Scylla? Why?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

No, it is not required, but it is highly recommended when using Scylla with more than one drive. Scylla requires one drive for its data file and one drive for commit log (can be the same). If you want to take advantage of more than one drive, the easiest way to do so is set RAID0 (striped) across all of them. If you choose, scylla_setup will setup RAID0 for you on your selected drive, as well as XFS file system (recommended). Similarly, Scylla AMI on EC2 will mount automatically all available SSD drive in on RAID0 for you.

Should I use RAID for replications, such as RAID1, RAID4 or higher?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can, but it is not recommended. Scylla :doc:`clustering architecture </architecture/ringarchitecture/index/>` already provides data replication across nodes and DCs. Adding another layer of replication in each node is redundant, slow down IO operation and reduce available storage. Want a higher level of replication? Increase the Replication Factor (RF) of :doc:`relevant Keyspaces </getting-started/ddl/>`.

Can I use JBOD and not use RAID0?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:term:`JBOD` is not supported by Scylla.

:abbr:`JBOD (Just a Bunch Of Disks)` may be a reasonable solution for Cassandra because it rebuilds nodes very slowly. As this is not an issue for Scylla, it's more efficient to use RAID. 

Explanation: There are two types of deployment when multiple disks exist. In the JBOD case, each disk is an isolated filesystem. I/O isn't stripped and thus performance can be slower than that of RAID. In addition, as the free space isn't shared, a single disk can be full while the others are available.

The benefit of JBOD vs RAID is that it isolates failures to individual disk and not the entire node.
However, Scylla rebuilds nodes quickly and thus it is not an issue when rebuilding an entire node.

As a result, it is much more advantageous to use RAID with Scylla


Is ``Nodetool Repair`` a Local (One Node) Operation or a Global (Full Cluster) Operation?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When running :doc:`nodetool repair </operating-scylla/nodetool-commands/repair/>` on a node, it performs a repair on every token range this node owns; this will also repair other nodes that share the same range.

If you wish to repair the entire cluster, it is recommended to run ``nodetool repair -pr`` on each node in the cluster, sequentially, or use the :doc:`Scylla Manager </operating-scylla/manager/index/>`.

in-memory tables
----------------

Is MV and SI supported for use with in-memory tables? If so, how will it affect the total memory size limitation?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can make MV table an in-memory, as you would with every other table. It effects the total memory size allocation just like any other table. Make sure before you create any kind of in-memory table that its use case warrants the creation. 
 
Can Scylla Enterprise in-memory tables be used without having a mirror file on disk?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
No. In Scylla Enterprise 2018.1.7, in-memory tables are always persistent using an on-disk mirror file.

What happens if we apply an ``ALTER`` CQL command to change a table from/to in memory?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It goes in and out of in-memory, as expected. This is `documented </using-scylla/in-memory/#change-a-table-to-an-in-memory-table>`_ in the Scylla Docs. 

Can I change the coredump mount point? 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yes, by edit ``sysctl.d``.
 
Procedure

1. Create ``/etc/sysctl.d/99-scylla-coredump.conf`` (this file exists by default in Scylla AMI).

2. Open the ``99-scylla-coredump.conf`` file.

3. Add the following line ``kernel.core_pattern=|/<path>/<coredump_directory> %p %u %g %s %t %e"``

For example:

.. code-block:: shell

   kernel.core_pattern=|/home/centos/core/ %p %u %g %s %t %e"

4. Run ``sysctl -p /etc/sysctl.d/99-scylla-coredump.conf`` 

Do I need to run a tool like ``upgradesstables`` when moving to a new format?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unlike Apache Cassandra, Scylla does not ship with upgradesstables, a tool that converts SSTables to newer formats. When upgrading to a new table format, Scylla can still continue to read from the old format. Having this option, ensures a smoother transition and upgrade. New writes use the new format and reads will use both formats until the old tables are removed. If you want to purge all of the old SSTables in a single step, generate a compaction with :doc:`nodetool compact </operating-scylla/nodetool-commands/compact/>` follow by :doc:`nodetool cleanup </operating-scylla/nodetool-commands/cleanup/>` to remove no longer needed token ranges that belong to that node.
 


Copyright
^^^^^^^^^
.. include:: /rst_include/apache-copyrights-index.rst

.. include:: /rst_include/apache-copyrights-index-all-attributes.rst
