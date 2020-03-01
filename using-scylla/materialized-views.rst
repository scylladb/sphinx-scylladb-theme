=========================
Scylla Materialized Views
=========================

Materialized Views is available as a production ready feature in Scylla Open Source 3.0. and Scylla Enterprise 2019.1. In prior versions of Scylla Open Source, Materialized Views was available as an experimental feature.

Occasionally, the same information record needs to be queried based on more than one key.  For example, when:

* user data includes ``name`` and ``ID`` fields, and needs to be queried once by ``name`` and once by ``ID``;

* you need to determine scores, and select the aggregated top scores from within different time ranges.

In Scylla, data is divided into partitions which can be looked up via a partition key. Sometimes the application needs to find a partition or partitions by the value of another column. Doing this efficiently requires indexing. You may also need to index an alternative clustering key.

Prior to the introduction of materialized views, the only way to implement this was using denormalization - creating two entirely separate tables and synchronizing them from within an application. However, ensuring any level of consistency between the data in two or more views this way can require duplicated code along with complex and slow application logic.

Scylla’s materialized views feature, moves this complexity out of the application and into the servers.  With fewer round trips to the applications, this implementation is faster and more reliable.

With materialized views, Scylla automates the process of maintaining separate tables to support different queries of the same data, and allows for fast lookups of data in each view using the standard read path.

A **materialized view** is a global index. It is effectively a new table, populated by a query running against the base table.  You cannot update a materialized view directly;  to update it, you must update the base table.

Each materialized view is a set of rows which corresponds to rows which are present in the underlying, or base, table specified in the materialized view’s ``SELECT`` statement.

Enable MV as an Experimental Feature (Scylla 2.x only)
------------------------------------------------------
To enable experimental features in Scylla, add the line ``experimental: true`` to ``scylla.yaml``. Stop and restart the node. You can also start a docker node using the ``-experimental 1`` option. 

Example
.......

Given the following ‘base’ table:

.. code-block:: cql

	CREATE TABLE buildings (
	    name text,
	    city text,
	    built int,
	    meters int,
	    PRIMARY KEY (name)
	);

Scylla can automatically maintain a materialized view table. In the following example, we want to search by city, but show all fields in the original table.

``city`` is the partition key, but since there can be more than building in each city, we must add ``name`` as the clustering key, so that ``(city, name)`` becomes the primary key:

.. code-block:: cql

	CREATE MATERIALIZED VIEW building_by_city AS
	 	SELECT * FROM buildings
		WHERE city IS NOT NULL
	 	PRIMARY KEY(city, name);

A materialized view may itself be queried just like any other table:

.. code-block:: cql

	SELECT * from building_by_city;

or

.. code-block:: cql

	SELECT name, built, meters from building_by_city LIMIT 1;

A second materialized view can be made by selecting only the primary key and ``meters`` field from the base table:

.. code-block:: cql

	CREATE MATERIALIZED VIEW building_by_city2 AS
	 	SELECT meters FROM buildings
	 	WHERE city IS NOT NULL 
	 	PRIMARY KEY(city, name);

Note that, although each materialized view is a separate table, a user cannot modify a view directly:

.. code-block:: shell
	
	cqlsh:mykeyspace> DELETE FROM building_by_city WHERE city='Taipei';

	InvalidRequest: code=2200 [Invalid query] message="Cannot directly modify a materialized view"

To modify views, remember that you must instead modify the base table associated with the view.

For more examples and current constraints, read the original blog_ on materialized views in Scylla.

.. _blog: http://www.scylladb.com/2017/07/27/materialized-views-preview-scylla-2-0/
