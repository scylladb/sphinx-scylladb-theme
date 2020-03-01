``--host <node IP>``

Specifies the hostname or IP of the node that will be used to discover other nodes belonging to the cluster.
Note that this will be persisted and used every time Scylla Manager starts.

=====

``-n, --name <alias>``

When a cluster is added, it is assigned a unique identifier.
Use this parameter to identify the cluster by an alias name which is more meaningful.
This alias name can be used with all commands that accept ``-c, --cluster`` parameter.

=====

``--ssh-identity-file <path to private key>``

Specifies the SSH private key to use for Scylla Manager server to connect to Scylla nodes.

=====

``--ssh-user <username>``

Specifies the SSH username which will be used to connect to the cluster nodes.
The SSH user defined here needs to be the owner of the SSH private key which is set with the ``--ssh-identity-file <string>`` property.
