Code Blocks
===========

Code block directives are for displaying code. By default the code is copyable and includes a copy icon.
To keep code snippets neat, separate the display from the command.
This keeps the command copyable without having the screen return inside the command.

For example using the rst code block before a |rst| example:

``.. code-block:: rst`` when used with the ``.. tip:: here's a tip`` as shown above, renders as:

.. code-block:: rst

   .. tip:: here's a tip

The code block directive can be changed to a language which is supported by |rst|.
For example, the following code-block is bash. If you add the following code block directive, to the code sample below:

``.. code-block:: bash``

.. code-block:: bash

   #!/bin/bash

   # Checks if local url matches the original repository
   original_repo='scylladb/sphinx-scylladb-theme'
   origin_repo=$(git config --get remote.origin.url)
   if [[ $origin_repo != *$original_repo* ]]; then
       echo "Error: You are tring to publish a new version of the theme"\
            "from your personal fork."\
            "Clone the repository '${original_repo}' locally,"\
            "then run 'deploy.sh' from the original project."
       exit 1
   fi

You see that there is syntax highlighting.

The key item to remember is that the entire code block needs **three** spaces before any line. The code will automatically be highlighted.
You can create code-blocks in any of the following `languages <https://pygments.org/languages/>`_. Using ``none`` is also acceptable. If you use none, there is no syntax highlighting.

.. code-block:: none

   #!/bin/bash

   # Checks if local url matches the original repository
   original_repo='scylladb/sphinx-scylladb-theme'
   origin_repo=$(git config --get remote.origin.url)
   if [[ $origin_repo != *$original_repo* ]]; then
       echo "Error: You are tring to publish a new version of the theme"\
            "from your personal fork."\
            "Clone the repository '${original_repo}' locally,"\
            "then run 'deploy.sh' from the original project."
       exit 1
   fi

If you are including a large example (an entire file) as a code-block, refer to :doc:`Literal Include <includes>`.
