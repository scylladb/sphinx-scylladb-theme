Large Partitions Hunting
========================

.. contents::
   :local:
   :depth: 2


This document describes how to catch a huge partition.

What Should Make You Want To Start Looking For A Huge Partition?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Any of the following:

* Latencies on a single shard become very long (look at the "Scylla Overview Metrics" dashboard)
* Huge allocations warning messages in the log:

.. code-block:: none

   seastar_memory - oversized allocation: 2842624 bytes, please report

  
* SSTable are bigger than expected (look at the `data` directory of the corresponding column family)

What To Do When You Suspect You May Have A Huge Partition?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1) For each table you suspect run:

.. code-block:: console

    nodetool flush <keyspace name> <table name>
    nodetool cfstats <keyspace name>.<table name> | grep "Compacted partition maximum bytes"


For example:

.. code-block:: console

    nodetool cfstats demodb.tmcr | grep "Compacted partition maximum bytes"

                    Compacted partition maximum bytes: 1188716932

If you detect a table with a huge partition there is a way to drill down even further starting from scylla 2.3 using :doc:`large partition table </troubleshooting/large_partition_table/>`

.. include:: /troubleshooting/_common/ts-return.rst
