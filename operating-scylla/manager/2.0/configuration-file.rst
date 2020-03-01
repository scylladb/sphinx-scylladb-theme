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


Healthcheck settings
--------------------

Healthcheck settings let you specify the timeout threshold. If there is no response from a node after this time period is reached, the `status <../sctool/#status>`_ report (``sctool status``) shows the node as DOWN. 

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
   #repair:
   # Maximal number of tokens in a segment.
   #  segment_tokens_max: 0
   #
   # Maximal number of shards on a host repaired at the same time.
   #  shard_parallel_max: 0
   #
   # Maximal allowed number of failed segments per shard. In case of a failure
   # to repair a segment Scylla Manager will try to repair it multiple times
   # depending on the specified number of retries (default 3). If the
   # shard_failed_segments_max limit is exceeded repair task will immediately
   # fail and the next repair run will start repair procedure from the beginning.
   #  shard_failed_segments_max: 25
   #
   # In case of an error hold back repair for the specified amount of time.
   #  error_backoff: 5m
   #
   # Frequency Scylla Manager poll Scylla node for repair command status.
   #  poll_interval: 200ms
   #
   # Maximal time a paused repair is considered fresh and can be continued,
   # if exceeded repair will start from the beginning.
   #  age_max: 36h
   #
   # Distribution of data among cores (shards) within a node.
   # Copy value from Scylla configuration file.
   # murmur3_partitioner_ignore_msb_bits: 12

Backup settings
---------------

Backup settings let you specify backup parameters.

.. code-block:: yaml

   # Backup service configuration.
   #backup:
   # Minimal amount of free disk space required to take a snapshot.
   #  disk_space_free_min_percent: 10
   #
   # Frequency Scylla Manager poll Scylla node for backup upload status.
   #  poll_interval: 1s
   #  max_age: 12h

