================
Restore a Backup
================

.. versionadded:: 2.0 Scylla Manager

This document provides information on how to restore data from backups that were taken using Scylla Manager.

There are two restore scenarios:

#. Backup to the same topology cluster.
   For example, restore data to the same source cluster.
#. Backup to a different topology cluster.
   For example, restore data to a smaller or bigger cluster, a cluster with different rack or DC topology, or different token distribution.

**Workflow**

#. `Prepare for restore`_
#. `Upload data to Scylla`_

Prepare for restore
===================

No matter which backup scenario you are using the procedures in this workflow apply.

**Workflow**

#. `Identify relevant backup files`_
#. `Restore the schema`_

Identify relevant backup files
------------------------------

**Procedure**

#. List all available backups and choose the one you would like to restore.
   Run: `sctool backup list <../sctool/#backup-list>`_, this command lists all backups for the cluster.

   .. code-block:: none

      sctool backup list -c my-cluster
      Snapshots:
       - sm_20191210145143UTC
       - sm_20191210145027UTC
       - sm_20191210144833UTC
      Keyspaces:
       - system_auth (2 tables)
       - system_distributed (1 table)
       - system_traces (5 tables)
       - auth_service (3 tables)


   Find the backup you want, and copy the desired snapshot tag.
   Snapshot tags encode date they were taken in UTC time zone.
   For example, ``sm_20191210145143UTC`` was taken on 12/10/2019 at 14:51 and 43 seconds UTC.
   The datasource for the listing is the cluster backup locations.
   Listing may take some time depending on how big the cluster is and how many backups there are.
   
#. Once you have snapshot tag, use `sctool backup files <../sctool/#backup-files>`_ in order to get paths of all the files uploaded during the backup.
   See `Backup Files Example <../sctool/#example-backup-files>`_ to see how to find out which files belongs to which nodes in the cluster.


.. Listing files for selected keyspace or tables

.. TODO: Instruct users to use ``--keyspace`` parameter in sctool backup list and sctool backup files

Listing files when your cluster is completely lost
..................................................

.. TODO: add a listing scenario when there is no cluster.

* Create a cluster
* Register the cluster in Scylla Manager
* Make sure that old cluster locations are available from new cluster nodes
* List the backups available and locate your backup, for example: 
  ``sctool backup list -c my-new-cluster --all-clusters -L dc1:s3:location1 -L dc2:s3:location2``
* List the files in the identified backup using ``sctool backup files`` - See `List the backup files`_ for an example.


Restore the schema
------------------

As Scylla 2019.1 and 3.2 do not backup schema information, you need to recreate it manually.

Follow `Steps 1 to 5 </operating-scylla/procedures/backup-restore/restore/#procedure>`_ to restore the Schema, delete the commit log, and to delete the files in the keyspace and table you want to restore to.


Upload data to Scylla
=====================

You can either upload the data:

* `To the same cluster`_: with the same nodes, topology, and the same token distribution **OR**
* `To a new cluster`_: of any number of nodes


To the same cluster
-------------------

List the backup files
.....................

List the backup files needed on each node and save the list to a file.

.. code-block:: none

   sctool backup files -c my-cluster --snapshot-tag sm_20191210145027UTC \
   --with-version > backup_files.out

Each line describes a backed-up file and where it should be downloaded. For example

.. code-block:: none

   s3://backups/backup/sst/cluster/1d781354-9f9f-47cc-ad45-f8f890569656/dc/dc1/node/ece658c2-e587-49a5-9fea-7b0992e19607/keyspace/auth_service/table/roles/5bc52802de2535edaeab188eecebb090/mc-2-big-CompressionInfo.db      auth_service/roles-5bc52802de2535edaeab188eecebb090

This file has to be copied to:

* Cluster - 1d781354-9f9f-47cc-ad45-f8f890569656
* Data Center - dc1
* Node - ece658c2-e587-49a5-9fea-7b0992e19607
* Directory - /var/lib/scylla/data/auth_service/roles-5bc52802de2535edaeab188eecebb090/upload

Download the backup files
.........................

This step must be executed on **each node** in the cluster.

#. Copy ``backup_files.out`` file as ``/tmp/backup_files.out`` on the node.

#. Run ``nodetool status`` to get to know the node ID

#. Download data into table directories.
   As the file is kept in S3 so we can use S3 CLI to download it (this step may be different with other storage providers).

   .. code-block:: none

      cd /var/lib/scylla/data
      grep ece658c2-e587-49a5-9fea-7b0992e19607 /tmp/backup_files.out | xargs aws s3 cp

#. Return to the Restore Procedure and follow `Steps 9 and 10 </operating-scylla/procedures/backup-restore/restore/#procedure>`_

Repair
......

After performing the above on all nodes, repair the cluster with Scylla Manager Repair.
This makes sure that the data is consistent on all nodes and between each node.

To a new cluster
----------------

In order to restore backup to cluster which has different topology, you have to use an external tool called `sstableloader </operating-scylla/procedures/cassandra_to_scylla_migration_process/>`_.
This procedure is much slower than restoring to same topology cluster.

**Procedure**

#. List all the backup files and save the list to a file.

   .. code-block:: none

      sctool backup files -c my-cluster --snapshot-tag sm_20191210145027UTC > backup_files.out

#. Copy ``backup_files.out`` file as ``/tmp/backup_files.out`` on the host where ``sstableloader`` is installed.

#. Download all files created during backup into temporary location.

   .. code-block:: none

      mkdir snapshot
      cd snapshot
      cat /tmp/backup_files.out | xargs aws s3 cp

#. Execute following command providing list of node IP addresses and path to sstable files.

   .. code-block:: none

      sstableloader -d <list of IP addresses> <path to snapshot directory>
