

====================
Setup Scylla Manager
====================

The following document walks you through the Scylla Manager setup phase, assuming you completed the `installation <https://www.scylladb.com/enterprise-download/#manager>`_.
When you install Scylla Manager, it installs a local instance of Scylla to use as it's database.
If you want to setup Scylla Manager with a remote database use `this guide <../use-a-remote-db>`_ first.

.. contents:: 
   :depth: 2
   :local:

Port Settings
=============

`sctool status` requires port `:9042` to be open in order to check node status. Confirm that this port is open.

Run setup script
================

The Scylla Manager setup script is a wizard that automates configuration of Scylla Manager.

**Procedure**

1. Run the ``scyllamgr_setup`` script to configure the service.
   The wizard contains questions about enabling services.
   If you answer no to the questions, you will have to start a service manually each time you want to use it.

.. code-block:: none

   sudo scyllamgr_setup
   Do you want to configure and enable the local ScyllaDB instance as a backend storage for this Scylla Manager installation?
   Answer yes to configure and automatically start ScyllaDB when the node boots; answer no to skip this step.
   [YES/no]
   Do you want to enable Scylla Manager?
   Answer yes to automatically start Scylla Manager when the node boots; answer no to skip this step.
   [YES/no]
   Created symlink from /etc/systemd/system/multi-user.target.wants/scylla-server.service to /usr/lib/systemd/system/scylla-server.service.
   Scylla Manager setup finished.

Start Scylla Manager
====================

Scylla Manager integrates with ``systemd`` and can be started and stopped using ``systemctl`` command.

**Procedure**

1. Run Scylla Manager server.

.. code-block:: none

   sudo systemctl start scylla-manager.service

2. Verify the Scylla Manager is running.

.. code-block:: none

   sudo systemctl status scylla-manager.service
   ● scylla-manager.service - Scylla Manager Server
      Loaded: loaded (/usr/lib/systemd/system/scylla-manager.service; enabled; vendor preset: disabled)
      Active: active (running) since Fri 2018-08-31 12:15:30 UTC; 5s ago
    Main PID: 32355 (scylla-manager)
       Tasks: 9
      Memory: 5.3M
      CGroup: /system.slice/scylla-manager.service
              └─32355 /usr/bin/scylla-manager

3. Enable bash completion for sctool - Scylla Manager CLI.
   Alternatively, you can just open a new terminal.

.. code-block:: none

   source /etc/bash_completion.d/sctool.bash

4. Confirm sctool is running by displaying the sctool version.

.. code-block:: none

   sctool version
   Client version: 1.3.0-0.20181130.03ae248
   Server version: 1.3.0-0.20181130.03ae248

.. note:: The first time you run this command, Scylla Manager may take a few seconds to start.

Add a cluster
=============

Continue with `adding a cluster <../add-a-cluster>`_.
