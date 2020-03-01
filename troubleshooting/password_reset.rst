Reset Authenticator Password
============================

This procedure describes the steps that need to be done in a case a user lost his password and can not reset it with a super user. 
The procedure requires a cluster downtime and all the system_auth information will be removed.

Procedure
.........

| 1. Stop Scylla nodes (**Stop all the nodes in the cluster**).

.. code-block:: shell 

   sudo systemctl stop scylla-server

| 2. Remove your tables under ``/var/lib/scylla/data/system_auth/``.

.. code-block:: shell  

   rm -rf /var/lib/scylla/data/system_auth/

| 3. Start Scylla nodes.

.. code-block:: shell 

   sudo systemctl start scylla-server

| 4. Verify that you can log in to your node using ``cqlsh`` command.
| The access is only possible using Scylla superuser.

.. code-block:: cql
 
   cqlsh -u cassandra -p cassandra

| 5. Recreate the users

.. include:: /troubleshooting/_common/ts-return.rst
