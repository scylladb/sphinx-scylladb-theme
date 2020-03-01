.. tabs::

   .. group-tab:: CentOS 7, Ubuntu 16.04/18.04, Debain 8/9

      .. code-block:: shell
                            
         sudo systemctl start scylla-server

   .. group-tab:: Ubuntu 14.04, Debian 7

      .. code-block:: shell

         sudo service scylla-server start

   .. group-tab:: Docker

      .. code-block:: shell

         docker exec -it some-scylla supervisorctl start scylla

      (with *some-scylla* container already running)
               
