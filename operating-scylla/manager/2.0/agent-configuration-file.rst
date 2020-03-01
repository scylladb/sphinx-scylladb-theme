========================
Agent Configuration File
========================

.. contents::
   :depth: 2
   :local:


This document covers the configurations settings you need to consider for the Sylla Manager Agent. 

The Scylla Manager Agent has a single configuration file /etc/scylla-manager-agent/scylla-manager-agent.yaml. 

Authentication token
====================

.. note:: Completing this section in the scylla-manager-agent.yaml file is mandatory

Scylla Agent uses token authentication in API calls so that the Scylla Manager Server can authenticate itself with the Scylla Manager Agent.
Once you have `created a token <../install-agent/#generate-an-authentication-token>`_ , and have configured the `agent configuration file <../install-agent/#configure-authentication-token-parameters>`_ as described.

.. code-block:: none

   # Specify authentication token
   auth_token: 6Es3dm24U72NzAu9ANWmU3C4ALyVZhwwPZZPWtK10eYGHJ24wMoh9SQxRZEluWMc0qDrsWCCshvfhk9uewOimQS2x5yNTYUEoIkO1VpSmTFu5fsFyoDgEkmNrCJpXtfM

HTTPS server settings
=====================

In this section, you can specify to which address Scylla Agent should listen.
By default, Scylla Manager Agent pulls these values from the Scylla itself.
Port 10001 is the default port, and traffic to this port should be allowed on firewall.
You can change the port to a different port by clearing the ``https`` label and adding an IP address and port.
In order to obtain TLS cert and key file, use the ``scyllamgr_ssl_cert_gen`` script.  

.. code-block:: none

   # Bind REST API to the specified TCP address using HTTPS protocol. By default
   # Scylla Manager Agent uses Scylla listen/broadcast address that is read from
   # the Scylla API (see scylla section).
   #https: 0.0.0.0:10001

   # TLS certificate and key files to use with HTTPS. To regenerate the files use
   # scyllamgr_ssl_cert_gen script shipped with the Scylla Manager Agent.
   #tls_cert_file: /var/lib/scylla-manager/scylla_manager.crt
   #tls_key_file: /var/lib/scylla-manager/scylla_manager.key

Prometheus settings
===================

In this section, you can set the Prometheus settings for the Scylla Manager Agent so that the Agent Manager metrics (from each Sylla node) can be viewed and monitored with Scylla Monitoring. 

.. code-block:: none

   # Bind prometheus API to the specified TCP address using HTTP protocol.
   # By default it binds to all network interfaces but you can restrict it
   # by specifying it like this 127:0.0.1:56090 or any other combination
   # of ip and port.
   #prometheus: ':56090'

If you change the Prometheus IP or port you must adjust the rules in the Prometheus server.

.. code-block:: none

   - targets:
     - IP:56090

Debug endpoint settings
=======================

In this section, you can enable the pprof debug server that allows you to run profiling on demand on a live application. By default, the server is not running, but to enable it set the IP and port as shown:

.. code-block:: none

   debug: 127.0.0.1:56112

CPU pinning settings
=======================

In this section, you can set the ``cpu`` setting which dictates the CPU to run Scylla Manager Agent on. 
By default, the agent reads the Scylla configuration from ``/etc/scylla.d/cpuset.conf`` and tries to find a core that is not used by Scylla. 
If that's not possible you can specify the core on which to run the Scylla Manager Agent.

.. code-block:: none

   cpu: 0

Log level settings
==================

In this section, you can set the Log level settings which specify log output and level. Available log levels are ``error``, ``info`` and ``debug``.

.. code-block:: none

   logger:
     level: info

Scylla API settings
===================

In this section, you can set the Scylla API settings. Scylla Manager Agent pulls all needed configuration options from the ``scylla.yaml`` file. In order to do this, Scylla Manager Agent needs to know where the Scylla API is exposed. You should copy the ``api_address`` and ``api_port`` values from ``/etc/scylla/scylla.yaml`` and add them here:

.. code-block:: none

   #scylla:
   #  api_address: 0.0.0.0
   #  api_port: 10000

Backup s3 settings
==================

In this section, you configure the AWS credentials (if required) for the backup location. 


IAM Role example
----------------

.. note:: If you are setting an IAM role in AWS, you do not need to change this section.  

.. _credentials:

AWS credentials configuration
-----------------------------

.. note:: Completing this section in the scylla-manager-agent.yaml file is mandatory if you are not using an IAM role. Make sure you understand the security ramifications of placing AWS credentials into the yaml file. 

Fill in the information below with your AWS Credentials information. If you do not know where your keys are located, read the `AWS Security Blogs <https://aws.amazon.com/blogs/security/wheres-my-secret-access-key/>`_ or `documentation <https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys>`_ for information.

.. code-block:: none

   s3:
   # S3 credentials, it's recommended to use IAM roles if possible, otherwise set
   # your AWS Access Key ID and AWS Secret Access Key (password) here.
     access_key_id: <your access key id>
     secret_access_key: <your secret access key> 
   #
   # Region to connect to, if running in AWS EC2 instance region is set
   # to the local region by default.
   #  region:
   #
   # Endpoint for S3 API, only relevant when using S3 compatible API.
   #  endpoint:
   #
   # The server-side encryption algorithm used when storing this object in S3.
   # If using KMS ID you must provide the ARN of Key.
   #  server_side_encryption:
   #  sse_kms_key_id:
   #
   # AWS S3 Transfer acceleration
   # https://docs.aws.amazon.com/AmazonS3/latest/dev/transfer-acceleration-examples.html
   #  use_accelerate_endpoint: false
   
Additional resources
====================

Scylla Manager `Configuration file <../configuration-file>`_
