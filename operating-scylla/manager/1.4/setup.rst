

====================
Setup Scylla Manager
====================

The procedures that follow assume that you already have downloaded and installed Scylla and Scylla Manager as outlined in the `Prerequisites`_.

.. contents:: 
   :depth: 2
   :local:

Prerequisites
=============

A Scylla datastore (local or remote) is prerequisite for Scylla Manager installation.
Scylla (Open Source or Enterprise) should be installed on the Scylla Nodes as well. 


**Scylla Manager for Scylla Enterprise**
When you install `Scylla Manager with Scylla Enterprise <https://www.scylladb.com/wp-login.php>`_, it includes a local instance of Scylla. If you want to setup Scylla Manager with a remote Scylla backend database follow `this procedure <../use-a-remote-db>`_ first.

**Scylla Manager for Scylla Open Source**
When you install Scylla Manager with Scylla Open Source, Scylla is not included. Therefore, before you install Scylla Manager, you need to:

1. Download and install Scylla either as a local or remote database. 
   
   * If you are installing Scylla as a backend database follow `this procedure <../use-a-remote-db>`_. 
   * If you are installing Scylla locally, `Download and Install Scylla <https://www.scylladb.com/download/open-source/>`_ on the same node as you are installing Scylla Manager.

2. Following Scylla Installation, do one of the following:

   * Run scylla_setup (on the download / installation `page <https://www.scylladb.com/download/>`_) or 
   * Enable `developer mode </getting-started/install_scylla/dev_mod/>`_

3. Confirm that Scylla Server service runs with no errors.  

4. `Download  and Install Scylla Manager <https://www.scylladb.com/download/open-source/scylla-manager/>`_ (registration required).   

Run the scyllamgr_setup script
==============================

The Scylla Manager setup script automates configuration of Scylla Manager by asking you some simple questions.

**Procedure**

Run the ``scyllamgr_setup`` script to configure the service.



.. code-block:: none

   sudo scyllamgr_setup
   Do you want to configure and enable the local ScyllaDB instance as a backend storage for this Scylla Manager installation?
   Answer yes to configure and automatically start ScyllaDB when the node boots; answer no to skip this step.
   [YES/no]

If you are using remote Scylla backend, answer ``no``, but make sure you have followed `this procedure <../use-a-remote-db>`_ first.
If you are not using a remote Scylla backend, answer ``yes``.

.. code-block:: none

   Do you want to enable Scylla Manager?
   Answer yes to automatically start Scylla Manager when the node boots; answer no to skip this step.
   [YES/no]

If you answer ``No`` to the question, you will have to start the service manually each time you want to use it.

If you answer ``Yes``, the script continues to create a symbolic link so that the Scylla server service starts automatically.

.. code-block:: none

   Created symlink from /etc/systemd/system/multi-user.target.wants/scylla-server.service to /usr/lib/systemd/system/scylla-server.service.
   Scylla Manager setup finished.

.. _Bash:

Enable Bash Script Completion
=============================

Enable bash completion for sctool: the Scylla Manager CLI. Alternatively, you can just open a new terminal.

.. code-block:: none

   source /etc/bash_completion.d/sctool.bash


Start Scylla Manager
====================

Scylla Manager integrates with ``systemd`` and can be started and stopped using ``systemctl`` command.

**Procedure**

1. Start the Scylla Manager server service.

.. code-block:: none

   sudo systemctl start scylla-manager.service

2. Verify the Scylla Manager server service is running.

.. code-block:: none

   sudo systemctl status scylla-manager.service
   ● scylla-manager.service - Scylla Manager Server
      Loaded: loaded (/usr/lib/systemd/system/scylla-manager.service; enabled; vendor preset: disabled)
      Active: active (running) since Tue 2019-04-02 17:59:37 UTC; 2h 22min ago
     Main PID: 5810 (scylla-manager)
       Tasks: 9
      Memory: 5.3M
      CGroup: /system.slice/scylla-manager.service
                   └─5810 /usr/bin/scylla-manager
   ...

   Hint: Some lines were ellipsized, use -l to show in full.

3. Confirm sctool is running by displaying the sctool version.

.. code-block:: none

   sctool version
   Client version: 1.4-0.20190324.247a5585
   Server version: 1.4-0.20190324.247a5585

.. note:: The first time you run this command, Scylla Manager may take a few seconds to start.

Add a cluster
=============

Continue with `adding a cluster <../add-a-cluster>`_.
