Scylla Snitches
===============

Snitch determines which data centers and racks nodes belong to, Snitches inform Scylla about the network topology so that requests are routed efficiently and allows Scylla to distribute replicas by grouping machines into data centers and racks.

Note that if you do not choose a snitch when creating a Scylla cluster, the simple snitch is used by default. 

Scylla supports the following snitches:

* SimpleSnitch_
* RackInferringSnitch_
* GossipingPropertyFileSnitch_
* Ec2Snitch_
* Ec2MultiRegionSnitch_
* GoogleCloudSnitch_ (**New** in Scylla 2.2)


SimpleSnitch
............
When working with single cluster deployments and all the nodes are under the same data-center use the SimpleSnitch, it binds all the nodes to the same Rack and data-center. This snitch is used in a single data-center deployments only.


RackInferringSnitch
...................
Bind Nodes to DCs and Racks according to their Broadcast IPs:


For Example:

Node has a Broadcast IP 192.168.100.200, then it would belong to a DC '168' and Rack '100'

GossipingPropertyFileSnitch 
...........................
When working with multi-cluster deployments and the nodes are in various data-centers use the GossipingPropertyFileSnitch.
Recommended to be used in production installations. It allows to explicitly define which DC and Rack a specific Node belongs to
This snitch read its configuration from a ``cassandra-rackdc.properties`` file that located under ``/etc/scylla/``

For Example:

.. code-block:: shell

   prefer_local=true 
   dc=my_data_center 
   rack=my_rack

Set the ``prefer_local`` to **true** will tell Scylla to use local IP address. The local IP address is the listen_address parameter from the scylla.yaml file which is located under ``/etc/scylla/``

.. _scylla.yaml: /operating-scylla/admin/#scylla-yaml

Ec2Snitch
.........

When working on EC2 with a single cluster deployments and all the nodes are under the same region use the Ec2Snitch. 
Basic snitch that reads its configuration from Amazon's EC2 registry services.
In EC2, the region name is treated as the datacenter name and availability zones are treated as racks within a datacenter. 
If the setup includes a single datacenter, there is no need to specify any parameters.
Because private IPs are used, this snitch does not work across multiple regions.

If you working with multiple datacenters, set the parameter ``dc_suffix``  in the ``cassandra-rackdc.properties`` file under ``/etc/scylla/``. 


For Example:

Node 1 region DC ``'us-west'`` and Rack ``Rack='1'`` will be ``us-west-1`` dc_suffix= ``scylla_node_1``

Node 2 region DC ``'us-west'`` and Rack ``Rack='1'`` will be ``us-west-1`` dc_suffix= ``scylla_node_2``

.. code-block:: shell

   us-west-1_scylla_node_1
   us-west-1_scylla_node_2

Ec2MultiRegionSnitch
....................

When working on EC2 using a multi-cluster deployments and the nodes are in various regions use the Ec2MultiRegionSnitch.
Works like the Ec2Snitch, in addition, it set the ``broadcast_address`` and ``broadcast_rpc_address`` of a node to the node's public IP. 
This would allow nodes from other zones to communicate with this node regardless of what is configured in the node's scylla.yaml_ configuration file for ``broadcast_address`` and ``broadcast_rpc_address`` parameters.

``Ec2MultiRegionSnitch`` also unconditionally imposes the "prefer local" policy on a node (similar to GossipingPropertyFileSnitch when prefer_local is set to true).

In EC2, the region name is treated as the datacenter name and availability zones are treated as racks within a datacenter. 

To change the DC and Rack names do the following:

Edit the ``cassandra-rackdc.properties`` file with the preferred data-center name. The file can be found under ``/etc/scylla/``
The ``dc_suffix`` defines a suffix added to the data-center name as described below.

For Example:

Node - region ``DC='us-west'`` and Rack ``Rack='1'`` will be ``us-west-1`` dc_suffix= ``scylla_node_west``

Node - region ``DC='us-east'`` and Rack ``Rack='2'`` will be ``us-east-2`` dc_suffix= ``scylla_node_east``

.. code-block:: shell

   us-west-1_scylla_node_west
   us-east-2_scylla_node_east

GoogleCloudSnitch
.................

Use the GoogleCloudSnitch (available in Scylla version 2.2 and later) for deploying Scylla on the Google Cloud Engine (GCE) platform across one or more regions. The region is treated as a datacenter and the availability zones are treated as racks within the datacenter. All communication occurs over private IP addresses within the same logical network.

To use the GoogleCloudSnitch, add the snitch to the scylla.yaml file which is located under ``/etc/scylla/`` for all nodes in the cluster. 

You can add a suffix to the data center name as an additional identifier. This suffix is appeneded to the Zone name without adding any spaces. To add this suffix edit the ``cassandra-rackdc.properties`` file, which can be found under ``/etc/scylla/`` and set the ``dc_suffix`` with an appropriate text string. It may help to add an underscore or dash in front. Keep in mind that this property file is used for all Scylla snitches. When using the GoogleCloudSnitch, all other properties are ignored.



**Example**

You have two datacenters running on GCE. One is located in region **us-east1**, and zone **us-east-1-b** and is allocated for your office in Miami. The other is located in **us-west1** and zone **us-west-1-b** and is allocated for your office in Portland. In this case, the data center one's name is us-east1 with rack name b and the second DC is us-west1 with rack b. (Racks are important for distributing replicas, but not for datacenter naming.) This snitch can work across multiple regions without additional configuration.

After creating the instances on GCE, edit the scylla.yaml file to indicate the GoogleCloudSnitch. While you have the file open, check that you have at least two seed nodes, one in each datacenter.

.. code-block:: none

   endpoint_snitch: GoogleCloudSnitch

As you want to set the data center suffix for the nodes in each datacenter, you open each node's properties file in the ``cassandra-rackdc.properties`` The file can be found under ``/etc/scylla/``. You set the following parameters for Miami:

.. code-block:: none

   # node 1 - 192.0.2.2 (you use the same properties for node #2 (192.0.2.3) and #3 (192.0.2.4)) 

   dc_suffix=_scylla_node_Miami
   
and for Portland:  

.. code-block:: none

   # node 4 192.0.2.5 

   dc_suffix=_scylla_node_Portland

You start the cluster, one node at a time starting with the seed nodes, and then run ``nodetool status`` to check connectivity. 

.. code-block:: shell

   nodetool status

   Datacenter: us-east1_scylla_node_Miami
   ======================================
   Status=Up/Down
   |/ State=Normal/Leaving/Joining/Moving
   --  Address       Load       Tokens       Owns    Host ID                               Rack
   UN  192.0.2.2     1.27 MB    256          ?       5b1d864f-a026-4076-bb19-3e7dd693abf1  b
   UN  192.0.2.3     954.89 KB  256          ?       783a815e-6e9d-4ab5-a092-bbf15fd76a9f  b
   UN  192.0.2.4     1.02 MB    256          ?       1edf5b52-6ae3-41c1-9ec1-c431d34a1aa1  b

   Datacenter: us-west1_scylla_node_Portland
   ======================================
   Status=Up/Down
   |/ State=Normal/Leaving/Joining/Moving
   --  Address       Load       Tokens       Owns    Host ID                               Rack
   UN  192.0.2.5     670.16 KB  256          ?       f0a44a49-0035-4146-8fdc-30e66c037f95  b


Related Topics

.. include:: /rst_include/advance-index.rst



