Tracing
-------

.. contents::
   :local:
   :depth: 2


Tracing is a ScyllaDB tool meant to help debugging and analyzing internal flows in the server.  There are three types of tracing you can use with Scylla:

* **User Defined CQL query** - One example of such a flow is CQL request processing. By placing a flag inside a CQL query you can start tracing.
* **Probalistic Tracing** randomly chooses a request to be traced with some defined probability.
* **Slow Query Logging** - records queries with handling time above the specified threshold.

.. note:: If you're planning to use either **probabilistic tracing** or **slow query logging** (see below), it's advisable to change the ``replication_factor`` of the  ``system_traces`` keyspace to ``ALL``. 


User Defined CQL Query Tracing 
..............................

Enabling
^^^^^^^^

While inside a ``cqlsh`` prompt you can enable tracing for this session with the command ``TRACING ON|OFF``.

.. raw:: html
	
	<div class="row">
		<script src="https://gist.github.com/Jammink2/fdfbd8e190db0e493f72c0de913d259b.js"></script>
	</div>

**NOTE:** ``source_elapsed`` starts over on ``127.0.0.1`` when execution gets there.

Viewing
^^^^^^^
The raw tracing data can be queried as below (scroll to view):

.. raw:: html
	
	<div class="row">
    	<script type="text/javascript" src="https://gist.github.com/Jammink2/16685281cfb11a845bd1941093f108dd.js"></script>
    </div>

Storing
^^^^^^^

Traces from ``cqlsh`` are stored in the ``system_traces`` keyspace for 24 hours. This setting cannot be changed. 

Probabilistic Tracing
.....................

Tracing implies a significant performance penalty on a cluster when enabled. Therefore, if tracing is required for some ongoing workload, it is undesirable to enable it for every request but rather for some (small) portion of requests. This can be done using  **probabilistic tracing**, which randomly chooses a request to be traced with some defined probability.

Enabling
^^^^^^^^
If you want to trace 0.01% of all queries in the cluster, you can set a probabilistic tracing with the probability ``0.0001``:

.. code-block:: console

   nodetool settraceprobability 0.0001

Viewing	
^^^^^^^

If we need trace points for a specific session, we can query the ``events`` table for a given session's id. For example:

 .. code-block:: cql

   SELECT * from system_traces.sessions where session_id = 141ab010-d994-11e7-899e-000000000002;

Storing 
^^^^^^^
Traces are stored in the ``system_traces`` keyspace for 24 hours. This setting cannot be changed. The keyspace consists of two tables with a replication factor of 2:

* ``sessions`` table contains a single row for each tracing session.
* ``events`` table contains a single row for each trace point.

Traces are created in the context of a **tracing session**. For instance, if we trace an ``INSERT`` CQL command, a tracing session with a unique ID (``session_id`` column in the tables mentioned above) will be created and all trace points hit during its execution will be stored in a context of this session.  This defines the format in which tracing data is stored.

``sessions`` table column descriptions
======================================

* ``session_id``: ID of this tracing session.
* ``command``: currently, this can only have a *QUERY* value.
* ``client``:  address of the client that sent this query.
* ``coordinator``: address of the coordinator node that received this query from the client.
* ``duration``:  the total duration of this tracing session.
* ``parameters``: this map contains string pairs that describe the query. This may include *query string* or *consistency level*.
* ``request``: a short string describing the current query, like "Execute CQL3 query".
* ``request_size``: size of the request (available from Scylla 3.0).
* ``response_size``: size of the response (available from Scylla 3.0).
* ``started_at``: a timestamp taken when the tracing session has begun.

``events`` table column descriptions
====================================

* ``session_id``: ID of this tracing session.
* ``event_id``: ID of this specific trace entry.
* ``activity``: a trace message.
* ``source``: address of a node where the trace entry has been created.
* ``scylla_parent_id``: ID of a parent span.
* ``scylla_span_id``: the ID of a span that sent an RPC that created the current span.
* ``source_elapsed``: a number of microseconds passed since the beginning of the tracing session on a specific node (see examples above).
* ``thread``: currently this contains a number of the shard on which this trace point has been taken.
    
Slow Query Logging
..................

Often in real life installations, one of the most important parameters of the system is the longest response time. Naturally, the shorter it is, the better. Therefore, capturing a request that takes a long time and understanding why it took it so long is a very critical and challenging task.

**Slow query logging** will greatly ease debugging related to long requests. When enabled, it records queries with handling time above the specified threshold. As a result, there will be a new record created in ``system_traces.node_slow_log`` table. All tracing records created in the context of the current query on a coordinator node will also be written. In addition, if handling on a given replica takes too long, traces will be stored.

Enabling and configuring
^^^^^^^^^^^^^^^^^^^^^^^^

Slow query logging is disabled by default. A REST API allows configuring and querying the configuration of the feature. 

To set the parameters, run:

.. code-block:: console

   curl -X POST --header "Content-Type: application/json" --header "Accept: application/json" "http://<Node's address>:10000/storage_service/slow_query?enable=<true|false>&ttl=<in seconds>&threshold=<threshold in microseconds>"

For example, to disable the feature on a node with the address ``127.0.0.1``, set the ``ttl`` to ``8600`` and the threshold to ``10000``:

.. code-block:: console

   curl -X POST --header "Content-Type: application/json" --header "Accept: application/json" "http://127.0.0.1:10000/storage_service/slow_query?enable=false&ttl=8600&threshold=10000"

To get the current configuration, run:

.. code-block:: console

   curl -X GET --header "Content-Type: application/json" --header "Accept: application/json" "http://<Node's address>:10000/storage_service/slow_query"

After the ``POST`` command above, the query and result will look as below:

.. code-block:: console

   curl -X GET --header "Content-Type: application/json" --header "Accept: application/json" "http://127.0.0.1:10000/storage_service/slow_query"
   {"threshold": 10000, "enable": false, "ttl": 8600}

Viewing
^^^^^^^

Two time series helper tables were introduced that will help simplify the querying of traces.

``sessions_time_idx`` is for querying regular traces. Another table, the ``node_slow_log_time_idx`` table, is for querying slow query records.

``sessions_time_idx`` and ``node_slow_log_time`` table column descriptions
==========================================================================

* ``minute``: the minute, from epoch time, from when the record was taken.
* ``started_at``: a timestamp taken when the tracing session has begun.
* ``session_id``: the corresponding tracing session ID.
* ``start_time``: time when the query was initiated.
* ``node_ip``: address of a coordinator node.
* ``shard``: shard ID on a coordinator, where the query has been handled.

With these tables, one may get the relevant traces using a query like the one below:

.. code-block:: cql

   SELECT * from system_traces.sessions_time_idx where minutes in ('2016-09-07 16:56:00-0700') and started_at > '2016-09-07 16:56:30-0700';

Storing 
^^^^^^^

Slow query logging results are stored in the ``node_slow_log`` table for 24 hours. This setting cannot be changed.

``node_slow_log`` table column descriptions
===========================================

* ``start_time`` and ``date``: time when the query was initiated.
* ``node_ip``: address of a coordinator node.
* ``shard``: shard ID on a coordinator, where the query has been handled.
* ``command``: the query command, e.g. ``select * from my_ks.my_cf``.
* ``duration``: the duration query handling in microseconds.
* ``parameters``: query parameters like a parameters column in a ``system_traces.sessions`` table.
* ``session_id``: the corresponding tracing session ID.
* ``source ip``: address of the client that sent this query.
* ``table_names``: a list of tables used for this query, where applicable.
* ``username``: a user name used for authentication with this query.

Large Partition Tracing
.......................

When we use `Slow Query Logging`_ trying to identify the source of high latencies due to heavy queueing, we have to deal with the problem of “collateral damage”. 
All requests are going to have a long latency because their latency will consist of the queue latency and their handling latency. 
Therefore all of them are likely going to hit the Slow Query threshold and get logged.

If queueing is caused by some particularly heavy request, we would like to be able to filter this request from those that got logged due to a long queueing. 
We have recently added tools that would help us do that:

New columns were added to `system_traces.sessions`_ (available from Scylla 3.0)

* ``request_size``
* ``response_size``

.. _`Slow Query Logging`: #slow-query-logging

.. _`system_traces.sessions`: #sessions-table-column-descriptions

Catching a Hot Partition
........................

After we started storing EXECUTE parameters in the ``system_traces.sessions`` we can now perform certain analytics tasks given a probabilistic traces recording, for instance, we can detect operations on hot partitions.

If we want to check if we have a hot partition then we can record a slice of a workload using probabilistic tracing.

For example:

.. code-block:: cql

  nodetool settraceprobability 0.01

Analyze the key distribution - get all entries from ``system_traces.sessions``.

For example:

.. code-block:: cql

   SELECT * FROM system_traces.sessions

Count how many queries of the type you are looking for (SELECT, INSERT, DROP, etc.) with the same key you used.
Compare it to the total amount of requests of the corresponding type and make your conclusion.
