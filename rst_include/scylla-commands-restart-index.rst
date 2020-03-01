.. tabs::

   .. group-tab:: CentOS 7, Ubuntu 16.04/18.04, Debain 8/9

      .. code-block:: shell

         sudo systemctl restart scylla-server

   .. group-tab:: Ubuntu 14.04, Debian 7

      .. code-block:: shell

         sudo service scylla-server restart

   .. group-tab:: Docker

      .. code-block:: shell

         docker exec -it some-scylla supervisorctl restart scylla

      (without restarting *some-scylla* container)
