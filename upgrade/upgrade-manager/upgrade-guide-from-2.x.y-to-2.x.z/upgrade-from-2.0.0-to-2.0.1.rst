======================================================
Scylla Manager Upgrade - Scylla Manager 2.0.0 to 2.0.1
======================================================

.. toctree::
   :maxdepth: 2

Applicable versions
===================

This guide covers upgrading Scylla Manager version 2.0.0 to version 2.0.1, on the following platforms:

- Red Hat Enterprise Linux, version 7
- CentOS, version 7
- Debian, version 9
- Ubuntu, versions 16.04, 18.04

Upgrade Procedure
=================

.. note:: In Scylla Manager 2.0.0 new component called Scylla Manager Agent is introduced which is running on each scylla node in the cluster as a sidecar. Upgrading this component means commands have to be executed for each node separately.

Upgrade procedure for the Scylla Manager includes upgrade of three components server, client, and the agent. Entire cluster shutdown is NOT needed. Scylla will be running while the manager components are upgraded. Overview of the required steps:

- Stop all Scylla Manager tasks (or wait for them to finish)
- Stop the Scylla Manager Server 2.0.0
- Stop the Scylla Manager Agent 2.0.0 on all nodes
- Upgrade the Scylla Manager Server and Client to 2.0.1
- Upgrade the Scylla Manager Agent to 2.0.1 on all nodes
- Start the Scylla Manager Agent 2.0.1 on all nodes
- Start the Scylla Manager Server 2.0.1
- Validate status of the cluster

Upgrade steps
=============

Stop all Scylla Manager tasks (or wait for them to finish)
----------------------------------------------------------

**On the Manager Server** check current status of the manager tasks:

.. code:: sh

    sctool task list -c <cluster>

None of the listed tasks should have status in RUNNING.

Stop the Scylla Manager Server 2.0.0
------------------------------------

**On the Manager Server** instruct Systemd to stop the server process:

.. code:: sh

    sudo systemctl stop scylla-manager

Ensure that it is stopped with:

.. code:: sh

    sudo systemctl status scylla-manager

It should have a status of *“Active: inactive (dead)”*.

Stop the Scylla Manager Agent 2.0.0 on all nodes
------------------------------------------------

**On each scylla node** in the cluster run:

.. code:: sh

    sudo systemctl stop scylla-manager-agent

Ensure that it is stopped with:

.. code:: sh

    sudo systemctl status scylla-manager-agent

It should have a status of *“Active: inactive (dead)”*.

Upgrade the Scylla Manager Server and Client to 2.0.1
-----------------------------------------------------

**On the Manager Server** instruct package manager to update server and the client:

CentOS, Red Hat:

.. code:: sh

    sudo yum update scylla-manager-server scylla-manager-client -y

Debian, Ubuntu:

.. code:: sh

    sudo apt-get update
    sudo apt-get install scylla-manager-server scylla-manager-client -y

Upgrade the Scylla Manager Agent to 2.0.1 on all nodes
------------------------------------------------------

**On each scylla node** instruct package manager to update the agent:

CentOS, Red Hat:

.. code:: sh

    sudo yum update scylla-manager-agent -y

Debian, Ubuntu:

.. code:: sh

    sudo apt-get update
    sudo apt-get install scylla-manager-agent -y

Start the Scylla Manager Agent 2.0.1 on all nodes
-------------------------------------------------

**On each scylla node** instruct Systemd to start the agent process:

.. code:: sh

    sudo systemctl start scylla-manager-agent

Ensure that it is running with:

.. code:: sh

    sudo systemctl status scylla-manager-agent

It should have a status of *“Active: active (running)”*.

Start the Scylla Manager Server 2.0.1
-------------------------------------

**On the Manager Server** instruct Systemd to start the server process:

.. code:: sh

    sudo systemctl stop scylla-manager

Ensure that it is stopped with:

.. code:: sh

    sudo systemctl status scylla-manager

It should have a status of *“Active: active (running)”*.

Validate status of the cluster
------------------------------

**On the Manager Server** check the version of the client and the server:

.. code:: sh

    sctool version
    Client version: 2.0.1-0.20200123.7cf18f6b
    Server version: 2.0.1-0.20200123.7cf18f6b

Check that cluster is up:

.. code:: sh

    sctool status -c <cluster>

All running nodes should be up.

Rollback Procedure
==================

.. note:: Rolling back to 2.0.0 is not recommended because 2.0.1 contains bug fixes and performance optimizations so you will be going back to a lesser version. This should be only used as a last resort.

Rollback procedure contains the same steps as upgrade but with downgrading the components to older version:

- Stop all Scylla Manager tasks (or wait for them to finish)
- Stop the Scylla Manager Server 2.0.1
- Stop the Scylla Manager Agent 2.0.1 on all nodes
- Downgrade the Scylla Manager Server and Client to 2.0.0
- Downgrade the Scylla Manager Agent to 2.0.0 on all nodes
- Start the Scylla Manager Agent 2.0.0 on all nodes
- Start the Scylla Manager Server 2.0.0
- Validate status of the cluster

Rollback steps
==============

Stop all Scylla Manager tasks (or wait for them to finish)
----------------------------------------------------------

**On the Manager Server** check current status of the manager tasks:

.. code:: sh

    sctool task list -c <cluster>

None of the listed tasks should have status in RUNNING.

Stop the Scylla Manager Server 2.0.1
------------------------------------

**On the Manager Server** instruct Systemd to stop the server process:

.. code:: sh

    sudo systemctl stop scylla-manager

Ensure that it is stopped with:

.. code:: sh

    sudo systemctl status scylla-manager

It should have a status of *“Active: inactive (dead)”*.

Stop the Scylla Manager Agent 2.0.1 on all nodes
------------------------------------------------

**On each scylla node** in the cluster run:

.. code:: sh

    sudo systemctl stop scylla-manager-agent

Ensure that it is stopped with:

.. code:: sh

    sudo systemctl status scylla-manager-agent

It should have a status of *“Active: inactive (dead)”*.

Downgrade the Scylla Manager Server and Client to 2.0.0
-------------------------------------------------------

**On the Manager Server** instruct package manager to downgrade server and the client:

CentOS, Red Hat:

.. code:: sh

    sudo yum downgrade scylla-manager-server-2.0.0* scylla-manager-client-2.0.0* -y

Debian, Ubuntu:

.. code:: sh

    sudo apt-get install scylla-manager-server=2.0.0 scylla-manager-client=2.0.0 -y

Downgrade the Scylla Manager Agent to 2.0.0 on all nodes
--------------------------------------------------------

**On each scylla node** instruct package manager to downgrade the agent:

CentOS, Red Hat:

.. code:: sh

    sudo yum downgrade scylla-manager-agent-2.0.0* -y

Debian, Ubuntu:

.. code:: sh

    sudo apt-get install scylla-manager-agent=2.0.0 -y

Start the Scylla Manager Agent 2.0.0 on all nodes
-------------------------------------------------

On all nodes instruct Systemd to start the agent process:

.. code:: sh

    sudo systemctl start scylla-manager-agent

Ensure that it is running with:

.. code:: sh

    sudo systemctl status scylla-manager-agent

It should have a status of *“Active: active (running)”*.

Start the Scylla Manager Server 2.0.0
-------------------------------------

**On the Manager Server** instruct Systemd to start the server process:

.. code:: sh

    sudo systemctl stop scylla-manager

Ensure that it is stopped with:

.. code:: sh

    sudo systemctl status scylla-manager

It should have a status of *“Active: active (running)”*.

Validate status of the cluster
------------------------------

**On the Manager Server** check the version of the client and the server:

.. code:: sh

    sctool version
    Client version: 2.0.0
    Server version: 2.0.0

Check that cluster is up:

.. code:: sh

    sctool status -c <cluster>

All running nodes should be up.

