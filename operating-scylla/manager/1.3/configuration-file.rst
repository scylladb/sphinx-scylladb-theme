==================
Configuration file
==================

.. contents::
   :depth: 2
   :local:

Scylla Manager has a single configuration file ``/etc/scylla-manager/scylla-manager.yaml``.
Note that the file will open as read-only unless you edit it as the root user or by using sudo.
Usually there is no need to edit the configuration file.

HTTP/HTTPS server settings
--------------------------

With server settings you may specify if Scylla Manager should be available over HTTP, HTTPS or both.

.. code-block:: yaml

   # Bind REST API to the specified TCP address using HTTP protocol.
   # http: 127.0.0.1:56080

   # Bind REST API to the specified TCP address using HTTPS protocol.
   https: 127.0.0.1:56443

   # TLS certificate file to use for HTTPS.
   tls_cert_file: /var/lib/scylla-manager/scylla_manager.crt

   # TLS key file to use for HTTPS.
   tls_key_file: /var/lib/scylla-manager/scylla_manager.key

Prometheus settings
-------------------

.. code-block:: yaml

   # Bind prometheus API to the specified TCP address using HTTP protocol.
   # By default it binds to all network interfaces but you can restrict it
   # by specifying it like this 127:0.0.1:56090 or any other combination
   # of ip and port.
   prometheus: ':56090'

If changing prometheus IP or port please remember to adjust rules in `prometheus server </operating-scylla/monitoring/monitoring_stack/#procedure>`_.

.. code-block:: yaml

   - targets:
     - IP:56090

Logging settings
----------------

Logging settings specify log output and level.

.. code-block:: yaml

   # Logging configuration.
   logger:
     # Where to output logs, syslog or stderr.
     mode: syslog
     # Available log levels are error, info and debug.
     level: info

Database settings
-----------------

.. versionchanged:: 1.3.1 Scylla Manager

Database settings allow for `using a remote cluster <../use-a-remote-db>`_ to store Scylla Manager data.

.. code-block:: yaml

   # Scylla Manager database, used to store management data.
   database:
     hosts:
       - 127.0.0.1
   # Enable or disable client/server encryption.
   #  ssl: false
   #
   # Database credentials.
   #  user: user
   #  password: password
   #
   # Local datacenter name, specify if using a remote, multi-dc cluster.
   #  local_dc:
   #
   # Database connection timeout.
   #  timeout: 600ms
   #
   # Keyspace for management data, for create statement see /etc/scylla-manager/create_keyspace.cql.tpl.
   #  keyspace: scylla_manager
   #  replication_factor: 1

SSL/TLS setting
---------------

.. versionadded:: 1.3.1 Scylla Manager

If *database.ssl* is set to true you may specify additional SSL configuration options.

.. code-block:: yaml

   # Optional custom client/server encryption options.
   #ssl:
   # CA certificate used to validate server cert. If not set will use he host's root CA set.
   #  cert_file:
   #
   # Verify the hostname and server cert.
   #  validate: true
   #
   # Client certificate and key in PEM format. It has to be provided when
   # client_encryption_options.require_client_auth=true is set on server.
   #  user_cert_file:
   #  user_key_file

SSH setting
-----------

.. versionadded:: 1.3.1 Scylla Manager

SSH settings let you change the default SSH port if needed.

.. code-block:: yaml

   # SSH global configuration, SSH is used to access scylla nodes. Username and
   # identity file are specified per cluster with sctool.
   #ssh:
   # Alternative default SSH port.
   #  port: 22
   #
   # Interval to send keepalive message through the encrypted channel and
   # request a response from the server.
   #  server_alive_interval: 15s
   #
   # The number of server keepalive messages which may be sent without receiving
   # any messages back from the server. If this threshold is reached while server
   # keepalive messages are being sent, ssh will disconnect from the server,
   # terminating the session.
   #  server_alive_count_max: 3

Healthcheck settings
--------------------

.. versionadded:: 1.3.1 Scylla Manager

Healthcheck settings let you specify the timeout threshold. If there is no response from a node after this time period is reached, the `status </operating-scylla/manager/1.3/sctool/#status>`_ report (``sctool status``) shows the node as DOWN. 

.. code-block:: yaml

   # Healthcheck service configuration.
   #healthcheck:
   # Timeout for CQL status checks.
   #  timeout: 250ms
   #  ssl_timeout: 750ms

Repair settings
---------------

Repair settings let you specify repair parameters.

.. code-block:: yaml

   # Repair service configuration.
   repair:
     # Granularity of repair. Repair works on segments, segment is a continuous
     # token range.
     #
     # Set the maximal number of tokens in a segment (zero is no limit).
     segment_size_limit: 0

     # Set number of segments to be repaired in one Scylla command.
     segments_per_repair: 1

     # Error tolerance.
     #
     # Set how many segments may fail to repair. Note that the manager would retry
     # to repair the failed segments. If the limit is exceeded, however, repair
     # will stop and the next repair will start from the beginning.
     segment_error_limit: 100

     # Set wait time if Scylla failed to execute a repair command. Note that if
     # stop_on_error is true this has no effect.
     error_backoff: 10s

     # Set how often to poll Scylla node for command status.
     poll_interval: 200ms

     # Set maximal time after which a restarted repair is forced to start from the
     # beginning.
     max_run_age: 36h

     # Distribution of data among cores (shards) within a node.
     # Copy value from Scylla configuration file.
     murmur3_partitioner_ignore_msb_bits: 12
