Scylla Monitoring Stack
=======================

This document describes the setup of Scylla monitoring Stack, base on `Scylla Prometheus API`_.

Scylla monitoring stack consists of three components, wrapped in Docker containers:

* `prometheus` - collects and stores metrics
* `alertmanager` - handles alerts
* `grafana` - dashboard server

.. image:: monitor.png

..  _`Scylla Prometheus API`: monitoring_apis/#prometheus/

The monitoring stack needs to be installed on a dedicated server, external to the Scylla cluster. Make sure the monitoring server have access to the Scylla nodes so that it can pull the metrics over the Prometheus API.

For evaluation, you can run Scylla monitoring stack on any server (or laptop) that can handle two Docker instances at the same time. For production, see recommendation below.

.. include:: min-prod-hw.rst


Prerequisites
.............

* `docker`_

..  _`docker`: https://www.docker.com/


Procedure
.........

1. Download and extract the latest `Scylla Monitoring Stack binary`_; for example, for release 2.2.0

.. _`Scylla Monitoring Stack binary`: https://github.com/scylladb/scylla-monitoring/releases

.. code-block:: sh

   wget https://github.com/scylladb/scylla-monitoring/archive/scylla-monitoring-2.2.tar.gz
   tar -xvf scylla-monitoring-2.2.tar.gz
   cd scylla-monitoring-scylla-monitoring-2.2

As an alternative, you can clone and use the git repository directly.

.. code-block:: sh

   git clone https://github.com/scylladb/scylla-monitoring.git
   cd scylla-monitoring
   git checkout branch-2.2

2. Start docker service if needed

.. code-block:: sh

   centos $ sudo service docker start
   ubuntu $ sudo systemctl restart docker



3. Update ``prometheus/scylla_servers.yml`` with the targets' IPs (the servers you wish to monitor).

.. note::
   It is important that the dc in the target files will match the datacenters names used by Scylla.
   Use the ``nodetool status`` command to validate the datacenter names used by Scylla.

For example:

.. code-block:: yaml

   targets:
       - 172.17.0.2
       - 172.17.0.3
   labels:
       cluster: cluster1
       dc: dc1


For general node information (disk, network, etc.) Scylla Monitoring Stack uses the node_exporter agent that runs on the same machine as Scylla does.
By default, Prometheus will assume you have a node_exporter running on each machine. If this is not the case, you can override the node_exporter
targets configuration file by creating an additional
file and pass it with the ``-n`` flag.

.. note::
   By default, there is no need to configure ``node_exporter_server.yml``. Prometheus will use the same targets it uses for
   Sylla and will assume you have a node_exporter
   running on each Scylla server.


It is possible to configure your own target file instead of updating ``scylla_servers.yml``, using the ``-s`` for scylla target file.

For example:

.. code-block:: yaml

   ./start-all.sh -s my_scylla_server.yml -d data_dir


Use Labels to mark different Data Centers

As can be seen in the examples, each target has its own set of labels to mark the cluster name and the data center (dc).
You can add multiple targets in the same file for multiple clusters or multiple data centers.

4. Connect to `Scylla Manager`_ by updating ``prometheus/scylla_manager_servers.yml``
If you are using Scylla Manager, you should set its ip.

..  _`Scylla Manager`: /operating-scylla/manager/

For example

.. code-block:: yaml

   # List Scylla Manager end points

   - targets:
     - 127.0.0.1:56090


Note that you do not need to add labels to the Scylla Manager targets.


Start and Stop
..............

Start

.. code-block:: yaml

   ./start-all.sh -d data_dir


Stop

.. code-block:: yaml

   ./kill-all.sh

Setting Specific Version
........................

By default, start-all.sh will start with dashboards for the latest two Scylla versions and the latest Scylla Manager version.

You can specify specific scylla version with the ``-v`` flag and Scylla Manager version with ``-M`` flag

For example:

.. code-block:: sh

   ./start-all.sh -v 3.0,master -M 1.3

will load the dashboards for Scylla versions ``3.0`` and ``master`` and the dashboard for Scylla Manager ``1.3``

View Grafana Monitor
....................

Point your browser to ``your-server-ip:3000``
By default, Grafana authentication is disabled. To enable it and set a password for user admin use the ``-a`` option

For example:

.. code-block:: yaml

   10.10.0.1:3000

* Choose Disk and network interface

The dashboard holds a drop down menu at its upper left corner for disk and network interface.
You should choose relevant disk and interface for the dashboard to show the graphs.


