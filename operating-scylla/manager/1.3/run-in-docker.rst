

=============
Run in Docker
=============

.. contents::
   :depth: 2
   :local:

.. versionadded:: 1.3.1 Scylla Manager

The best way to run Scylla Manager in a Docker container is by using the official `Scylla Manager Docker image <https://hub.docker.com/r/scylladb/scylla/scylla-manager>`_.
You can pull the image directly from Docker Hub.

.. code-block::  none

   docker pull scylladb/scylla-manager

Scylla Manager is using Scylla as a backend storage.
When running Scylla Manager in a Docker container, you can either use an existing Scylla cluster as a backend or run a dedicated Scylla container and link them.
This can be done automatically with docker-compose (refer to `Running with docker-compose`_) or manually with plain Docker command (refer to `Running with docker`_).

.. note:: Scylla Manager for Scylla Open Source users is limited to 5 nodes. See the `Scylla Manager Proprietary Software License Agreement <https://www.scylladb.com/scylla-manager-software-license-agreement/>`_.

Running with docker-compose
---------------------------

`Docker compose <https://docs.docker.com/compose/>`_ is a tool for defining and running multi-container applications.

**Procedure**

1. Copy the following snippet and save it to your current working directory as ``docker-compose.yaml``.

.. code-block:: yaml

   version: '3'

   services:
     scylla-manager:
       image: scylladb/scylla-manager
       container_name: scylla-manager
       depends_on:
         - scylla-manager-db

     scylla-manager-db:
       image: scylladb/scylla
       container_name: scylla-manager-db

This file instructs Docker to create two containers, *scylla-manager* that runs the Scylla Manager Server, and *scylla-manager-db* that Scylla Manager uses to save its data.

2. Create and start the containers by running the ``docker-compose`` command.

.. code-block:: none

   docker-compose up -d

3. Verify that Scylla Manager started by using the ``docker-compose logs`` command.

.. code-block:: none

   docker-compose logs -f scylla-manager

4. Continue to `using sctool`_.

Running with Docker
-------------------

**Procedure**

1. Start a Scylla container to use as the datastore for Scylla Manager data.

.. code-block:: none

   docker run -d --name scylla-manager-db scylladb/scylla

More on :doc:`Best Practices for Running Scylla on Docker </operating-scylla/procedures/tips/best_practices_scylla_on_docker>`

2. Start Scylla Manager container and link with the *scylla-manager-db* container.

.. code-block:: none

   docker run -d --name scylla-manager --link scylla-manager-db scylladb/scylla-manager

Scylla Manager expects a Scylla node available as *scylla-manager-db*.

.. note:: You can give the Scylla container a different name or connect scylla-manager-db container to an already existing container. To do so, use the scylla-manager-db alias in the following link flag: ``--link some-scylla:scylla-manager-db.``

3. Verify that Scylla Manager stared by using ``docker logs`` command.

.. code-block:: none

   docker logs -f scylla-manager

Using sctool
------------

Sctool is the Scylla Manager commandline tool, to learn more about it see `sctool reference <../sctool>`_.

Use ``docker exec`` to invoke sctool in a running container.

.. code-block:: none

   docker exec -it scylla-manager sctool version

You can also exec bash and run sctool from within a bash session in the container.
This would give you the benefit of bash completion for sctool.

.. code-block:: none

   docker exec -it scylla-manager bash
   [root@49910e75d06f /]# sctool
   cluster  repair   status   task     version
   [root@49910e75d06f /]# sctool version

Using a remote database
-----------------------

If you with to persist Scylla Manager data on a remote cluster you need to adjust the configuration options.
The `configuration file </operating-scylla/manager/1.3/configuration-file/>`_ document covers all the Scylla Manager configuration options.

**Procedure**

1. Open editor and create an empty yaml file.

2. Copy the ``database`` and ``ssl`` sections from `the configuration file document </operating-scylla/manager/1.3/configuration-file/>`_.

3. Follow the procedure in `edit scylla manager configuration <../use-a-remote-db/#edit-scylla-manager-configuration>`_ and adjust the configuration file.

4. Optionally, you can remove any comments or not changed lines leaving only relevant changes.

5. Save the file as ``scylla-manager-user.yaml`` in an appropriate location.

6. Start *scylla-manager* container with file ``scylla-manager-user.yaml`` you created earlier mounted as a volume. Pass it as an additional Docker command (``docker run``) parameter.

.. code-block:: none

   docker run -d --name scylla-manager --link scylla-manager-db scylladb/scylla-manager -c /etc/scylla-manager/scylla-manager-user.yaml

Exposed ports
-------------

Scylla Manager exposes the following ports, which are used for integrating Scylla Manager with other services such as Scylla Monitoring.

.. list-table::
   :widths: 15 15 70
   :header-rows: 1

   * - Port
     - Network
     - Service
   * - 56080
     - tcp
     - HTTP server
   * - 56443
     - tcp
     - HTTPS server
   * - 56090
     - tcp
     - Prometheus metrics
   * - 56112
     - tcp
     - Diagnostic port

Exposed volumes
---------------

It is often useful to attach host files and directories to the Scylla Manager container.  The following volumes are exposed from Scylla Manager.

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Path
     - Contents
   * - /var/lib/scylla-manager/.certs
     - SSH identity files and SSL key pairs to access the managed clusters
   * - /var/lib/scylla-manager/scylla_manager.crt
     - HTTPS certificate
   * - /var/lib/scylla-manager/scylla_manager.key
     - HTTPS key

Example for mapping Scylla Manager a volume in ``docker run`` command:

.. code::

   docker run -d --name scylla-manager -v certs:/var/lib/scylla-manager/.certs:Z \
   -v scylla-manager-user.yaml:/etc/scylla-manager/scylla-manager-user.yaml \
   --link scylla-manager-db scylladb/scylla-manager -c /etc/scylla-manager/scylla-manager-user.yaml

