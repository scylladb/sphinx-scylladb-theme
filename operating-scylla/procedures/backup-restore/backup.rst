================
Backup your Data
================

Even though Scylla is a fault-tolerant system, it is recommended to regularly backup the data to an external storage.
Backup is a per node procedure. Make sure to backup each node in your cluster.
Backup includes two procedures. These are:

* Full_ Backup_ - copy the entire data of a node

* Incremental_ - updates (delta) - flushed SSTables

.. _Backup: /operating-scylla/procedures/backup-restore/backup/#full-backup-snapshots
.. _Full: /operating-scylla/procedures/backup-restore/backup/#full-backup-snapshots


.. _Incremental: /operating-scylla/procedures/backup-restore/backup/#incremental-backup

Full Backup - Snapshots
=======================

Snapshots are taken using `nodetool snapshot`_. The command first flushes the MemTables from memory to SSTables on disk, then create a hard link for each SSTable in each keyspace.
With time, SSTables are compacted, but the hard link keeps a copy of each file. This takes up an increasing amount of disk space. It is important to clear space by `clean unnecessary snapshots`_.

.. _`nodetool snapshot`: /operating-scylla/nodetool-commands/snapshot

.. _`clean unnecessary snapshots`: /operating-scylla/procedures/backup-restore/delete_snapshot

**Procedure**

| 1. Data can only be restored from a snapshot if the table schema and data exist in a backup.. Backup your schema, with the following command:

| ``$: cqlsh -e "DESC SCHEMA" > <schema_name.cql>``

For example:

| ``$: cqlsh -e "DESC SCHEMA" > db_schema.cql``

|
| 2. Take a snaphost, including every keyspace you want to backup.

| ``$ nodetool snapshot <KEYSPACE_NAME>``

| For example:

| ``$ nodetool snapshot mykeyspace``

| The snapshot is created under Scylla data directory ``/var/lib/scylla/data``
| It will have the following structure:
| ``keyspace_name/table_name-UUID/snapshots/snapshot_name``

| For example:
| ``/mykeyspace/team_roster-91cd2060f99d11e6a47a000000000000/snapshots/1487847672222``

From one of the nodes, recreate the schema. Repeat these steps for each node in the cluster.

Incremental Backup
==================

| Enabling the incremental backup (disabled by default) will create a hard-link from each SSTable, right after it is **flushed**, to a backups directory.
| For a complete point in time backup the following is required: a snapshot plus incremental backups and commit logs since from the time of the snapshot. Make sure to delete unnecessary incremental backups, Scylla does not do this automatically.

**Procedure**

| 1. In the ``/etc/scylla/scylla.yaml`` file set the ``incremental backups`` parameters to ``true`` and restart the Scylla service. Snapshot are created under Scylla data directory ``/var/lib/scylla/data``
| with the following structure:
| ``keyspace_name/table_name-UUID/backups/backups_name``

| For example:
| ``/mykeyspace/team_roster-91cd2060f99d11e6a47a000000000000/backups/1437827672721``


Additional Resources
====================

* `Scylla Snapshots`_


.. _`Scylla Snapshots`: /kb/snapshots

