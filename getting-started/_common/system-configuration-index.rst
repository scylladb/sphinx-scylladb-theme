Configure Scylla
================

System configuration steps are performed automatically by the Scylla RPM and deb packages. For information on getting started with Scylla, see :doc:`Getting Started </getting-started/index>`.

All Scylla AMIs and Docker images are pre-configured by a script with the following steps. This document is provided as a reference.

System Configuration Files and Scripts
--------------------------------------
Several system configuration settings should be applied. For ease of use, the necessary scripts and configuration files are provided. Files are under :code:`dist/common` and :code:`seastar/scripts` in the Scylla source code, and installed in the appropriate system locations. (For information on Scylla’s own configuration file, see Scylla Configuration.)

System Configuration Files
^^^^^^^^^^^^^^^^^^^^^^^^^^
+----------------------------------------+--------------------------------------------+-----------------------------------+
|Source file	                         |   Installed location	                      | Description                       |
+========================================+============================================+===================================+
|limits.d/scylla.conf	                 | /etc/security/limits.d/scylla.conf         |Remove system resource limits      |
+----------------------------------------+--------------------------------------------+-----------------------------------+
|sysconfig/scylla-server                 |/etc/sysconfig/scylla-server                |  Server startup options           |
+----------------------------------------+--------------------------------------------+-----------------------------------+
|(written by                             | ``/etc/sysconfig/sysctl.d/99-scylla.conf`` | Configure core dumps to use the   |
|``scripts/scylla_coredump_setup``       |                                            | ``scylla_save_coredump`` script   |
|, below)                                |                                            |                                   |
+----------------------------------------+--------------------------------------------+-----------------------------------+

Setup Scripts
^^^^^^^^^^^^^
The following scripts are documented for reference purposes. All of them are invoked by the :code:`scylla_setup` script, which should be run at the time of installation, or when the system hardware changes.

+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------+-----------------------------------------------------------------------+
|Source file                                                                                                                                                                                                       |  Installed location                             |    Description                                                        |
+==================================================================================================================================================================================================================+=================================================+=======================================================================+
|``scripts/scylla_bootparam_setup``                                                                                                                                                                                |   :code:`/usr/lib/scylla/scylla_bootparam_setup`|    Set kernel options in bootloader                                   |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------+-----------------------------------------------------------------------+
|:code:`scripts/scylla_coredump_setup`                                                                                                                                                                             |  :code:`/usr/lib/scylla/scylla_coredump_setup`  |   Remove crash reporting software and set pattern for core dump names |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------+-----------------------------------------------------------------------+
|:code:`scripts/scylla_ntp_setup`                                                                                                                                                                                  |  :code:`/usr/lib/scylla/scylla_ntp_setup`       |   Configure Network Time Protocol                                     |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------+-----------------------------------------------------------------------+
|:code:`scripts/scylla_prepare`                                                                                                                                                                                    |  :code:`/usr/lib/scylla/scylla_prepare`         |   Set up RAID and invoke network configuration                        |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------+-----------------------------------------------------------------------+
|:code:`scripts/scylla_raid_setup`                                                                                                                                                                                 |  :code:`/usr/lib/scylla/scylla_raid_setup`      |   Configure RAID and make XFS filesystem                              |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------+-----------------------------------------------------------------------+
|:code:`scripts/scylla_run`                                                                                                                                                                                        |  :code:`/usr/lib/scylla/scylla_run`             |   Wrapper to run Scylla with arguments from environment               |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------+-----------------------------------------------------------------------+
|:code:`scripts/scylla_save_coredump`                                                                                                                                                                              | :code:`/usr/lib/scylla/save_coredump`           |  Compress a core dump file (Ubuntu only)                              |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------+-----------------------------------------------------------------------+
|:code:`scripts/scylla_stop`                                                                                                                                                                                       |     :code:`/usr/lib/scylla/scylla_stop`         |      Reset network mode if running in virtio or DPDK mode             |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------+-----------------------------------------------------------------------+
|:code:`scripts/scylla_sysconfig_setup`                                                                                                                                                                            | :code:`/usr/lib/scylla/sysconfig_setup`         |  Rewrite the :code:`/etc/sysconfig/scylla file`                       |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------+-----------------------------------------------------------------------+
|:code:`seastar/scripts/posix_net_conf.sh`                                                                                                                                                                         |    :code:`/usr/lib/scylla/posix_net_conf.sh`    |     Set up networking options                                         |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------------------------------------------------+-----------------------------------------------------------------------+

Bootloader Settings
-------------------
If Scylla is installed on an Amazon AMI, the bootloader should provide the :code:`clocksource=tsc` and :code:`tsc=reliable` options. This enables an accurate, high-resolution `Time Stamp Counter (TSC) <https://software.intel.com/en-us/blogs/2013/06/20/eliminate-the-dreaded-clocksource-is-unstable-message-switch-to-tsc-for-a-stable>`_ for setting the system time.

This configuration is provided in the file :code:`/usr/lib/scylla/scylla_bootparam_setup`.

Remove Crash Reporting Software
-------------------------------
Remove the :code:`apport-noui` or :code:`abrt` packages if present, and set up a location and file name pattern for core dumps.

This configuration is provided in the file :code:`/usr/lib/scylla/scylla_bootparam_setup`.

Set Up Network Time Synchronization
-----------------------------------
It is highly recommended to enforce time synchronization between Scylla servers.

Run :code:`ntpstat` on all nodes to check that system time is synchronized. If you are running in a virtualized environment and your system time is set on the host, you may not need to run NTP on the guest. Check the documentation for your platform.

If you have your own time servers shared with an application using Scylla, use the same NTP configuration as for your application servers. The script :code:`/usr/lib/scylla/scylla_ntp_setup` provides sensible defaults, using Amazon NTP servers if installed on the Amazon cloud, and other pool NTP servers otherwise.

Set Up RAID and Filesystem
--------------------------
Setting the file system to XFS is the most important and mandatory for production. Scylla will significantly slow down without it.

The script :code:`/usr/lib/scylla/scylla_raid_setup` performs the necessary RAID configuration and XFS filesystem creation for Scylla.

Arguments to the script are

* :code:`-d` specify disks for RAID
* :code:`-r` MD device name for RAID
* :code:`-u` update /etc/fstab for RAID

On the Scylla AMI, the RAID configuration is handled automatically in the :code:`/usr/lib/scylla/scylla_prepare script`.

CPU Pining
----------

When installing Scylla it is highly recommanded to use the the scylla_setup_ script.
Scylla should not share CPUs with any CPU consuming process. In addition on AWS, we recommend pinning all NIC IRQs to CPU0 (due to the same reason). As a result, Scylla should be prevented from running on CPU0 and its hyper-threading siblings. To verify that Scylla is pinning CPU0 use the command below:
If the node have four or less CPUs don't use this option.

.. _scylla_setup: /getting-started/system-configuration/#setup-scripts

To verify:

.. code-block:: shell

   cat /etc/scylla.d/cpuset.conf 


Example output:

.. code-block:: shell

   --cpuset `1-15,17-31`

Networking
----------
On AWS:
^^^^^^^
1. Prevent irqbalance from moving your NICs’ IRQs.
2. Bind all NICs’ HW queues to CPU0:

.. code-block:: shell

   for irq in `cat /proc/interrupts | grep <networking iface name> | cut -d":" -f1`
   do echo "Binding IRQ $irq to CPU0" echo 1 > /proc/irq/$irq/smp_affinity done

3. Enable RPS and bind RPS queues to CPUs other than CPU0 and its hyper-threading siblings.
4. Enable XPS and distribute all XPS queues among all available CPUs.

The `posix_net_conf.sh <https://github.com/scylladb/seastar/blob/master/scripts/posix_net_conf.sh>`_ script does all of the above.*

On Bare Metal Setups with Multi-Queue NICs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1. Prevent irqbalance from moving your NICs IRQs.
2. Bind each NIC’s IRQ to a separate CPU.
3. Enable XPS exactly the same way as for AWS above.
4. Set higher values for a listen() socket backlog and for unacknowledged pending connections backlog:

.. code-block:: shell

   echo 4096 > /proc/sys/net/core/somaxconn
   echo 4096 > /proc/sys/net/ipv4/tcp_max_syn_backlog

The `posix_net_conf.sh <https://github.com/scylladb/seastar/blob/master/scripts/posix_net_conf.sh>`_ script with the :code:`-mq` parameter does all of the above.

Configuring Scylla
------------------
Configuration for Scylla itself is in the `Scylla Configuration`_ section of the administration guide.

..  _`Scylla Configuration`: /operating-scylla/admin/#scylla-configuration/

Development System Configuration
--------------------------------
*The following item is not required in production.*

When working on DPDK support for Scylla, enable hugepages.

.. code-block:: shell

   NR_HUGEPAGES=128
   mount -t hugetlbfs -o pagesize=2097152 none /mnt/huge
   mount -t hugetlbfs -o pagesize=2097152 none /dev/hugepages/
   for n in /sys/devices/system/node/node?; do
       echo $NR_HUGEPAGES > $n/hugepages/hugepages-2048kB/nr_hugepages;
   done

Huge page configuration is written to :code:`/etc/sysconfig/scylla-server` by the script :code:`/usr/lib/scylla/sysconfig_setup`




Related Topics
--------------

:doc:`System Limits </kb/system-limits>` - outlines the system limits which should be set or removed

.. include:: /rst_include/advance-index.rst


