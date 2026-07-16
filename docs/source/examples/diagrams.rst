Diagrams
========

The documentation toolchain supports rendering diagrams and charts using `Mermaid <https://mermaid.js.org/intro/>`_, a library designed for creating sequence diagrams, flowcharts, and other visualizations.

Default
-------

Use the ``mermaid`` directive to render a diagram inline.

.. code-block:: python

   .. mermaid ::

      graph TD
      A --> B
      B -- Label --> C

Renders:

.. mermaid ::

   graph TD
   A --> B
   B -- Label --> C

For more details, refer to the `sphinxcontrib-mermaid <https://sphinxcontrib-mermaid-demo.readthedocs.io/en/latest/>`_ documentation.

Diagrams with metadata
----------------------

Mermaid diagrams can be wrapped with the ``diagram`` directive to attach metadata, so external tools can filter and extract them.

.. code-block:: none

   .. diagram::
      :id: request-flow
      :tags: networking, ingress
      :categories: architecture
      :deployment: core
      :last-reviewed: 2026-06-01

      .. mermaid::

         graph TD
         Client --> Gateway
         Gateway -- Auth --> Service
         Service --> Database

Renders:

.. diagram::
   :id: request-flow
   :tags: networking, ingress
   :categories: architecture
   :deployment: core
   :last-reviewed: 2026-06-01

   .. mermaid::

      graph TD
      Client --> Gateway
      Gateway -- Auth --> Service
      Service --> Database

Diagram catalog
---------------

Every ``diagram`` directive on the site is also indexed in a single ``diagrams.json`` published at the build root (e.g. ``https://sphinx-theme.scylladb.com/stable/diagrams.json``).
Each entry carries the metadata plus either an absolute image URL or the raw mermaid source, so external tools can filter and extract diagrams without scraping HTML.

Example entries with one mermaid diagram and one :doc:`image <images>`, illustrating both ``type`` values:

.. code-block:: json

   {
     "diagrams": [
       {
         "id": "request-flow",
         "page": "examples/diagrams",
         "page_url": "https://sphinx-theme.scylladb.com/stable/examples/diagrams/#request-flow",
         "tags": ["networking", "ingress"],
         "categories": ["architecture"],
         "deployment": "core",
         "last_reviewed": "2026-06-01",
         "type": "mermaid",
         "content": "graph TD\nClient --> Gateway\nGateway -- Auth --> Service\nService --> Database"
       },
       {
         "id": "auth-flow",
         "page": "examples/images",
         "page_url": "https://sphinx-theme.scylladb.com/stable/examples/images/#auth-flow",
         "tags": ["networking", "security"],
         "categories": ["security"],
         "deployment": "core",
         "last_reviewed": "2026-06-01",
         "type": "image",
         "content": "https://sphinx-theme.scylladb.com/stable/_images/diagram.svg"
       }
     ]
   }
