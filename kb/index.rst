Knowledge Base
==============

.. toctree::
   :maxdepth: 2
   :hidden:

   /kb/compaction
   /kb/dpdk-hardware
   /kb/gossip
   /kb/ntp
   /kb/os-support
   /kb/posix
   /kb/quiz-administrators
   /kb/scylla-and-spark-integration
   /kb/social-reader
   /kb/memory-usage
   /kb/disk-utilization
   /kb/snapshots
   /kb/system-limits
   /kb/yaml-address
   /kb/cqlsh-more
   /kb/map-cpu
   /kb/use-perf
   /kb/flamegraph
   /kb/raid-device
   /kb/unresponsive-nodes
   /kb/decode-stack-trace
   



.. panel-box::
  :title: Planning and Setup
  :id: "getting-started"
  :class: my-panel 

  * :doc:`Compaction </kb/compaction>` - To free up disk space and speed up reads, Scylla must do compaction operations.
  * :doc:`DPDK mode </kb/dpdk-hardware>` - Learn to select and configure networking for DPDK mode
  * :doc:`Operating System (OS) Support Guide </kb/os-support>` - Operating System support.
  * :doc:`POSIX networking for Scylla </kb/posix>` - Scylla's POSIX mode works on all physical and virtual network devices and is useful for development work.
  * :doc:`System Limits </kb/system-limits>` - outlines the system limits which should be set or removed


.. panel-box::
  :title: Scylla under the hood
  :id: "getting-started"
  :class: my-panel 

  * :doc:`Gossip in Scylla </kb/gossip>` - Scylla, like Cassandra, uses a type of protocol called “gossip” to exchange metadata about the identities of nodes in a cluster. Here's how it works behind the scenes.
  * :doc:`Scylla consistency quiz for administrators </kb/quiz-administrators>` - How much do you know about NoSQL, from the administrator point of view?
  * :doc:`Data model for a social reader application </kb/social-reader>` - A simple data model for a link sharing and recommendation site
  * :doc:`Scylla Memory Usage </kb/memory-usage>` - Short explanation how Scylla manages memory 
  * :doc:`Scylla Nodes are Unresponsive </kb/unresponsive-nodes>` - How to handle swap in Scylla
  * :doc:`CQL Query Does Not Display Entire Result Set </kb/cqlsh-more>` - What to do when a CQL query doesn't display the entire result set.
  * :doc:`Snapshots and Disk Utilization </kb/disk-utilization>` - How snapshots affect disk utilization
  * :doc:`Scylla Snapshots </kb/snapshots>` - what Scylla snapshots are, what they are used for, and how they get created and removed.

.. panel-box::
  :title: Configuring and Integrating Scylla
  :id: "getting-started"
  :class: my-panel 

  * :doc:`NTP configuration for Scylla </kb/ntp>` - Scylla depends on an accurate system clock. Learn to configure NTP for your data store and applications.
  * :doc:`Scylla and Spark integration </kb/scylla-and-spark-integration>` - How to run an example Spark application that uses Scylla to store data?
  * :doc:`Map CPUs to Scylla Shards </kb/map-cpu>` - Mapping between CPUs and Scylla shards
  * :doc:`Recreate RAID devices </kb/raid-device>` - How to recreate your RAID devices without running scylla-setup
  * :doc:`Configure Scylla Networking with Multiple NIC/IP Combinations </kb/yaml-address>` - examples for setting the different IP addresses in scylla.yaml
  * :doc:`Kafka Sink Connector Quickstart </using-scylla/integrations/kafka-connector>`
  * :doc:`Kafka Sink Connector Configuration </using-scylla/integrations/sink-config>`


.. panel-box::
  :title: Analyzing Scylla
  :id: "getting-started"
  :class: my-panel 
   
  * :doc:`Using the perf utility with Scylla </kb/use-perf>` - Using the perf utility to analyze Scylla
  * :doc:`Debug your database with Flame Graphs </kb/flamegraph>` - How to setup and run a Flame Graph
  * :doc:`Decoding Stack Traces </kb/decode-stack-trace>` - How to decode stack traces in Scylla Logs














