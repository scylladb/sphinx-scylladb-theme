=================================
Scylla Manager Agent Installation
=================================

Scylla Manager Agent is an executable, installed on each Scylla node. 
The Server communicates with the Agent over REST/HTTPS. 
The Agent communicates with the local Scylla node over the REST/HTTP.

.. contents::
   :depth: 2
   :local:


Install Scylla Manager Agent
----------------------------

Prerequisites
=============

* Scylla cluster running on any `OS supported by Scylla Manager 2.0 </getting-started/os-support/>`_
* Traffic on port 10001 unblocked to Scylla nodes from the dedicated host

.. note:: Scylla Manager only works with Scylla clusters that are using the Murmur3 partitioner (Scylla default partitioner). To check your cluster's partitioner, run the cqlsh command ``DESCRIBE CLUSTER``.

Download packages
=================

**Procedure**

Download and install Scylla Manager Agent (from the Scylla Manager Download Page) according to the desired version:

* `Scylla Manager for Open Source <https://www.scylladb.com/download/open-source/scylla-manager/>`_ - Registration Required
* Scylla Enterprise - Login to the `Customer Portal <https://www.scylladb.com/customer-portal/>`_

Configure Scylla Manager Agent
------------------------------
There are three steps you need to complete:

* Generate a `token`_
* Place token `parameters`_ in the Agent configuration file
* Start or Restart Scylla Manager Agent `service <../install-agent/#services>`_ and confirm all is running without errors

.. _token:

Generate an authentication token
================================

**Procedure**

#. Generate an authentication token an to be used to authenticate Scylla Manager with Scylla nodes. 
   This procedure is done **once** for each cluster. It is recommended to use a different token for each cluster. 

   .. note:: Use the same token on all nodes in the same cluster. 

   From **one node only** Run the token generator script. 

   For example:

   .. code-block:: none

      $ scyllamgr_auth_token_gen
      6Es3dm24U72NzAu9ANWmU3C4ALyVZhwwPZZPWtK10eYGHJ24wMoh9SQxRZEluWMc0qDrsWCCshvfhk9uewOimQS2x5yNTYUEoIkO1VpSmTFu5fsFyoDgEkmNrCJpXtfM

   If you want to change the token, you will need to repeat this procedure and place the new token on all nodes. 
   This procedure sets up the Scylla agent on each node. 
   Repeat the procedure for **every** Scylla node in the cluster that you want to be managed under Scylla Manager.

.. _parameters:

Configure authentication token parameters
=========================================

**Procedure**

#. Take the authentication `token`_ you generated, and place it into ``/etc/scylla-manager-agent/scylla-manager-agent.yaml`` as part of the ``auth_token`` `section <../agent-configuration-file/#authentication-token>`_.  

   For Example:

   .. code-block:: none

      $ cat /etc/scylla-manager-agent/scylla-manager-agent.yaml
      # Scylla Manager Agent config YAML

      # Specify authentication token, the auth_token needs to be the same for all the
      # nodes in a cluster. Use scyllamgr_auth_token_gen to generate the auth_token
      # value.
      auth_token: 6Es3dm24U72NzAu9ANWmU3C4ALyVZhwwPZZPWtK10eYGHJ24wMoh9SQxRZEluWMc0qDrsWCCshvfhk9uewOimQS2x5yNTYUEoIkO1VpSmTFu5fsFyoDgEkmNrCJpXtfM

.. _services:

Start Scylla Manager Agent service
==================================

**Procedure**

#. Start Scylla Manager Agent service

   .. code-block:: none

      $ sudo systemctl start scylla-manager-agent

#. Validate Scylla Manager Agent is running

   .. code-block:: none

      $ sudo systemctl status scylla-manager-agent
      ● scylla-manager-agent.service - Scylla Manager Agent
        Loaded: loaded (/usr/lib/systemd/system/scylla-manager-agent.service; disabled; vendor preset: disabled)
        Active: active (running) since Wed 2019-10-30 10:46:51 UTC; 7s ago
          Main PID: 14670 (scylla-manager-)
          CGroup: /system.slice/scylla-manager-agent.service
                 └─14670 /usr/bin/scylla-manager-agent

      Oct 30 10:46:51 ip-172-31-0-11.ec2.internal systemd[1]: Started Scylla Manager Agent.
      Oct 30 10:46:52 ip-172-31-0-11.ec2.internal scylla-manager-agent[14670]: {"L":"INFO","T":"2019-10-30T10:46:52.027Z","M":"Scylla Manager    Agent","version":"2.0-0.20191030.9442dd9b","_trace_id":"FaheEpqXS2CTIy2lA1fkBg"}
      Oct 30 10:46:52 ip-172-31-0-11.ec2.internal scylla-manager-agent[14670]: {"L":"INFO","T":"2019-10-30T10:46:52.027Z","M":"Using config","config":   {"AuthToken":"***************************************************************...er/scylla_mana
      Oct 30 10:46:52 ip-172-31-0-11.ec2.internal scylla-manager-agent[14670]: {"L":"INFO","T":"2019-10-30T10:46:52.027Z","M":"Looking for a free CPU to run on","_trace_id":"FaheEpqXS2CTIy2lA1fkBg"}
      Oct 30 10:46:52 ip-172-31-0-11.ec2.internal scylla-manager-agent[14670]: {"L":"INFO","T":"2019-10-30T10:46:52.028Z","M":"Could not get a free CPU","error":"Scylla cpuset parse error run    scylla_cpuset_setup or set cpu fiel...CTIy2lA1fkBg"}
      Oct 30 10:46:52 ip-172-31-0-11.ec2.internal scylla-manager-agent[14670]: {"L":"INFO","T":"2019-10-30T10:46:52.028Z","N":"rclone","M":"registered s3 provider"}
      Oct 30 10:46:52 ip-172-31-0-11.ec2.internal scylla-manager-agent[14670]: {"L":"INFO","T":"2019-10-30T10:46:52.028Z","N":"rclone","M":"registered localdir provider data rooted at /var/lib/scylla/data"}
      Oct 30 10:46:52 ip-172-31-0-11.ec2.internal scylla-manager-agent[14670]: {"L":"INFO","T":"2019-10-30T10:46:52.028Z","M":"Starting HTTPS    server","address":"172.31.0.11:10001","_trace_id":"FaheEpqXS2CTIy2lA1fkBg"}
      Hint: Some lines were ellipsized, use -l to show in full.

#. Enable the Scylla Manager Agent to run when the node starts.

   .. code-block:: none

      $ sudo systemctl enable scylla-manager-agent


#.    Repeat the procedure for **every** Scylla node in the cluster that you want to be managed under Scylla Manager starting with `Configure authentication token parameters`_. 

Prepare nodes for backup
------------------------

Adding the cluster to Scylla Manager automatically creates a backup task. Validate the connection to your backup location is accessible from Scylla Manager before adding the cluster to avoid errors.  

**Procedure**

#. Create a storage location for the backup. 
   Currently, Scylla Manager 2.0 supports `S3 buckets <https://aws.amazon.com/s3/>`_ created on AWS. 
   You can use an S3 bucket that you already created. 
#. Choose how you want to configure access to the S3 Bucket. 
   You can use an IAM role (recommended) or you can add your AWS credentials to the agent configuration file. 
   This method is less secure as you will be propagating each node with this security information and in cases where you need to change the key, you will have replace it on each node.  

   * To use an IAM Role:

     #. Create an `IAM role <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide//iam-roles-for-amazon-ec2.html>`_ for the S3 bucket which adheres to your company security policy. You can use a role you already created. 
     #. `Attach the IAM role <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide//iam-roles-for-amazon-ec2.html#attach-iam-role>`_ to **each EC2 instace (node)** in the cluster.

   * To add your AWS credentials the Scylla Manager Agent configuration file:

     #. Edit the ``/etc/scylla-manager-agent/scylla-manager-agent.yaml`` in the ``S3`` section your authentication information about the S3 bucket. 
        Refer to `AWS Credentials Configuration <../agent-configuration-file/#aws-credentials-configuration>`_ for details. 

#. Validate that the manager has access to the backup location. 
   If there is no response, the S3 bucket is accessible. If not, you will see an error. 

   .. code-block:: none
      
      $ scylla-manager-agent check-location --location s3:<your S3 bucket name>


Register a cluster
------------------

Continue with `Add a Cluster <../add-a-cluster>`_.
