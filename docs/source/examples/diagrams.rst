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
