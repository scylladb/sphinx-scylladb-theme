Scylla SSTable - 3.x
====================

.. toctree::
   :hidden:

   sstables_3_data_file_format
   sstables_3_statistics
   sstables_3_summary
   sstables_3_index
   sstable_format

.. include:: ../_common/sstable_what_is.rst

* In Scylla 3.1, mc format is enabled by default. 

* In Scylla 3.0, mc format is disabled by default and can be enabled by adding the ``enable_sstables_mc_format`` parameter as 'true' in ``scylla.yaml`` file.

For example: 

.. code-block:: shell

   enable_sstables_mc_format: true


For more information on Scylla 3.x SSTable formats, see below:

* :doc:`SSTable 3.0 Data File Format <sstables_3_data_file_format>`
* :doc:`SSTable 3.0 Statistics <sstables_3_statistics>` 
* :doc:`SSTable 3.0 Summary <sstables_3_summary>`
* :doc:`SSTable 3.0 Index <sstables_3_index>`
* :doc:`SSTable 3.0 Format in Scylla <sstable_format>`
