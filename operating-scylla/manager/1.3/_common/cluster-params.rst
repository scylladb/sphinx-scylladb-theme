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

=====

.. versionadded:: 1.3.1 Scylla Manager

``--ssl-user-cert-file <path to SSL certificate>``

Specifies the SSL user certificate. This setting is needed only when using client/server encryption with *require_client_auth* enabled.
In such cases, setting it incorrectly results in `status`_ command malfunction. This parameter requires setting ``--ssl-user-key-file <path to SSL certificate key>`` as well. 

=====

.. versionadded:: 1.3.1 Scylla Manager

``--ssl-user-key-file <path to SSL certificate key>``

Specifies the key to the SSL certificate. It's required when setting ``--ssl-user-cert-file`` parameter.
