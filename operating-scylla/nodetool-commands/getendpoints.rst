Nodetool getendpoints
=====================
**getendpoints** - :code:`<keyspace>` :code:`<table>` :code:`<key>`- Print the end-points IP or name of the nodes that own the partition key.

Use this command to know which node holds the specific partition key.

For example:

``nodetool getendpoints nba player_name Russell``

==========  ==============  
Parameter   Description  
==========  ==============  
keyspace    keyspace name       
----------  --------------  
table       table name           
----------  --------------  
key         partition key  
==========  ==============  



.. include:: nodetool-index.rst
