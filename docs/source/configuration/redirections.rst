====================
Redirections support
====================

With Scylla Sphinx Theme, you can define 301 redirections when moving or deleting a document.

By doing so, you will avoid broken links in other sites pointing to your documentation.

.. note:: When multi version is enabled, the extension only creates redirections for the latest version of the documentation.

Redirections file
-----------------

The ``redirections.yaml`` file is inside ``docs/_utils``.

File structure
--------------

The redirections file has this structure:

.. code-block:: none

    # old_path: new_path

    # redirection to internal link
    /previous_path/page_a:/new_path/page_a

    # redirection to external link
    /previous_path/page_b:https://docs.scylladb.com/

.. note:: Do not add trailing paths ``/`` to define old paths.

Create a redirection
--------------------

To create a redirection:

#. Create a file ``redirections.yaml`` in ``docs/_utils`` if it does not exist.
#. Add a new entry to the YAML file, assigning the old path in the left site operator and the new path on the right side.

    For example, to redirect to another internal page:

    .. code-block:: none

        /previous_path/page_a:/new_path/page_a

    Or, to redirect to an external URL:

    .. code-block:: none

        /previous_path/page_b:https://docs.scylladb.com/
