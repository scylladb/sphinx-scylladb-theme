``--host <node IP>``

Specifies the hostname or IP of the node that will be used to discover other nodes belonging to the cluster.
Note that this will be persisted and used every time Scylla Manager starts. You can use either an IPv4 or IPv6 address.

=====

``-n, --name <alias>``

When a cluster is added, it is assigned a unique identifier.
Use this parameter to identify the cluster by an alias name which is more meaningful.
This alias name can be used with all commands that accept ``-c, --cluster`` parameter.

=====

``--auth-token <token>``

Specifies the `auththentication token <../install-agent/#generate-an-authentication-token>`_ you identified in ``/etc/scylla-manager-agent/scylla-manager-agent.yaml``

=====

``--without-repair`` 

When cluster is added, Manager schedules repair to repeat every 7 days. To create a cluster without a scheduled repair, use this flag.


