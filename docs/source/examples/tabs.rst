====
Tabs
====

Using:

.. code-block:: rst

   .. tabs::

      .. group-tab:: CentOS 7, Ubuntu 16.04/18.04, Debian 8/9

         .. code-block:: shell

            sudo systemctl stop scylla-server

      .. group-tab:: Ubuntu 14.04, Debian 7

         .. code-block:: shell

            sudo service scylla-server stop

      .. group-tab:: Docker

         .. code-block:: shell

            docker exec -it some-scylla supervisorctl stop scylla

         (without stopping *some-scylla* container)

Results in:

.. tabs::

   .. group-tab:: CentOS 7, Ubuntu 16.04/18.04, Debian 8/9

      .. code-block:: shell

         sudo systemctl stop scylla-server

   .. group-tab:: Ubuntu 14.04, Debian 7

      .. code-block:: shell

         sudo service scylla-server stop

   .. group-tab:: Docker

      .. code-block:: shell

         docker exec -it some-scylla supervisorctl stop scylla

      (without stopping *some-scylla* container)
