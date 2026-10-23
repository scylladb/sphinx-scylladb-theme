# Markup reference

This file covers RST and ScyllaDB Sphinx theme markup. The source is
https://sphinx-theme.scylladb.com/stable/examples/index.html.

## Contents

1. Doctree and files
2. Redirects
3. Headings and page structure
4. Links
5. Admonitions
6. Code blocks
7. Tabs
8. Images and diagrams
9. Tables
10. Lists
11. Inline markup
12. Other directives and roles
13. Directives not to use

---

## 1. Doctree and files

**Every page must be in a toctree.** Sphinx fails the build for a page that is in no
toctree. Usually the right toctree is in the `index.rst` of the same folder:

```rst
.. toctree::
   :maxdepth: 2
   :hidden:

   existing-page
   Your New Page <your-new-page>
```

- List each entry without the `.rst` extension.
- `Title <path>` overrides the title shown in the navigation.
- Paths are relative to the current file. A leading `/` makes a path relative to the
  docs source root, which is the folder that contains `conf.py`.

**Section index pages.** A section's `index.rst` usually has two parts:

- a `:hidden:` toctree, which builds the left navigation
- a visible list of links in the page body, often in a `.. panel-box::` or
  `.. topic-box::`

When you add a page to the toctree, also add it to the visible list if the index has
one. Otherwise readers of the index page never see the new page.

```rst
.. panel-box::
  :title: Procedures
  :id: "getting-started"
  :class: my-panel

  * :doc:`Back Up a Cluster </operating-scylla/procedures/backup/>` - How to take a backup
```

**Don't use `:orphan:` to avoid adding a page to a toctree.** Use it only for pages
that are deliberately hidden from navigation, and only with a maintainer's agreement.

**File names:**
- Use short, descriptive lowercase words separated by hyphens, for example
  `configure-tls.rst`.
- Don't use underscores or capital letters. The file name becomes the URL.
- Store images in an `images/` folder next to the pages that use them.

**Reusing content:**
- `.. include:: /rst_include/some-file.rst` inserts another RST file. Shared fragments
  live in `rst_include/`, and a path that starts with `/` is relative to the source
  root.
- `.. literalinclude:: path` inserts a non-RST file, such as a config file or code
  sample, as a code block. Use `:lines: 1-10` to include only part of it.

## 2. Redirects

When you move, rename, or delete a page, add an entry to `docs/_utils/redirects.yaml`.
Other sites link to our pages, and without a redirect those links break:

```yaml
/stable/old-folder/old-page.html: /stable/new-folder/new-page.html
/stable/removed-page.html: https://docs.scylladb.com/
```

- Copy the path format that the existing entries in that repo use. Versioned projects
  include `/stable/`.
- Don't put a trailing `/` on the old path.
- Update every `:doc:` and `:ref:` that pointed to the old page.

## 3. Headings and page structure

Use this hierarchy:

| Level      | Markup                              |
|------------|-------------------------------------|
| Page title | `=` above and below, used only once |
| H1         | `-` below                           |
| H2         | `=` below                           |
| H3         | `.` below                           |
| H4         | `^` below                           |

```rst
==================
Configure TLS
==================

Encrypt Client Connections
--------------------------

Generate Certificates
=====================

Self-Signed Certificates
........................

Rotate Certificates
^^^^^^^^^^^^^^^^^^^
```

Rules:

- **Underlines and overlines must be at least as long as the heading text.** A shorter
  one causes a warning, which fails the strict build. A title's overline and underline
  must also be the same length.
- **Don't skip levels.** For example, don't put an H3 directly under an H1.
- **Don't go deeper than H4.** If you need a fifth level, restructure the page.
- **Keep the existing order on existing pages.** Many existing pages use other orders,
  such as a title with no overline, or `=` followed by `^`. RST assigns levels by order
  of appearance within each file, so follow the file's existing order rather than
  mixing in the table above.
- **Use Title Case for titles and headings,** for example "Configure Client-to-Node
  Encryption". When you add a heading next to existing headings at the same level that
  use different capitalization, match them. Consistency within the page is more
  important.
- **Keep titles under about 60 characters,** so that search results don't truncate
  them.
- **Don't use substitutions (`|name|`) in headings.** The replaced text can be longer
  than the underline, which breaks the build.
- **Don't add a mini-TOC (`.. contents::`).** The theme generates the "On This Page"
  sidebar. To show deeper headings in it, add `:toc-depth: 3` (or `4`) at the top of
  the page.
- **Add a meta description to new pages.** Search engines show it in results:

  ```rst
  .. meta::
     :description: How to enable client-to-node encryption in ScyllaDB.
  ```

**Topic types.** Give each page one topic type, and don't bury a procedure in the
middle of a conceptual page:

- **Concept:** what something is and why it matters.
- **Procedure:** how to do something.
- **Reference:** parameters, commands, or metrics.

**Procedures:**

- Start with an introduction of 1–3 sentences: what the procedure does, when to use
  it, and what it gives the reader.
- List prerequisites before the first step.
- Write the steps as a numbered list (`#.`), with one action per step.
- After a configuration change, add a step that verifies the change worked.
- If the action can be undone, describe the rollback as a separate procedure.

**Command reference pages** use the sections Name, Description, Syntax, Parameters,
and Example.

## 4. Links

**Never link to a section by its title.** A title-based link like `` `Section Title`_ ``
works until someone renames the section, and then it silently becomes a dead link.
Add an explicit anchor above the section instead:

```rst
.. _configure-tls-client:

Configure Client-to-Node Encryption
-----------------------------------
```

Then reference the anchor from anywhere in the project:

```rst
:ref:`configure-tls-client`
:ref:`client encryption settings <configure-tls-client>`
```

- Prefer the first form. Sphinx fills in the current section title, so the link text
  stays correct after a rename.
- Use custom text only when the sentence needs wording that differs from the title.
- Anchors are global across the project. Use descriptive, unique names such as
  `configure-tls-prerequisites`, not `prerequisites`.

| Link type | Markup | Notes |
|---|---|---|
| Another page | ``:doc:`Text </path/to/page>` `` | Write the path without `.rst`. A leading `/` is relative to the source root and survives file moves. |
| A section | ``:ref:`anchor-name` `` | Requires an explicit anchor. |
| An external site | `` `Text <https://example.com>`_ `` | Opens in a new tab with an "external" icon. If the same text is used for two different URLs on one page, use `__` to avoid a duplicate-target warning. |
| A config parameter (scylladb/scylladb only) | ``:ref:`text <confprop_parameter_name>` `` | Group: ``:ref:`text <confgroup_group_name>` ``. No anchor needed. |
| A file to download | ``:download:`text <path>` `` | |
| A JavaScript-generated anchor | ``:page-anchor:`text </path#anchor>` `` | For Redoc or Swagger API pages only. Sphinx can't check it, so prefer `:ref:` or `:doc:`. |

- **Link to other ScyllaDB products with full URLs,** for example
  `https://manager.docs.scylladb.com/stable/...`. Link to the content instead of
  copying it.
- **Write meaningful link text,** such as the destination's title. Don't use "here"
  or "this link".

## 5. Admonitions

Keep boxes rare. Each one interrupts reading, and every extra box weakens the others:
when everything is highlighted, nothing is.

- **Default to a plain paragraph.** Use a box only when missing the information would
  cost the reader real money, real data, or a working cluster: a destructive
  operation, an irreversible setting, or a known correctness trap. Context,
  background, caveats, and nice-to-know details belong in the paragraph they relate
  to.
- **Judge density per section.** A section rarely needs more than one box, and two
  boxes should never sit back to back. Where boxes cluster, fold the weakest ones
  back into the text.
- **Never use a box for roadmap items or version availability.**

Allowed types:

| Directive | Use for |
|---|---|
| `.. note::` | Helpful information with no risk. |
| `.. tip::` | Something that saves time or improves performance. |
| `.. caution::` | Risk of degraded performance or partial data loss. |
| `.. warning::` | Risk of total data loss, crashes, or physical harm. |

- Don't use `important`, `attention`, `danger`, `error`, `hint`, `seealso`, or a
  generic `admonition`.
- Where you would have used `important`, use `note`, or `caution`/`warning` if there is
  real risk.
- `.. alert::` is an announcement banner. Use it only with a maintainer's agreement.

```rst
.. warning::

   This command deletes all data on the node and can't be undone.
```

## 6. Code blocks

```rst
.. code-block:: cql

   SELECT * FROM ks.users WHERE id = 1;
```

- **Always set a language,** such as `cql`, `shell`, `console`, `yaml`, `json`,
  `python`, `java`, `go`, or `none`. Use `none` for output and plain text.
- **Indent the code three spaces under the directive,** with a blank line between the
  directive (or its options) and the code.
- **Don't prefix commands with `$` or `#`.** The copy button would copy the prompt along
  with the command.
- **Put command output in its own block** (language `none`). That keeps the command
  block copyable:

  ```rst
  .. code-block:: shell

     nodetool status

  The output looks similar to this:

  .. code-block:: none

     Datacenter: dc1
     UN  192.0.2.10  ...
  ```
- **Never include real customer data, hosts, IP addresses, keys, tokens, or passwords.**
  Use placeholders such as `<keyspace_name>`, `192.0.2.10` (an IP range reserved for
  documentation), and `example.com`.
- **Use `.. literalinclude::` for whole files.**

Options:

| Option | Effect |
|---|---|
| `:substitutions:` | Enables `\|name\|` substitutions inside the block. |
| `:emphasize-lines: 2,4` | Highlights lines. |
| `:linenos:` | Shows line numbers. |
| `:class: hide-copy-button` | Hides the copy button, for example for output that shouldn't be copied. |

## 7. Tabs

Use tabs when the reader picks one option and keeps it for the whole procedure, such as
an OS or distribution, a cloud provider, a driver language, or packages versus Docker.

```rst
.. tabs::

   .. group-tab:: Debian/Ubuntu

      .. code-block:: shell

         sudo systemctl stop scylla-server

   .. group-tab:: Docker

      .. code-block:: shell

         docker exec -it some-scylla supervisorctl stop scylla
```

- **Use `group-tab`, not plain `tab`.** Group tabs stay in sync across the page:
  choosing "Docker" once switches every tab set on the page.
- **Use the same labels for the same choice** everywhere on the page, so that syncing
  works.
- **Put tabs only around the step that differs.** Don't wrap a whole procedure in tabs
  when only one step depends on the reader's choice.

## 8. Images and diagrams

Every image and figure needs alt text that describes what it shows. Don't write
"screenshot" or "image".

```rst
.. image:: images/cluster-details.png
   :alt: Cluster details page with the Connect button highlighted

.. figure:: images/architecture.png
   :alt: Three-datacenter cluster with eight nodes per datacenter
   :width: 600px

   Caption text, shown below the figure.
```

- **Choose the directive by caption.** Use `figure` when the image needs a caption,
  and `image` otherwise.
- **Set `:width:` on large images.** Readers can click a resized image to see it at
  full size.
- **Prefer Mermaid (`.. mermaid::`) for flowcharts and sequence diagrams.** Diagrams
  written as text are reviewable and easy to update.
- **Keep text inside diagrams to a minimum.** Use labels with a legend table instead.
- **Show 8 nodes per cluster in architecture diagrams.**
- **Use sufficient color contrast.**
- **Crop screenshots to the relevant UI,** and remove or blur personal and account
  data. Screenshots go stale quickly, so add them only when they add real value.
- **To attach metadata, wrap the image in `.. diagram::`,** with options such as `:id:`,
  `:tags:`, `:categories:`, and `:last-reviewed:`.

## 9. Tables

Use `list-table`. It is easier to edit and to review in a diff than a grid table:

```rst
.. list-table:: Supported Platforms
   :widths: 30 70
   :header-rows: 1

   * - Platform
     - Notes
   * - Ubuntu 24.04
     - Supported
```

- **Give every table a caption.** Captions help both SEO and screen readers.
- **Make the number of `:widths:` values match the number of columns,** and set
  `:header-rows: 1` when there is a header row.
- **Use grid tables only when you need merged cells.**
- **Use `|v|` and `|x|` for check and cross marks.**

## 10. Lists

```rst
#. First step.
#. Second step.

   * A nested bullet, indented under the item's text.

#. Third step.
```

- **Choose the list type by order.** Use numbered lists (`#.`, which number
  automatically) for steps and bulleted lists (`*`) when order doesn't matter.
- **Put a blank line before and after every list.** Indent nested lists and
  continuation content so that they line up under the item's text.
- **Introduce a list with a sentence that ends in a colon.**
- **Write the items in parallel form:** all imperative, or all noun phrases.

## 11. Inline markup

| Markup | Use for |
|---|---|
| `**Bold**` | UI elements: Click **Create Cluster**. |
| `*Italics*` | A new term the first time it appears: A *node* is... |
| ` ``code`` ` | Commands, file names, paths, parameters, and CQL keywords. RST uses double backticks; single backticks aren't inline code. |

- **Don't nest inline markup.** For example, RST can't make code bold.
- **Put a space or punctuation before and after inline markup.**

## 12. Other directives and roles

Use these sparingly:

| Markup | Use for |
|---|---|
| ``:label-tip:`Text` `` | Status or availability labels, such as ``:label-caution:`Experimental` `` or ``:label-tip:`Available with the Professional plan and above` ``. Styles: `default`, `note`, `tip`, `caution`, `warning`. Labels can appear in headings. |
| ``:term:`Text <Glossary Term>` `` | A link to a glossary entry. |
| ``:include_tooltip:`text <Glossary Term>` `` | A glossary definition shown on hover. Tooltips can also contain inline text. |
| ``:abbr:`SSTable (Sorted Strings Table)` `` | An abbreviation, defined on first use. |
| `.. collapse:: Title` | Long, optional content such as full config files or long output. Don't hide required steps in a collapsible. |
| `\|name\|` substitutions | Defined in `rst_prolog` in `conf.py`. The defaults are `\|v\|` and `\|x\|`. |
| `:full-width:`, `:landing:`, `:hide-*:` | Page options for landing and index pages only. |

## 13. Directives not to use

| Don't use | Use instead |
|---|---|
| `.. versionadded::`, `.. versionchanged::`, `.. deprecated::` | State version information once, in prose. See `style.md`. |
| `.. important::` and other admonitions not listed in section 5 | `.. note::` (or `caution`/`warning` if there is real risk) |
| `.. contents::` | Nothing. The theme generates the "On This Page" sidebar. |
| `:orphan:` (to avoid adding a page to a toctree) | A toctree entry |
| `` `Section Title`_ `` | ``:ref:`anchor` `` |
