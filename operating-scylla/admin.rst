Administration Guide
********************
.. contents:: 
   :depth: 1
   :local:

System requirements
===================
Make sure you have met the `System Requirements </getting-started/system-requirements>`_  before you install and configure Scylla. 

Download and Install
====================

See the :doc:`getting started page </getting-started/index>` for info on installing Scylla on your platform.


System configuration
====================
See `System Configuration Guide`_ for details on optimum OS settings for Scylla. (These settings are performed automatically in the Scylla packages, Docker containers, and Amazon AMIs.)

..  _`System Configuration Guide`: /getting-started/system-configuration/#system-configuration-files-and-scripts

Scylla Configuration
====================
Scylla configuration files are:

+-------------------------------------------------------+---------------------------------+
| Installed location                                    | Description                     |
+=======================================================+=================================+
| :code:`/etc/default/scylla-server` (Ubuntu/Debian)    | Server startup options          |
| :code:`/etc/sysconfig/scylla-server` (others)         |                                 |
+-------------------------------------------------------+---------------------------------+
| :code:`/etc/scylla/scylla.yaml`                       | Main Scylla configuration file  |
+-------------------------------------------------------+---------------------------------+
| :code:`/etc/scylla/cassandra-rackdc.properties`       | Rack & dc configuration file    |
+-------------------------------------------------------+---------------------------------+

Address Configuration in Scylla
-------------------------------

The following addresses can be configured in scylla.yaml:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Address Type
     - Description
   * - listen_address
     - Address Scylla listens for connections from other nodes. See storage_port and ssl_storage_ports.
   * - rpc_address
     - Address on which Scylla is going to expect Thrift and CQL clients connections. See rpc_port, native_transport_port and native_transport_port_ssl in the `Networking </operating-scylla/admin/#networking>`_ parameters.
   * - broadcast_address
     - Address that is broadcasted to tell other Scylla nodes to connect to. Related to listen_address above.
   * - broadcast_rpc_address
     - Address that is broadcasted to tell the clients to connect to. Related to rpc_address.
   * - seeds
     - These are broadcast_addresses of seeder nodes.
   * - endpoint_snitch
     - Node's address resolution helper.
   * - api_address
     - Address for REST API requests. See api_port in the `Networking </operating-scylla/admin/#networking>`_ parameters.
   * - prometheus_address
     - Address for Prometheus queries. See prometheus_port in the `Networking </operating-scylla/admin/#networking>`_ parameters and `Scylla Monitoring </operating-scylla/monitoring/>`_ for more details.
   * - replace_address
     - Address of the node this Scylla instance is meant to replace. Refer to `Replace a Dead Node in a Scylla Cluster </operating-scylla/procedures/cluster-management/replace_dead_node/>`_ for more details.

.. note:: When the listen_address, rpc_address, broadcast_address and broadcast_rpc_address parameters are not set correctly, Scylla does not to work as expected.

scylla-server
-------------
The :code:`scylla-server` file contains configuration related to starting up the Scylla server.

.. include:: /operating-scylla/scylla-yaml.rst


internode_compression
---------------------

internode_compression controls whether traffic between nodes is compressed.

* all  - all traffic is compressed.
* dc   - traffic between different datacenters is compressed.
* none - nothing is compressed (default).

Configuring TLS/SSL in scylla.yaml
----------------------------------

Scylla versions 1.1 and greater support encryption between nodes and between client and node. See the Scylla `Scylla TLS/SSL guide: </operating-scylla/security/>`_ for configuration settings.

Networking
----------

.. include:: /operating-scylla/_common/networking-ports.rst

.. image:: /operating-scylla/security/scylla-ports-diagram.png


All ports above need to be open to external clients (CQL), external admin systems (JMX), and other nodes (RPC). REST API port can be kept closed for external incoming connections.

The JMX service, :code:`scylla-jmx`, runs on port 7199. It is required in order to manage Scylla using :code:`nodetool` and other Apache Cassandra-compatible utilities. The :code:`scylla-jmx` process must be able to connect to port 10000 on localhost. The JMX service listens for incoming JMX connections on all network interfaces on the system.

Advanced networking
-------------------
It is possible that a client, or another node, may need to use a different IP address to connect to a Scylla node from the address that the node is listening on. This is the case when a node is behind port forwarding. Scylla allows for setting alternate IP addresses.

Do not set any IP address to :code:`0.0.0.0`.

.. list-table::
   :widths: 30 40 30
   :header-rows: 1

   * - Address Type
     - Description
     - Default
   * - listen_address (required)
     - Address Scylla listens for connections from other nodes. See storage_port and ssl_storage_ports.
     - No default
   * - rpc_address (required)
     - Address on which Scylla is going to expect Thrift and CQL clients connections. See rpc_port, native_transport_port and native_transport_port_ssl in the `Networking </operating-scylla/admin/#networking>`_ parameters.
     - No default
   * - broadcast_address
     - Address that is broadcasted to tell other Scylla nodes to connect to. Related to listen_address above.
     - listen_address
   * - broadcast_rpc_address
     - Address that is broadcasted to tell the clients to connect to. Related to rpc_address.
     - rpc_address


If other nodes can connect directly to :code:`listen_address`, then :code:`broadcast_address` does not need to be set.

If clients can connect directly to :code:`rpc_address`, then :code:`broadcast_rpc_address` does not need to be set.

.. note:: For tips and examples on how to configure these addresses, refer to `How to Properly Set Address Values in scylla.yaml </kb/yaml-address>`_


Core dumps
----------
On RHEL and CentOS, the Automatic Bug Reporting Tool (`ABRT <https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/System_Administrators_Guide/ch-abrt.html>`_) conflict with Scylla coredump configuration. Remove it before installing Scylla: :code:`sudo yum remove -y abrt`

Scylla places any core dumps in :code:`var/lib/scylla/coredump`. They are not visible with the :code:`coredumpctl` command. See the :doc:`System Configuration Guide </getting-started/system-configuration/>` for details on core dump configuration scripts. Check with Scylla support before sharing any core dump, as they may contain sensitive data.

Schedule fstrim
===============

Scylla sets up daily fstrim on the filesystem(s).
Containing your Scylla commitlog and data directory. This utility will
discard, or trim, any blocks no longer in use by the filesystem.

Monitoring
==========
Scylla exposes interfaces for online monitoring, as described below.

Monitoring Interfaces
---------------------

:monitor_lst:`Scylla Monitoring Interfaces</monitoring_apis/>`

Monitoring Stack
----------------

:monitor_lst:`Scylla Monitoring Stack</monitoring_stack/>`

JMX
---
Scylla JMX is compatible with Apache Cassandra, exposing the relevant subset of MBeans.

.. REST

.. include:: /operating-scylla/rest.rst

Un-contents
-----------

Scylla is designed for high performance before tuning, for fewer layers that interact in unpredictable ways, and to use better algorithms that do not require manual tuning. The following items are found in the manuals for other data stores, but do not need to appear here.

Configuration un-contents
^^^^^^^^^^^^^^^^^^^^^^^^^

* Generating tokens
* Configuring virtual nodes

Operations un-contents
^^^^^^^^^^^^^^^^^^^^^^

* Tuning Bloom filters
* Data caching
* Configuring memtable throughput
* Configuring compaction
* Compression

Testing compaction and compression
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Tuning Java resources
* Purging gossip state on a node


Help with Scylla
================
Contact `Support <http://www.scylladb.com/services/support/>`_, or visit the Scylla `Community <http://www.scylladb.com/community/>`_ page for peer support.

.. include:: /rst_include/apache-copyrights-index.rst

.. include:: /rst_include/apache-copyrights-index-all-attributes.rst
