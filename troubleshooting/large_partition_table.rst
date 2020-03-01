Scylla Large Partitions Table
=============================

.. versionadded:: 2.3

.. contents::
   :local:
   :depth: 2


This document describes how to work with Scylla's large partitions table.
The large partitions table can be used to trace large partitions in a cluster.
The table is updated every time a partition is written and/or deleted,and includes a compaction process which flushes memtables to SSTables.

Large Partitions can cause any of the following symptoms:

* Longer latencies on a single shard (look at the “Scylla Overview Metrics” dashboard from Scylla Monitor)
* Huge allocations warning messages in the log: ``seastar_memory - oversized allocation: 2842624 bytes, please report``
* SSTable are bigger than expected (look at the data directory of the corresponding column family)

If you are experiencing any of the above, search to see if you have large partitions. 

Viewing - Find Large Partitions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Search for large partitions.

For example:

.. code-block:: console

   SELECT * FROM system.large_partitions;

Example output:

.. code-block:: console

   keyspace_name | table_name | sstable_name                                                                       | partition_size | partition_key                                       | compaction_time
   --------------+------------+------------------------------------------------------------------------------------+----------------+-----------------------------------------------------+--------------------------
          demodb |       tmcr | /var/lib/scylla/data/demodb/tmcr-cba79c008e4f11e8908a000000000001/la-6-big-Data.db |     1188716932 | {key: pk{000400000001}, token:-4069959284402364209} | 2018-07-23 08:10:34
          testdb |       tmcr | /var/lib/scylla/data/demodb/tmcr-cbs45c008e4f11e3418a000871000002/la-7-big-Data.db |     1188816032 | {key: pk{000400000001}, token:-3169959284402457813} | 2018-07-23 08:10:34
  
================================================  =================================================================================
Parameter                                         Description
================================================  =================================================================================
keyspace_name                                     The keyspace name that holdes the large partition
------------------------------------------------  ---------------------------------------------------------------------------------
table_name                                        The table name that holdes the large partition
------------------------------------------------  ---------------------------------------------------------------------------------
sstable_name                                      The SSTable name that holdes the large partition
------------------------------------------------  ---------------------------------------------------------------------------------
partition_size                                    The size of the partition
------------------------------------------------  ---------------------------------------------------------------------------------
partition_key                                     The key that holdes the large partition
------------------------------------------------  ---------------------------------------------------------------------------------
compaction_time                                   Time when compaction occur
================================================  =================================================================================

* Search within all the large partitions for a specific keyspace and or table.
 
For example we are looking for the keyspace ``demodb`` and table ``tmcr``:

.. code-block:: console

   SELECT * FROM system.large_partitions WHERE keyspace_name = 'demodb' AND table_name = 'tmcr;

Example output:

.. code-block:: console

   keyspace_name | table_name | sstable_name                                                                       | partition_size | partition_key                                       | compaction_time
   --------------+------------+------------------------------------------------------------------------------------+----------------+-----------------------------------------------------+--------------------------
          demodb |       tmcr | /var/lib/scylla/data/demodb/tmcr-cba79c008e4f11e8908a000000000001/la-6-big-Data.db |     1188716932 | {key: pk{000400000001}, token:-4069959284402364209} | 2018-07-23 08:10:34



Configure
^^^^^^^^^

Configured the large partitions detection threshold can be set in the scylla.yaml file with the ``compaction_large_partition_warning_threshold_mb`` parameter (default: 100MB). Each partition bigger than this threshold is going to be reported in the large_partitions table and generate a warning in the :doc:`log </getting-started/logging/>`.

For example (set to 500MB):

.. code-block:: console

   compaction_large_partition_warning_threshold_mb: 500


Storing
^^^^^^^

Large partitions are stored in a system table with the following schema:

.. code-block:: console

   DESCRIBE TABLE system.large_partitions;
   
   CREATE TABLE system.large_partitions (
       keyspace_name text,
       table_name text,
       sstable_name text,
       partition_size bigint,
       partition_key text,
       compaction_time timestamp,
       PRIMARY KEY ((keyspace_name, table_name), sstable_name, partition_size, partition_key)
   ) WITH CLUSTERING ORDER BY (sstable_name ASC, partition_size DESC, partition_key ASC)




Expiring Data
^^^^^^^^^^^^^

In order to prevent stale data from appearing, all rows in ``system.large_partitions`` table are inserted with Time To Live (TTL) equal to 30 days.

.. include:: /troubleshooting/_common/ts-return.rst

Additional Resources
^^^^^^^^^^^^^^^^^^^^
` Large Partitions Hunting </troubleshooting/debugging_large_partition/>`_
