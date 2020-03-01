
==============================
Integrate Scylla with Kafka
==============================

.. toctree::
   :hidden:
   
   kafka-connector
   sink-config

Apache Kafka is capable of delivering reliable, scalable, high-throughput data streams across a myriad of data sources and sinks. A great number of open source users and enterprise customers use Scylla and Kafka together. You can use Scylla and Apache Kafka in integration solutions such as creating a scalable backend for an IoT service.


Shard-Aware Kafka Connector for Scylla
==========================================

You can use the Kafka Sink Connector for Scylla to bridge Scylla and Kafa. The connector allows you to use Apache Kafka and the Confluent platform while taking advantage of Scylla’s underlying shard-per-core, shared-nothing architecture.  

The following documents will get you started with the Kafka Connector:

* `Kafka Sink Connector Quickstart <../kafka-connector/>`_
* `Kafka Sink Connector Configuration <../sink-config/>`_
* `Introducing the Kafka Scylla Connector <https://www.scylladb.com/2020/02/18/introducing-the-kafka-scylla-connector/>`_ - Scylla Users blog

If you have tested your application with Scylla and Kafka and want to publish the results, contact us using the `mailing list <https://groups.google.com/d/forum/scylladb-users>`_.


