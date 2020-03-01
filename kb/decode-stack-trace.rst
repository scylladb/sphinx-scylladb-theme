=====================
Decoding Stack Traces
=====================

**Topic: Decoding stack traces in Scylla logs**

**Environment: Any Scylla setup on any supported OS**

**Audience: All**

Synopsis
--------

This article describes how to decode the stack traces found in Scylla logs.

.. contents::
   :depth: 2
   :local:

What are Stack Traces?
----------------------

Stack traces can appear in the logs due to various errors or in the course of regular database operation. It is useful to be able to decode the trace in order to understand what exactly happened. Decoding the stack trace requires the Debug binaries for the specific Scylla build and OS in use are installed.

Note that sharing the stack trace as part of your support ticket or Github issue, helps the Scylla support team to understand the issue better.


Install Debug Binary files
--------------------------

Install the Debug binaries according to your OS distribution


RPM based distributions
^^^^^^^^^^^^^^^^^^^^^^^

Scylla Open Source
..................

.. code-block:: none

   yum install scylla-debuginfo

Scylla Enterprise
..................

.. code-block:: none

   yum install scylla-enterprise-debuginfo

DEB based distributions
^^^^^^^^^^^^^^^^^^^^^^^

Scylla Open Source
..................

.. code-block:: none
   
   apt-get install scylla-server-dbg

Scylla Enterprise
..................

.. code-block:: none

   apt-get install scylla-enterprise-server-dbg

Validate the debug binary file name
-----------------------------------

To later determine the actual debug binary, look in the ``/usr/lib/debug/`` directory
for a file named scylla.debug.

For example:

.. code-block:: none

   # find /usr/lib/debug/ | grep scylla.debug
   /usr/lib/debug/usr/bin/scylla.debug

Locate and Analyze the Logs
----------------------------

**Procedure**

1. Copy the stack from the ``scylla.debug`` logs and place it in a file (trace.txt, for example).

.. code-block:: none

   Jul 14 16:56:50 hostname01 scylla: Aborting on shard 8.
   Jul 14 16:56:50 hostname01 scylla: Backtrace:
   Jul 14 16:56:50 hostname01 scylla: 0x0000000000688602
   Jul 14 16:56:50 hostname01 scylla: 0x00000000005a36fc
   Jul 14 16:56:50 hostname01 scylla: 0x00000000005a39a5
   Jul 14 16:56:50 hostname01 scylla: 0x00000000005a3a53
   Jul 14 16:56:50 hostname01 scylla: /lib64/libpthread.so.0+0x000000000000f6cf
   Jul 14 16:56:50 hostname01 scylla: /lib64/libc.so.6+0x0000000000036276
   Jul 14 16:56:50 hostname01 scylla: /lib64/libc.so.6+0x0000000000037967
   Jul 14 16:56:50 hostname01 scylla: 0x00000000024ce37b
   Jul 14 16:56:50 hostname01 scylla: 0x00000000024d2a47
   Jul 14 16:56:50 hostname01 scylla: 0x00000000024df1d5
   Jul 14 16:56:50 hostname01 scylla: 0x00000000023dccec
   Jul 14 16:56:50 hostname01 scylla: 0x00000000023feac1
   Jul 14 16:56:50 hostname01 scylla: 0x00000000024324b9
   Jul 14 16:56:50 hostname01 scylla: 0x00000000024357e4
   Jul 14 16:56:50 hostname01 scylla: 0x0000000001eace90
   Jul 14 16:56:50 hostname01 scylla: 0x0000000001eaf944
   Jul 14 16:56:50 hostname01 scylla: 0x0000000000584ab6
   Jul 14 16:56:50 hostname01 scylla: 0x0000000000584c71
   Jul 14 16:56:50 hostname01 scylla: 0x00000000006522ff
   Jul 14 16:56:50 hostname01 scylla: 0x00000000006554e5
   Jul 14 16:56:50 hostname01 scylla: 0x000000000073d3cd
   Jul 14 16:56:50 hostname01 scylla: /lib64/libpthread.so.0+0x0000000000007e24
   Jul 14 16:56:50 hostname01 scylla: /lib64/libc.so.6+0x00000000000febac   



2. Do one of the following:

   * For Scylla 3.0 and prior, download `seastar-addr2line <https://github.com/scylladb/seastar/blob/master/scripts/seastar-addr2line>`_ and make it executable.
   * For Scylla 3.1 and later, the script is part of the standard installation.

3. Run the decoder:

.. code-block:: none

   ./seastar-addr2line -e /usr/lib/debug/usr/bin/scylla.debug -f trace.txt > trace_decoded.txt

``trace_decoded.txt`` now contains the decoded version of the stack trace:

For example:

.. code-block:: none

   void seastar::backtrace<seastar::backtrace_buffer::append_backtrace()::{lambda(seastar::frame)#1}>(seastar::backtrace_buffer::append_backtrace()::{lambda(seastar::frame)#1}&&) at /usr/src/debug/scylla-2.3.2/seastar/util/backtrace.hh:56
   seastar::backtrace_buffer::append_backtrace() at /usr/src/debug/scylla-2.3.2/seastar/core/reactor.cc:390
    (inlined by) print_with_backtrace at /usr/src/debug/scylla-2.3.2/seastar/core/reactor.cc:411
   seastar::print_with_backtrace(char const*) at /usr/src/debug/scylla-2.3.2/seastar/core/reactor.cc:418
   sigabrt_action at /usr/src/debug/scylla-2.3.2/seastar/core/reactor.cc:3939
    (inlined by) operator() at /usr/src/debug/scylla-2.3.2/seastar/core/reactor.cc:3921
    (inlined by) _FUN at /usr/src/debug/scylla-2.3.2/seastar/core/reactor.cc:3917
   ...

   seastar::reactor::run_tasks(seastar::reactor::task_queue&) at /usr/src/debug/scylla-2.3.2/seastar/core/reactor.cc:2621
   seastar::reactor::run_some_tasks() at /usr/src/debug/scylla-2.3.2/seastar/core/reactor.cc:3033
   seastar::reactor::run_some_tasks() at /opt/scylladb/include/c++/7/chrono:377
    (inlined by) seastar::reactor::run() at /usr/src/debug/scylla-2.3.2/seastar/core/reactor.cc:3180




