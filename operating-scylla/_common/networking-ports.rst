
Scylla uses the following ports:

======  ============================================  ========
Port    Description                                   Protocol
======  ============================================  ========
9042    CQL (native_transport_port)                   TCP
------  --------------------------------------------  --------
9142    SSL CQL (secure client to node)               TCP
------  --------------------------------------------  --------
7000    Inter-node communication (RPC)                TCP
------  --------------------------------------------  --------
7001    SSL inter-node communication (RPC)            TCP
------  --------------------------------------------  --------
7199    JMX management                                TCP
------  --------------------------------------------  --------
10000   Scylla REST API                               TCP
------  --------------------------------------------  --------
9180    Prometheus API                                TCP
------  --------------------------------------------  --------
9100    node_exporter (Optionally)                    TCP
------  --------------------------------------------  --------
9160    Scylla client port (Thrift)                   TCP
------  --------------------------------------------  --------
10001   Scylla Manager Agent REST API :sup:`*`        TCP
------  --------------------------------------------  --------
5609    Scylla Manager Prometheus API                 HTTP
------  --------------------------------------------  --------
56090   Scylla Manager Agent Prometheus API :sup:`*`  TCP 
======  ============================================  ========

:sup:`*` Available in Scylla Manager version 2.0 and higher
