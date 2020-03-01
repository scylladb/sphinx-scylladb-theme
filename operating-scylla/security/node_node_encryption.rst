Encryption: Data in Transit Node to Node
========================================

Communication between all or some nodes can be encrypted. The controlling parameter is :code:`server_encryption_options`.

See :doc:`generating a self-signed certificate chain using openssl </operating-scylla/security/generate_certificate/>` section.

Procedure
^^^^^^^^^

1. Configure the ``internode_encryption``, under :code:`/etc/scylla/scylla.yaml`.

Available options are:

* none (default)
* all
* dc: encrypts the traffic between the data centers.
* rack: encrypts the traffic between the racks.
* certificate - A PEM format certificate, either self-signed, or provided by a certificate authority (CA).
* keyfile - The corresponding PEM format key for the certificate.
* truststore - Optional path to a PEM format certificate store of trusted CA:s. If not provided, Scylla will attempt to use the system trust store to authenticate certificates.

scylla.yaml example:

.. code-block:: yaml

   server_encryption_options:
       internode_encryption: <none|rack|dc|all>
       certificate: <path to PEM encoded certificate file>
       keyfile: <path to PEM encoded key for certificate>
       truststore: <optional path to PEM encoded trust store>

2. Restart Scylla node to apply the changes.

.. include:: /rst_include/scylla-commands-restart-index.rst


See Also
--------
* :doc:`Encryption Data in Transit Client to Node </operating-scylla/security/client_node_encryption/>`
* :doc:`Generating a self-signed Certificate Chain Using openssl </operating-scylla/security/generate_certificate/>`
* :doc:`Authorization</operating-scylla/security/authorization/>`
