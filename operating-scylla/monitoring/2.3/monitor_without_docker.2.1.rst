Deploying Scylla Monitoring Without Docker
==========================================

The following instructions will help to deploy :doc:`Scylla Monitoring Stack</operating-scylla/monitoring/2.3/monitoring_stack/>` in the case you can not use the docker version.

Please note, Scylla recommends you use the docker version as it will provide you with most updated, current scylla monitoring system.

.. include:: /operating-scylla/monitoring/2.3/min-prod-hw.rst

The main item to set an alert on is the available disk space in the monitoring system. Data is indefinitely accrued on the Prometheus data directory. The current monitoring solution does not churn data.

Install Scylla Monitor
----------------------

The following procedure is using a ``CentOS 7`` based instance

1. Download the latest monitoring release. Currently it is |mon_version|.

``wget https://github.com/scylladb/scylla-monitoring/archive/scylla-monitoring-2.3.tar.gz``


2. open the tar

``tar -xvf scylla-monitoring-2.3.tar.gz``

Install Alertmanager
--------------------

Tested with alertmanager 0.16.0 version

1. Install `alertmanager`_

..  _`alertmanager` : https://prometheus.io/download/

2. Copy the following file: ``rule_config.yml`` from ``scylla-monitoring-scylla-monitoring-2.3/prometheus`` directory to ``alertmanager.yml`` in the alertmanager installation directory.

For example:

.. code-block:: shell

   cp -p /home/centos/scylla-monitoring-scylla-monitoring-2.3/prometheus/rule_config.yml /home/centos/alertmanager-0.16.0.linux-amd64/alertmanager.yml

3. Start the Alertmanager

For example:

.. code-block:: shell

   ./alertmanager


4. Verify that Alertmanager is up and running, point your browser to the Alertmanager IP:Port

For example:

.. code-block:: shell

   http://192.168.135.166:9093/

.. image:: alertmanager.png


Install Prometheus
------------------

Tested with prometheus version 2.6.1 

1. Install `Prometheus`_

..  _`Prometheus` : https://prometheus.io/download/

2. Copy the following files: ``scylla_servers.yml``, ``node_exporter_servers.yml``, ``prometheus.rules.yml`` from ``scylla-monitoring-scylla-monitoring-2.3/prometheus`` directory to prometheus installation directory.

Copy ``prometheus/prometheus.yml.template`` to ``prometheus.yml``

For example:

.. code-block:: shell

   cp -p /home/centos/scylla-monitoring-scylla-monitoring-2.3/prometheus/*.yml /home/centos/prometheus-2.6.1.linux-amd64

3. Edit the ``prometheus.yml`` file to point to the correct static data sources.

.. note:: Make sure to include the ``honor_labels: false`` parameter in the prometheus.yml file.

.. code-block:: shell

   sudo vi /<prometheus_installation_location>/prometheus-2.6.1.linux-amd64/prometheus.yml

Set the alertmanger address and port by replacing ``AM_ADDRESS`` in the file.

For example if the alertmanager will run on the same host:

.. code-block:: shell

   alerting:
      alertmanagers:
      - static_configs:
          - targets:
              - 127.0.0.1:9093

For example the scrap config for scylla:

.. code-block:: shell

   global:
     scrape_interval: 5s # By default, scrape targets every 5 second.
     scrape_timeout: 4s # Timeout before trying to scape a target again

     # Attach these labels to any time series or alerts when communicating with
     # external systems (federation, remote storage, Alertmanager).
     external_labels:
       monitor: 'scylla-monitor'

   scrape_configs:
   - job_name: scylla
     honor_labels: false
     file_sd_configs:
       - files:
         - /home/centos/prometheus-2.6.1.linux-amd64/scylla_servers.yml
     relabel_configs:
      - source_labels: [__address__]
        regex:  '(.*):.+'
        target_label: instance
        replacement: '${1}'


4. Edit the, ``scylla_servers.yml``, ``node_exporter_servers.yml`` and ``scylla_manager_serer.yml`` files to point to your Scylla nodes.

.. note::
   There is no need to configure ``node_exporter_server``. Instead, in the prometheus scrap config of the node_exporter
   you can use the same file you used for scylla and Prometheus will assume you have a node_exporter running on each Scylla server.

Add the labels for the cluster and data-center

``scylla_servers.yml``:

For example:

.. code-block:: shell

   cat scylla_servers.yml
   # List Scylla end points

   - targets:
     - 192.168.66.6:9180
     - 192.168.66.244:9180
     labels:
       cluster: cluster1
       dc: dc1
   - targets:
       - 172.17.0.3:9180
     labels:
       cluster: cluster1
       dc: dc2

.. note::
   See the previous note about deprecating the ``node_exporter_servers.yml`` file.

``node_exporter_servers.yml``:

For example:

.. code-block:: shell

   cat node_exporter_servers.yml
   # List end points with node exporter

   - targets:
     - '192.168.66.6:9100'
     - '192.168.66.244:9100'
     labels:
       cluster: cluster1
       dc: dc1
   - targets:
       - 172.17.0.3:9100
     labels:
       cluster: cluster1
       dc: dc2

``scylla_manager_serer.yml``

For example:

.. code-block:: shell

   - targets:
     - 127.0.0.1:56090

5. Create a data directory for prometheus to store the metrics data

For example:

.. code-block:: shell

   sudo mkdir /home/centos/prometheus-2.6.1.linux-amd64/mydata


6. Start Prometheus server:

For example:

.. code-block:: shell

   sudo ./prometheus --config.file=prometheus.yml --storage.tsdb.path /home/centos/prometheus-2.6.1.linux-amd64/mydata

Data should start accumulate on: /home/centos/prometheus-2.6.1.linux-amd64/mydata

7. Verify that Prometheus is up and running, point your browser to the Prometheus IP:Port

For example:

.. code-block:: shell

   http://192.168.135.166:9090/

.. image:: 1.png

Prometheus console should be visible

8. Verify that the node_expoerter and scylla metrics accumulating in the server by executing a query through the console

For example:

``node_memory_MemFree``

.. image:: 2.png

And

``scylla_reactor_utilization``

.. image:: 3.png

At this point Scylla is emitting the metrics and Prometheus is able to store them.


Install Grafana
---------------

1. Install Grafana base on the instructions `here`_ make sure to use version 5.0.0 or higher

..  _`here` : http://docs.grafana.org/installation/

Depends if you installed Grafana from a repository (yum install), or if you downloaded the zip version, the directory structure will be
different in the rest of the steps.

2. Access Scylla-Grafana-monitoring directory

``cd /home/centos/scylla-monitoring-scylla-monitoring-2.3/``

3. Copy the plugins to the grafana plugins directory (by default ``/var/lib/grafana/``)

.. code-block:: shell

   sudo cp -r grafana/plugins /var/lib/grafana/

If you installed Grafana from packages, instead of ``/var/lib/grafana/`` you should copy it to ``public/app`` inside the directory you
opened Grafana in.

For example:

.. code-block:: shell

   cp -r grafana/plugins /home/centos/grafana-5.4.3/public/app

4. Generate the dashboards you would like to load and provision them

For example scylla version 3.0 and scylla manager version 1.3

.. code-block:: shell

   ./generate-dashboards.sh -v 3.0 -M 1.3

For Grafana installed with ``yum install``

.. code-block:: shell

   sudo cp grafana/provisioning/dashboards/load.* /etc/grafana/provisioning/dashboards/
   sudo mkdir -p /var/lib/grafana/dashboards
   sudo cp -r grafana/build/* /var/lib/grafana/dashboards

For Grafana installed from packages

.. code-block:: shell

   cp -p -r grafana/build/* /home/centos/grafana-5.4.3/public/build/
   cp -p grafana/provisioning/dashboards/load.* /home/centos/grafana-5.4.3/conf/provisioning/dashboards/

Edit the ``load.*``  files in ``/home/centos/grafana-5.4.3/conf/provisioning/dashboards/`` for the correct path,
for example ``load.3.0.yaml`` would point to: ``/home/centos/grafana-5.4.3/public/build/ver_3.0``


5. Set the data source by copy ``datasource.yml`` and edit it

.. code-block:: shell

   sudo cp grafana/datasource.yml /etc/grafana/provisioning/datasources/

For Grafana installed from packages

.. code-block:: shell

   cp -p grafana/datasource.yml /home/centos/grafana-5.4.3/conf/provisioning/datasources/

You should set the prometheus and the alertmanager ip and port.

For example

.. code-block:: shell

   sudo cat /etc/grafana/provisioning/datasources/datasource.yml
   apiVersion: 1
   datasources:
    - name: prometheus
      type: prometheus
      url: http://192.168.135.167:9090
      access: proxy
      basicAuth: false

    - name: alertmanager
      type: camptocamp-prometheus-alertmanager-datasource
      orgId: 1
      typeLogoUrl: public/img/icn-datasource.svg
      access: proxy
      url: http://192.168.135.166:9093
      password:
      user:
      database:
      basicAuth:
      isDefault:
      jsonData:
        severity_critical: '4'
        severity_high: '3'
        severity_warning: '2'
        severity_info: '1'

6. Start the Grafana service

For Grafana installed with `yum install`

``sudo service grafana-server start``

For Grafana installed from packages:

``cp -p /home/centos/grafana-5.4.3/conf/sample.ini /home/centos/grafana-5.4.3/conf/scylla.ini``

Edit scylla.ini to reflect the right paths in the paths section of the file.


.. code-block:: shell

    plugins = /home/centos/grafana-5.4.3/public/app/plugins
    provisioning = /home/centos/grafana-5.4.3/conf/provisioning


Start the server:

.. code-block:: shell

    cd /home/centos/grafana-5.4.3/
    ./bin/grafana-server -config /home/centos/grafana-5.4.3/conf/scylla.ini

7. Make sure Grafana is running

Point your browser to the Grafana server port 3000, the assumption is that Grafana and Prometheus are collocated on the same server.

.. image:: grafana.png


