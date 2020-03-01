:term:`Sorted Strings Table (SSTable)<SSTable>` is the persistent file format used by Scylla and Apache Cassandra. SSTable is saved as a persistent, ordered, immutable set of files on disk.
Immutable means SSTables are never modified; they are created by a MemTable flush and are deleted by a compaction.
The location of Scylla SSTables is specified in scylla.yaml ``data_file_directories`` parameter (default location: ``/var/lib/scylla/data``).

Scylla Open Source versions up to 3.0 and Scylla Enterprise versions up to 2019.1 used Apache Cassandra 2.x SSTable compatible format (known as 'la'). 

Scylla Open Source 3.x and Scylla Enterprise 2019.1 now support the Apache Cassandra 3.x format ('mc') which is more efficient and requires less disk space than the Scylla 2.x.
