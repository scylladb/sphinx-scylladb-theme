===============================
Global Secondary Indexes
===============================

Global Secondary Indexes is available as a production ready feature in Scylla Open Source 3.0. and Scylla Enterprise 2019.1. In prior versions of Scylla Open Source, Secondary Indexes was available as an experimental feature. 

The data model in Scylla partitions data between cluster nodes using a partition key, which is defined in the database schema. This is an efficient way to look up rows because you can find the node hosting the row by hashing the partition key.

However, this also means that finding a row using a non-partition key requires a full table scan which is inefficient.

**Global Secondary indexes** (named "Secondary indexes" for the rest of this doc) are a mechanism in Scylla which allows efficient searches on non-partition keys by creating an index. In effect, they are indexes created on columns other than the primary (partition) key. (Note that you will be able to create an index on clustering key in later versions).

Secondary indexes provide the following advantages:

1. Secondary Indexes are (mostly) transparent to your application. Queries have access to all the columns in the table, and you can add or remove indexes on the fly without changing the application.

2. We can use the value of the indexed column to find the corresponding index table row in the cluster so that reads are scalable.

3. Updates can be more efficient with secondary indexes that materialized views because only changes to the primary key and indexed column cause an update in the index view.

What’s more, the size of an index is proportional to the size of the indexed data. As data in Scylla is distributed to multiple nodes, it’s impractical to store the whole index on a single node, as it limits the size of the index to the capacity of a single node, not the capacity of the whole cluster.

For this reason, secondary indexes in Scylla are **global** rather than local. With global indexing, a materialized view is created is created for each index. This :doc:`materialized view </using-scylla/materialized-views/>` has the indexed column as a partition key and primary key (partition key and clustering keys) of the indexed row as clustering keys.

Secondary indexes created globally provide a further advantage: you can use the value of the indexed column to find the corresponding index table row in the cluster so reads are scalable. Note however, that with this approach, writes are slower than with local indexing because of the overhead required to keep the indexed view up to date.

How Secondary Index Queries Work
................................

Scylla breaks indexed queries into two parts:

1. a query on the index table to retrieve partition keys for the indexed table, and
2. a query to the indexed table using the retrieved partition keys.

.. image:: secondary_index.png

In the example above:

1. The query arrives on node 7, which acts as a coordinator for the query.
2. The node notices the query on an index column and issues a read to index table on node two, which has the index table row for “user@example.com”;
3. This query will return a set of user IDs that are now used to retrieve contents of the indexed table.

Enable Secondary Indexes as an Experimental Feature (Scylla 2.1 and later)
--------------------------------------------------------------------------
To enable experimental features in Scylla, add the line ``experimental: true`` to ``scylla.yaml``. Stop and restart the node. You can also start a docker node using the ``-experimental 1`` option.

Example
.......

Given the following schema:

.. raw:: html
	
	<div class="row">
  	<script type="text/javascript" src="https://gist.github.com/rusher81572/23725c99a6a0f37c27b6f06c93d10937.js"></script>
  </div>

Let’s populate it with some test data:

.. raw:: html
	
	<div class="row">
  	<script type="text/javascript" src="https://gist.githubusercontent.com/rusher81572/e772fefbfd451891fe6ecf31276bb40a.js"></script>
  </div>

Note that if we try to query on a column (the part after the ``WHERE`` clause) in a Scylla table that isn’t part of the primary key, we’ll see that this is not permitted. For example:

.. code-block:: cql

	SELECT * FROM ks.users WHERE email = 'beassebyv@house.gov';

will result in an error.

Secondary indexes are designed to allow efficient querying of non-partition key columns. If we create an index for each of our ``email`` and ``country`` columns by executing the following CQL statements:

.. raw:: html
	
	<div class="row">
  	<script type="text/javascript" src="https://gist.github.com/rusher81572/e42c35f71180007b94b52a44b0bf8e9f.js"></script>
  </div>

We can now query the indexed columns as if they were partition keys:

.. raw:: html
	
	<div class="row">
  	<script type="text/javascript" src="https://gist.github.com/rusher81572/1d6a233e8fa39e7b78ed2fede1a4dd75.js"></script>
  </div>

Note that you can use the ``DESCRIBE`` command to see the whole schema for the ks.users table, including created indexes and views:

.. raw:: html
	
	<div class="row">
  	<script type="text/javascript" src="https://gist.github.com/rusher81572/700bc065dc8014fd97c43461e30320fc.js"></script>
  </div>
