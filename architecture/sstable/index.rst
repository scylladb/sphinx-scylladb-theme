Scylla SSTable Format
=====================

.. toctree::
   :hidden:

   sstable2/index
   sstable3/index

.. include:: _common/sstable_what_is.rst


* In Scylla 3.1, mc format is enabled by default. 

* In Scylla 3.0, mc format is disabled by default and can be enabled by adding the ``enable_sstables_mc_format`` parameter as 'true' in ``scylla.yaml`` file.

For example: 

.. code-block:: shell

   enable_sstables_mc_format: true

.. note:: If you change the default setting in either Scylla version, you must apply this change to **all** nodes in order for it to take effect. 

For more information on each of the SSTable formats, see below:

* :doc:`SSTable 2.0 <sstable2/index>` 
* :doc:`SSTable 3.0 <sstable3/index>` 
