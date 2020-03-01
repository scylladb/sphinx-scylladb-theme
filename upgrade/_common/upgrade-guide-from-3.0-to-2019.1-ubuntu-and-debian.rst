=============================================================================
Upgrade Guide - Scylla 3.0 to Scylla Enterprise 2019.1 for |OS|
=============================================================================

This document is a step by step procedure for upgrading from Scylla 3.0 to Scylla Enterprise 2019.1, and rollback to 3.0 if required.

.. contents::
   :local:

Applicable versions
===================
This guide covers upgrading Scylla from the following versions: 3.0.x to Scylla Enterprise version 2019.1.y on the following platform:

* |OS|

.. include:: /upgrade/_common/note-ubuntu14-ent.rst

Upgrade Procedure
=================

.. include:: /upgrade/_common/warning.rst

A Scylla upgrade is a rolling procedure which does **not** require full cluster shutdown.
For each of the nodes in the cluster, you will:

* Check cluster schema
* Drain node and backup the data
* Backup configuration file
* Stop Scylla
* Download and install new Scylla packages
* Start Scylla
* Validate that the upgrade was successful

Apply the following procedure **serially** on each node. Do not move to the next node before validating the node is up and running with the new version.

**During** the rolling upgrade it is highly recommended:

* Not to use new 2019.1 features
* Not to run administration functions, like repairs, refresh, rebuild or add or remove nodes. See `here </operating-scylla/manager/1.3/sctool/>`_ for suspending Scylla Manager scheduled or running repairs.
* Not to apply schema changes


.. include:: /upgrade/_common/upgrade_to_2019_warning.rst
  
Upgrade steps
=============
Check cluster schema
--------------------
Make sure that all nodes have the schema synched prior to upgrade, we won't survive an upgrade that has schema disagreement between nodes.

.. code:: sh

       nodetool describecluster

Drain node and backup the data
------------------------------
Before any major procedure, like an upgrade, it is recommended to backup all the data to an external device. In Scylla, backup is done using the ``nodetool snapshot`` command. For **each** node in the cluster, run the following command:

.. code:: sh

   nodetool drain
   nodetool snapshot

Take note of the directory name that nodetool gives you, and copy all the directories having this name under ``/var/lib/scylla`` to a backup device.

When the upgrade is complete (all nodes), the snapshot should be removed by ``nodetool clearsnapshot -t <snapshot>``, or you risk running out of space.


Backup configuration files
--------------------------

.. code:: sh

   for conf in $(cat /var/lib/dpkg/info/scylla-*server.conffiles /var/lib/dpkg/info/scylla-*conf.conffiles /var/lib/dpkg/info/scylla-*jmx.conffiles | grep -v init ); do sudo cp -v $conf $conf.backup-3.0; done

Gracefully stop the node
------------------------

.. code:: sh

   sudo service scylla-server stop

Download and install the new release
------------------------------------
Before upgrading, check what version you are running now using ``dpkg -s scylla-server``. You should use the same version in case you want to |ROLLBACK|_ the upgrade. If you are not running a 3.0.x version, stop right here! This guide only covers 3.0.x to 2019.1.y upgrades.

To upgrade:

1. Update the |APT_ENTERPRISE|_ to **2019.1**

2. Install

.. code:: sh

   sudo apt-get update
   sudo apt-get remove scylla\*
   sudo apt-get install scylla-enterprise
   for conf in $(cat /var/lib/dpkg/info/scylla-*server.conffiles /var/lib/dpkg/info/scylla-*conf.conffiles /var/lib/dpkg/info/scylla-*jmx.conffiles | grep -v init ); do sudo cp -v $conf.backup-3.0 $conf; done
   sudo systemctl daemon-reload (Ubuntu 16.04)

Answer ‘y’ to the first two questions.

Start the node
--------------

.. code:: sh

   sudo service scylla-server start

Validate
--------
1. Check cluster status with ``nodetool status`` and make sure **all** nodes, including the one you just upgraded, are in UN status.
2. Use ``curl -X GET "http://localhost:10000/storage_service/scylla_release_version"`` to check scylla version.
3. Check scylla-server log (by ``journalctl _COMM=scylla``) and ``/var/log/syslog`` to validate there are no errors.
4. Check again after 2 minutes, to validate no new issues are introduced.

Once you are sure the node upgrade is successful, move to the next node in the cluster.

* More on :doc:`Scylla Metrics Update - Scylla 3.0 to 2019.1<metric-update-3.0-to-2019.1>`

Rollback Procedure
==================

.. include:: /upgrade/_common/warning_rollback.rst

The following procedure describes a rollback from Scylla Enterprise release 2019.1.x to Scylla 3.0.y. Apply this procedure if an upgrade from 3.0 to 2019.1 failed before completing on all nodes. Use this procedure only for nodes you upgraded to 2019.1

Scylla rollback is a rolling procedure which does **not** require full cluster shutdown.
For each of the nodes rollback to 3.0, you will:

* Drain the node and stop Scylla
* Retrieve the old Scylla packages
* Restore the configuration file
* Restart Scylla
* Validate the rollback success

Apply the following procedure **serially** on each node. Do not move to the next node before validating the node is up and running with the new version.

Rollback steps
==============
Gracefully shutdown Scylla
--------------------------

.. code:: sh

   nodetool drain
   sudo service scylla-server stop

download and install the old release
------------------------------------
1. Remove the old repo file.

.. code:: sh

   sudo rm -rf /etc/apt/sources.list.d/scylla.list

2. Update the |APT|_ to **3.0**

3. install

.. code:: sh

   sudo apt-get update
   sudo apt-get remove scylla\* -y
   sudo apt-get install scylla

Answer ‘y’ to the first two questions.

Restore the configuration files
-------------------------------
.. code:: sh

   for conf in $(cat /var/lib/dpkg/info/scylla-*server.conffiles /var/lib/dpkg/info/scylla-*conf.conffiles /var/lib/dpkg/info/scylla-*jmx.conffiles | grep -v init ); do sudo cp -v $conf.backup-3.0 $conf; done
   sudo systemctl daemon-reload (Ubuntu 16.04)

Start the node
--------------

.. code:: sh

   sudo service scylla-server start

Validate
--------
Check upgrade instruction above for validation. Once you are sure the node rollback is successful, move to the next node in the cluster.
