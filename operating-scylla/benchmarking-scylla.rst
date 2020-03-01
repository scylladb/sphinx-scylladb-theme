===================
Benchmarking Scylla
===================

.. contents::
   :local:

Benchmarking NoSQL databases is always a tricky task. Benchmarking Scylla is no different. On the contrary: while Scylla, by using the Seastar framework, does an excellent job in isolating itself from most of OS and third-party components’ performance influences, that same ability may cause existing setups not to use Scylla to its full potential.

Not long ago, Datastax’ Jonathan Ellis wrote a by now famous article named `How not to benchmark Cassandra <http://www.datastax.com/dev/blog/how-not-to-benchmark-cassandra>`_. That article provides invaluable insights about what are common caveats one should take into account while testing Cassandra. Most of those remarks arise from how Cassandra is architected and since Scylla employs the same architecture, it is recommended that one start from there. That is all still relevant for Scylla deployments.

This document targets people who are already familiar with benchmarking Apache Cassandra, and focuses on things one should keep in mind while evaluating the performance of Scylla, specially but not limited to, in comparison to Cassandra.

Basic server setup

Scylla is not meant to be ran over rotating media. Because of that, even more so than in traditional setups, an SSD must be used for any performance meaningful measurement.

As it is the case for any SSD setup, one must make sure the partitions are properly aligned to the SSD’s erase block size. There is an array of documents online describing how to do that, like `this article <https://wiki.archlinux.org/index.php/Partitioning#Partition_alignment>`_ and `this <https://www.thomas-krenn.com/en/wiki/Optimize_SSD_Performance>`_. One also should check that the io scheduler configuration is sane, which can be done by:

.. code-block:: shell

   cat /sys/class/block/<device>/queue/scheduler

   noop [deadline] cfq

While we do recommend the deadline scheduler, noop should ultimately be fine. But do make sure you are not using the cfq.

Any meaningful measurement must be extracted using the XFS filesystem, so make sure you are testing against that. You can set that up in scylla.yaml the same way you would for cassandra.yaml.

Networking
..........
To achieve top performance, Scylla should use DPDK. Of course, if your Deployment will not include a card that is supported by DPDK, you can safely benchmark using Scylla’s POSIX stack. But for best results, do consider using cards supported by the DPDK project.

Client Setup
............
Unfortunately, the YCSB benchmark is `known not to work <https://github.com/brianfrankcooper/YCSB/issues/293>`_ with the cassandra-cql driver for Cassandra-2.1. That being the Apache Cassandra version with which Scylla claims compatibility, that will not work for Scylla as well. On the other hand, cassandra-stress is expected to work fine. However, the client count as compared to a previous Cassandra deployment will surely need to be raised. While benchmarking, one should not assume that the same client count used to extract maximum performance from Cassandra will do the same for Scylla. It will not.

Even within the same client machine, with all else being equal, you should see better results if you aggregate more than one process instead of just bumping the number of threads in a single process. That is specially true for cassandra-stress, that will keep a fixed number of socket connections ongoing even at higher thread counts. Scylla will work better with more connections that will allow it to better distribute its load. If you are running your own benchmark in which you control the connection count, you should experiment with making that higher.

When using multiple processes in the same client machine, use taskset to make sure that the processes are properly isolated from each other. An example command line that restricts each process to 4 cores (may not be the best for your case) would be:

.. code-block:: shell

   CPU=0
   for i in $(seq 0 $((PROCESSES-1))); do
   taskset -c $CPU,$(($CPU+1)),$(($CPU+2)),$((CPU+3))	\
   cassandra-stress user profile=$FILE ops\($OPS\) duration=$DUR -rate \
   threads=$THREADS -node $NODE -mode cql3 native -log file=$LDIR/$i &
	   CPU=$((CPU+4))
   done

That assumes the proper keyspace and tables all already exist.

Benchmark Hygiene
.................

Caching and Warming Up
......................
Let’s start by talking prep work: it is usually advisable to drop all OS caches before starting any benchmark that is expected the disk. While this is not harmful to Scylla - you can keep it in your scripts if they were already there - it is not needed. Scylla uses Direct I/O to read from and write to the disk, which should bypass the OS’ page cache.

Warm up time also has a very different meaning when comparing Apache Cassandra and Scylla. Because Scylla does not depend on the JVM or any other JIT-employing technique, warm up times of the database code are not relevant for Scylla. However, for a read workload, Scylla’s caches will obviously take time to warm up.

This is an area in which Apache Cassandra and Scylla differ radically: the former relies on the Linux page cache and having a row cache as an auxiliary mechanism, while the latter bypasses the Linux page cache entirely and makes a row cache central to performance. For that reason, the warm up time used for previous Cassandra runs should not assumed to be relevant for Scylla, and should be independently determined.

The same applies for the number of rows you are dealing with: due to their different caching mechanisms, the amount of rows that each database will be able to cache varies. As a result of that, an workload that forces Apache Cassandra to the disk may be kept entirely in-memory for Scylla. If you want to make sure the some reads are hitting the disk, do not assume the same partition count will do the job.

Handling the Data Directory
...........................
Write benchmarks should always be ran against an empty data directory. It is fine in principle to reboot Scylla reusing the same data directory, if that is the scenario you would like to test: cold boot read times, etc. But care must be taken while doing this: because Scylla and Apache Cassandra use the same file format for their SSTables, one could be tempted to reuse them between runs to test read workloads.

That should not be done. Despite the format of the individual file being the same, Scylla keeps tracks of its SSTables in a very different fashion, with individual cores being responsible for different tables. Using Apache Cassandra SSTables with Scylla will work, but will force Scylla to keep track of more metadata than would have been otherwise the case. For similar reasons, the same is true for runs between which you change Scylla’s core count.

Doing the other way around - using Scylla tables with Apache Cassandra - should be even worse, specially for large core counts: not being aware of any sharding, Cassandra will try to read from many of them, and ultimately be unfairly penalized. In a nutshell, it’s fine to reuse the same data directory if and only if you don’t really change anything else

Further Reading
...............
* `Scylla vs. Apache Cassandra benchmark <http://www.scylladb.com/technology/cassandra-vs-scylla-benchmark/>`_
* `Low level analysis of performance metrics <http://www.scylladb.com/2015/09/22/watching_scylla_serve_1m/>`_
* `Scylla Procedures </operating-scylla/procedures/>`_

Copyright
^^^^^^^^^

.. include:: /rst_include/apache-copyrights-index.rst

.. include:: /rst_include/apache-copyrights-index-all-attributes.rst



