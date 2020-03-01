===========================
Scylla Manager Installation
===========================

.. versionchanged:: 2.0 Scylla Manager

.. contents:: 
   :depth: 2
   :local:

System requirements
===================

Scylla Manager Server has modest systems requirements.
While a minimal server can run on a system with 2 cores and 1GB RAM, the following configuration is recommended:

* **CPU** - 2vCPUs
* **Memory** - 8GB+ DRAM

.. note::  If you are running `Scylla Monitoring Stack </operating-scylla/monitoring/monitoring_stack/>`_ on the same server as Scylla Manager, your system should also meet the minimal `Monitoring requirements </operating-scylla/monitoring/monitoring_stack/#minimal-production-system-recommendations>`_.

Installation workflow
=====================

#. `Install Scylla Manager`_
#. `Run the scyllamgr_setup script`_
#. `Enable Bash Script Completion`_ 
#. `Start Scylla Manager Service`_ and verify Scylla Manager is Running and that sctool is running

.. _service:

Install Scylla Manager
----------------------

Choose one of the following installation methods:

**Scylla Manager for Scylla Enterprise**

#. Download and install Scylla Manager from the `Enterprise Download page <https://www.scylladb.com/download/enterprise/#manager>`_.
#. Follow the entire installation procedure.
#. Continue with `Run the scyllamgr_setup script`_.

**Scylla Manager for Scylla Open Source**

#. On the same node as you are installing Scylla Manager, download and install Scylla as a local database from the `Scylla Open Source Download page <https://www.scylladb.com/download/open-source/>`_. 
   There is no need to run the Scylla setup as it is taken care of by the ``scyllamgr_setup`` script.
#. Download and Install Scylla Manager from the `Scylla Manager Open Source Download page <https://www.scylladb.com/download/open-source/scylla-manager/>`_.
#. Follow the entire installation procedure.
#. Continue with `Run the scyllamgr_setup script`_.

Run the scyllamgr_setup script
------------------------------

The Scylla Manager setup script automates configuration of Scylla Manager by asking you some simple questions.
It can be run in non-interactive mode if you'd like to script it.

There are three decisions you need to make:

* Do you want to enable the service to start automatically? If not, you will have to start the service manually each time you want to use it.
* Do you want to set up and enable a local Scylla backend? If not, you will need to set up a `remote DB <../use-a-remote-db>`_
* Do you want Scylla Manager to check periodically if updates are available? If not, you will need to check yourself.

.. code-block:: none

   scyllamgr_setup -h
   Usage: scyllamgr_setup [-y][--no-scylla-setup][--no-enable-service][--no-check-for-updates]

   Options:
     -y, --assume-yes          assume that the answer to any question which would be asked is yes
     --no-scylla-setup         skip setting up and enabling local Scylla instance as a storage backend for Scylla Manager
     --no-enable-service       skip enabling service
     --no-check-for-updates    skip enabling periodic check for updates
     -h, --help                print this help

   Interactive mode is enabled when no flags are provided.

**Procedure**

#. Run the ``scyllamgr_setup`` script to configure the service. You can run the script in interactive mode (no flags) or automate your decision making by using flags. 

Enable bash script completion
-----------------------------

Enable bash completion for sctool: the Scylla Manager CLI. Alternatively, you can just open a new terminal.

.. code-block:: none

   source /etc/bash_completion.d/sctool.bash

Start Scylla Manager service
============================

Scylla Manager integrates with ``systemd`` and can be started and stopped using ``systemctl`` command. 

**Procedure**

#. Start the Scylla Manager server service.

   .. code-block:: none

      sudo systemctl start scylla-manager.service

#. Verify the Scylla Manager server service is running.

   .. code-block:: none
      
      sudo systemctl start scylla-manager
      ● scylla-manager.service - Scylla Manager Server
         Loaded: loaded (/usr/lib/systemd/system/scylla-manager.service; enabled; vendor preset: disabled)
         Active: active (running) since Wed 2019-10-30 11:00:01 UTC; 20s ago
       Main PID: 5805 (scylla-manager)
         CGroup: /system.slice/scylla-manager.service
                 └─5805 /usr/bin/scylla-manager

      Oct 30 11:00:07 ip-10-0-0-252.ec2.internal scylla-manager[5805]: {"L":"INFO","T":"2019-10-30T11:00:07.590Z","M":"Running migration","migration":"017-repair_run_drop_status.cql"}
      Oct 30 11:00:08 ip-10-0-0-252.ec2.internal scylla-manager[5805]: {"L":"INFO","T":"2019-10-30T11:00:08.078Z","M":"Running migration","migration":"018-empty.cql"}
      Oct 30 11:00:08 ip-10-0-0-252.ec2.internal scylla-manager[5805]: {"L":"INFO","T":"2019-10-30T11:00:08.082Z","M":"Running migration","migration":"019-repair_segment_error_pos.cql"}
      Oct 30 11:00:08 ip-10-0-0-252.ec2.internal scylla-manager[5805]: {"L":"INFO","T":"2019-10-30T11:00:08.233Z","M":"Running migration","migration":"v2.0.0.cql"}
      Oct 30 11:00:09 ip-10-0-0-252.ec2.internal scylla-manager[5805]: {"L":"INFO","T":"2019-10-30T11:00:09.618Z","M":"Schema up to date","keyspace":"scylla_manager","_trace_id":"D6uI41ikRAmIvffVRPC0Fg"}
      Oct 30 11:00:09 ip-10-0-0-252.ec2.internal scylla-manager[5805]: {"L":"INFO","T":"2019-10-30T11:00:09.630Z","N":"scheduler","M":"Loading tasks from database","_trace_id":"D6uI41ikRAmIvffVRPC0Fg"}
      Oct 30 11:00:09 ip-10-0-0-252.ec2.internal scylla-manager[5805]: {"L":"INFO","T":"2019-10-30T11:00:09.633Z","N":"scheduler","M":"All tasks scheduled","_trace_id":"D6uI41ikRAmIvffVRPC0Fg"}
      Oct 30 11:00:09 ip-10-0-0-252.ec2.internal scylla-manager[5805]: {"L":"INFO","T":"2019-10-30T11:00:09.633Z","M":"Starting HTTPS    server","address":"127.0.0.1:56443","client_ca":"","_trace_id":"D6uI41ikRAmIvffVRPC0Fg"}
      Oct 30 11:00:09 ip-10-0-0-252.ec2.internal scylla-manager[5805]: {"L":"INFO","T":"2019-10-30T11:00:09.633Z","M":"Starting Prometheus server","address":":56090","_trace_id":"D6uI41ikRAmIvffVRPC0Fg"}
      Oct 30 11:00:09 ip-10-0-0-252.ec2.internal scylla-manager[5805]: {"L":"INFO","T":"2019-10-30T11:00:09.633Z","M":"Service started","_trace_id":"D6uI41ikRAmIvffVRPC0Fg"}


#. Confirm sctool is running by displaying the sctool version.

   .. code-block:: none

      sctool version
      Client version: 2.0-0.20191030.9442dd9b
      Server version: 2.0-0.20191030.9442dd9b


.. note:: The first time you run this command, Scylla Manager may take a few seconds to start because it must create database schema.

Install Scylla Manager Agent
============================

Continue with `Setup Scylla Manager Agent <../install-agent>`_
