Scylla consistency quiz for administrators
==========================================
**Topic: Architecture and development**

**Learn: Understanding consistency in Scylla: a quiz**

**Audience: Scylla administrators**

Q: When you run ``nodetool decommission`` to remove a node…

1. Will the token range the node had will be relocated to other nodes?
   What about vnodes?

2. When and how will we know the “decommission” operation is finished?

A1. Yes. The node enters the state “STATE\_LEAVING” while streaming its
data to other nodes. Then it is in “STATE\_LEFT” when the data has been
streamed.

A2. Use ``nodetool netstats`` to check the state of a node.

Q: Let's say I have a 16 node cluster using Network Topology Strategy
across 2 data centers. The replication factor is 2 in each datacenter
(DC1: 2, DC2: 2). If I write using a LOCAL\_QUORUM, I will write the
data to 4 nodes (2 in each data center) but when will the
acknowledgement happen?

A: The quorum is local to the data center, so there will be 2 writes
local and 2 reads local. Asynchronously the local coordinator will send
the write to a remote coordinator but the local read and write don't
need it

`Knowledge Base 
</kb/>`_
