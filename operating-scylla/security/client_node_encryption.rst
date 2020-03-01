Encryption: Data in Transit Client to Node
==========================================

| Follow the procedures below to enable a client to node encryption.
| Each Scylla node needs to be enabled for SSL encryption separately. Repeat this procedure for each node.

.. note::

   If you are working on a new cluster skip steps 1 & 2.

Node side

| Steps 1-5 must be executed on every Scylla node, one node at a time (one by one).

Client side 

| Steps 6-10 are client-side validation steps to demonstrate that clients can now connect in SSL encryption mode.


Procedure
^^^^^^^^^

**Node side**

1. Run ``nodetool drain``.

2. Stop Scylla.

.. include:: /rst_include/scylla-commands-stop-index.rst

3. Edit ``/etc/scylla/scylla.yaml`` to modify the ``client_encryption_options``.

Available options are:

* enabled (default - false)
* certificate - A PEM format certificate, either self-signed, or provided by a certificate authority (CA).
* keyfile - The corresponding PEM format key for the certificate
* truststore - Optional path to a PEM format certificate store of trusted CA:s. If not provided, Scylla will attempt to use the system truststore to authenticate certificates.

.. note::

   If using a self-signed certificate, the "truststore" parameter need to be set to a PEM format container with the private authority.

For example:

.. code-block:: yaml

   client_encryption_options:
       enabled: true
       certificate: /etc/scylla/db.crt
       keyfile: /etc/scylla//db.key
       truststore: <optional path to PEM encoded trust store>

Note: params (enabled, certificate, keyfile) must be 4 spaces indent to the header (``client_encryption_options:``)

4. Start Scylla: 

.. include:: /rst_include/scylla-commands-start-index.rst

5. To validate that encrypted connection to the node is enabled, check the logs using ``journalctl _COMM=scylla``. You should see the following ``message: storage_service - Enabling encrypted CQL connections between client and node``.

**Client side validation steps**

6. In order for cqlsh to work in client to node encryption SSL mode, you need to `generate cqlshrc file`_:
``vi ~/.cassandra/cqlshrc`` 

.. code-block:: yaml

   Example:
   [authentication]
   username = myusername
   password = mypassword
   [cql]
   ; Substitute for the version of Cassandra you are connecting to.
   version = 3.3.1
   [connection]
   hostname = 127.0.0.1
   port = 9042
   factory = cqlshlib.ssl.ssl_transport_factory
   [ssl]
   certfile = /etc/scylla/db.crt
   ; Note: If validate = true then the certificate name must match the machine's hostname
   validate = true
   ; If using client authentication (require_client_auth = true in cassandra.yaml) you'll also need to point to your userkey and usercert.
   ; SSL client authentication is only supported via cqlsh on C* 2.1 and greater.
   ; This is disabled by default on all Instaclustr-managed clusters.
   userkey = /etc/scylla/db.key
   usercert = /etc/scylla/db.crt

..  _`generate cqlshrc file` : https://www.instaclustr.com/blog/2016/02/08/connecting-to-a-cassandra-cluster-using-tls-ssl/

7. Copy the following created files (db.key, db.crt, cadb.key, cadb.pem) to your client/s, from which you run cassandra-stress
8. In order to run cassandra-stress using SSL you need to create java key store (jks) from the ``.pem`` file on the every client that runs cassandra-stress

* Generate the Java keystore for the node certs

.. code-block:: yaml

   openssl pkcs12 -export -out keystore.p12 -inkey /home/scylla/server_files/db.key -in /home/scylla/server_files/db.crt 

   keytool -importkeystore -destkeystore keystore.jks -srcstoretype PKCS12 -srckeystore keystore.p12

* Generate the Java truststore for the trust provider

.. code-block:: yaml

   openssl pkcs12 -export -out truststore.p12 -inkey /home/scylla/server_files/cadb.key -in /home/scylla/server_files/cadb.pem 

   keytool -importkeystore -destkeystore truststore.jks -srcstoretype PKCS12 -srckeystore truststore.p12

* `Download`_ and install the Java security providers:

..  _`Download` : http://www.oracle.com/technetwork/java/javase/downloads/jce8-download-2133166.html

Install to ``<jre>/lib/security``

Note: make sure you have the latest version from this location. 

9. Run Cassandra stress with the parameters below:

.. code-block:: yaml

   cassandra-stress write n=1000000 cl=ONE -node 10.240.0.48 -transport keystore=keystore.jks keystore-password=[password] truststore=truststore.jks truststore-password=[password] -mode native cql3 -pop -rate threads=50

Note: when running cassandra-stress you may encounter an exception, if some nodes are still not in client to node SSL encrypted mode, yet the cassandra-stress will continue to run and connect only to the nodes it can.

Note2: This procedure works as-is for v1.7 or higher. When using Scylla v1.6.x you will need a dummy keystore in the default (conf/.keystore) location with password "cassandra" to run. The contents is irrelevant. Also, it only pertains to cassandra-stress. It has no impact/relation to using the normal java driver connection or cqlsh.

10. Enable encryption on the client application.

See Also
--------
* :doc:`Encryption Data in Transit Node to Node </operating-scylla/security/node_node_encryption/>`
* :doc:`Generating a self-signed Certificate Chain Using openssl </operating-scylla/security/generate_certificate/>`
* :doc:`Authorization</operating-scylla/security/authorization>`
