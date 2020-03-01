Enable and Disable Authentication Without Downtime
==================================================

.. versionadded:: 2.1

.. contents::
   :local:
   :depth: 2

Authentication is the process where login accounts and their passwords are verified and the user is allowed access into the databse. Authentication is done internally within Scylla and is not done with a third party. Users and passwords are created with `roles </operating-scylla/security/authorization>`_ using a ``CREATE ROLE`` statement. This procedure enables authentication on the Scylla servers using a transit state, allowing clients work with or without authentication at the same time. In this state, you can update the clients (application using Scylla/Apache Cassandra drivers) one at the time. Once all the clients are using Authentication, you can enforce authentication on all Scylla nodes as well. If you would rather perform a faster authentication procedure where all clients (application using Scylla/Apache Cassandra drivers) will stop working, until they are updated to work with Authentication, refer to `Enable Authentication </operating-scylla/security/runtime-authentication>`_.



Enable Authentication Without Downtime
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This procedure allows you to enable authentication on a live Scylla cluster without downtime.

Prerequisites
-------------

Set the ``system_auth`` keyspace replication factor the number of nodes in the datacenter and set the class to ``NetworkTopologyStrategy`` (required in production environments):

For example:

* Single DC (NetworkTopologyStrategy)

.. code-block:: cql

   ALTER KEYSPACE system_auth WITH REPLICATION =
     { 'class' : 'NetworkTopologyStrategy', 'dc1' : <new_rf> };

* Multi - DC (NetworkTopologyStrategy)

.. code-block:: cql

   ALTER KEYSPACE system_auth WITH REPLICATION =
     {'class' : 'NetworkTopologyStrategy', 'dc1' : <new_rf>, 'dc2' : <new_rf>};

Procedure
---------

1. Update the scylla.yaml ``authenticator`` parameter for all the nodes in the cluster. **Change** authenticator: AllowAllAuthenticator **to** authenticator: com.scylladb.auth.TransitionalAuthenticator

.. code-block:: yaml

    authenticator:  com.scylladb.auth.TransitionalAuthenticator

2. Run the `nodetool drain </operating-scylla/nodetool-commands/drain/>`_ command (Scylla stops listening to its connections from the client and other nodes).

3. Restart the nodes one by one to apply the effect.

.. include:: /rst_include/scylla-commands-restart-index.rst

4. Login with the default superuser credentials and create an authenticated user with strong password.

For example:

.. code-block:: cql

    cqlsh -ucassandra -pcassandra    

    cassandra@cqlsh> CREATE USER scylla WITH PASSWORD '123456' AND LOGIN = true AND SUPERUSER = true;
    cassandra@cqlsh> list users;

    name      |super
    ----------+-------
    cassandra |True
    scylla    |True

5. Login with the new user created and drop the superuser cassandra.

.. code-block:: cql

   cqlsh -u scylla -p 123456

   scylla@cqlsh> DROP USER cassandra;

   scylla@cqlsh> list users;

   name      |super
   ----------+-------
   scylla    |True

6. Update the scylla.yaml ``authenticator`` parameter for all the nodes in the cluster.

* **change** authenticator: com.scylladb.auth.TransitionalAuthenticator **to** authenticator: PasswordAuthenticator

.. code-block:: yaml
 
    authenticator: PasswordAuthenticator

7. Restart the nodes one by one to apply the effect.

.. include:: /rst_include/scylla-commands-restart-index.rst

8. Run repair on the ``system_auth`` keyspace, one node at a time on all the nodes in the cluster.

   For example:

   .. code-block:: cql

      nodetool repair system_auth

9. Verify that all the client applications are working correctly with authentication enabled.
                              

Disable Authentication Without Downtime
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This procedure allows you to disable authentication on a live Scylla cluster without downtime. Once disabled, you will have to re-enable authentication where required. 

Procedure
---------

1. Update the scylla.yaml ``authenticator`` parameter for all the nodes in the cluster.

* **change** authenticator: PasswordAuthenticator **to** authenticator: com.scylladb.auth.TransitionalAuthenticator

.. code-block:: yaml

    authenticator: com.scylladb.auth.TransitionalAuthenticator

2. Restart the nodes one by one to apply the effect.

.. code-block:: shell

   sudo systemctl restart scylla-server

3. Update the scylla.yaml ``authenticator`` parameter for all the nodes in the cluster. **Change** authenticator: com.scylladb.auth.TransitionalAuthenticator **to** authenticator: AllowAllAuthenticator
 
.. code-block:: yaml

    authenticator: AllowAllAuthenticator 

4. Restart the nodes one by one to apply the effect.

.. include:: /rst_include/scylla-commands-restart-index.rst

5. Run repair on the ``system_auth`` keyspace, one node at a time on all the nodes in the cluster.

For example:

.. code-block:: cql

   nodetool repair system_auth

6. Verify that all the client applications are working correctly with authentication disabled. 

