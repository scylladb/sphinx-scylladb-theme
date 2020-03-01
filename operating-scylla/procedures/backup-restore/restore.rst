Restore from a Backup and Incremental Backup
********************************************

Restoring a keyspace from a backup requires all snapshot files of the tables, and (if available) incremental backup files taken after the snapshot. Before restoring from backup, the table data must be truncated, making sure that the existing data does not overwrite the restored data.

---------
Procedure
---------

| 1. From one of the nodes, recreate the schema.

``cqlsh -e "SOURCE '/path_to_schema/<schema_name.cql>'"``

| For example:

``cqlsh -e "SOURCE 'centos/db_schema.cql'"``
Repeat the following steps for each node in the cluster:

| 2. Run the :doc:`nodetool drain </operating-scylla/nodetool-commands/drain/>` command to ensure the data is flushed to the SSTables

| 3. Shut down the node

.. include:: /rst_include/scylla-commands-stop-index.rst

| 4. Delete all the files in the commitlog. Deleting the commitlog will prevent the newer insert from overriding the restored data.

``sudo rm -rf /var/lib/scylla/commitlog/*``

| 5. Delete all the files in the keyspace_name_table. Note that by default the snapshots are created under Scylla data directory ``/var/lib/scylla/data/keyspace_name/table_name-UUID/``.
| Make sure NOT to delete the existing snapshots in the process.

| For example:

.. code-block:: shell

   sudo ll /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000

   -rw-r--r-- 1 scylla   scylla     66 Mar  5 09:19 nba-team_players-ka-1-CompressionInfo.db
   -rw-r--r-- 1 scylla   scylla    669 Mar  5 09:19 nba-team_players-ka-1-Data.db
   -rw-r--r-- 4 scylla   scylla     10 Mar  5 08:46 nba-team_players-ka-1-Digest.sha1
   -rw-r--r-- 1 scylla   scylla     24 Mar  5 09:19 nba-team_players-ka-1-Filter.db
   -rw-r--r-- 1 scylla   scylla    218 Mar  5 09:19 nba-team_players-ka-1-Index.db
   -rw-r--r-- 1 scylla   scylla     38 Mar  5 09:19 nba-team_players-ka-1-Scylla.db
   -rw-r--r-- 1 scylla   scylla   4446 Mar  5 09:19 nba-team_players-ka-1-Statistics.db
   -rw-r--r-- 1 scylla   scylla     89 Mar  5 09:19 nba-team_players-ka-1-Summary.db
   -rw-r--r-- 4 scylla   scylla    101 Mar  5 08:46 nba-team_players-ka-1-TOC.txt
   drwx------ 5 scylla   scylla     69 Mar  6 08:14 snapshots
   drwx------ 2 scylla   scylla      6 Mar  5 08:40 upload

   sudo rm -f  /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000/*

     rm: cannot remove ‘/var/lib/scylla/data/nba/team_roster-c019f8108fda11e8b16a000000000001/snapshots’: Is a directory
     rm: cannot remove ‘/var/lib/scylla/data/nba/team_roster-c019f8108fda11e8b16a000000000001/upload’: Is a directory

   sudo ll /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000/

     drwx------ 5 scylla   scylla     69 Mar  6 08:14 snapshots
     drwx------ 2 scylla   scylla      6 Mar  5 08:40 upload


| 6. Select the snapshot you want to restore (usualy the most recent one) 

.. code-block:: shell

   /var/lib/scylla/data/keyspace_name/table_name-UUID/snapshots/<snapshot_name>

| For example:

.. code-block:: shell

   cd /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000/snapshots/1487847672222


| 7. Copy the snapshots directory content to the ``/var/lib/scylla/data/keyspace_name/table_name-UUID/`` directory

| For example:

.. code-block:: shell

   sudo cp -r * /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000

| 8. If you have incremental backup files, copy them from the **backups** folder ``/var/lib/scylla/data/keyspace_name/table_name-UUID/backups/<backups_name>`` to  the ``/var/lib/scylla/data/keyspace_name/table_name-UUID/`` directory

| For example:

.. code-block:: shell

   sudo cp -r * /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000

| 9. Make sure that all files are owned by the ``scylla`` user and group:

.. code-block:: shell

   sudo chown -R scylla:scylla /var/lib/scylla/data/mykeyspace/team_players-6e856600017f11e790f4000000000000

| 10. Start the node

.. include:: /rst_include/scylla-commands-start-index.rst

| 11. Run ``nodetool repair`` command to guarantee that your data is consistent with other nodes.

After performing the above on all nodes, repair the cluster with nodetool repair. This makes sure that the data is consistent on all nodes and between each node.

