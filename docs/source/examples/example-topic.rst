=============
Example Topic
=============

.. contents:: On this page
   :depth: 2
   :local:

.. This template should be used for all new topics, no matter which Scylla Project they belong to. To use the template, copy it to your project, changing the name.

Heading Hierarchy
-----------------

HEADINGS
========

Use the following

.. code-block:: none

   =====
   Title
   =====
   H1
   ---
   H2
   =====
   H3
   .....
   H4
   ^^^^^
   H5
   ~~~~


Lorem Ipsum: usage
------------------
Lorem ipsum is:

* a pseudo-Latin text used in web design, typography, layout, and printing in place of English to emphasise design elements over content.
* Also called placeholder (or filler) text.
* A convenient tool for mock-ups.
* Helps to outline the visual elements of a document or presentation, eg typography, font, or layout.
* Latin text by the classical author and philosopher Cicero.

#. Its words and letters have been changed by addition or removal, so to deliberately render its content nonsensical;
#. It's not genuine, correct, or comprehensible Latin anymore.
#. While lorem ipsum's still resembles classical Latin, it actually has no meaning whatsoever.
#. As Cicero's text doesn't contain the letters K, W, or Z, alien to latin, these, and others are often inserted randomly to mimic the typographic appearance of European languages, as are digraphs not to be found in the original.

Lorem Ipsum: common examples
============================

Most of its text is made up from sections 1.10.32–3 of Cicero's De finibus bonorum et malorum (On the Boundaries of Goods and Evils;
finibus may also be translated as purposes). Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit is the first known version
("Neither is there anyone who loves grief itself since it is grief and thus wants to obtain it").
It was found by Richard McClintock, a philologist, director of publications at Hampden-Sydney College in Virginia;
he searched for citings of consectetur in classical Latin literature, a term of remarkably low frequency in that literary corpus.

Lorem ipsum dolor
.................

Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor.
Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.
Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo.
Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi.


Panel Box
---------
used on the index pages

.. code-block:: none

   .. panel-box::
      :title: Admin
      :id: "getting-started"
      :class: my-panel

Creating Tabs
--------------
Adding

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

Results in

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

Glossary and Abbreviations
--------------------------

Inline abbreviation. The word in parenthesis is shown when you hover over the abbreviation.

.. code-block:: none

   :abbr:`LIFO (last-in, first-out)`.
   :abbr:`Overwrite (Same data cells overwritten many times)`

Inline Glossary term definition. Links to the glossary page.

.. code-block:: none

   :term:`term <Link in Glossary>`
   :term:`Size-tiered Compaction Strategy (STCS)<Size-tiered Compaction Strategy>`

.. _link-format-examples:

Links
-----
There are a few links you can use with different purposes.

* This is an example of an `External Link <https://docs.scylladb.com/some-doc>`_. It links to another site and has a arrow pointing out icon. It opens in a new tab.
* This is an example of an :ref:`Internal Link <link-format-examples>`. This is an internal cross reference. It requires a bookmark.
* This is an example of an :doc:`Internal Doc <../index>`. This is an internal doc cross reference. it looks for a file. A full path is required.
* This is an example of an :download:`download <index.rst>`. This opens a download window. It is for downloading software.


Images
------

use the following syntax:

.. code-block:: none

   .. image:: ../static/img/vertigto.jpg
      :width: 200pt


Tables
------

.. list-table::
   :widths: 33 33 33
   :header-rows: 1

   * - header name
     - header name
     - header name
   * - body text
     - body text
     - body text

Versioning in Scylla
--------------------
version add directives should be used when introducing or deprecating a feature
inline directive


.. code-block:: none

   .. versionadded:: version

   .. versionchanged:: version

   .. deprecared:: version

When using, these directives a blank line must follows

.. versionadded:: 1.1 Scylla Manager

.. versionchanged:: 2018.1 Scylla Enterprise

.. deprecated:: 2.0 Scylla Open Source


Admonitions
-----------

using

.. code-block:: none

   .. note:: text follows here

   .. caution:: look out

   .. warning:: take care

   .. tip:: here's a tip

results in

.. note:: text follows here

.. caution:: look out

.. warning:: take care

.. tip:: here's a tip


Frequently used Includes
------------------------

.. code-block:: none

   .. include:: /rst_include/scylla-commands-stop-index.rst

   .. include:: /rst_include/scylla-commands-start-index.rst

   .. include:: /rst_include/scylla-commands-restart-index.rst

