Failed Decommission
===================

This procedure describes the steps which need to be done in case a node decommission fails.
When decommissioning a node a streaming process will start, and the node will streams his data to the other nodes in the Scylla cluster.
Failure can happen in cases where a node fails to read from the HDD or a network problem occurs, a node decommission may fail. The failure causes the node to stream its data to other nodes in the Scylla cluster. While looking at the logs will validate the error occurred (see `How to Verify`_), the following procedure is a remedy for the failed decommission.

..  _`How to Verify`: /troubleshooting/failed_decommission/#how-to-verify

Problem
^^^^^^^
The node is stuck in a decommission status, the node status is Up Leaving (UL).

How to Verify
^^^^^^^^^^^^^
Check the node status by using the nodetool ``status command``, the expected result is (UL), also need to check the node status from the other nodes in the cluster and see that the decommissioned node status is (UL).
However, ``nodetool netstats`` command does not show an ongoing streaming. 
The following error message will appear in the logs_

.. _logs: /getting-started/logging/ 

.. code-block:: shell

   nodetool: Scylla API server HTTP POST to URL '/storage_service/decommission' failed: stream_ranges failed

Solution
^^^^^^^^

1. Restart the decommission node.

.. include:: /rst_include/scylla-commands-restart-index.rst

2. Use ``nodetool status`` command to verify the node is in ``UN`` status.

3. Run ``nodetool decommission`` again.

.. include:: /troubleshooting/_common/ts-return.rst
