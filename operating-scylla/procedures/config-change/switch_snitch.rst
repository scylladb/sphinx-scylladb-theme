
How to Switch Snitches
**********************

This procedure describes the steps that need to be done when switching from one type of snitch to another.
Such scenario can be when increasing the cluster and adding more data-centers in different locations. 
Snitches are responsible how Scylla will distribute the replicas, the procedure depends if there are any changes in the cluster topology.

**Note** - Switching a snitch require full cluster shutdown, so It is highly recommended to choose the right_ snitch_ for your needs at cluster setup phase.

.. _right: /operating-scylla/system-configuration/snitch/#scylla-snitches
.. _snitch: /operating-scylla/system-configuration/snitch/#scylla-snitches

+------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
|Cluster Status	                                                                     |Needed Procedure	                                                                  |
+====================================================================================+====================================================================================+
|No change in network topology                                                       |Set the new snitch                                                                  |
+------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
|Network topology was changed                                                        |Set the new snitch and run repair                                                   | 
+------------------------------------------------------------------------------------+------------------------------------------------------------------------------------+


Changes in network topology mean that there are changes in the racks or data-centers where the nodes are located. 

For example:

**No topology changes**

Original cluster: three nodes cluster on a single data-center with Simplesnitch_ or Ec2snitch_. 

.. _Simplesnitch: /operating-scylla/system-configuration/snitch/#simplesnitch

Change to: three nodes in one datacenter and one rack using a GossipingPropertyFileSnitch_ or Ec2multiregionsnitch_.

.. _GossipingPropertyFileSnitch: /operating-scylla/system-configuration/snitch/#gossipingPropertyFileSnitch

**Topology changes**

Original cluster: three nodes using the Simplesnitch_ or Ec2snitch_ in a single datacenter.

.. _Ec2snitch: /operating-scylla/system-configuration/snitch/#ec2snitch

Change to: nine nodes in two data-centers using the GossipingPropertyFileSnitch_ or Ec2multiregionsnitch_ (add a new data-center).

.. _Ec2multiregionsnitch: /operating-scylla/system-configuration/snitch/#ec2multiregionsnitch

---------
Procedure
---------

1. Stop all the nodes in the cluster.

.. include:: /rst_include/scylla-commands-stop-index.rst

2. In the ``scylla.yaml`` file edit the endpoint_snitch. The file can be found under ``/etc/scylla/``, change the endpoint_snitch to all the nodes in the cluster.

For example:

``endpoint_snitch: GossipingPropertyFileSnitch``

3. In the ``cassandra-rackdc.properties`` file edit the rack and data-center information.  

For example, ``Ec2MultiRegionSnitch``:

A node in the ``us-east-1`` region, us-east is the data center name and 1 is the rack location. 

4. Start the nodes in the cluster one by one.

.. include:: /rst_include/scylla-commands-start-index.rst

5. Run full repair (consult with the table above if this action is needed).


