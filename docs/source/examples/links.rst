Links
=====

There are a few links you can use with different purposes.

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Link type
     - Markup
     - Renders as
     - Description
   * - External Link
     - .. code-block:: rst

          `External Link <https://docs.scylladb.com/>`_
     - `External Link <https://docs.scylladb.com/>`_
     - Use this markup to create a link to another site or project. When rendered it has an arrow pointing out icon. It opens the content in a new tab.
   * - Internal Cross-reference
     - .. code-block:: rst

          :ref:`Internal Link <here>`
     - :ref:`Internal Link <here>`
     - This is an internal cross reference. It requires a bookmark. Content opens in the same tab.
   * - Internal Cross-reference Bookmark
     - .. code-block:: rst

          .. _here:
     - .. _here:
     - This is an internal cross reference bookmark. It requires an internal cross-reference anchor (above). It does not render, but serves as a point to link to.
   * - Internal Cross-reference to Parameters
     - .. code-block:: rst

          :ref:`Link to a config param <confprop_parameter_name>`
     - Renders the parameter name as a hyperlink.
     - This is an internal cross-reference to a parameter on the `Configuration Parameters <https://opensource.docs.scylladb.com/stable/reference/configuration-parameters.html>`_ page.
       It does NOT require a bookmark, as parameter names on that are page implicit bookmarks. Content opens in the same tab.
       This option only applies to the ``scylladb/sylladb`` and ``scylladb/scylla-enterprise`` projects. 
   * - Internal Cross-reference to Parameter Gropus
     - .. code-block:: rst

          :ref:`Link to a config param <confgroup_parameter_name>`
     - Renders the name of the parameter group as a hyperlink.
     - This is an internal cross-reference to a parameter group on the `Configuration Parameters <https://opensource.docs.scylladb.com/stable/reference/configuration-parameters.html>`_ page.
       It does NOT require a bookmark, as group names on that are page implicit bookmarks. Content opens in the same tab.
       This option only applies to the ``scylladb/sylladb`` and ``scylladb/scylla-enterprise`` projects. 
   * - Internal Doc Reference
     - .. code-block:: rst

          :doc:`Internal Doc <../index>`
     - :doc:`Internal Doc <../index>`
     - This is an internal doc cross reference. it looks for a file. A full path is required.
   * - Download Link
     - .. code-block:: rst

          :download:`download <index.rst>`

     - :download:`download <index.rst>`
     - This opens a download window. It is used to help users download software or files.
