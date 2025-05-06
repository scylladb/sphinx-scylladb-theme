Code blocks
===========

Code block directives are for displaying code. By default the code is copyable and includes a copy icon.
To keep code snippets neat, separate the display from the command.
This keeps the command copyable without having the screen return inside the command.

Basic usage
-----------

For example using the rst code block before a |rst| example:

``.. code-block:: rst`` when used with the ``.. tip:: here's a tip`` as shown above, renders as:

.. code-block:: rst

   .. tip:: here's a tip

The code block directive can be changed to a language which is supported by |rst|.
For example, the following code-block is cql. If you add the following code block directive, to the code sample below:

``.. code-block:: cql``

.. code-block:: cql

   create_keyspace_statement: CREATE KEYSPACE [ IF NOT EXISTS ] `keyspace_name` WITH `options`

You see that there is syntax highlighting.

The key item to remember is that the entire code block needs **three** spaces before any line. The code will automatically be highlighted.
You can create code-blocks in any of the following `languages <https://pygments.org/languages/>`_. Using ``none`` is also acceptable. If you use none, there is no syntax highlighting.

.. code-block:: none

   create_keyspace_statement: CREATE KEYSPACE [ IF NOT EXISTS ] `keyspace_name` WITH `options`

If you are including a large example (an entire file) as a code-block, refer to :doc:`Literal Include <includes>`.

Show line number
----------------

To show the line number, add the option `:linenos:` to the code-block directive.

For example:

.. code-block:: rst

   .. code-block:: rst
      :linenos:

      Line 1
      Line 2

Renders:

.. code-block:: rst
   :linenos:
   
   Line 1
   Line 2

Hide copy button
----------------

Add the class ``hide-copy-button`` to the ``code-block`` directive to hide the copy button.

For example:

.. code-block:: rst

   .. code-block:: rst
      :class: hide-copy-button

      .. tip:: here's a tip

Renders:

.. code-block:: rst
   :class: hide-copy-button

   .. tip:: here's a tip


Highlight lines
---------------

To highlight lines, add the option `:emphasize-lines: <number>` to the code-block directive.

For example:

.. code-block:: rst

   .. code-block:: rst
      :emphasize-lines: 1,3

      Line 1
      Line 2
      Line 3

Renders:

.. code-block:: rst
   :emphasize-lines: 1,3

   Line 1
   Line 2
   Line 3