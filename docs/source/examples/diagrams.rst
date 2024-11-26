Diagrams 
========

The documentation toolchain supports rendering diagrams and charts using `Mermaid <https://mermaid.js.org/intro/>`_, a library designed for creating sequence diagrams, flowcharts, and other visualizations.

Using:

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