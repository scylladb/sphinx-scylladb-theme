Enable Authentication
=====================

Authentication is the process where login accounts and their passwords are verified and the user is allowed access into the database. Authentication is done internally within Scylla and is not done with a third party. Users and passwords are created with roles using a ``CREATE ROLE`` statement. Refer to `Grant Authorization CQL Reference </operating-scylla/security/authorization>`_ for details.  

This procedure enables authentication on the Scylla servers. It is intended to be used when you do **not** have applications running with Scylla/Cassandra drivers

.. warning:: Once you enable authentication, all clients (such as applications using Scylla/Apache Cassandra drivers) will **stop working**, until they are updated or reconfigured to work with Authentication.

If this downtime is not an option, you can follow the instructions in `Enable and Disable Authentication Without Downtime </operating-scylla/security/runtime-authentication>`_ which, using a transient state, allows clients work with or without authentication at the same time. In this state, you can update the clients (application using Scylla/Apache Cassandra drivers) one at the time. Once all the clients are using Authentication, you can enforce authentication on all Scylla nodes as well.

**Procedure** 

1. For each Scylla node in the cluster edit the ``/etc/scylla/scylla.yaml`` file, and change the ``authenticator`` parameter from ``AllowAllAuthenticator`` to ``PasswordAuthenticator``.

.. code-block:: yaml

   authenticator: PasswordAuthenticator

2. Set the ``system_auth`` keyspace replication factor to be equal to the number of nodes in the datacenter. This makes sure that the user's information is kept highly available for the cluster. If you do not do this and the node that holds this information fails, any user whose information is on that node (including yours) will be denied access.

For **production environments** use only ``NetworkTopologyStrategy``.

* Single DC (SimpleStrategy)

.. code-block:: cql

   ALTER KEYSPACE system_auth WITH REPLICATION =
     { 'class' : 'SimpleStrategy', 'replication_factor' : <new_rf> };

For example

.. code-block:: cql

   ALTER KEYSPACE system_auth WITH REPLICATION =
     { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };

* Multi - DC (NetworkTopologyStrategy)

.. code-block:: cql

   ALTER KEYSPACE system_auth WITH REPLICATION =
     {'class' : 'NetworkTopologyStrategy', 'dc1' : <new_rf>, 'dc2' : <new_rf>};

For example

.. code-block:: cql

   ALTER KEYSPACE system_auth WITH REPLICATION =
     {'class' : 'NetworkTopologyStrategy', 'dc1' : 3, 'dc2' : 3};

3. Restart  Scylla

.. include:: /rst_include/scylla-commands-restart-index.rst

4. Start cqlsh with the default superuser username and password The default username is ``cassandra`` default password is ``cassandra``. You can change this later if you are enabling authorization.  

.. code-block:: cql

   cqlsh -u cassandra -p cassandra

5. Run a repair on the ``system_auth`` keyspace on **all** the nodes in the cluster.
	
For example:
	
.. code-block:: none
	
   nodetool repair system_auth

6. If you want to create users and roles, continue to `Enable Authorization </operating-scylla/security/enable-authorization/>`_.


Additional Resources
--------------------

* :doc:`Enable and Disable Authentication Without Downtime </operating-scylla/security/runtime-authentication/>`
* :doc:`Enable Authorization </operating-scylla/security/enable-authorization/>` 
* :doc:`Authorization </operating-scylla/security/authorization/>` 



