* Make sure that all the ports_ are open.

* Obtain the IP addresses of all nodes which have been created for the cluster.

* Select a unique name as ``cluster_name`` for the cluster (identical for all the nodes in the cluster).

* Decide which nodes will be the seed nodes (It is recommended to define more than one node as a seed node).

* Choose which snitch_ to use (identical for all the nodes in the cluster). For a production system, it is recommended to use a DC-aware snitch, which can support a ``NetworkTopologyStrategy`` replication-strategy_ for your Keyspaces.


.. _ports: /operating-scylla/admin/#networking
.. _snitch: /faq/#which-snitch-or-replication-strategy-should-i-use
.. _replication-strategy: /getting-started/ddl/#create-keyspace-statement
