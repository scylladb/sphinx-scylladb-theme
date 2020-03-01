Nodetool compact
================

.. caution:: It is always best to allow Scylla to automatically run minor compactions using a `compaction strategy </kb/compaction>`_. Using Nodetool to run a compaction can quickly exaust all resources, increase operational costs, and take up valuable disk space. For this reason, major compactions should be avoided and are not reccomended for any production system.  


**compact** ``[<keyspace> <cfnames>...]``- Force a (major) compaction on one or more tables. Compaction is an optimization that reduces the cost of IO and CPU over time by merging rows in the background. By default, major compaction runs on all the ``keyspaces`` and tables. Major compactions will take all the SSTables for a column family and merge them into a single large SSTable. If keyspace is provided, the compaction will run on all the tables in that keyspace. If one or more tables are provided as command-line arguments, the compaction will run on all the tables.

For Example:

.. code-block:: shell

   nodetool compact
   nodetool compact keyspace1
   nodetool compact standard1

See Also
--------

.. include:: nodetool-index.rst

`Compaction Overview </kb/compaction>`_

`CQL compaction Reference </getting-started/compaction/>`_

`How to choose a Compaction Strategy </architecture/compaction/compaction-strategies/>`_

