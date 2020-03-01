Create a Scylla Cluster on EC2 (Single or Multi Data Center)
============================================================

The easiest way to run a Scylla cluster on EC2 is using CentOS base `Scylla AMI`_. However, if you wish to use a different OS or your own `AMI`_ (Amazon Machine Image), or setup a multi DC Scylla cluster, you will need to configure Scylla cluster on your own. This page guides you through this process.

..  _`Scylla AMI`: https://www.scylladb.com/download/open-source/#aws 

..  _`AMI`: https://en.wikipedia.org/wiki/Amazon_Machine_Image

Scylla cluster on EC2 can deployed as a single-DC or a multi-DC. The table below described how to configure ``scylla.yaml`` parameters for each node in your cluster for each case.

Best practice is to use each EC2 region as a Scylla DC. In such a case, nodes communicating using Internal (private) IPs inside the region, and using External (Public) IPs between regions (Data Centers)

For further information on `AWS instance addressing`_  

..  _`AWS instance addressing`: http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-instance-addressing.html

EC2 Configuration Table
-----------------------

=====================  ====================  ====================
Parameter              Single DC             Multi DC 
=====================  ====================  ====================
seeds	               Internal IP address   External IP address                
---------------------  --------------------  --------------------  
listen_address         Internal IP address   Internal IP address          
---------------------  --------------------  --------------------  
rpc_address            Internal IP address   Internal IP address      
---------------------  --------------------  --------------------
broadcast_address      Internal IP address   External IP address
---------------------  --------------------  --------------------
broadcast_rpc_address  Internal IP address   External IP address
---------------------  --------------------  --------------------
endpoint_snitch        Ec2Snitch             Ec2MultiRegionSnitch
=====================  ====================  ====================

Prerequisites
-------------

* EC2 instance with ssh access.

* Make sure that all the relevant ports_ are open in your EC2 Security Group.

* Select a unique name as ``cluster_name`` for the cluster (identical for all the nodes in the cluster).

* Decide which nodes will be the seed nodes (It is recommended to define more than one node as a seed node per data-center).

.. _ports: /operating-scylla/admin/#networking


Procedure
---------

These steps need to be done for each of the nodes in the new cluster.

1. Install Scylla on a node, see :doc:`Getting Started</getting-started/index>` for further instructions.
Follow the Scylla install procedure up to ``scylla.yaml`` configuration phase.

In case that Scylla service is already running, for example, if you are using `Scylla AMI`_, stop it before moving to the next step by using :doc:`these instructions </operating-scylla/procedures/cluster-management/clear_data>`

2. In the ``scylla.yaml`` file edit the parameters listed below,
the file can be found under ``/etc/scylla/`` consult the table_ above how to configure your cluster.

.. _table: /operating-scylla/procedures/cluster-management/ec2_dc/#ec2-configuration-table

- **cluster_name** - Set the selected cluster_name
- **seeds** - Set the selected seed nodes
- **listen_address** - IP address that Scylla used to connect to other Scylla nodes in the cluster 
- **auto_bootstrap** - By default, this parameter is set to **true**, it allow new nodes to migrate data to themselves automatically. If using Scylla AMI add ``--bootstrap`` to the user settings when creating a node

- **endpoint_snitch** - Set the selected snitch 

- **rpc_address** - Address for client connection (Thrift, CQL)

- **broadcast_address** - The IP address a node tells other nodes in the cluster to contact it by 

- **broadcast_rpc_address** - Default: unset, RPC address to broadcast to drivers and other Scylla nodes. This cannot be set to 0.0.0.0. If left blank, this will be set to the value of rpc_address. If rpc_address is set to 0.0.0.0, broadcast_rpc_address must be configured

3. After you have installed and configured Scylla and edit ``scylla.yaml`` file on all the nodes, start the seed nodes one at a time, and then start the rest of the nodes in your cluster using
``sudo systemctl start scylla-server``

4. Verify that the node added to the cluster using.
``nodetool status``

EC2 snitchs Default DC and Rack Names, and how to Override DC Names
...................................................................

EC2snitch and Ec2MultiRegionSnitch give each DC and rack default names, the region name defined as datacenter name and `availability zones`_ are defined as racks within a datacenter. 
EC2snitch and Ec2MultiRegionSnitch give each DC and rack default names, the region name defined as datacenter name and `availability zones`_ are defined as racks within a datacenter, the rack names can't be changed.

.. _`availability zones`: /faq/#what-is-the-best-scenario-to-add-a-node-to-a-multi-availability-zone-az

For example:

A node in the ``us-east-1`` region, 
us-east is the data center name and 1 is the rack location. 

To change the DC names do the following:

Edit the ``cassandra-rackdc.properties`` file with the prefered data-center name.
The file can be found under ``/etc/scylla/``

The dc_suffix defines a suffix added to the data-center name as described below.


For example:

Region us-east

``dc_suffix=_1_scylla`` will be ``us-east_1_scylla``

Or

Region us-west

``dc_suffix=_1_scylla`` will be ``us-west_1_scylla``



