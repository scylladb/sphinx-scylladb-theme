## Overview

Scylla is a NoSQL database compatible with [Apache Cassandra](http://cassandra.apache.org/).

Scylla will work with existing Apache Cassandra CQL clients. However, mixed clusters of Scylla and Cassandra nodes are not supported. A Scylla node cannot join a Cassandra cluster, and a Cassandra node cannot join a Scylla cluster.

More on [Scylla status](/technology/status).


## System requirements

### Platform support

Scylla runs on 64-bit Linux.  The following operating system releases are supported:

```
| Dist | version |
|------|---------|
| CentOS / RHEL | 7.2 |
| Fedora | 22|
| Ubuntu |  14.04 |
| Ubuntu |  16.04 |
```

Scylla requires a fix to XFS append introduced in kernel *3.15* (back-ported to 3.10 in RHEL/CentOS). Scylla will not run with earlier kernel versions. Details in [Scylla issue 885](https://github.com/scylladb/scylla/issues/885).

### Hardware requirements and sizing

Scylla tries to maximize the resource usage of all system components.  The shard-per-core approach allows linear scale-up with the number of cores.  As you have more cores, it makes sense to balance the other resources, from memory to network.

#### CPU

Any number will work since Scylla scales up with the number of cores.  A practical approach is to use a large number of cores as long as the hardware price remains reasonable. 20-60 logical cores (including hyperthreading) is a good number, but any number fits. When using virtual machines, containers, or public cloud, remember that each virtual CPU is mapped to a single logical core, or hyperthread.

### Memory requirements

One logical core (lcore) is one hyperthreaded core on a hyperthreaded system, or one physical core on a system without hyperthreading.

 * Minimum: 256 MiB on 1 lcore (when run with `--smp 1`)

 * Recommend minimum for test environments: 1 GiB or 256 MiB/lcore (whichever is higher)

 * Recommended minimum for production environments: 4 GiB or 0.5 GiB/lcore (whichever is higher)

 * Typical recommended for production: **16 GiB or 2GiB/lcore** (whichever is higher)

 * Absolute maximum: 1 TiB / lcore, up to 256 lcores

The more memory you have, the better Scylla will perform, since Scylla can use all of it for caching.  The wider your rows in your schema, the more memory you'll need.  64GiB-256GiB is good range for a medium or high workload.

### Disks

We highly recommend SSD and local disks. Scylla is built to handle up to 10TB per node. It is not rare to observe a rate of 1.5TB/s with Scylla per node.  When there are multiple drives, we recommend a RAID-0 setup and a replication factor of 3 within the local datacenter (RF=3).

HDDs are supported but may become a bottleneck. Some workloads may work with HDDs, especially if they play nice and minimize random seeks. An example of an HDD-friendly workload is a write-mostly (98% writes) workload, with minimal random reads. If you use HDDs, try to allocate a separate disk for the commit log (not needed with SSDs).

### Network

10Gbps is preferred, especially for large nodes. Make sure you run our [setup scripts](/doc/system-configuration/#setup-scripts) which tune the interrupts and their queues.  

## Common recommended setups

Overall, it's recommended to have a balanced setup&mdash;if you have just 4-8 lcores, you may not need large disks or 10Gbps networking. It goes the opposite direction as well.  Here are assorted common recommended setups:

### Physical hardware

| Installation | Cores | Memory | Disk | Network |
|------|---------|------|----|-----|
| Test, minimal | 4 | 2 GB | Single plain SSD | 1 Gbps |
| Production | 20 cores - 2 socket, 10 cores each | 128 GB | RAID-0, 4 SSDs, 1-5TBs |  10 Gbps |
| Analytics, heavy duty | 28 cores - 2 socket, 14 cores each | 256GB - 1TB | NVMe, 10TB | 10-56 Gbps |

### Cloud, AWS

We highly recommend i2 instances&mdash;High I/O. This family includes the High Storage Instances that provide very fast SSD-backed instance storage optimized for very high random I/O performance, and provide high IOPS at a low cost. We recommend on using enhanced networking that exposes the physical network cards to the VM.

|Model|	vCPU|	Mem (GB)	| Storage (GB) |
|------|---------|------|----|-----|
|i2.xlarge	|4	|30.5|	1 x 800 SSD|
|i2.2xlarge	|8	|61|	2 x 800 SSD|
|i2.4xlarge	|16	|122|	4 x 800 SSD|
|i2.8xlarge	|32	|244|	8 x 800 SSD|

### Cloud, GCE

Pick a zone where you can find Haswell CPUs. Local SSD performance offers, according to Google, less than 1 ms of latency and up to 680,000 read IOPS and 360,000 write IOPS.  We recommend the CentOS 7.x image with NVMe disk interface. ([More info](https://cloud.google.com/compute/docs/disks/local-ssd))

|Model| vCPU|   Mem (GB)        | Storage (GB) |
|------|---------|------|----|-----|
|n1-standard-8	| 8  | 30 | eight 375 GB partitions for 3 TB |
|n1-standard-16	| 16  |60 |eight 375 GB partitions for 3 TB |
|n1-standard-32	| 32  |120 |  eight 375 GB partitions for 3 TB |
|n1-himem-16	| 16  |104 |eight 375 GB partitions for 3 TB |
|n1-himem-32	| 32  |208 |  eight 375 GB partitions for 3 TB |

## Download and Install

See the [getting started page](/doc/getting-started/) for info on installing Scylla on your platform.

 * [Amazon EC2](/doc/getting-started-amazon/)

 * [Docker](/doc/getting-started/#docker)

 * [Fedora/RHEL/CentOS](/doc/getting-started-rpm/)

 * [Ubuntu 14](/doc/getting-started-ubuntu/)

 * [Ubuntu 16/Debian 8](/doc/getting-started-ubuntu16.04/)


## Migrating data from Apache Cassandra to Scylla
Scylla supports the **ka** version of the Apache Cassandra SSTable format, meaning that your Cassandra version should be 2.1.\* for compatibility.

#### Migrating Data Directory

The default data directory for Scylla is `/var/lib/scylla/data`. To migrate data, simply copy or soft link your Apache Cassandra SSTable directory to this location. The copy will guarantee that your original data is preserved.

#### Migrating the Commit Log

The Apache Cassandra commit log will not be migrated. Make sure to empty (flush) the Apache Cassandra node commit log before migration.

#### Migrating cassandra.yaml config file

Simply copy `cassandra.yaml` to `scylla.yaml`. The `scylla.yaml` default location is `/etc/scylla/scylla.yaml`


## System configuration

See [System Configuration Guide](/doc/system-configuration/) for details on optimum OS settings for Scylla. (These settings are performed automatically in the Scylla packages, Docker containers, and Amazon AMIs.)


## Scylla Configuration

Scylla configuration files are:

|**Installed location**                                                           |**Description**               |
|`/etc/default/scylla-server` (Ubuntu)<br>`/etc/sysconfig/scylla-server` (others) |Server startup options        |
|`/etc/scylla/scylla.yaml`                                                        |Main Scylla configuration file|

### scylla-server 

The `scylla-server` file contains configuration related to starting up the Scylla server.

### scylla.yaml

scylla.yaml is equivalent to the Apache Cassandra cassandra.yaml configuration file, and it is compatible for relevant parameters.
Below is a **subset** of scylla.yaml with parameters you are likely to update. For full list of parameters, look at the file itself.

```yaml
# The name of the cluster. This is mainly used to prevent machines in
# one logical cluster from joining another.
cluster_name: 'Test Cluster'

# This defines the number of tokens randomly assigned to this node on the ring
# The more tokens, relative to other nodes, the larger the proportion of data
# that this node will store. You probably want all nodes to have the same number
# of tokens assuming they have equal hardware capability.
#
# If you already have a cluster with 1 token per node, and wish to migrate to
# multiple tokens per node, see http://wiki.apache.org/cassandra/Operations
num_tokens: 256

# Directory where Scylla should store data on disk.
data_file_directories:
    - /var/lib/scylla/data

# commit log.  when running on magnetic HDD, this should be a
# separate spindle than the data directories.
commitlog_directory: /var/lib/scylla/commitlog

# seed_provider class_name is saved for future use.
# seeds address are mandatory!
seed_provider:
    # Addresses of hosts that are deemed contact points. 
    # Scylla nodes use this list of hosts to find each other and learn
    # the topology of the ring.  You must change this if you are running
    # multiple nodes!
    - class_name: org.apache.cassandra.locator.SimpleSeedProvider
      parameters:
          # seeds is actually a comma-delimited list of addresses.
          # Ex: "<ip1>,<ip2>,<ip3>"
          - seeds: "127.0.0.1"

# Address or interface to bind to and tell other Scylla nodes to connect to.
# You _must_ change this if you want multiple nodes to be able to communicate!
#
# Setting listen_address to 0.0.0.0 is always wrong.
listen_address: localhost

# Address to broadcast to other Scylla nodes
# Leaving this blank will set it to the same value as listen_address
# broadcast_address: 1.2.3.4

# port for the CQL native transport to listen for clients on
# For security reasons, you should not expose this port to the internet.  Firewall it if needed.
native_transport_port: 9042
```

By default scylla.yaml is located at ```/etc/scylla/scylla.yaml```

### scylla.yaml required settings

The following configuration items do not have defaults and must be set.

|*Item*|*Content*|
|seeds|comma-separated list of seed nodes|
|listen_address|IP address of interface for inter-node connections|
|rpc_address|IP address of interface for client connections|

## Configuring TLS/SSL in scylla.yaml

Scylla versions 1.1 and greater support encryption between nodes and between client and node.  See the [Scylla TLS/SSL Guide](/doc/tls-ssl/) for configuration settings.

### Networking

Scylla uses the following ports:

| CQL (native_transport_port) | 9042 | TCP
|Inter-node communication (RPC) |              7000| TCP
|SSL inter-node communication (RPC) |  7001| TCP
|JMX management|                        7199| TCP
| Scylla REST API | 10000 | TCP

All ports above need to be open to external clients (CQL), external admin systems (JMX), and other nodes (RPC).
REST API port can be kept closed for external incoming connections.

The JMX service, `scylla-jmx`, runs on port 7199. It is required in order to manage Scylla using `nodetool` and other Apache Cassandra-compatible utilities. The `scylla-jmx` process must be able to connect to port 10000 on localhost.  The JMX service listens for incoming JMX connections on all network interfaces on the system.

### Advanced networking

It is possible that a client, or another node, may need to use a different IP address to connect to a Scylla node from the address that the node is listening on. This is the case when a node is behind port forwarding.  Scylla allows for setting alternate IP addresses.

Do not set any IP address to `0.0.0.0`.

|*Address*|*Content*|*Default*|
|listen_address|IP address of interface for inter-node connections, as seen from localhost.|No default (required)|
|broadcast_address|IP address of interface for inter-node connections, as seen from other nodes in the cluster.|listen_address|
|rpc_address|IP address of interface for client connections, as seen from localhost|No default (required)|
|broadcast_rpc_address|IP address of interface for client connections, as seen from clients|rpc_address|

If other nodes can connect directly to `listen_address`, then `broadcast_address` does not need to be set.

If clients can connect directly to `rpc_address`, then `broadcast_rpc_address` does not need to be set.

### Core dumps

On RHEL, Fedora and CentOS, the Automatic Bug Reporting Tool ([ABRT](https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/System_Administrators_Guide/ch-abrt.html)) conflict with Scylla coredump configuration. Remove it before installing Scylla: 
`sudo yum remove -y abrt`

Scylla places any core dumps in `var/lib/scylla/coredump`. They and are not visible with the `coredumpctl` command.  See the [System Configuration Guide](/doc/system-configuration/) for details on core dump configuration scripts.  Check with [Scylla support](/support/) before sharing any core dump, as they may contain sensitive data.


## Schedule fstrim

You must run the `fstrim` utility regularly on the filesystem(s) containing your Scylla commitlog and data directory.  This utility will discard, or trim, any blocks no longer in use by the filesystem.

Configure a daily or weekly `cron` job, or equivalent, to run `fstrim`.  You can run `fstrim -a` to trim all mounted filesystems that support it, or trim individual filesystems by passing the mount points as arguments.


## Basic Operations

### Taking a snapshot

Taking a snapshot makes a copy of the current state of Scylla data on a given node.  Each snapshot is node-local and cannot necessarily be used to reconstruct the data for the full cluster.  In order to back up a cluster, you need to take snapshots on multiple or all nodes, depending on replication design.

To create a snapshot:

```sh
nodetool snapshot
```

The result is a large number of files under the Scylla data directory.  A snapshot is not placed in a single file or directory, but spread throughout the Scylla data heirarchy.

Snapshot files are hardlinks, not copies of the individual data files.  Scylla will replace the individual files and leave the snapshots in place.

Scylla assigns a unique snapshot name, an integer, based on the current time.  The output of a successful snapshot command looks like:

```sh
Requested creating snapshot(s) for [all keyspaces] with snapshot name [1452303033540]
Snapshot directory: 1452303033540
```

All snapshot files are named with the pattern:

```sh
$DATA_DIRECTORY/$KEYSPACE/$COLUMN_FAMILY/snapshots/$SNAPSHOT_NAME/$FILENAME
```

For example, a snapshot file in the `chat` keyspace could be named

```sh
/var/lib/scylla/data/chat/users-fd8bf0a0b66f11e58db3000000000000/snapshots/1452302843716/chat-users-ka-1-Data.db
```

This is a data file that is part of the "users" table in the "chat" keyspace.

It is important to keep all the files that are part of a given snapshot together.


### Restoring from a snapshot

Remove any files under `commitlog` and `data` in the Scylla data directory.

Copy the snapshot files into place under `data`.

Move the individual files up two levels, from `snapshots/$SNAPSHOT_NAME` into the main table directory.  For example:

```sh
mv ./snapshots/1452302843716/* .
```

Restart Scylla.


## Monitoring

Scylla exposes three interfaces for online monitoring, as described below.

### JMX

Scylla JMX is compatible with Apache Cassandra, exposing the relevant subset of MBeans.

### REST

For each JMX operation, attribute get and set, Scylla expose a matching REST API.  You can interact with the REST API using `curl` or using the Swagger UI available at ```your-ip:10000/ui```

### Collectd
By default, Scylla send metrics to a local [Collectd](https://collectd.org/) process, allowing you to watch Scylla status with [scyllatop](http://www.scylladb.com/2016/03/22/scyllatop/). Scylla can also sends metric over Collectd protocol to external Collectd server, [Graphite](http://graphite.wikidot.com/) or similar tools.
To forward metrics to external server, update `/etc/collectd.d/scylla.conf` to work as a proxy:

```
LoadPlugin network
<Plugin "network">
  Listen "127.0.0.1" "25826"
  Server "remote-ip" "25826"
  Forward true
</Plugin>
```
Where `remote-ip` is the IP of your external Collectd server. Make sure to keep other elements of the file as is.
Restart the collectd server for the new configuration to apply `sudo service collectd restart`

To change sample rate of Scylla metrics, update the `SCYLLA_ARGS` line in `/etc/sysconfig/scylla-server` file, parameter `--collectd-poll-period 3000` (number in ms).

## Logging

### Logging with the systemd journal (CentOS, Fedora, Amazon AMI, Ubuntu 16.04)

On distributions with systemd, Scylla logs are written to the [systemd journal](http://www.freedesktop.org/software/systemd/man/systemd-journald.service.html).  You can retrieve log entries with the [journalctl](http://www.freedesktop.org/software/systemd/man/journalctl.html) command.

Here are a few useful examples.

* get only Scylla logs: `journalctl _COMM=scylla`
* filter only Scylla logs by priority:
    `journalctl _COMM=scylla -p err..emerg` or
    `journalctl _COMM=scylla -p warning`
* filter only Scylla logs by date:
    `journalctl _COMM=scylla --since="2013-3-16 23:59:59"` or
    `journalctl _COMM=scylla --since "2015-01-10" --until "2015-01-11 03:00"` or
    `journalctl _COMM=scylla --since yesterday`
* filter only Scylla logs since last server boot: `journalctl _COMM=scylla  -b`

### Logging on Ubuntu 14.04

On Ubuntu 14.04, Scylla writes its initial boot message into `/var/log/upstart/scylla-server.log`.

After Scylla has started, logs are stored in `/var/log/syslog`. You can filter Scylla logs by creating a `rsyslog` configuration file with the following rule (for example, in `/etc/rsyslog.d/10-scylla.conf`):

```
:syslogtag, startswith, "scylla" /var/log/scylla/scylla.log
& ~
```

And then creating the log file with the correct permissions and restarting the service:

```
install -o syslog -g adm -m 0640 /dev/null /var/log/scylla/scylla.log
service rsyslog restart
```

This will send Scylla only logs to `/var/log/scylla/scylla.log`.

## Un-contents

Scylla is designed for high performance before tuning, for fewer layers that interact in unpredictable ways, and to use better algorithms that do not require manual tuning. The following items are found in the manuals for other data stores, but do **not** need to appear here.


### Configuration un-contents

* Generating tokens
* Configuring virtual nodes

### Operations un-contents

* Tuning Bloom filters
* Data caching
* Configuring memtable throughput
* Configuring compaction
* Compression

Testing compaction and compression

* Tuning Java resources
* Purging gossip state on a node


## Help with Scylla

Contact [Support]({{ site.baseurl }}/support/), or visit the Scylla [Community](/community/) page for peer support.

## Copyright

© 2017, ScyllaDB. All rights reserved.

© 2016, The Apache Software Foundation.

Apache®, Apache Cassandra®, Cassandra®, the Apache feather logo and and the Apache Cassandra® Eye logo are either registered trademarks or trademarks of the Apache Software Foundation in the United States and/or other countries. No endorsement by The Apache Software Foundation is implied by the use of these marks.
