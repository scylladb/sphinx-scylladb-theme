===================
Scylla Health Check
===================

Scylla Manager automatically adds a health check task to all new nodes when the cluster is added to Scylla Manager and to all existing nodes during the upgrade procedure.
The health check task ensures that CQL native port is accessible on all the nodes.
For each node, in parallel, Scylla Manager opens a connection to a CQL port and asks for server options.
If there is no response or the response takes longer than 250 milliseconds, the node is considered to be `DOWN` otherwise the node is considered to be `UP`.
The results are available using the `sctool status <../sctool/#status>`_ command.

If you have enabled the Scylla Monitoring stack, Monitoring stack 2.0 Manager dashboard includes the same cluster status report.
In addition, the Prometheus Alert Manager has an alert to report when a Scylla node health check fails and the node is considered `DOWN`.



