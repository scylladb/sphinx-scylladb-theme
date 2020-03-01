
===============
Scylla Counters
===============

Counters are useful for any application where you need to increment a count,  such as keeping track of:

* the number of web page views on a website;
* the number of apps/updates downloaded;
* the number of clicks on an ad or pixel;
* the number of points earned in a game;

A **counter** is a special data type (column) that only allows its value to be incremented, decremented, read or deleted.  As a type, counters are a 64-bit signed integer. Updates to counters are atomic, making them perfect for counting. 

Counters are created when a table is created, for example:

.. code-block:: shell

	cqlsh:mykeyspace> CREATE TABLE cf (pk int PRIMARY KEY, my_counter counter);
	cqlsh:mykeyspace> UPDATE cf SET my_counter = my_counter + 6 WHERE pk = 0;
	cqlsh:mykeyspace> SELECT * FROM cf;

	pk | my_counter
	---+-------------
	0  | 6

Counters are updated when the update command is run:

.. code-block:: shell

	(1 rows)
	cqlsh:mykeyspace> UPDATE cf SET my_counter = my_counter - 1 WHERE pk = 0;
	cqlsh:mykeyspace> SELECT * FROM cf;

	pk | my_counter
	---+-----------
	0  | 5

However, counters have limitations not present in other column types:

* A table cannot contain both counter and regular columns. This safeguards correct handling of counter and non-counter updates by not allowing them in the same operation.
* All non-counters columns in the table must be part of the primary key.
* Counter columns, on the other hand, may not be part of the primary key.
* A table that contains counters (outside of the primary key) may only contain counters.
* Counters may not be indexed.
* Counters may not be part of a materialized view.
* One cannot use TIMESTAMP or set a TTL (time to live) when updating a counter.
* Once deleted, counter column values cannot be used again.
* Counters cannot be set to a specific value, other than when using the UPDATE command at initialization.
* Updates are not idempotent. In the case of a write failure, the client cannot safely retry the request. 


Example:
........

Create a table. The table can only contain the primary key and the counter column(s):

.. code-block:: shell

	cqlsh:mykeyspace> CREATE TABLE cf (pk int PRIMARY KEY, my_counter counter);

Increment the count:

.. code-block:: shell

	cqlsh:mykeyspace> UPDATE cf SET my_counter = my_counter + 3 WHERE pk = 0;
	cqlsh:mykeyspace> SELECT * FROM cf;

	pk | my_counter
	---+-------------
	0  | 3

Decrement the count:

.. code-block:: shell

	cqlsh:mykeyspace> UPDATE cf SET my_counter = my_counter - 1 WHERE pk = 0;
	cqlsh:mykeyspace> SELECT * FROM cf;

	pk | my_counter
	---+-----------
	0  | 2


Delete the row:

.. code-block:: shell

	cqlsh:mykeyspace> delete from cf where pk = 0;
	cqlsh:mykeyspace> select * from cf;

	pk | my_counter
	---+-----------
    
Read our blog_ on counters, or see the data type description_.

.. _blog: http://www.scylladb.com/2017/04/04/counters/

.. _description: /getting-started/types/#counters/
