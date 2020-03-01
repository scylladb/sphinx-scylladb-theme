======================================================================
Upgrade Guide - Scylla Enterprise 2018.x.y to 2018.x.z for |OS|
======================================================================

This document is a step by step procedure for upgrading from Scylla Enterprise 2018.x.y to 2018.x.z.

.. contents::
   :local:

Applicable versions
===================
This guide covers upgrading Scylla Enterprise from the following versions: 2018.x.y to 2018.x.z on the following platform:

* |OS|

Upgrade Procedure
=================

.. include:: /upgrade/_common/warning.rst

A Scylla Enterprise upgrade is a rolling procedure which does **not** require full cluster shutdown.
For each of the nodes in the cluster, you will:

* Drain node and backup the data
* Check your current release
* Backup configuration file
* Stop Scylla
* Download and install new Scylla packages
* Start Scylla
* Validate that the upgrade was successful

Apply the following procedure **serially** on each node. Do not move to the next node before validating the node is up and running with the new version.

**During** the rolling upgrade it is highly recommended:

* Not to use new 2018.x.z features
* Not to run administration functions, like repairs, refresh, rebuild or add or remove nodes
* Not to apply schema changes

Upgrade steps
=============
Drain node and backup the data
------------------------------
Before any major procedure, like an upgrade, it is recommended to backup all the data to an external device. In Scylla, backup is done using the ``nodetool snapshot`` command. For **each** node in the cluster, run the following command:

.. code:: sh

   nodetool drain
   nodetool snapshot

Take note of the directory name that nodetool gives you, and copy all the directories having this name under ``/var/lib/scylla`` to a backup device.

When the upgrade is complete (all nodes), the snapshot should be removed by ``nodetool clearsnapshot -t <snapshot>``, or you risk running out of space.

Backup configuration file
-------------------------

.. code:: sh

   sudo cp -a /etc/scylla/scylla.yaml /etc/scylla/scylla.yaml.backup-2018.x.z

If you upgrade from 2018.1.x(x<5) to 2018.1.y(y>=5), you need to backup more configure files.

.. code:: sh

   for conf in $(cat /var/lib/dpkg/info/scylla-*server.conffiles /var/lib/dpkg/info/scylla-*conf.conffiles /var/lib/dpkg/info/scylla-*jmx.conffiles | grep -v init ); do sudo cp -v $conf $conf.backup-2.1; done

Gracefully stop the node
------------------------

.. code:: sh

   sudo service scylla-server stop

Download and install the new release
------------------------------------
Before upgrading, check what version you are running now using ``dpkg -s scylla-server``. You should use the same version in case you want to |ROLLBACK|_ the upgrade. If you are not running a 2018.x.y version, stop right here! This guide only covers 2018.x.y to 2018.x.z upgrades.

To upgrade:

1. Update the |APT|_ to **2018.x**
2. Install

.. code:: sh

   sudo apt-get update
   sudo apt-get dist-upgrade scylla-enterprise

Answer ‘y’ to the first two questions.

Start the node
--------------

.. code:: sh

   sudo service scylla-server start

Validate
--------
1. Check cluster status with ``nodetool status`` and make sure **all** nodes, including the one you just upgraded, are in UN status.
2. Use ``curl -X GET "http://localhost:10000/storage_service/scylla_release_version"`` to check scylla version.
3. Check scylla-server log (check ``/var/log/upstart/scylla-server.log`` for Ubuntu 14.04, execute ``journalctl _COMM=scylla`` for Ubuntu 16.04) and ``/var/log/syslog`` to validate there are no errors.
4. Check again after 2 minutes, to validate no new issues are introduced.

Once you are sure the node upgrade is successful, move to the next node in the cluster.

Rollback Procedure
==================

.. include:: /upgrade/_common/warning_rollback.rst

The following procedure describes a rollback from Scylla Enterprise release 2018.x.z to 2018.x.y. Apply this procedure if an upgrade from 2018.x.y to 2018.x.z failed before completing on all nodes. Use this procedure only for nodes you upgraded to 2018.x.z

Scylla rollback is a rolling procedure which does **not** require full cluster shutdown.
For each of the nodes rollback to 2018.x.y, you will:

* Gracefully shutdown Scylla
* Downgrade to previous release
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

Downgrade to previous release
-----------------------------
1. install

Scylla-enterprise 2018.1.5 starts to use new gcc packages, the gcc packages should be removed before downgrade if you upgrade from 2018.1.x(x<5) to 2018.1.y(y>=5).

.. code:: sh

   sudo apt-get remove scylla-gcc73\* -y


.. code:: sh

   sudo apt-get install scylla-enterprise=2018.x.y\* scylla-enterprise-server=2018.x.y\* scylla-enterprise-jmx=2018.x.y\* scylla-enterprise-tools=2018.x.y\* scylla-enterprise-tools-core=2018.x.y\* scylla-enterprise-kernel-conf=2018.x.y\* scylla-enterprise-conf=2018.x.y\*

Answer ‘y’ to the first two questions.

Restore the configuration file
------------------------------

.. code:: sh

   sudo rm -rf /etc/scylla/scylla.yaml
   sudo cp -a /etc/scylla/scylla.yaml.backup-2018.x.z /etc/scylla/scylla.yaml

If you upgrade from 2018.1.x(x<5) to 2018.1.y(y>=5), you need to restore more config files.

.. code:: sh

   for conf in $(cat /var/lib/dpkg/info/scylla-*server.conffiles /var/lib/dpkg/info/scylla-*conf.conffiles /var/lib/dpkg/info/scylla-*jmx.conffiles | grep -v init ); do sudo cp -v $conf.backup-2.1 $conf; done
   sudo systemctl daemon-reload (Ubuntu 16.04 and Debian 8)

Start the node
--------------

.. code:: sh

   sudo service scylla-server start

Validate
--------
Check upgrade instruction above for validation. Once you are sure the node rollback is successful, move to the next node in the cluster.
