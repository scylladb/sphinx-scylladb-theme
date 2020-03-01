
======================================
Enable Authentication Without Downtime
======================================

Production ready in Scylla 2.1
..............................

This procedure allows you to enable authentication on a live Scylla cluster without downtime.

Prerequisites
-------------

For production environment use only ``NetworkTopologyStrategy``.

Set the ``system_auth`` keyspace replication factor to 3 - 5 nodes per datacenter:

For example:

* Single DC (NetworkTopologyStrategy)

.. code-block:: cql

   ALTER KEYSPACE system_auth WITH REPLICATION =
     { 'class' : 'NetworkTopologyStrategy', 'replication_factor' : <new_rf> };

* Multi - DC (NetworkTopologyStrategy)

.. code-block:: cql

   ALTER KEYSPACE system_auth WITH REPLICATION =
     {'class' : 'NetworkTopologyStrategy', 'dc1' : <new_rf>, 'dc2' : <new_rf>};

Procedure
---------

1. Update the scylla.yaml parameters ``authenticator`` and ``authorizer`` for all the nodes in the cluster.

.. code-block:: shell

    authenticator: 'com.scylladb.auth.TransitionalAuthenticator'
    authorizer: 'com.scylladb.auth.TransitionalAuthorizer'

2. Restart the nodes one by one to apply the effect.

.. code-block:: shell

   sudo systemctl restart scylla-server

3. Login with the default super user credentials and create an authenticated user with strong password.

For example:

.. code-block:: cql

    cqlsh -ucassandra -pcassandra    

    cassandra@cqlsh> CREATE USER scylla WITH PASSWORD '123456' SUPERUSER ;
    cassandra@cqlsh> list users;

    name      |super
    ----------+-------
    cassandra |True
    scylla    |True

4. Login with the new user created and drop the superuser cassandra.

.. code-block:: cql

   cqlsh -u scylla -p 123456

   scylla@cqlsh> DROP USER cassandra;

   scylla@cqlsh> list users;

   name      |super
   ----------+-------
   scylla    |True

5. Update the scylla.yaml parameters ``PasswordAuthenticator`` and ``CassandraAuthorizer`` for all the nodes in the cluster.

.. code-block:: cql
 
    authenticator: 'PasswordAuthenticator'
    authorizer: 'CassandraAuthorizer'

6. Restart the nodes one by one to apply the effect.

.. code-block:: cql

   sudo systemctl restart scylla-server

7. Run repair on the ``system_auth`` keyspace, one node at a time on all the nodes in the cluster.

For example:

.. code-block:: cql

   nodetool repair system_auth

8. Verify that all the client applications are working correctly with authentication enabled.
                              
:doc:`Authorization</operating-scylla/security/authorization/>`
