Overview
========

Scylla Manager is a product for database operations automation.
It can manage multiple Scylla clusters and run cluster-wide tasks in a controlled and predictable way.

No sidecar
----------

The concept of having a companion application installed together with another application is known as a sidecar.
Scylla Manager is designed so that there is no need for sidecar processes running on Scylla nodes.
Scylla Manager supports SSH tunnelling for its interactions with Scylla clusters.
While SSH communication with the cluster is not mandatory, it is recommended as it does not require any database configuration changes and only requires a dedicated user with minimal permissions.
Included in the Scylla Manager package is a script which sets up SSH connectivity to all nodes using one simple command.

Deployment
----------

Scylla Manager consists of two components:

* Server - daemon that exposes REST API
* Sctool - a command-line interface (CLI) for interacting with the server over the REST API

The server persists its data to a Scylla cluster.
It comes with a pre-installed single node cluster running locally but can be changed to an external cluster
(see `Use a remote database for Scylla Manager <../use-a-remote-db>`_ for details).

The diagram below presents a logical view on Scylla Manager managing two Scylla Clusters.

.. image:: overview.png

Requirements
------------
Scylla Manager has modest systems requirements. While a minimal Manager server can run on a system with 2 cores, 1GB system, the following configuration is recommended:

* **CPU** - 2vCPUs
* **Memory** - 8GB+ DRAM

.. note::  If you are running `Scylla Monitoring </operating-scylla/monitoring/monitoring_stack/>`_ on the same server as Manager, your system should also meet the minimal `Monitoring requirements </operating-scylla/monitoring/monitoring_stack/#minimal-production-system-recommendations>`_.

Topology awareness
------------------

Scylla Manager discovers cluster topology and is aware of nodes belonging to different datacenters.
By default, Scylla Manager automatically selects a local DC based on ping latency measurements and whenever possible tries to use hosts in a that DC to interact with the cluster.

See Also
--------

* `Setup Scylla Manager <../setup>`_
* `sctool Reference <../sctool>`_
