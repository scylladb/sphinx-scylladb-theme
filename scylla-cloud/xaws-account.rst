========================================
Deploy Scylla Cloud on your AWS Account 
========================================


This document instructs you on how to set-up a Scylla Cloud managed cluster on your AWS account. 

By the end of this procedure, you will be able to use Scylla Cloud Web application to create ScyllaDB clusters using the resources from your AWS account, thus enjoying Scylla Cloud’s fully-managed database service on the AWS account you already own. 
The guide will define the needed actions in your AWS account to allow Scylla Cloud DBaaS to manage your ScyllaDB resources. 
It will include defining policies and the ScyllaCloud role. 
You can choose to have a dedicated AWS account for Scylla Cloud by using AWS Organizations and follow this procedure within this dedicated account. 
If you choose not to use an AWS Organization and a dedicated account, you can follow this procedure in your main AWS account. 

.. caution:: Deploying Scylla Cloud on your AWS account gives you access to your database resources. We **strongly** recommend not to change/remove any of the resources that you create for the Scylla Cloud role, or in its policies, to make sure that the database services are all properly set and functioning according to your company security policy. 

Prerequisites
-------------

Before you begin:

* Confirm you have filled in the `registration page <https://cloud.scylladb.com/user/signup>`_ and signed up to Scylla Cloud service. 
* Do **not** click **Create a New Cluster**, as this requires cooperation between the Scylla Cloud team and yourself. 
* Confirm that your AWS account has the correct account limits (Instances, VPCs, Elastic IPs, Cloudformation Stacks, etc). See `AWS Account Limits`_ and `AWS Credentials`_ below. 


Workflow
--------

#. `Request services`_ Send a request for the cross AWS account
#. `Define a security policy`_ for Scylla Cloud on your AWS account
#. `Create a Scylla Cloud policy`_ for your AWS account
#. `Create a Scylla Cloud Role`_ and give it specific priviledges
#. `Run Scylla Cloud`_ from your AWS account

.. _received:

Request services
================

#. Request a Cross-AWS-Account deployment
   Contact either your account representitive or open a support ticket ​and request a Cross-AWS-account deployment. 
   As a response to your request, the Scylla Cloud team will send you by e-mail a ``boundary.json`` file. 
#. Save the file in an acessible location as you will need it later.


Define a security policy
========================

#. Define a `policy <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html>`_ to limit Scylla Cloud permissions in your AWS account.
   Use this policy file to define a new policy named ``ScyllaCloudBoundary``. 
   This policy will restrict Scylla Cloud's permissions on your AWS account and will be used in further steps. 
#. From the AWS console, navigate to IAM Services > Policies and click **Create Policy**. 
#. Click the **JSON** tab.
#. Paste the contents of the ``boundary.json`` file that you `received`_ from Scylla Cloud Support team into the text box and click **next**.
#. Click **Review Policy**.
#. Name the policy ``ScyllaCloudBoundary`` and click **create policy**.
#. Navigate to the **Policies** main window, search for the ``ScyllaCloudBoundary`` policy and click on it to open the policy details. 
#. Copy the ``Policy ARN`` (output should be similar to the following example: ``arn:aws:iam::734708892259:policy/ScyllaCloudBoundary``) and send it by email to Scylla support. 
#. As a response, Scylla Cloud Support will send you a file named ``cross.json``. Save the file in an acessible location as you will need it in the next step.
 
Create a Scylla Cloud policy
============================

Create a new policy ScyllaCloud to manage Scylla Cloud role and resources 

#. From the AWS console, navigate to **IAM Services > Policies** and click **Create Policy**
#. Click the **JSON** tab and paste in the window the contents of the file ``cross.json``, which was sent to you from the Scylla Cloud team by email.  
#. Click **Review Policy**
#. Name the policy: ``ScyllaCloud``. 
#. Click **create policy** to save the new policy. 

Create a Scylla Cloud Role
===========================

#. From the AWS console, navigate to **IAM > Roles** and click on **create role**.
#. When asked for a type of trusted entity, select **Another AWS account** and enter ``Scylla Production Account ID(696340704738)``. 
#. Check **Require external ID** and fill in the following: 
   * Put a random long string in the ``External ID`` text box, for example, a UUID.
   * This string should be treated as a password and kept secure 
   * Save the string as you will need to use it later 

   .. note:: Require MFA should **NOT** be checked 

#. Click **Next: Permissions** 
#. Search for the policy ScyllaCloud and check it 
#. Click **Next: Add Tags** and Enter the tag ``Scylla Cloud`` and any other tags you want 
#. Click **Next: Review** and fill in the following fields:
   * In **Role Name** Enter ``ScyllaCloudRole`` 
   * **Role Description** is optional. Enter any description that makes sense to you, as this is only for your usage. 
#. Click **Create Role**. Make sure the ScyllaCloud role is listed in the new role ARN list. 
#. Send cloud-support@scylladb.com the following information: 
   * The new role ARN (for example: ``arn:aws:iam::734708892259:role/ScyllaCloudRole``) 
   * The new role external ID value. This can be seen in tab **trust relationships**. (if you used UUID it would be something like ``ae15dc91-87d0-4c7d-a4b8-0c9b0f81ab1d``) 

#. Based on the new role ARN and external ID, the Scylla Cloud team will set the needed configuration to support the new deployment under your AWS account. 

   * Once it’s ready, you will be notified via e-mail that the procedure had finished and you are welcome to start creating and launching ScyllaDB clusters. 

Run Scylla Cloud 
================

#. To run Scylla Cloud from your account, sign in to the Scylla Cloud web application and navigate to the Create Cluster page and launch a new cluster. The cluster will run on your AWS account. 
#. Validate from your AWS console that the instances are listed. Search for the tag ``Scylla Cloud`` to identify managed Scylla Cloud instances. You should see the Scylla instances and the Scylla Monitoring instance running. 

AWS Account Limits 
------------------- 

Make sure you add the following limits to your AWS account for the resources Scylla Cloud will use. 
Please make sure that you repeat the resource allocation for each region you plan to use. 
Note that the following numbers should be in addition to your existing resource allocation. 

Use **AWS Service Quotas** to increase the following resources limits: 

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Service Name
     - Quota Code
     - Additional Requested Value
     - Quota Name
   * - Amazon Virtual Private Cloud (Amazon VPC)
     - L-F678F1CE
     - 50
     - VPCs per region 
   * - Amazon Elastic Compute Cloud (Amazon EC2) 
     - L-0263D0A3
     - 200
     - Number of EIPs - VPC EIPs 
   * - Amazon Elastic Compute Cloud (Amazon EC2) 
     - L-1216C47A
     - 1000 (see note) 
     - Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances 
   * - Amazon Simple Storage Service (Amazon S3)
     - L-DC2B2D3D
     - 50
     - Buckets
   * - AWS CloudFormation 
     - L-0485CB21
     - 100
     - Stack count
 
.. note:: 1000 doesn’t represent the limit for the number of instances, but the limit for vCPUs. Any launched instance of any of the listed instance types (A, C, D, H, I, M, R, T, Z) contributes its vCPU counttowards this quota. See more in this `AWS blog <https://aws.amazon.com/blogs/compute/preview-vcpu-based-instance-limits/>`_. 

AWS Credentials
----------------

Scylla Cloud requires the following credentials to manage its service while being deployed on your AWS account. 

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Purpose
     - Action 
   * - Scylla cloud will use this to restrict itself for only creating a new policy with access to its S3 backup and with no access to any other policy 
     - * iam:CreatePolicyVersion 
       * iam:DeletePolicy 
       * iam:DeletePolicyVersion 
       * iam:SetDefaultPolicyVersion
   * - Create/expend clusters
     - * ec2:CreateKeyPair 
       * ec2:ImportKeyPair 
       * ec2:DeleteKeyPair cloudformation:ValidateTemplate 
       * ec2:Describe* 
       * ec2:allocateAddress 
       * ec2:associateAddress 
       * ec2:CreateInternetGateway 
       * ec2:AttachInternetGateway 
       * ec2:CreateVpc 
       * ec2:ModifyVpcAttribute 
       * ec2:createTags 
       * ec2:CreateSecurityGroup 
       * ec2:CreateSubnet 
       * ec2:ModifySubnetAttribute 
       * ec2:CreateRouteTable 
       * ec2:AssociateRouteTable 
       * ec2:CreateNetworkInterface 
       * ec2:ModifyNetworkInterfaceAttribute 
       * ec2:CreateRoute ec2:RunInstances 
       * ec2:DescribeInstances 
       * ec2:releaseAddress 
       * ec2:disassociateAddress 
       * ec2:DisassociateRouteTable 
       * ec2:DeleteNetworkInterface 
       * ec2:DeleteRoute 
       * ec2:DeleteRouteTable 
       * ec2:DeleteInternetGateway 
       * ec2:CreateVpcPeeringConnection 
       * ec2:AcceptVpcPeeringConnection 
       * ec2:DeleteVpcPeeringConnection
   * - Delete clusters 
     - * ec2:TerminateInstances
       * ec2:DeleteSecurityGroup 
       * ec2:AuthorizeSecurityGroupIngress 
       * ec2:RevokeSecurityGroupIngress 
       * ec2:DetachInternetGateway 
       * ec2:DeleteSubnet 
       * ec2:DeleteVpc 
       * cloudformation:DeleteStack 
       * cloudformation:CreateStack 
       * cloudformation:Describe* 
   * - Create a backup bucket on S3 
     - * s3:CreateBucket 
       * s3:PutBucketTagging 
   * - Grant each Scylla instance access to its S3 backup bucket 
     - * iam:CreateRole 
       * iam:AttachRolePolicy 
       * iam:DetachRolePolicy 
       * iam:PassRole 
       * iam:CreatePolicy        
       * iam:CreateInstanceProfile 
       * iam:AddRoleToInstanceProfile 
       * ec2:AssociateIamInstanceProfile
   * - Validate that security policy is complete and up-to-date
     - * iam:GetPolicy
       * iam:GetPolicyVersion


