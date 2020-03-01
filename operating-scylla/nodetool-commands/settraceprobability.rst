Nodetool settraceprobability
============================

**settraceprobability** -  ``<value>`` - Sets the probability for tracing a request. Value is trace probability between 0 and 1.

This command is useful to determine the cause of intermittent query performance problems by identifying which queries are responsible.
It can trace some or all the queries sent to the cluster, setting the probability to 1.0 will trace everything, set to a lower number will reduce the traced queries.
Use caution when setting the ``settraceprobability`` high, it can affect active systems, as system-wide tracing will have a performance impact.
Trace information is stored under ``system_traces`` keyspace for more information you can read our `CQL tracing in Scylla`_ blog

..  _`CQL tracing in Scylla`: https://www.scylladb.com/2016/08/04/cql-tracing/

For example:

.. code-block:: shell
   
   nodetool settraceprobability 0.1

.. include:: nodetool-index.rst
