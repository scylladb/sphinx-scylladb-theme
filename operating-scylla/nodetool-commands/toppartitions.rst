Nodetool toppartitions
======================

.. versionadded:: 3.1

**toppartitions** <keyspace> <table> <duration> - Samples cluster writes and reads and reports the most active partitions in a specified table and time frame.

.. note::

   The command need to be run while there are writes and reads operations.

=========  ============================
Parameter  Description
=========  ============================
keyspace   The keyspace name
---------  ----------------------------
table      The table name
---------  ----------------------------
duration   The duration in milliseconds
=========  ============================

For example:

.. code-block:: shell

   nodetool toppartitions nba team_roster 5000

Example output:

.. code-block:: shell

   WRITES Sampler:
     Cardinality: ~5 (256 capacity)
     Top 10 partitions:
	    Partition                Count       +/-
            Russell Westbrook         100         0
	    Jermi Grant               25          0
	    Victor Oladipo            17          0
	    Andre Roberson            1           0
	    Steven Adams              1           0

   READS Sampler:
     Cardinality: ~5 (256 capacity)
     Top 10 partitions:
	    Partition                Count       +/-
            Russell Westbrook         100         0
	    Victor Oladipo            17          0
	    Jermi Grant               12          0
	    Andre Roberson            5           0
	    Steven Adams              1           0

In this example we can see that for the ``Partition`` with ``Partition Key`` "Russell Westbrook" were done 100 writes and 100 read operations during the set duration.

For each of the samplers (WRITES and READS in this specific example), nodetool toppartitions reports:

* The cardinality of the sampled operations (number of unique operations in the sample set).

* The number of partitions in a specified table that had the most traffic in a specified time period.

=============  =============================================================================================
Parameter      Description
=============  =============================================================================================
Partition      The partition key
-------------  ---------------------------------------------------------------------------------------------
Count          The number of operations of the specified type that occurred during the specified time period
-------------  ---------------------------------------------------------------------------------------------
+/-            The margin of error for the Count statistic
-------------  ---------------------------------------------------------------------------------------------
Write Count    The total number of writes since last boot
-------------  ---------------------------------------------------------------------------------------------
Write Latency  The average read latency
=============  =============================================================================================

To know which node hold the partition key use the nodetool :doc:`getendpoints </operating-scylla/nodetool-commands/getendpoints/>` command.

For example:

.. code-block:: shell

   nodetool getendpoints nba team_roster Russell Westbrook

Example output:

.. code-block:: shell

   10.0.0.72

.. include:: nodetool-index.rst
