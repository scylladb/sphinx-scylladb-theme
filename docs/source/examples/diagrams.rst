Diagrams 
========

The documentation toolchain supports rendering diagrams and charts using `Mermaid <https://mermaid.js.org/intro/>`_, a library designed for creating sequence diagrams, flowcharts, and other visualizations.

Installation
------------

To use Mermaid with your documentation:

1. Install the extension:

   .. code-block:: console

      poetry add sphinxcontrib-mermaid

2. Load the extension in the `conf.py` configuration file:

   .. code-block:: python

      extensions = ["sphinxcontrib.mermaid"]

3. In your documentation files, Include graphs using the `.. mermaid ::` directive:

   .. code-block:: python

      .. mermaid ::

         graph TD
         A --> B
         B -- Label --> C

   The previous code example renders the following graph:
   
   .. mermaid ::

      graph TD
      A --> B
      B -- Label --> C

   For more details, refer to the `sphinxcontrib-mermaid <https://sphinxcontrib-mermaid-demo.readthedocs.io/en/latest/>`_ documentation.