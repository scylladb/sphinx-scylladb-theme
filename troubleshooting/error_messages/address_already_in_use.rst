"Address already in use" messages
=================================

Phenomena
^^^^^^^^^
Spurious ``"Address already in use"`` messages coming from different contexts in the log, for example:

.. code-block:: none

                
                Dec 14 04:10:10 sjc-315.rfiserve.net scylla[370430]:  [shard 60] gossip - Fail to handle GOSSIP_DIGEST_SYN: std::system_error (error system:98, Address already in use)                       
                Dec 14 02:23:38 sjc-315.rfiserve.net scylla[370430]:  [shard 39] repair - repair 1 failed - std::system_error (error system:98, Address already in use)                                       

These errors may cause all sorts of actual problems, e.g. gossip on a remote side decides that the node where you see these errors is DOWN.

Problem
^^^^^^^

The root cause is the networking stuck ran out of free ports due to too many sockets in a ``TIME_WAIT/CLOSE_WAIT`` state.

How to verify that?

.. code-block:: none

                netstat -np | grep -i "_wait"

Solution
^^^^^^^^

Usually, the situation described above is unexpected and is caused by some misbehaving program. In order to find which program is that one needs to see which programs are the main consumers of TCP sockets:

Here is what I can see on my laptop which doesn't have an issue:

.. code-block:: none

   netstat -npt | tr -s ' ' | cut -d" " -f7- | sort | uniq -c

   (Not all processes could be identified, non-owned process info
   will not be shown, you would have to be root to see it all.)
                 
      1
      3 -
     18 13464/firefox
      3 13942/python3
     18 18603/chromium-brow
      4 19879/tusk
      2 20627/zoom
      3 2485/vladz --pid=24
      7 2525/vladz --pid=24
      1 2594/Preload.js --c
      1 26112/ssh
      8 32620/scylla
      8 376/scylla
      1 4549/gvfsd-smb-brow
      1 4755/python3
      1 4883/WhatsDesk
      8 571/scylla
      5 9359/thunderbird
      1 Address State PID/Program name


However if one of applications stands out and uses a lot of sockets you may want to take a closer look.
Note that in the output above we included the PID of the program and as a result each instance of the same program appears separately (e.g. scylla above).

If you see that some program appears too many times you may want to aggregate all its appearances:
``$ netstat -npt | tr -s ' ' | cut -d" " -f7- | cut -d"/" -f2- | sort | uniq -c``
