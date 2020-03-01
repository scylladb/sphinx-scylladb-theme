===================
System Requirements
===================

.. contents::
   :depth: 2
   :local:

Supported Platforms
===================

Scylla runs on 64-bit Linux. The following operating system releases are supported:

.. list-table::
   :widths: 60 40
   :header-rows: 1

   * - Linux distribution  
     - Version
   * - CentOS/RHEL/Oracle Linux
     - 7.2 and above
   * - Ubuntu
     - 14.04 :sup:`*`, 16.04
   * - Ubuntu
     - 18.04 :sup:`**`
   * - Debian 
     - 8.6 and above (minor releases)
   * - Debian 
     - 9.0 :sup:`**`

:sup:`*` Supported in Scylla 3.0 and below. Not supported in Scylla 3.1 and 2019.1 and above

:sup:`**` Supported in Scylla 2.3 and above

.. note:: Ubuntu 14 is not supported in future versions of Scylla Open Source 3.1 and Scylla Eneterprise 2019.1 and above. This is because Ubuntu has decided to EOL version 14. For more details refer to `Ubuntu Release page <https://wiki.ubuntu.com/Releases>`_.

For a more detailed list with recommendations refer to `Operating System (OS) Support Guide </kb/os-support/>`_.

Scylla requires a fix to the XFS append introduced in kernel 3.15 (back-ported to 3.10 in RHEL/CentOS). Scylla will not run with earlier kernel versions. Details in `Scylla issue 885 <https://github.com/scylladb/scylla/issues/885>`_.

Hardware Requirements
=====================

It’s recommended to have a balanced setup. If there are only 4-8 :term:`Logical Cores <Logical Core (lcore)>`, large disks or 10Gbps networking may not be needed. This works in the opposite direction as well. Scylla can be used in many types of installation environments. Each one has its own recommended hardware requirements. The three use cases most often used with their requirements include:

=====================  ==================================  ==============  =======================  =============
Installation           Cores                               Memory	       Disk                     Network
=====================  ==================================  ==============  =======================  =============
Test, minimal          4                                   2 GB	           Single plain SSD         1 Gbps
---------------------  ----------------------------------  --------------  -----------------------  -------------
Production             20 cores - 2 socket, 10 cores each  128 GB          RAID-0, 4 SSDs, 1-5 TBs  10 Gbps
---------------------  ----------------------------------  --------------  -----------------------  -------------
Analytics, heavy duty  28 cores - 2 socket, 14 cores each  256 GB - 1 TB   NVMe, 10 TB              10-56 Gbps
=====================  ==================================  ==============  =======================  =============


Core Requirements 
-----------------
Scylla tries to maximize the resource usage of all system components. The shard-per-core approach allows linear scale-up with the number of cores. As you have more cores, it makes sense to balance the other resources, from memory to network.

CPU
^^^
Scylla requires modern Intel CPUs that support the SSE4.2 instruction set and will not boot without it.

In terms of the number of cores, any number will work since Scylla scales up with the number of cores. A practical approach is to use a large number of cores as long as the hardware price remains reasonable. Between 20-60 logical cores (including hyperthreading) is a recommended number. However any number will fit. When using virtual machines, containers, or the public cloud, remember that each virtual CPU is mapped to a single logical core, or hyperthread. Allow Scylla to run independently without any additional CPU intensive tasks on the same server/cores as Scylla.

Memory Requirements
-------------------
The more memory available, the better Scylla performs, as Scylla uses all of available memory for caching. The wider the rows are in the schema, the more memory will be required. 64 GB-256 GB is the recommended range for a medium to high workload. Memory requirements are calculated based on the number of :abbr:`lcores (logical cores)` you are using in your system. 

* Recommended size: 16 GB or 2GB per lcore (whichever is higher)
* Maximum: 1 TiB per lcore, up to 256 lcores
* Minimum: 

  - For test environments: 1 GB or 256 MiB per lcore (whichever is higher)
  - For production environments: 4 GB or 0.5 GB per lcore (whichever is higher)


Disk Requirements
-----------------

SSD
^^^
We highly recommend SSD and local disks. Scylla is built for a large volume of data and large storage per node. The rule of thumb is using 30:1 Disk/RAM ratio, for example, 30 TB of storage requires 1 TB of RAM. When there are multiple drives, we recommend a RAID-0 setup and a replication factor of 3 within the local datacenter (RF=3). 

HDD
^^^
HDDs are supported but may become a bottleneck. Some workloads may work with HDDs, especially if they play nice and minimize random seeks. An example of an HDD-friendly workload is a write-mostly (98% writes) workload, with minimal random reads. If you use HDDs, try to allocate a separate disk for the commit log (not needed with SSDs).

Network Requirements
--------------------

Network speed of 10 Gbps or more is recommended, especially for large nodes. To tune the interrupts and their queues, run the Scylla setup scripts.

Cloud Instance Recommendations
===============================

Amazon Web Services (AWS)
--------------------------------

We highly recommend EC2 **I3** instances—High I/O. This family includes the High Storage Instances that provide very fast SSD-backed instance storage optimized for very high random I/O performance, and provide high IOPS at a low cost. We recommend on using enhanced networking that exposes the physical network cards to the VM.

i3 instances are designed for I/O intensive workloads and equipped with super-efficient NVMe SSD storage, it can deliver up to 3.3 Million IOPS.
An i3 instance is great for low latency and high throughput, compared to the i2 instances, the i3 instance provides storage that it's less expensive and denser along with the ability to deliver substantially more IOPS and more network bandwidth per CPU core.

i3 instances
^^^^^^^^^^^^
===========================  ===========  ============  =====================
Model	                     vCPU         Mem (GB)      Storage (NVMe SSD)
===========================  ===========  ============  =====================
i3.xlarge	             4	          30.5	        0.950 TB
---------------------------  -----------  ------------  ---------------------
i3.2xlarge	             8	          61	        1.9 TB
---------------------------  -----------  ------------  ---------------------
i3.4xlarge	             16	          122           3.8 TB
---------------------------  -----------  ------------  ---------------------
i3.8xlarge	             32	          244           7.6 TB
---------------------------  -----------  ------------  ---------------------
i3.16xlarge	             64	          488	        15.2 TB
---------------------------  -----------  ------------  ---------------------
i3.metal New in version 2.3  72 :sup:`*`  512           8 x 1.9 NVMe SSD
===========================  ===========  ============  =====================

:sup:`*` i3.metal provides 72 logical processors on 36 physical cores

Source: `EC2 Instance Types <https://aws.amazon.com/ec2/instance-types/i3/>`_

More on using Scylla with `i3.metal vs i3.16xlarge <https://www.scylladb.com/2018/06/21/impact-virtualization-database/>`_ 

i3en instances
^^^^^^^^^^^^^^
i3en instances have up to 4x the networking bandwidth of i3 instances, enabling up to 100 Gbps of sustained network bandwidth. 

i3en support is available for Scylla Enterprise 2019.1.1 and higher and Scylla Open Source 3.1 and higher. 


===========================  ===========  ============  =====================
Model	                     vCPU         Mem (GB)      Storage (NVMe SSD)
===========================  ===========  ============  =====================
i3en.large	             2	          16	        1 x 1,250 GB
---------------------------  -----------  ------------  ---------------------
i3en.xlarge	             4	          32	        1 x 2,500 GB
---------------------------  -----------  ------------  ---------------------
i3en.2xlarge	             8	          64	        2 x 2,500 GB
---------------------------  -----------  ------------  ---------------------
i3en.3xlarge	             12	          96            1 x 7,500 GB
---------------------------  -----------  ------------  ---------------------
i3en.6xlarge	             24	          192           2 x 7,500 GB
---------------------------  -----------  ------------  ---------------------
i3en.12xlarge	             48	          384	        4 x 7,500 GB
---------------------------  -----------  ------------  ---------------------
i3en.24xlarge	             96	          768	        8 x 7,500 GB
===========================  ===========  ============  =====================

All i3en instances have the following specs:

* 3.1 GHz all core turbo Intel® Xeon® Scalable (Skylake) processors
* Intel AVX†, Intel AVX2†, Intel AVX-512†, Intel Turbo 
* EBS Optimized
* Enhanced Networking

Refer to `Amazon Web Services <https://aws.amazon.com/ec2/instance-types/i3en/>`_ for specific information. 

Google Compute Engine (GCE)
-----------------------------------

Pick a zone where Haswell CPUs are found. Local SSD performance offers, according to Google, less than 1 ms of latency and up to 680,000 read IOPS and 360,000 write IOPS. The CentOS 7.x image with NVMe disk interface is recommended. (`More info <https://cloud.google.com/compute/docs/disks/local-ssd>`_)

.. list-table::
   :widths: 30 20 20 30
   :header-rows: 1

   * - Model
     - vCPU
     - Mem (GB)
     - Storage
   * - n1-standard-8
     - 8
     - 30
     - 8x 375 GB partitions for 3 TB
   * - n1-standard-16
     - 16
     - 60
     - 8x 375 GB partitions for 3 TB
   * - n1-standard-32
     - 32
     - 120
     - 8x 375 GB partitions for 3 TB
   * - n1-himem-16
     - 16
     - 104
     - 8x 375 GB partitions for 3 TB
   * - n1-himem-32
     - 32
     - 208
     - 8x 375 GB partitions for 3 TB

Microsoft Azure
---------------

The `Lsv2-series <https://azure.microsoft.com/en-us/blog/announcing-the-general-availability-of-lsv2-series-azure-virtual-machines/>`_  features high throughput, low latency, and directly mapped local NVMe storage. The Lsv2 VMs run on the AMD EPYCTM 7551 processor with an all core boost of 2.55GHz.


.. list-table::
   :widths: 30 20 20 30
   :header-rows: 1

   * - Model
     - vCPU
     - Mem (GB)
     - Storage
   * - L8s_v2
     - 8
     - 64
     - 1 x 1.92 TB
   * - L16s_v2
     - 16
     - 128
     - 2 x 1.92 TB
   * - L32s_v2
     - 32
     - 256
     - 4 x 1.92 TB
   * - L64s_v2
     - 64
     - 512
     - 8 x  1.92 TB
   * - L80s_v2
     - 80
     - 640
     - 10 x 1.92 TB
       
More on Azure Lsv2 instances `here <https://azure.microsoft.com/en-us/blog/announcing-the-general-availability-of-lsv2-series-azure-virtual-machines/>`_

Oracle Cloud Infrastructure (OCI)
----------------------------------------

An OCPU is defined as the CPU capacity equivalent of one physical core of an Intel Xeon processor with hyper threading enabled. For Intel Xeon processor each OCPU corresponds to two hardware execution threads, known as vCPUs.

.. list-table::
   :widths: 30 20 20 30
   :header-rows: 1

   * - Model
     - OCPU
     - Mem (GB)
     - Storage
   * - VM.DenseIO2.8
     - 8
     - 120
     - 6.4 TB
   * - VM.DenseIO2.16
     - 16
     - 240
     - 12.8 TB
   * - VM.DenseIO2.24
     - 24
     - 320 
     - 25.6 TB
   * - BM.DenseIO2.52 
     - 52 
     - 768 
     - 51.2 TB
   * - BM.HPC2.36 
     - 36 
     - 384 
     - 6.7 TB

.. include:: /rst_include/advance-index.rst

