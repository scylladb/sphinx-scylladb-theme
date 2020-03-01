=====================
Scylla Auditing Guide
=====================

Available only for Scylla Enterprise 2018.1 or later
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the auditing feature allows the administrator to know "who did / looked at / changed what and when."
It also allows logging some or all the activities a user performs on Scylla cluster.

Enabling auditing is controlled by the ``audit:`` parameter in the ``scylla.yaml`` file. 
There are three options of auditing which can be set:

* none - This is the default value, and it means that audit is disabled.
* table - This means that audit is on and messages are stored in a Scylla table.
* syslog - This means that audit is on and messages are sent to syslog.

Using any other value for the configuration, results an error at Scylla startup.

Configuring Audit
-----------------

Audit can be tuned using the following flags or scylla.yaml entries:

==================  ==================================  ========================================================================================================================
Flag                Default Value                       Description
==================  ==================================  ========================================================================================================================
audit_categories    ""                                  Comma separated list of statement categories that should be audited
------------------  ----------------------------------  ------------------------------------------------------------------------------------------------------------------------
audit_tables        “”                                  Comma separated list of table names that should be audited, in the format of <keyspacename>.<tablename>
------------------  ----------------------------------  ------------------------------------------------------------------------------------------------------------------------
audit_keyspaces     “”                                  Comma separated list of keyspaces that should be audited
==================  ==================================  ========================================================================================================================

To audit all the tables in a keyspace: set the ``audit_keyspaces`` with the relevant keyspace and leave ``audit_tables`` empty.

You can use DCL, AUTH, and ADMIN audit categories without including any keyspace or table.

audit_categories parameter description
**************************************

=========  =========================================================================================
Parameter  Logs Description
=========  =========================================================================================
AUTH       Logs login events
---------  -----------------------------------------------------------------------------------------
DML        Logs insert, update, delete, and other data manipulation language (DML) events
---------  -----------------------------------------------------------------------------------------
DDL        Logs object and role create, alter, drop, and other data definition language (DDL) events
---------  -----------------------------------------------------------------------------------------
DCL        Logs grant, revoke, create role, drop role, and list roles events
---------  -----------------------------------------------------------------------------------------
QUERY      Logs all queries
---------  -----------------------------------------------------------------------------------------
ADMIN*     Logs service level operations: create, alter, drop, attch, detach, list
=========  =========================================================================================

* ADMIN for `service level </using-scylla/workload-prioritization/#service-level-management>`_ auditing is available for Scylla Enterprise customers version 2019.1 and above.

Note that audit for every DML or QUERY might result in impacting performance and consume a lot of storage.



Audit Storage
^^^^^^^^^^^^^

Auditing messages can be sent to syslog_ or store in a Scylla table_. 

.. _syslog: /operating-scylla/security/auditing/#syslog-storage

.. _table: /operating-scylla/security/auditing/#table-storage

Currently, auditing messages can only be saved to one location at a time. You cannot log into both a table and the syslog.

Syslog Storage
--------------

With this option, messages are sent to syslog. 

Procedure
---------

1. Edit the ``audit`` parameter under ``scylla.yaml`` file.

For example:

.. code-block:: shell

   # audit setting
   # by default, Scylla does not audit anything.
   # It is possible to enable auditing to the following places:
   #   - audit.audit_log column family by setting the flag to "table"
   audit: "syslog"
   #
   # List of statement categories that should be audited.
   audit_categories: "DCL,DDL,AUTH"
   # 
   # List of tables that should be audited.
   audit_tables: "mykespace.mytable"
   #
   # List of keyspaces that should be fully audited.
   # All tables in those keyspaces will be audited
   audit_keyspaces: "mykespace"

2. Restart Scylla node 

.. include:: /rst_include/scylla-commands-restart-index.rst

By default, audit messages are written to the same destination as using Scylla logging_, with scylla-audit as process name.

.. _logging: /getting-started/logging/

Logging output example (drop table): 

.. code-block:: shell

   Mar 18 09:53:52 ip-10-143-2-108 scylla-audit[28387]: "10.143.2.108", "DDL", "ONE", "team_roster", "nba", "DROP TABLE nba.team_roster ;", "127.0.0.1", "anonymous", "false"

To redirect the syslog output to a file, follow the steps below (available only for CentOS) :

1. Install rsyslog sudo ``dnf install rsyslog``.
2. Edit ``/etc/rsyslog.conf`` and append the following to the file: ``if $programname contains 'scylla-audit' then /var/log/scylla-audit.log``.
3. Start rsyslog ``systemctl start rsyslog``.
4. Enable rsyslog ``systemctl enable rsyslog``.

Logging output example:


Table Storage
-------------

With this option messages are stored in a Scylla table named ``audit.audit_log``. 

For example:

.. code-block:: shell   
   
   CREATE TABLE IF NOT EXISTS audit.audit_log (
         date timestamp,
         node inet,
         event_time timeuuid,
         category text,
         consistency text,
         table_name text,
         keyspace_name text,
         operation text,
         source inet,
         username text,
         error boolean,
         PRIMARY KEY ((date, node), event_time));

Procedure
---------

1. Edit the ``audit`` parameter under ``scylla.yaml`` file.

For example:

.. code-block:: shell

   # audit setting
   # by default, Scylla does not audit anything.
   # It is possible to enable auditing to the following places:
   #   - audit.audit_log column family by setting the flag to "table"
   audit: "table"
   #
   # List of statement categories that should be audited.
   audit_categories: "DCL,DDL,AUTH"
   # 
   # List of tables that should be audited.
   audit_tables: "mykespace.mytable"
   #
   # List of keyspaces that should be fully audited.
   # All tables in those keyspaces will be audited
   audit_keyspaces: "mykespace"

2. Restart Scylla node 

.. include:: /rst_include/scylla-commands-restart-index.rst

Table output example (drop table):

.. code-block:: shell

   SELECT * FROM audit.audit_log ;

    date                    | node         | event_time                           | category | consistency | error | keyspace_name | operation                    | source          | table_name  | username |
   -------------------------+--------------+--------------------------------------+----------+-------------+-------+---------------+------------------------------+-----------------+-------------+----------+
   2018-03-18 00:00:00+0000 | 10.143.2.108 | 3429b1a5-2a94-11e8-8f4e-000000000001 |      DDL |         ONE | False |           nba | DROP TABLE nba.team_roster ; | 127.0.0.1       | team_roster | Scylla   | 
   (1 row)

See also:

:doc:`Authorization</operating-scylla/security/authorization>` 

:doc:`Authentication</operating-scylla/security/authentication>` 







