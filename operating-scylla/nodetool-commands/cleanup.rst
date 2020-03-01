Nodetool cleanup
================
**cleanup** ``[<keyspace> <cfnames>...]``- Triggers the immediate cleanup of keys no longer belonging to a node. By default, clean all keyspaces. This command cleans keys that no longer belong to the node. If no key is specified all the keyspaces will be removed. It’s important to use the nodetool cleanup command when adding or removing nodes of a cluster.

For example:

To clean up the data of a specific node use this command:

.. code-block:: shell

   nodetool cleanup -h 127.0.0.1 keyspace1

.. note::

   If using Scylls Enterprise 2018.1.5, Scylla Open Source 2.2.0, 2.3.0 or lower version **Do not** run the ``nodetool cleanup`` command before upgrading to the latest release of your branch, see this issue_ for further information.

.. _issue: https://github.com/scylladb/scylla/issues/3872

.. include:: nodetool-index.rst
