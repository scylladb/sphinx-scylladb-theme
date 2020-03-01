Nodetool status
===============
**status** - Print the cluster information for a single or all keypsaces.

For example:

::

    nodetool status

Example output:

::

    Print the cluster information for a single or all keypsaces

    Datacenter: datacenter1
    =======================
    Status=Up/Down
    |/ State=Normal/Leaving/Joining/Moving
    --  Address    Load       Tokens  Owns (effective)  Host ID                               Rack
    UN  127.0.0.1  394.97 MB  256     33.4%             292a6c7f-2063-484c-b54d-9015216f1750  rack1
    UN  127.0.0.2  151.07 MB  256     34.3%             102b6ecd-2081-4073-8172-bf818c35e27b  rack1
    UN  127.0.0.3  249.07 MB  256     32.3%             20db6ecd-2981-447s-l172-jf118c17o27y  rack1

+----------+---------------------------------------+
|Parameter |Description                            |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
+==========+=======================================+
|Datacenter|Which data center holds the informati  |
|          |on                                     |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
+----------+---------------------------------------+
|Status    |U for up or D for down                 |
|          |                                       |
|          |                                       |
+----------+---------------------------------------+
|State     |(N)ormal, (L)eaving , (J)oining or     |
|          |(M)oving                               |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
+----------+---------------------------------------+
|Address   |Node IP address                        |
|          |                                       |
+----------+---------------------------------------+
|Load      |The size on disk the scylla data takes |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
+----------+---------------------------------------+
|Tokens    |The number of tokens per node          |
|          |                                       |
|          |                                       |
|          |                                       |
+----------+---------------------------------------+
|Owns      |Show the data percentage owned by the  |
|          |node (per datacenter) times the        |
|          |replication factor that you are using  |
|          |For example - node can own 25% of the  |
|          |ring, but show 100% if the replication |
|          |factor is 4                            |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
|          |                                       |
+----------+---------------------------------------+
|Host ID   |The host network ID                    |
|          |                                       |
|          |                                       |
+----------+---------------------------------------+
|Rack      |The rack                               |
+----------+---------------------------------------+

.. include:: nodetool-index.rst
