Scylla Features
===============


.. toctree::
   :maxdepth: 2
   :hidden:
   
   Workload Prioritization </using-scylla/workload-prioritization/>
   In-memory tables </using-scylla/in-memory/>
   Global Secondary Indexes </using-scylla/secondary-indexes/>
   Local Secondary Indexes </using-scylla/local-secondary-indexes/>
   Materialized Views </using-scylla/materialized-views/>
   Counters </using-scylla/counters/>

.. raw:: html

   <div class="panel callout radius animated">
            <div class="row">
              <div class="medium-3 columns">
                <h5 id="getting-started">Scylla Open Source Features</h5>
              </div>
              <div class="medium-9 columns">

The following are **new features** for Scylla Open Source 3.2.x 

* `IPv6 </operating-scylla/scylla-yaml/#ipv6-addresses>`_ support for client-to-node, node-to-node, Manager to node, and Monitor to node communication - Scylla now supports IPv6 Global Scope Addresses for all IPs: seeds, listen_address, broadcast_address etc. This functionality is available for Scylla Manager in Scylla Manager 2.0 and in Scylla Monitor in 3.0.
* `Like Operator </getting-started/dml/#like-operator>`_ - when used on ``SELECT`` statements informs Scylla that you are looking for a pattern match. The expression ‘column LIKE pattern’ yields true only if the entire column value matches the pattern.
* `Group Results </getting-started/dml/#grouping-results>`_ - using the CQL ``GROUP BY`` option you can condense into a single row all selected rows that share the same values for a set of columns. 
* `Non-Frozen UDTs </getting-started/types/#user-defined-types>`_ - User Defined Types that are not in a collection do not have to be frozen. UDTs in a collection must be frozen. 
* `Auto-expanding Replication Factor </getting-started/ddl/#auto-expand-replication-factor>`_ -  allows you to set a single replication factor for all Data Centers, including all existing Data Centers.
* `Light Weight Transactions </getting-started/dml/#if-condition>`_ - Allows you to create and manipulate data according to a specified condition This feature is available as **Technical Preview**..

The following are **new features** for Scylla Open Source 3.1.x

* `CQL Per Partition Limit </getting-started/dml/#limiting-results>`_ - This new per partition limit further allows you to set the number of partitions returned as a result. You can mix both row limits and per partition limits in the same CQL statement.
* :doc:`Local Secondary Indexes </using-scylla/local-secondary-indexes/>` - More efficient Secondary Index searches when the base table and index share the same partition key. 
* `BYPASS CACHE </getting-started/dml/#bypass-cache>`_ - This CQL command introduced in Scylla Enterprise 2019.1.1, now available in open source, informs the database that the data being read is unlikely to be read again in the near future, and also was unlikely to have been read in the near past; therefore no attempt should be made to read it from the cache or to populate the cache with the data. 
* `Large Cell / Collection Detector </troubleshooting/large_rows_large_cells_tables/>`_ - Makes finding large partitions easier.
* `Nodetool toppartitions </operating-scylla/nodetool-commands/toppartitions/>`_ - Samples cluster writes and reads and reports the most active partitions in a specified table and time frame.
* Row-level Repair - `nodetool repair </operating-scylla/nodetool-commands/repair/>`_ operation now uses `row-level repair <https://www.scylladb.com/2019/08/13/scylla-open-source-3-1-efficiently-maintaining-consistency-with-row-level-repair/>`_, adding additional granularity with repairs. 
* ``ALLOW FILTERING`` `CQL Command </getting-started/dml/#allowing-filtering>`_ that allows for server side data filtering that is not based on the primary key. Introduced in 3.0, this feature was further enhanced in version 3.1.

The following are **new features** for Scylla Open Source 3.0.x

* :doc:`Scylla Materialized Views </using-scylla/materialized-views/>` - An alternate view table for finding a partition by the value of another column. Experimental in prior versions, this feature was made production ready in Scylla Open Source 3.0.
* :doc:`Global Secondary Indexes </using-scylla/secondary-indexes/>` - A mechanism for allowing efficient searches on non-partition keys using Materialized Views. Experimental in prior versions, this feature was made production ready in Scylla Open Source 3.0.
* `Hinted Handoff </architecture/anti-entropy/hinted-handoff/#scylla-hinted-handoff>`_ - ensures availability and consistency
* `SSTable 3.0 </architecture/sstable/sstable3>`_ - new SSTable format
* ``ALLOW FILTERING`` `CQL Command </getting-started/dml/#allowing-filtering>`_ that allows for server side data filtering that is not based on the primary key. 

More information in the `Release Notes <https://www.scylladb.com/product/release-notes/>`_.



.. raw:: html

   </div>
   </div>
   </div>


.. raw:: html

   <div class="panel callout radius animated">
            <div class="row">
              <div class="medium-3 columns">
                <h5 id="getting-started">Scylla Enterprise 2019.1 Features</h5>
              </div>
              <div class="medium-9 columns">

The following are **new features** for Scylla Scylla Enterprise 2019.1.x:

* `Incremental Compaction Strategy </kb/compaction/#incremental-compaction-strategy-ics>`_ - (version 2019.1.4) - significantly lowers SA (size amplification) for workloads which run STCS and should be used instead of STCS.
* `IPv6 </operating-scylla/scylla-yaml/#ipv6-addresses>`_ (version 2019.1.4) support for client-to-node, node-to-node, Manager to node, and Monitoring to node communication - Scylla now supports IPv6 Global Scope Addresses for all IPs: seeds, listen_address, broadcast_address etc. This functionality is available for Scylla Manager in Scylla Manager 2.0.
* :doc:`Workload Prioritization </using-scylla/workload-prioritization/>` - Grant a level of service to roles in your organization. 
* :doc:`Scylla Materialized Views </using-scylla/materialized-views/>` - An alternate view table for finding a partition by the value of another column.
* :doc:`Global Secondary Indexes </using-scylla/secondary-indexes/>` - A mechanism for allowing efficient searches on non-partition keys using Materialized Views.
* :doc:`Local Secondary Indexes </using-scylla/local-secondary-indexes/>` - More efficient Secondary Index searches when the base table and index share the same partition key. Scylla 3.1 and later.
* ``ALLOW FILTERING`` `CQL Command </getting-started/dml/#allowing-filtering>`_ that allows for server side data filtering that is not based on the primary key.
* `Hinted Handoff </architecture/anti-entropy/hinted-handoff/#scylla-hinted-handoff>`_ - ensures availability and consistency
* `SSTable 3.0 </architecture/sstable/sstable3>`_ - new SSTable format
* `Full (multi-partition) <https://www.scylladb.com/2018/11/01/more-efficient-range-scan-paging-with-scylla-3-0/>`_ blog describing improvements for fulll scans.
* `Role Based Access Control (RBAC) </operating-scylla/security/rbac_usecase>`_ - compatible with Apache Cassandra 3.x using CQL commands to `grant roles </operating-scylla/security/authorization/#grant-authorization-cql-reference>`_ to users in an organization. 
* `GoogleCloudSnitch </operating-scylla/system-configuration/snitch/#googlecloudsnitch>`_- optimized for use with GCE instances
* `Large Partitions Support <https://www.scylladb.com/2018/09/11/large-partitions-support-scylla-2-3/>`_ - Scylla supports large partitions. 
* `Encryption at Rest </operating-scylla/security/encryption-at-rest/>`_ - protects your data persisted in storage or backup.
* `BYPASS CACHE </getting-started/dml/#bypass-cache>`_ - This CQL command informs the database that the data being read is unlikely to be read again in the near future, and also was unlikely to have been read in the near past; therefore no attempt should be made to read it from the cache or to populate the cache with the data. 

Read the `Release Notes <https://www.scylladb.com/product/release-notes/>`_ for more information. 



.. raw:: html

   </div>
   </div>
   </div>

.. raw:: html

   <div class="panel callout radius animated">
            <div class="row">
              <div class="medium-3 columns">
                <h5 id="getting-started">Scylla Enterprise 2018.1 Features</h5>
              </div>
              <div class="medium-9 columns">

The following are **new features** for Scylla Scylla Enterprise 2018.1.x

* :doc:`Scylla Auditing Guide </operating-scylla/security/auditing>` -  allows administrators to know which users performed what action at what time.
* :doc:`Scylla in-memory tables </using-scylla/in-memory/>` - an alternative table type for storing data in RAM.
* :doc:`Scylla Counters </using-scylla/counters/>` - A data type for counting
* `Time Window Compaction Strategy </kb/compaction/#time-window-compaction-strategy-twcs>`_ - a replacement compaction strategy for Date-Tiered Compaction Strategy, refined for time-series data.
* `Heat Weighted Load Balancing <https://www.scylladb.com/2017/09/21/scylla-heat-weighted-load-balancing/>`_ a blog entry which investigates what happens if one of the nodes loses its cache and the solution Heat Weighted Load Balancing.


Read the `Release Notes <https://www.scylladb.com/product/release-notes/>`_ for more information.




.. raw:: html

   </div>
   </div>
   </div>


