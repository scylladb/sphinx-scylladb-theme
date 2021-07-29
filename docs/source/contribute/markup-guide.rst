===================================
Markup Guide for Docs Contributors
===================================

.. versionadded:: 0.1.24 Scylla Sphinx Theme


This guide covers the markup convention used for Scylla Docs. Our official documentation is written in RestructuredText.
We will also accept content written in Markdown.

This guide covers the RestructuredText elements.
If you are not familiar with RestructuredText, refer to `this cheat sheet <https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html>`_.
Keep in mind, that in this cheat sheet there may be directives or elements of the markup we're not using.

In general, there are  main components to the markup of any document.

.. contents::
   :depth: 2
   :local:


Headings
--------

While Sphinx supports many layers of headings, at Scylla we try to keep the hierarchy limited to 4, excluding the title.
If you have the need for a H4, chances are that you need to re-arrange the content.
Watch the length of your text vs the markup. It must be at least as long as the text.
It can be longer, but shorter will produce an error.
Also, if your markup has a line above and below both lines must be the same length.

Use the following convention for headings:

.. list-table:: Markup for Headings
   :widths: 33 33 33
   :header-rows: 1

   * - Heading
     - Markup
     - Description
   * - Page Title
     - .. code-block:: rst

          =========
          Title
          =========
     - Has an equal sign above and below the text. Use for the title of the page. It should be used only once per page
   * - H1
     - .. code-block:: rst

          Heading 1
          ---------
     - Has  a dash below the text. Use for the first level heading.
   * - H2
     - .. code-block:: rst

          Heading 2
          =========
     - Has an equal sign below the text. Use for the second level heading.
   * - H3
     - .. code-block:: rst

          Heading 3
          .........
     - Has dots below the text. Use for a third level heading.
   * - H4
     - .. code-block:: rst

          Heading 4
          ^^^^^^^^^
     - Has carats below the text. Use for a fourth level heading. If you need more levels, re-arrange the text.

Paragraph Styles
----------------

A paragraph style is markup which applies to an entire paragraph.
In RestructuredText, there is no need to markup body text.
Any text which is not marked up will be treated as body text.

Lists
=====
There are two kinds of lists, ordered and unordered.
Remember to insert a blank line before and after the lists.

.. list-table:: Markup for Lists
   :widths: 25 25 25 25
   :header-rows: 1

   * - List type
     - Markup
     - Renders as
     - Description
   * - Ordered List
     - .. code-block:: rst

          #. First Item
          #. Second Item

             a. Sub Item
             #. Sub Item

          #. Third Item
     -    #. First Item
          #. Second Item

             a. Sub Item
             #. Sub Item

          #. Third Item

     - Use this markup for procedures and in any place where oder matters. Use number sign for the number. When the page is generated it is numbered automatically. A blank line is required at the end of a list.
   * - Unordered List
     - .. code-block:: rst

          * First Item
          * Second Item

            * Sub Item
            * Sub Item

          * Third Item
     -    * First Item
          * Second Item

            * Sub Item
            * Sub Item

          * Third Item

     - Use for any list where order doesn't matter. Use an asterisk for the bullet. When the page is generated it is bulleted automatically. A blank line is required at the end of a list.

Links
=====

There are a few links you can use with different purposes.


.. list-table:: Markup for Links
   :widths: 25 25 25 25
   :header-rows: 1

   * - Link type
     - Markup
     - Renders as
     - Description
   * - External Link
     - .. code-block:: rst

          `External Link <https://docs.scylladb.com/some-doc>`_
     - `External Link <https://docs.scylladb.com/some-doc>`_
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

Character Styles (in-line Markup)
---------------------------------

The following markup is used within a line of text.

* Note that you **cannot** mix inline markup types together.
* Use only one type of markup text at a time.
* Use a space before any markup **and** after the text that follows.


.. list-table:: In-line Markup
   :widths: 25 25 25 25
   :header-rows: 1

   * - Name
     - Markup
     - Renders as
     - Description
   * - Bold
     - .. code-block:: rst

          **Bold Text**
     - **Bold Text**
     - Use this markup to create boldface text. Note that there are no spaces next to the asterisks.
   * - Italics
     - .. code-block:: rst

          *Italics*
     - *Italics*
     - Use this markup to create italic text. Note that there are no spaces next to the asterisks.
   * - Code
     - .. code-block:: rst

          ``command line text``
     - ``command line text``
     - Use this markup to create command line text. Note that there are two tick marks before and after the command and no spaces next to the tick marks.


Substitutions
=============

Substitutions are variables. They are declared in any document and defined in the ``conf.py`` file, ``rst_prolog`` setting.
Do not use substitutions in headings. The reason is the text that replaces the variable may be longer than the line that is over or below the text and this will produce an error.
Refrain from making up substitutions without discussing it with the doc team first.

Currently, we are using the following substitutions:

* ``|v|`` for |v|
* ``|x|`` for |x|

Tables
------

We use the List Table directive for tables.
If possible give your table a name as this helps with SEO and screen readers for Accessibility.
In the width declaration, determine the number of columns and the width for each.

.. code-block:: rst

   .. list-table:: Table Name
      :widths: 33 33 33
      :header-rows: 1

      * - header name
        - header name
        - header name
      * - body text
        - body text
        - body text

Renders as

.. list-table:: Table Name
   :widths: 33 33 33
   :header-rows: 1

   * - header name
     - header name
     - header name
   * - body text
     - body text
     - body text

Directives
----------

At Scylla, we use the following directives. Some directives are custom built for Scylla.

* Admonitions_
* :ref:`Code Blocks <codeblocks>`
* Images_
* Includes_
* :ref:`Tabbed Content <tabbedcontent>`
* Metadata_
* Versions_
* :ref:`Glossary and Abbreviations <abbreviations>`
* :ref:`TOC and Mini-TOC <toc-mini>`
* :ref:`Panel Box and Topic Box <panelbox>`


Admonitions
===========

At Scylla, we limit the admonitions. Although |rst| will allow for more, use the following:

* Note_
* Caution_
* Warning_
* Tip_

Note
....

Use a note to point out something to the reader. This action does not have any risk.

.. code-block:: rst

   .. note:: text follows here

Renders as:

.. note:: text follows here

Caution
.......

Use caution if there is any potential risk to data loss or lower performance.

.. code-block:: rst

   .. caution:: look out

Renders as

.. caution:: look out

Warning
.......

Use warning if there is any potential risk to total data loss or physical danger.

.. code-block:: rst

   .. warning:: take care

Renders as:

.. warning:: take care

Tip
...

This is a time-saving or performance enhancing option.

.. code-block:: rst

   .. tip:: here's a tip

Renders as:

.. tip:: here's a tip

.. _codeblocks:

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

If you are including a large example (an entire file) as a code-block, refer to :ref:`Literal Include <literalinclude>`.

Images
======

There are two possible directives for images. One is the image directive and the other is the figure directive.
Refer to `DocUtils <https://docutils.sourceforge.io/docs/ref/rst/directives.html#images>`_ for more options.

.. code-block:: none

  .. image:: checkmark.png
      :scale: 50 %
      :alt: checkmark

renders the image

.. image:: checkmark.png
   :scale: 50 %
   :alt: checkmark


Whereas the Figure directive allows you to use captions

.. code-block:: none

   .. figure:: checkmark.png
      :scale: 50 %
      :alt: checkmark

   This is the caption for the image

Renders the image as:

.. figure:: checkmark.png
   :scale: 50 %
   :alt: checkmark

   This is the caption for the image

Includes
========

An include directive allows you to include the entire contents of one restructured text file directly into another.
This is the easiest way to control content re-use.

When given an absolute path, the directive takes it as relative to the root of the source directory.
It is Scylla practice to place global include files in the *rst_include* directory.

For example, here are some very commonly used include statements:

.. code-block:: none

   .. include:: /rst_include/scylla-commands-stop-index.rst

.. code-block:: none

   .. include:: /rst_include/scylla-commands-start-index.rst

.. code-block:: none

   .. include:: /rst_include/scylla-commands-restart-index.rst


.. _literalinclude:

Literal Include
...............

If the file you want to include is **not** |rst|, you can use the Literal Include directive. This adds the page cited as a code-block.

For example:

.. code-block:: none

   .. literalinclude:: ../conf.py
      :lines: 1-10

Gets the conf.py file from the parent directory and displays the first 10 lines.

.. literalinclude:: ../conf.py
      :lines: 1-10

.. _tabbedcontent:

Tabbed Content
==============

When there are several languages or options available and the reader will use one and keep using that option throughout the procedure, a tabbed content box is the best way to display this informaiton.

For example:

.. code-block:: none

   .. tabs::

      .. group-tab:: CentOS 7, Ubuntu 16.04/18.04, Debian 8/9

         .. code-block:: shell

            sudo systemctl stop scylla-server

      .. group-tab:: Ubuntu 14.04, Debian 7

         .. code-block:: shell

            sudo service scylla-server stop

      .. group-tab:: Docker

         .. code-block:: shell

            docker exec -it some-scylla supervisorctl stop scylla

         (without stopping *some-scylla* container)

Renders as:

.. tabs::

   .. group-tab:: CentOS 7, Ubuntu 16.04/18.04, Debian 8/9

      .. code-block:: shell

         sudo systemctl stop scylla-server

   .. group-tab:: Ubuntu 14.04, Debian 7

      .. code-block:: shell

         sudo service scylla-server stop

   .. group-tab:: Docker

      .. code-block:: shell

         docker exec -it some-scylla supervisorctl stop scylla

      (without stopping *some-scylla* container)

Metadata
========

Adds Metadata to your document.

.. code-block:: none

   .. meta::
      :description: The reStructuredText plaintext markup language
      :keywords: plaintext, markup language

This would be converted to the following HTML:

.. code-block:: html

   <meta name="description"
      content="The reStructuredText plaintext markup language">
   <meta name="keywords" content="plaintext, markup language">

Versions
========

This is an inline directive which should be used when introducing or deprecating a feature


.. code-block:: rst

   .. versionadded:: version

.. code-block:: rst

   .. versionchanged:: version

.. code-block:: rst

   .. deprecated:: version

When using, these directives a blank line must follow. Until we have separated the content, please use the product name with the version number.

.. versionadded:: 1.1 Scylla Manager

.. versionchanged:: 2018.1 Scylla Enterprise

.. deprecated:: 2.0 Scylla Open Source

.. _abbreviations:

Glossary and Abbreviations
==========================

Using the glossary.rst page you can create a glossary. The terms can be entered in any order and it will create an alphabetical list.
Terms need to be written with a hanging indent from the definition. Consult the Glossary Template for details.

To cite a term in a document that is not the glossary use the following convention:

.. code-block:: rst

   :term:`term <term as written in Glossary>`

For example:

.. code-block:: rst

   :term:`Size-tiered Compaction Strategy (STCS)<Size-tiered Compaction Strategy>`

Abbreviations and acronyms are defined in-line. The initial letters or abbreviation is first followed by the longer form.
For example:

.. code-block:: rst

   :abbr:`LIFO (last-in, first-out)`.

.. code-block:: rst

   :abbr:`Overwrite (Same data cells overwritten many times)`

.. _toc-mini:

TOC and Mini-TOC
================
These directives create TOCs automatically

TOC
...

The :abbr:`TOC (Table of Contents)` is automatically generated in sphinx when you build the site.

Each index.rst needs to have a toctree directive in order to build the left side nav menu.

See the template for more details.

.. code-block:: rst

   .. toctree::
    :maxdepth: 2

Mini-TOC
........

Every topic which has more than one heading in it needs to have a mini-toc.
The Contents directive creates a mini-TOC using the headings you have in the document.
You can set the level of headings to include in the TOC. The recommended depth is 2 for H1 and H2.


.. code-block:: rst

   .. contents::
   :depth: 2
   :local:

.. _panelbox:

Panel Box and Topic Box
=======================

Panel Box
.........

This is a custom directive which creates boxes on the index screens. Do not use the panel-box on the root index.rst.

.. code-block:: rst

  .. panel-box::
    :title: Admin
    :id: "getting-started"
    :class: my-panel

Topic Box
.........

This is a custom directive which creates graphical boxes on root index screens. Do not use the topic-box on the subordinate index.rst files.


.. code-block:: rst

  .. topic-box::
    :title: Getting Started
    :link: /getting-started/
    :icon: fa fa-power-off
    :icon_color: rgba(95,113,180,1)
    :icon_bg: rgba(95,113,180,0.1)
    :class: my-box
