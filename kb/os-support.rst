Operating System (OS) Support Guide
===================================
**Topic: Administration**

**Learn: Which Operating Systems are supported by Scylla**

**Audience: Scylla administrators**

Scylla is supported on `Red Hat Enterprise
Linux <https://access.redhat.com/products/red-hat-enterprise-linux/>`__
versions 7 and up, `CentOS <https://www.centos.org>`__ version 7 and up,
`Ubuntu <http://www.ubuntu.com/>`__ 14.04 and 16.04 LTS and Debian 8. Scylla may also build
on other distributions and versions, but is not tested on them. We
recommend using one of the supported distributions am for production.

As Scylla relies heavily on XFS, RHEL or CentOS are preferred over
Ubuntu. This is because RHEL and CentOS have a strong focus on XFS,
resulting in greater performance and more timely delivery of bug fixes.

We recommend using the latest updates of your operating system, to avoid
known bugs or security vulnerabilities.

OS Support Matrix
-----------------

.. note:: For all OS versions listed in this table, the term *and above*, refers to minor release versions only. 

.. role:: raw-html(raw)
   :format: html

+------------------------------------+-----------------------------+-----------------------------+
| OS                                 | Supported?                  | Recommended?                |
+====================================+=============================+=============================+
| RHEL 7.2 and above                 |:raw-html:`<span             |:raw-html:`<span             |
|                                    |class="icon-yes"/>`          |class="icon-yes"/>`          |
+------------------------------------+-----------------------------+-----------------------------+
| RHEL 7.0 - 7.1                     |:raw-html:`<span             |                             |
|                                    |class="icon-yes"/>`          |                             |
+------------------------------------+-----------------------------+-----------------------------+
| CentOS 7.2 and above               |:raw-html:`<span             |:raw-html:`<span             |
|                                    |class="icon-yes"/>`          |class="icon-yes"/>`          |
+------------------------------------+-----------------------------+-----------------------------+
| CentOS 7.0 - 7.1                   |:raw-html:`<span             |                             |
|                                    |class="icon-yes"/>`          |                             |
+------------------------------------+-----------------------------+-----------------------------+
| Oracle Linux 7.2 and above         |:raw-html:`<span             |                             |
|                                    |class="icon-yes"/>`          |                             |
+------------------------------------+-----------------------------+-----------------------------+
| Ubuntu 14.04 LTS                   |:raw-html:`<span             |                             |
|                                    |class="icon-yes"/>`          |                             |
+------------------------------------+-----------------------------+-----------------------------+
| Ubuntu 16.04 LTS                   |:raw-html:`<span             |                             |
|                                    |class="icon-yes"/>`          |                             |
+------------------------------------+-----------------------------+-----------------------------+
| Ubuntu 18.04 LTS :sup:`*`          |:raw-html:`<span             |                             |
|                                    |class="icon-yes"/>`          |                             |
+------------------------------------+-----------------------------+-----------------------------+
| Debian 8.6 and above               |:raw-html:`<span             |                             |
|                                    |class="icon-yes"/>`          |                             |
+------------------------------------+-----------------------------+-----------------------------+
| Debian 9.0 :sup:`*`                |:raw-html:`<span             |                             |
|                                    |class="icon-yes"/>`          |                             |
+------------------------------------+-----------------------------+-----------------------------+

:sup:`*`  Supported in Scylla 2.3 

References
----------

-  `Red Hat Enterprise Linux
   7 <https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/index.html>`__
-  `CentOS 7 <https://www.centos.org/download/>`__
-  `Ubuntu 14.04 LTS <http://releases.ubuntu.com/14.04/>`__

`Knowledge Base 
</kb/>`_
