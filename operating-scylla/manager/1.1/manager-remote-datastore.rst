

======================================
Scylla Manager with a remote datastore
======================================

.. versionadded:: 1.1 Scylla Manager

.. contents:: 
    :depth: 1
    :local:

When you install Scylla Manager, it typically installs a local instance of Scylla to use as its backend data server. You are not required to use the local instance and can install Scylla Manager’s backend server on a remote server, or on a third-party database. 

Requirements
============

* Scylla Cluster to be used as Scylla Manager persistent backend
* ``scylla-manager`` installed


Install Scylla Manager with a remote datastore
==============================================

**Procedure**

1. Using an editor open the Scylla Manager configuration file ``/etc/scylla-manager/scylla-manager.yaml`` .
   Edit the ``database.hosts`` parameter. Change the IP address to the IP address for the remote datastore.  

   Optionally, edit the ``database.user`` and ``database.password`` parameters, to change the database credentials. By default, there is no username or password.

.. code-block:: none

   # Scylla Manager database, used to store management data.

   database:
   hosts:
     - 192.0.2.0

.. code-block:: none

   # Database credentials
   # user: scylla-manager

   user: scylla-manager

2. The default replication factor is set to 1. If you want to use a simple replication strategy (SimpleStrategy), adjust the replication factor. Refer to `Scylla Architecture - Fault Tolerance </architecture/architecture-fault-tolerance>`_ for more information. 


.. code-block:: none

   # replication_factor: 1
   
   replication_factor: 3

3. When Scylla Manager starts, it checks for a keyspace to write its data to. The keyspace can be named with any name you choose. 

.. code-block:: none

   # keyspace: scylla_manager
   
   keyspace: my_keyspace

4. Continue with the `Scylla Manager Setup <../manager-setup/>`_.  
 
Related References
==================

* :doc:`Scylla Architecture - Fault Tolerance </architecture/architecture-fault-tolerance>` - Deep dive into Scylla Fault Tolerance and replication factor

