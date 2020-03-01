
.. highlight:: cql

Data Manipulation
-----------------

.. include:: /rst_include/cql-version-index.rst

This section describes the statements supported by CQL to insert, update, delete and query data.

:ref:`SELECT <select-statement>`

.. _select:

:ref:`INSERT <insert-statement>`

.. _insert:

:ref:`UPDATE <update-statement>`

.. _update:

:ref:`DELETE <delete_statement>`

.. _delete:

:ref:`BATCH <batch_statement>`

.. _batch:


.. _select-statement:

SELECT
^^^^^^

Querying data from data is done using a ``SELECT`` statement:

.. productionlist::
   select_statement: SELECT [ DISTINCT ] ( `select_clause` | '*' )
                   : FROM `table_name`
                   : [ WHERE `where_clause` ]
                   : [ ORDER BY `ordering_clause` ]
                   : [ PER PARTITION LIMIT (`integer` | `bind_marker`) ]
                   : [ LIMIT (`integer` | `bind_marker`) ]
                   : [ ALLOW FILTERING ]
                   : [ BYPASS CACHE ]
   select_clause: `selector` [ AS `identifier` ] ( ',' `selector` [ AS `identifier` ] )
   selector: `column_name`
           : | `term`
           : | CAST '(' `selector` AS `cql_type` ')'
           : | `function_name` '(' [ `selector` ( ',' `selector` )* ] ')'
           : | COUNT '(' '*' ')'
   where_clause: `relation` ( AND `relation` )*
   relation: `column_name` `operator` `term`
           : '(' `column_name` ( ',' `column_name` )* ')' `operator` `tuple_literal`
           : TOKEN '(' `column_name` ( ',' `column_name` )* ')' `operator` `term`
   operator: '=' | '<' | '>' | '<=' | '>=' | '!=' | IN | CONTAINS | CONTAINS KEY
   ordering_clause: `column_name` [ ASC | DESC ] ( ',' `column_name` [ ASC | DESC ] )*

For instance::

    SELECT name, occupation FROM users WHERE userid IN (199, 200, 207);
    SELECT name AS user_name, occupation AS user_occupation FROM users;

    SELECT time, value
    FROM events
    WHERE event_type = 'myEvent'
      AND time > '2011-02-03'
      AND time <= '2012-01-01'

    SELECT COUNT (*) AS user_count FROM users;

The ``SELECT`` statement reads one or more columns for one or more rows in a table. It returns a result-set of the rows
matching the request, where each row contains the values for the selection corresponding to the query. Additionally,
functions including aggregation ones can be applied to the result.

A ``SELECT`` statement contains at least a :ref:`selection clause <selection-clause>` and the name of the table on which
the selection is on (note that CQL does **not** joins or sub-queries and thus a select statement only apply to a single
table). In most case, a select will also have a :ref:`where clause <where-clause>` and it can optionally have additional
clauses to :ref:`order <ordering-clause>` or :ref:`limit <limit-clause>` the results. Lastly, :ref:`queries that require
filtering <allow-filtering>` can be allowed if the ``ALLOW FILTERING`` flag is provided.

.. _selection-clause:

Selection clause
~~~~~~~~~~~~~~~~

The :token:`select_clause` determines which columns needs to be queried and returned in the result-set, as well as any
transformation to apply to this result before returning. It consists of a comma-separated list of *selectors* or,
alternatively, of the wildcard character (``*``) to select all the columns defined in the table.

Selectors
`````````

A :token:`selector` can be one of:

- A column name of the table selected, to retrieve the values for that column.
- A term, which is usually used nested inside other selectors like functions (if a term is selected directly, then the
  corresponding column of the result-set will simply have the value of this term for every row returned).
- A casting, which allows you to convert a nested selector to a (compatible) type.
- A function call, where the arguments are selector themselves.

Aliases
```````

Every *top-level* selector can also be aliased (using `AS`). If so, the name of the corresponding column in the result
set will be that of the alias. For instance::

    // Without alias
    SELECT intAsBlob(4) FROM t;

    //  intAsBlob(4)
    // --------------
    //  0x00000004

    // With alias
    SELECT intAsBlob(4) AS four FROM t;

    //  four
    // ------------
    //  0x00000004

.. note:: Currently, aliases aren't recognized anywhere else in the statement where they are used (not in the ``WHERE``
   clause, not in the ``ORDER BY`` clause, ...). You must use the orignal column name instead.


``WRITETIME`` and ``TTL`` function
```````````````````````````````````

Selection supports two special functions (which aren't allowed anywhere else): ``WRITETIME`` and ``TTL``. Both functions
take only one argument and that argument *must* be a column name (so, for instance, ``TTL(3)`` is invalid).

Those functions let you retrieve meta-information that is stored internally for each column, namely:

- the timestamp of the value of the column for ``WRITETIME``.
- the remaining time to live (in seconds) for the value of the column if it set to expire (and ``null`` otherwise).

.. _where-clause:

The ``WHERE`` clause
~~~~~~~~~~~~~~~~~~~~

The ``WHERE`` clause specifies which rows must be queried. It is composed of relations on the columns that are part of
the ``PRIMARY KEY``.

Not all relations are allowed in a query. For instance, non-equal relations (where ``IN`` is considered as an equal
relation) on a partition key are not supported (see the use of the ``TOKEN`` method below to do non-equal queries on
the partition key). Moreover, for a given partition key, the clustering columns induce an ordering of rows and relations
on them restricted to the relations that let you select a **contiguous** (for the ordering) set of rows. For
instance, given::

    CREATE TABLE posts (
        userid text,
        blog_title text,
        posted_at timestamp,
        entry_title text,
        content text,
        category int,
        PRIMARY KEY (userid, blog_title, posted_at)
    )

The following query is allowed::

    SELECT entry_title, content FROM posts
     WHERE userid = 'john doe'
       AND blog_title='John''s Blog'
       AND posted_at >= '2012-01-01' AND posted_at < '2012-01-31'

But the following query is not, as it does not select a contiguous set of rows (and we suppose no secondary indexes are
set)::

    // Needs a blog_title to be set to select ranges of posted_at
    SELECT entry_title, content FROM posts
     WHERE userid = 'john doe'
       AND posted_at >= '2012-01-01' AND posted_at < '2012-01-31'

When specifying relations, the ``TOKEN`` function can be used on the ``PARTITION KEY`` column to query. In that case,
rows will be selected based on the token of their ``PARTITION_KEY`` rather than on the value. Note that the token of a
key depends on the partitioner in use, and that in particular the RandomPartitioner won't yield a meaningful order. Also
note that ordering partitioners always orders token values by bytes (so even if the partition key is of type int,
``token(-1) > token(0)`` in particular). For example::

    SELECT * FROM posts
     WHERE token(userid) > token('tom') AND token(userid) < token('bob')

Moreover, the ``IN`` relation is only allowed on the last column of the partition key and on the last column of the full
primary key.

It is also possible to “group” ``CLUSTERING COLUMNS`` together in a relation using the tuple notation. For instance::

    SELECT * FROM posts
     WHERE userid = 'john doe'
       AND (blog_title, posted_at) > ('John''s Blog', '2012-01-01')

will request all rows that sort after the one having “John's Blog” as ``blog_title`` and '2012-01-01' for ``posted_at``
in the clustering order. In particular, rows having a ``post_at <= '2012-01-01'`` will be returned as long as their
``blog_title > 'John''s Blog'``, which would not be the case for::

    SELECT * FROM posts
     WHERE userid = 'john doe'
       AND blog_title > 'John''s Blog'
       AND posted_at > '2012-01-01'

The tuple notation may also be used for ``IN`` clauses on clustering columns::

    SELECT * FROM posts
     WHERE userid = 'john doe'
       AND (blog_title, posted_at) IN (('John''s Blog', '2012-01-01'), ('Extreme Chess', '2014-06-01'))

The ``CONTAINS`` operator may only be used on collection columns (lists, sets, and maps). In the case of maps,
``CONTAINS`` applies to the map values. The ``CONTAINS KEY`` operator may only be used on map columns and applies to the
map keys.

.. _group-by-clause:

Grouping results
~~~~~~~~~~~~~~~~~

.. versionadded:: 3.2 Scylla Open Source

The ``GROUP BY`` option lets you condense into a single row all selected rows that share the same values for a set of columns. 
Using the ``GROUP BY`` option, it is only possible to group rows at the partition key level or at a clustering column level. 
The ``GROUP BY`` arguments must form a prefix of the primary key. 

For example, if the primary key is ``(p1, p2, c1, c2)``, then the following queries are valid::

    GROUP BY p1
    GROUP BY p1, p2
    GROUP BY p1, p2, c1
    GROUP BY p1, p2, c1, c2

The following should be considered when using the ``GROUP BY`` option:

* If a primary key column is restricted by an equality restriction, it is not required to be present in the ``GROUP BY`` clause. 

* Aggregate functions will produce a separate value for each group. 

* If no ``GROUP BY`` clause is specified, aggregate functions will produce a single value for all the rows.

* If a column is selected without an aggregate function, in a statement with a ``GROUP BY``, the first value encounter in each group will be returned.


.. _ordering-clause:

Ordering results
~~~~~~~~~~~~~~~~

The ``ORDER BY`` clause lets you select the order of the returned results. It takes as argument a list of column names
along with the order for the column (``ASC`` for ascendant and ``DESC`` for descendant, omitting the order being
equivalent to ``ASC``). Currently the possible orderings are limited by the :ref:`clustering order <clustering-order>`
defined on the table:

- if the table has been defined without any specific ``CLUSTERING ORDER``, then then allowed orderings are the order
  induced by the clustering columns and the reverse of that one.
- otherwise, the orderings allowed are the order of the ``CLUSTERING ORDER`` option and the reversed one.

.. _limit-clause:

Limiting results
~~~~~~~~~~~~~~~~

.. versionchanged::  3.1 Scylla Open Source

The ``LIMIT`` option to a ``SELECT`` statement limits the number of rows returned by a query, while the ``PER PARTITION
LIMIT``  option (introduced in Scylla 3.1) limits the number of rows returned for a given partition by the query. Note that both types of limit can
used in the same statement.

.. _allow-filtering:

Allowing filtering
~~~~~~~~~~~~~~~~~~

By default, CQL only allows select queries that don't involve “filtering” server side, i.e. queries where we know that
all (live) record read will be returned (maybe partly) in the result set. The reasoning is that those “non filtering”
queries have predictable performance in the sense that they will execute in a time that is proportional to the amount of
data **returned** by the query (which can be controlled through ``LIMIT``).

The ``ALLOW FILTERING`` option lets you explicitly allow (some) queries that require filtering. Please note that a
query using ``ALLOW FILTERING`` may thus have unpredictable performance (for the definition above), i.e. even a query
that selects a handful of records **may** exhibit performance that depends on the total amount of data stored in the
cluster.

For instance, consider the following table holding user profiles with their year of birth (with a secondary index on
it) and country of residence::

    CREATE TABLE users (
        username text PRIMARY KEY,
        firstname text,
        lastname text,
        birth_year int,
        country text
    )

    CREATE INDEX ON users(birth_year);

Then the following queries are valid::

    SELECT * FROM users;
    SELECT * FROM users WHERE birth_year = 1981;

because in both cases, Scylla guarantees that these queries' performance will be proportional to the amount of data
returned. In particular, if no users were born in 1981, then the second query performance will not depend on the number
of user profiles stored in the database (not directly at least: due to secondary index implementation consideration, this
query may still depend on the number of nodes in the cluster, which indirectly depends on the amount of data stored.
Nevertheless, the number of nodes will always be multiple order of magnitude lower than the number of user profile
stored). Of course, both queries may return very large result sets in practice, but the amount of data returned can always
be controlled by adding a ``LIMIT``.

However, the following query will be rejected::

    SELECT * FROM users WHERE birth_year = 1981 AND country = 'FR';

because Scylla cannot guarantee that it won't have to scan large amount of data even if the result to those query is
small. Typically, it will scan all the index entries for users born in 1981 even if only a handful are actually from
France. However, if you “know what you are doing”, you can force the execution of this query by using ``ALLOW
FILTERING`` and so the following query is valid::

    SELECT * FROM users WHERE birth_year = 1981 AND country = 'FR' ALLOW FILTERING;

Bypass Cache
~~~~~~~~~~~~~~~~~~

.. versionadded:: Scylla Enterprise 2019.1.1
.. versionadded:: Scylla 3.1
                  

The ``BYPASS CACHE`` clause on SELECT statements informs the database that the data being read is unlikely to be read again in the near future, and also was unlikely to have been read in the near past; therefore no attempt should be made to read it from the cache or to populate the cache with the data. This is mostly useful for range scans; these typically process large amounts of data with no temporal locality and do not benefit from the cache.
The clause is placed immediately after the optional ALLOW FILTERING clause.

``BYPASS CACHE`` is a Scylla CQL extension and not part of Apache Cassandra CQL.

For example::
  
  SELECT * FROM users BYPASS CACHE;
  SELECT name, occupation FROM users WHERE userid IN (199, 200, 207) BYPASS CACHE;
  SELECT * FROM users WHERE birth_year = 1981 AND country = 'FR' ALLOW FILTERING BYPASS CACHE;
  
LIKE Operator
~~~~~~~~~~~~~

.. versionadded:: 3.2 Scylla Open Source

The ``LIKE`` operation on ``SELECT`` statements informs Scylla that you are looking for a pattern match. The expression ‘column LIKE pattern’ yields true only if the entire column value matches the pattern.   
 
The search pattern is a string of characters with two wildcards, as shown:

* ``_`` matches any single character
* ``%`` matches any substring (including an empty string)
* ``\`` escapes the next pattern character, so it matches verbatim
* any other pattern character matches itself
* an empty pattern matches empty text fields
 
 
.. note:: Only string types (ascii, text, and varchar) are valid for matching

Currently, the match is **case sensitive**. The entire column value must match the pattern. 
For example consider the search pattern 'M%n' - this will match ``Martin``, but will not match ``Moonbeam`` because the ``m`` at the end isn't matched. In addition, ``moon`` is not matched because ``M`` is not the same as ``m``. Both the pattern and the column value are assumed to be UTF-8 encoded.
 
A query can find all values containing some text fragment by matching to an appropriate ``LIKE`` pattern.

**Example A**
 
In this example, ``LIKE`` specifies that the match is looking for a word that starts with the letter ``S``. The ``%`` after the letter ``S`` matches any text to the end of the field. 

.. code-block:: none

   SELECT * FROM pet_owners WHERE firstname LIKE ‘S%’ ALLOW FILTERING;
   ╭──────────┬─────────────────────┬────────────────╮
   │ID        │LastName             │FirstName       │
   ├──────────┼─────────────────────┼────────────────┤
   │1         │Adams                │Steven          │
   ├──────────┼─────────────────────┼────────────────┤
   │15        │Erg                  │Sylvia          │
   ├──────────┼─────────────────────┼────────────────┤
   │20        │Goldberg             │Stephanie       │
   ├──────────┼─────────────────────┼────────────────┤
   │25        │Harris               │Stephanie       │
   ├──────────┼─────────────────────┼────────────────┤
   │88        │Rosenberg            │Samuel          │
   ├──────────┼─────────────────────┼────────────────┤
   │98        │Smith                │Sara            │
   ├──────────┼─────────────────────┼────────────────┤
   │115       │Williams             │Susan           │
   ├──────────┼─────────────────────┼────────────────┤
   │130       │Young                │Stuart          │
   ╰──────────┴─────────────────────┴────────────────╯




**Example B**

In this example, you are searching for all pet owners whose last name contains the characters 'erg'.

.. code-block:: none

   SELECT * FROM pet_owners WHERE lastname LIKE ‘%erg%’ ALLOW FILTERING;

   ╭──────────┬─────────────────────┬────────────────╮
   │ID        │LastName             │FirstName       │
   ├──────────┼─────────────────────┼────────────────┤
   │11        │Berger               │David           │
   ├──────────┼─────────────────────┼────────────────┤
   │18        │Gerg                 │Lawrence        │
   ├──────────┼─────────────────────┼────────────────┤
   │20        │Goldberg             │Stephanie       │
   ├──────────┼─────────────────────┼────────────────┤
   │88        │Rosenberg            │Samuel          │
   ├──────────┼─────────────────────┼────────────────┤
   │91        │Schulberg            │Barry           │
   ├──────────┼─────────────────────┼────────────────┤
   │110       │Weinberg             │Stuart          │
   ╰──────────┴─────────────────────┴────────────────╯

Note that this query does not return: 

.. code-block:: none

   ╭──────────┬─────────────────────┬────────────────╮
   │ID        │LastName             │FirstName       │
   ├──────────┼─────────────────────┼────────────────┤
   │15        │Erg                  │Sylvia          │
   ╰──────────┴─────────────────────┴────────────────╯

As it is case sensitive. 


**Example C**

This table contains some commonly used ``LIKE`` filters and the matches you can expect the filter to return.

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Filter
     - Matches
   * - %abe%
     - Babel, aberration, cabernet, scarabees
   * - _0\%
     - 10%, 20%, 50%
   * - a%t
     - asphalt, adapt, at

.. _insert-statement:

INSERT
^^^^^^

Inserting data for a row is done using an ``INSERT`` statement:

.. code-block:: cql

   insert_statement ::=  INSERT INTO table_name ( names_values | json_clause )
                         [ IF NOT EXISTS ]
                         [ USING update_parameter ( AND update_parameter )* ];

Where:

.. code-block:: cql

   names_values::= `names` VALUES `tuple_literal`
   json_clause ::=  JSON string [ DEFAULT ( NULL | UNSET ) ]
   names::= '(' `column_name` ( ',' `column_name` )* ')'
   update_parameter::= ( TIMESTAMP | TTL ) ( `integer` | `bind_marker` )

For example:

.. code-block:: cql

    INSERT INTO NerdMovies (movie, director, main_actor, year)
          VALUES ('Serenity', 'Joss Whedon', 'Nathan Fillion', 2005)
          USING TTL 86400 IF NOT EXISTS;

The ``INSERT`` statement writes one or more columns for a given row in a table. Note that since a row is identified by
its ``PRIMARY KEY``, at least the columns composing it must be specified. The list of columns to insert to must be
supplied when using the ``VALUES`` syntax.

Note that unlike in SQL, ``INSERT`` does not check the prior existence of the row by default: the row is created if none
existed before, and updated otherwise. Furthermore, there is no means to know which of creation or update happened.

All updates for an ``INSERT`` are applied atomically and in isolation.

Please refer to the :ref:`UPDATE <update-parameters>` section for information on the :token:`update_parameter`.

Also note that ``INSERT`` does not support counters, while ``UPDATE`` does.


.. note:: New in Scylla Open Source 3.2, you can use the ``IF NOT EXISTS`` condition with the ``INSERT`` statement. When this is used, the insert is only made if the row does not exist prior to the insertion.  Using ``IF NOT EXISTS`` incurs a non negligible performance cost (internally, as Paxos will be used), so use ``IF NOT EXISTS`` wisely.


Starting with Scylla Open Source 3.2 if `enabled </getting-started/ddl/#cdc-options>`_ on a table, you can use UPDATE, INSERT, and DELETE statements with Change Data Capture (CDC) tables. Note that this feature is `experimental </operating-scylla/scylla-yaml/#enabling-experimental-features>`_  in version 3.2. 

.. to-do - add link to cdc doc

.. _update-statement:

UPDATE
^^^^^^

Updating a row is done using an ``UPDATE`` statement:

.. code-block:: cql

   update_statement: UPDATE `table_name`
                   : [ USING `update_parameter` ( AND `update_parameter` )* ]
                   : SET `assignment` ( ',' `assignment` )*
                   : WHERE `where_clause`
                   : [ IF ( EXISTS | `condition` ( AND `condition` )*) ]

   update_parameter: ( TIMESTAMP | TTL ) ( `integer` | `bind_marker` )

   assignment: `simple_selection` '=' `term`
             :| `column_name` '=' `column_name` ( '+' | '-' ) `term`
             :| `column_name` '=' `list_literal` '+' `column_name`

   simple_selection: `column_name`
                   :| `column_name` '[' `term` ']'
                   :| `column_name` '.' `field_name

   condition: `simple_selection` `operator` `term`

For instance::

    UPDATE NerdMovies USING TTL 400
       SET director   = 'Joss Whedon',
           main_actor = 'Nathan Fillion',
           year       = 2005
     WHERE movie = 'Serenity';

    UPDATE UserActions
       SET total = total + 2
       WHERE user = B70DE1D0-9908-4AE3-BE34-5573E5B09F14
         AND action = 'click';

The ``UPDATE`` statement writes one or more columns for a given row in a table. The :token:`where_clause` is used to
select the row to update and must include all columns composing the ``PRIMARY KEY``. Non primary key columns are then
set using the ``SET`` keyword.

Note that unlike in SQL, ``UPDATE`` does not check the prior existence of the row by default, 

(except through IF_, see below): 

the row is created if none existed before, and updated otherwise. Furthermore, there is no way to know
whether a creation or update occurred.

In an ``UPDATE`` statement, all updates within the same partition key are applied atomically and in isolation.

Regarding the :token:`assignment`:

- ``c = c + 3`` is used to increment/decrement counters. The column name after the '=' sign **must** be the same as
  the one before the '=' sign. Note that increment/decrement is only allowed on counters, and are the *only* update
  operations allowed on counters. See the section on :ref:`counters <counters>` for details.
- ``id = id + <some-collection>`` and ``id[value1] = value2`` are for collections, see the :ref:`relevant section
  <collections>` for details.
- ``id.field = 3`` is for setting the value of a field on a non-frozen user-defined types. 

.. _IF:

IF condition
~~~~~~~~~~~~

.. versionadded:: 3.2 Scylla Open Source

It is, however, possible to use the conditions on some columns through ``IF``, in which case the row will not be updated
unless the conditions are met. But, please note that using ``IF`` conditions will incur a non-negligible performance
cost (internally, Paxos will be used) so this should be used sparingly.


.. _update-parameters:

Update parameters
~~~~~~~~~~~~~~~~~

The ``UPDATE``, ``INSERT`` (and ``DELETE`` and ``BATCH`` for the ``TIMESTAMP``) statements support the following
parameters:

- ``TIMESTAMP``: sets the timestamp for the operation. If not specified, the coordinator will use the current time (in
  microseconds) at the start of statement execution as the timestamp. This is usually a suitable default.
- ``TTL``: specifies an optional Time To Live (in seconds) for the inserted values. If set, the inserted values are
  automatically removed from the database after the specified time. Note that the TTL concerns the inserted values, not
  the columns themselves. This means that any subsequent update of the column will also reset the TTL (to whatever TTL
  is specified in that update). By default, values never expire. A TTL of 0 is equivalent to no TTL. If the table has a
  default_time_to_live, a TTL of 0 will remove the TTL for the inserted or updated values. A TTL of ``null`` is equivalent
  to inserting with a TTL of 0.

.. _delete_statement:

DELETE
^^^^^^

Deleting rows or parts of rows uses the ``DELETE`` statement:

.. code-block:: cql

   delete_statement: DELETE [ `simple_selection` ( ',' `simple_selection` ) ]
                   : FROM `table_name`
                   : [ USING `update_parameter` ( AND `update_parameter` )* ]
                   : WHERE `where_clause`
                   : [ IF ( EXISTS | `condition` ( AND `condition` )*) ]

For instance::

    DELETE FROM NerdMovies USING TIMESTAMP 1240003134
     WHERE movie = 'Serenity';

    DELETE phone FROM Users
     WHERE userid IN (C73DE1D3-AF08-40F3-B124-3FF3E5109F22, B70DE1D0-9908-4AE3-BE34-5573E5B09F14);

The ``DELETE`` statement deletes columns and rows. If column names are provided directly after the ``DELETE`` keyword,
only those columns are deleted from the row indicated by the ``WHERE`` clause. Otherwise, whole rows are removed.

The ``WHERE`` clause specifies which rows are to be deleted. Multiple rows may be deleted with one statement by using an
``IN`` operator. A range of rows may be deleted using an inequality operator (such as ``>=``).

``DELETE`` supports the ``TIMESTAMP`` option with the same semantics as in :ref:`updates <update-parameters>`.

In a ``DELETE`` statement, all deletions within the same partition key are applied atomically and in isolation.

A ``DELETE`` operation can be conditional through the use of an ``IF`` clause, similar to ``UPDATE`` and ``INSERT``
statements. However, as with ``INSERT`` and ``UPDATE`` statements, this will incur a non-negligible performance cost
(internally, Paxos will be used) and so should be used sparingly.


Range deletions
~~~~~~~~~~~~~~~

Range deletions allow you to delete rows from a single partition given that the clustering key is within the given range. The delete request can be determined on both ends or it can be open-ended.


Open range deletions
~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 3.2 Scylla Open Source 

Open range deletions delete rows based on an open-ended request (>, <, >=, =<, etc.)

For example, suppose your data set for events at Madison Square Garden includes:


.. code-block:: none

   CREATE KEYSPACE mykeyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}  AND durable_writes = true;
   use mykeyspace ;
   CREATE TABLE events ( id text, created_at date, content text, PRIMARY KEY (id, created_at) );
   
   INSERT into events (id, created_at, content) VALUES ('concert', '2019-11-19', 'SuperM');
   INSERT into events (id, created_at, content) VALUES ('concert', '2019-11-15', 'Billy Joel');
   INSERT into events (id, created_at, content) VALUES ('game', '2019-11-03', 'Knicks v Sacramento');
   INSERT into events (id, created_at, content) VALUES ('concert', '2019-10-31', 'Dead & Company');
   INSERT into events (id, created_at, content) VALUES ('game', '2019-10-28', 'Knicks v Chicago');
   INSERT into events (id, created_at, content) VALUES ('concert', '2019-10-25', 'Billy Joel');


   SELECT * from events;

    id      | created_at | content
   ---------+------------+---------------------
       game | 2019-10-28 |    Knicks v Chicago
       game | 2019-11-03 | Knicks v Sacramento
    concert | 2019-10-25 |          Billy Joel
    concert | 2019-10-31 |      Dead & Company
    concert | 2019-11-15 |          Billy Joel
    concert | 2019-11-19 |              SuperM

   (6 rows)

And you wanted to delete all of the concerts from the month of October using an open-ended range delete. You would run:

.. code-block:: none
  
   DELETE FROM events WHERE id='concert' AND created_at <= '2019-10-31';

   SELECT * from events;

    id      | created_at | content
   ---------+------------+---------------------
       game | 2019-10-28 |    Knicks v Chicago
       game | 2019-11-03 | Knicks v Sacramento
    concert | 2019-11-15 |          Billy Joel
    concert | 2019-11-19 |              SuperM

   (4 rows)

.. _batch_statement:

BATCH
^^^^^

Multiple ``INSERT``, ``UPDATE`` and ``DELETE`` can be executed in a single statement by grouping them through a
``BATCH`` statement:

.. code-block:: cql

   batch_statement: BEGIN [ UNLOGGED | COUNTER ] BATCH
                   : [ USING `update_parameter` ( AND `update_parameter` )* ]
                   : `modification_statement` ( ';' `modification_statement` )*
                   : APPLY BATCH
   
   modification_statement: `insert_statement` | `update_statement` | `delete_statement`

For instance::

    BEGIN BATCH
       INSERT INTO users (userid, password, name) VALUES ('user2', 'ch@ngem3b', 'second user');
       UPDATE users SET password = 'ps22dhds' WHERE userid = 'user3';
       INSERT INTO users (userid, password) VALUES ('user4', 'ch@ngem3c');
       DELETE name FROM users WHERE userid = 'user1';
    APPLY BATCH;

The ``BATCH`` statement group multiple modification statements (insertions/updates and deletions) into a single
statement. It serves several purposes:

- It saves network round-trips between the client and the server (and sometimes between the server coordinator and the
  replicas) when batching multiple updates.
- All updates in a ``BATCH`` belonging to a given partition key are performed in isolation.
- By default, all operations in the batch are performed as *logged*, to ensure all mutations eventually complete (or
  none will). See the notes on :ref:`UNLOGGED batches <unlogged-batches>` for more details.

Note that:

- ``BATCH`` statements may only contain ``UPDATE``, ``INSERT`` and ``DELETE`` statements (not other batches for instance).
- Batches are *not* a full analogue for SQL transactions.
- If a timestamp is not specified for each operation, then all operations will be applied with the same timestamp
  (either one generated automatically, or the timestamp provided at the batch level). Due to Scylla's conflict
  resolution procedure in the case of `timestamp ties <http://wiki.apache.org/cassandra/FAQ#clocktie>`__, operations may
  be applied in an order that is different from the order they are listed in the ``BATCH`` statement. To force a
  particular operation ordering, you must specify per-operation timestamps.
- A LOGGED batch to a single partition will be converted to an UNLOGGED batch as an optimization.

.. _unlogged-batches:

``UNLOGGED`` batches
~~~~~~~~~~~~~~~~~~~~

By default, Scylla uses a batch log to ensure all operations in a batch eventually complete or none will (note
however that operations are only isolated within a single partition).

There is a performance penalty for batch atomicity when a batch spans multiple partitions. If you do not want to incur
this penalty, you can tell Scylla to skip the batchlog with the ``UNLOGGED`` option. If the ``UNLOGGED`` option is
used, a failed batch might leave the patch only partly applied.

``COUNTER`` batches
~~~~~~~~~~~~~~~~~~~

Use the ``COUNTER`` option for batched counter updates. Unlike other
updates in Scylla, counter updates are not idempotent.


:doc:`Apache Cassandra Query Language </getting-started/cql/>`

Copyright
^^^^^^^^^

.. include:: /rst_include/apache-copyrights-index.rst

.. include:: /rst_include/apache-copyrights-index-all-attributes.rst


.. Licensed to the Apache Software Foundation (ASF) under one
.. or more contributor license agreements.  See the NOTICE file
.. distributed with this work for additional information
.. regarding copyright ownership.  The ASF licenses this file
.. to you under the Apache License, Version 2.0 (the
.. "License"); you may not use this file except in compliance
.. with the License.  You may obtain a copy of the License at
..
..     http://www.apache.org/licenses/LICENSE-2.0
..
.. Unless required by applicable law or agreed to in writing, software
.. distributed under the License is distributed on an "AS IS" BASIS,
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. See the License for the specific language governing permissions and
.. limitations under the License.

