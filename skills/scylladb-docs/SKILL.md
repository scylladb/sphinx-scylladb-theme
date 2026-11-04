---
name: scylladb-docs
description: Write, update, and review ScyllaDB user documentation pages in reStructuredText (.rst) built with the ScyllaDB Sphinx theme and published on docs.scylladb.com and its subdomains. Use this skill whenever you create, edit, move, or delete files under a `docs/` folder in any ScyllaDB project (scylladb, scylla-cloud-doc, scylla-manager, scylla-operator, scylla-monitoring, drivers, and others); when you add a page to the doctree or fix links, headings, admonitions, tabs, code blocks, or images in `.rst` files; and when you review a docs change or docs pull request before it is submitted. Use it even if the user doesn't mention the style guide or the theme. It does not apply to `docs/dev/` in scylladb/scylladb and scylladb/scylla-enterprise, which holds unpublished developer notes.
---

# ScyllaDB documentation

This skill helps contributors, most of whom are developers rather than technical
writers, create and update ScyllaDB user documentation so that it builds cleanly,
fits the doctree, and reads like the rest of the docs.

The rules come from three places:

- the ScyllaDB Sphinx theme (https://sphinx-theme.scylladb.com/stable/examples/)
- the ScyllaDB style guide
  (https://github.com/scylladb/scylladb-docs-homepage/blob/main/STYLEGUIDE.md)
- the ScyllaDB Cloud docs conventions

Everything you need from those sources is in this skill's two reference files:

- `references/markup.md`: RST and theme markup, including the doctree, headings,
  links, admonitions, code blocks, tabs, images, tables, lists, and redirects. Read
  the section for any construct you are about to write or review.
- `references/style.md`: language, word choice, version information, and errors in
  the current docs. Read it before you write or review prose.

## Step 1: Check the scope

1. **Which files are in scope.** Only user documentation is in scope: files under
   `docs/`, whose sources are in `docs/` or `docs/source/`. In scylladb/scylladb and
   scylladb/scylla-enterprise, skip everything under `docs/dev/`. Those files are
   Markdown developer notes that are never published, so these rules don't apply to
   them, even when the same change also touches published docs. In other projects,
   `docs/dev/` is in scope like the rest of `docs/`.
2. **Which file format.** This skill covers reStructuredText (`.rst`) pages only.
   Some projects publish Markdown pages written in MyST, for example
   scylladb/scylla-operator. For `.md` pages:
   - Apply only the language rules in `references/style.md`.
   - Follow the markup of the surrounding Markdown pages instead of
     `references/markup.md`, which describes RST.
   - Never convert Markdown pages to RST, and never mix RST syntax into Markdown.
   - Tell the contributor that the skill's markup checks don't cover Markdown pages.
3. **Which project this is.** Check the repository name, for example with
   `git remote -v`. Some rules apply only to scylladb/scylla-cloud-doc; they are
   marked "Cloud only" in the references.
4. **Project overrides.** Projects aren't supposed to have a `CLAUDE.md`, but some
   might. If one exists at the repository root or in `docs/`, read it. Where its rules
   overlap with this skill's, the `CLAUDE.md` rules win. Also skim `docs/README.md`
   for project-specific build details.

## Step 2: Write or update content

1. **Find where the content belongs.** Open the folder's `index.rst` and a couple of
   neighboring pages. This tells you the section structure, the anchor naming, and
   whether the index has a visible list of links. Don't copy their markup blindly:
   many existing pages break the current rules (see "Errors in the current docs" in
   `references/style.md`). Follow this skill, not the neighbors.
2. **Edit existing pages in place.** Keep the page's existing heading order. RST
   assigns heading levels by order of appearance, so mixing styles breaks the
   hierarchy. Fix rule violations in the lines you touch. Leave unrelated legacy
   problems alone, because large cleanups belong in a separate PR, where reviewers
   can check mechanical changes apart from content changes.
3. **For a new page:**
   - Start from the page template below.
   - Name the file with lowercase words separated by hyphens. The file name becomes
     the URL.
   - Add the page to a toctree, or the build fails.
   - If the section's `index.rst` also lists its pages visibly, for example in a
     `panel-box`, add the page there too.
4. **When you move, rename, or delete a page,** add a redirect in
   `docs/_utils/redirects.yaml`, and update every `:doc:` and `:ref:` that pointed to
   the old location. Other sites link to our pages, and the redirect is the only thing
   that keeps those links working.
5. **Write the content** following the core rules below and the reference files.

### Page template

```rst
.. meta::
   :description: One sentence that describes the page for search results.

======================
Configure Something
======================

One to three sentences: what this page covers, who it is for, and why it matters.

.. _configure-something-prerequisites:

Prerequisites
-------------

* ...

Configure Something
-------------------

#. Do the first thing.

   .. code-block:: shell

      sudo systemctl restart scylla-server

#. Verify that it worked.
```

The template shows the heading hierarchy: the title has `=` above and below, H1 uses
`-`, H2 uses `=`, H3 uses `.`, and H4 uses `^`.

## Core rules

These rules break the build, break links, or are the most common review comments.
The references explain each one in detail.

- **Every page must be in a toctree.** Without that, Sphinx fails the build.
- **Heading underlines must be at least as long as the text.** A shorter underline
  causes a warning, and the strict build treats warnings as errors.
  - Use the hierarchy from the page template. Don't skip levels, and don't go deeper
    than H4.
  - Use Title Case, unless the other headings at the same level on the page use
    different capitalization. Consistency within the page wins.
- **Link to sections with an explicit anchor and `:ref:`, never by the section
  title.** A link like `` `Section Title`_ `` silently breaks when someone renames
  the section.
  - Put `.. _unique-anchor-name:` above the heading.
  - Prefer the plain form ``:ref:`unique-anchor-name` ``, so that the link text
    follows the title when it changes.
  - Link to whole pages with ``:doc:`Text </path/to/page>` ``.
  - Write external links as `` `Text <https://...>`_ ``.
- **Keep admonitions rare.** Use a box only when missing the information would cost
  the reader money, data, or a working cluster.
  - Allowed types are `note`, `tip`, `caution`, and `warning`. Use `note` where you
    would have used `important`.
  - Don't use a box for roadmap items or version availability.
  - Don't put two boxes back to back.
- **Don't use version directives.** That means no `versionadded`, `versionchanged`, or
  `deprecated`.
- **Don't document unreleased features.** That also rules out pre-announcements and
  "coming soon" notes.
- **Code blocks need a language,** for example `.. code-block:: cql`. Don't use `$`
  prompts. Put command output in a separate block, and use placeholders instead of
  real hosts, keys, or customer data.
- **Every image and figure needs `:alt:` text** that describes what the image shows.
- **Write for the reader:** use "you", active voice, present tense, and American
  English. Use "ScyllaDB", not "Scylla". Bold UI elements.

## Step 3: Review the changes before submitting

Run this review when the user asks for it, and also after you finish writing or
editing docs.

1. **Run the checker.** From the repository root, run:

   ```bash
   python <path-to-this-skill>/scripts/check_docs.py
   ```

   The checker compares your work, committed or not, with the upstream default branch.
   It checks only `.rst` files and lists any changed Markdown pages it skipped. It
   reports mechanical problems in the lines you added:
   - images without alt text
   - code blocks with no language, and `$` prompts
   - links to section titles
   - unsupported admonitions and version directives
   - discouraged terms
   - heading underlines that are too short
   - new pages that aren't in any toctree
   - moved or deleted pages that have no redirect

   Options:
   - **`--base <ref>`** compares with a different branch. Use it when the change targets
     a release branch rather than the default branch, for example
     `--base upstream/branch-2026.1`. Release branches diverge from the default
     branch, so without `--base` the release branch's own content shows up as added
     lines and produces unrelated findings. Take the target branch from the pull
     request if there is one, or ask the contributor.
   - **`--all`** checks every line of the changed files, not only the added lines.

   The script uses heuristics, so treat its findings as candidates: confirm each one in
   the file before you report or fix it.
2. **Review the diff yourself** for things a script can't judge:
   - Title Case and consistent headings
   - admonition density
   - whether each page has one topic type, and whether procedures follow the expected
     structure
   - link text
   - the prose rules in `references/style.md`
   - in scylla-cloud-doc, how version information is written
3. **Build the docs strictly.** A strict build uses Sphinx's `-W` option, which turns
   every warning into an error. Fix every warning that your change introduced.
   - Run the same command that the project's CI runs on pull requests. Look in
     `.github/workflows/docs-pr.yaml`, and copy any make variables it passes. For
     example, scylladb/scylla-enterprise runs `make -C docs FLAG=enterprise test`.
     Without the flag, the build uses a different configuration and doesn't validate
     the Enterprise site.
   - If there is no such workflow, find the strict target in the project's
     `docs/Makefile`. Most projects have a `test` target, so you run
     `make -C docs test`.
   - Some projects have no `test` target and add `-W` to the options that every target
     uses instead. scylladb/scylla-operator is one. In those projects, run
     `make -C docs dirhtml`.
   - If no target builds with `-W`, say so. Don't report a build without `-W` as
     strict.
   - The build needs a Unix-like shell (WSL on Windows), Python, `make`, and the
     project's Python package manager. Most projects use `uv`, but some use Poetry,
     for example scylladb/scylla-enterprise. Check `docs/Makefile` (or
     `docs/README.md`) to see which one the project uses. The first run downloads
     dependencies and can take several minutes.
   - If the build can't run on this machine, say so plainly. Don't claim it passed. In
     most projects, the **Docs / Build PR** check runs the strict build on the pull
     request.
4. **Check the built HTML.** After a successful build, find each changed page in
   `docs/_build/dirhtml/<page-path>/index.html` and confirm that:
   - the page exists
   - every `<img>` has a non-empty `alt` attribute
   - every tab set rendered
5. **Check the pull request text,** if a PR exists or you are writing it:
   - The title starts with `docs:`, for example `docs: document the restore procedure`.
   - The description references the issue that the PR fixes and explains why the
     change was made, not only what changed.

### Review report

When you report a review, group the findings by file and give a line number for each
finding, so that the contributor can jump straight to it:

```
docs/operating-scylla/procedures/backup.rst
  42  Image has no :alt: text. Describe what the screenshot shows.
  88  Link to a section title (`Restore`_). Add an anchor and use :ref:.

Build: make -C docs test passed with no warnings.
PR title: missing the "docs:" prefix.
```

If the user asked you to write or edit docs, fix the findings in the lines you changed
instead of only listing them. If the user asked only for a review, list the findings
and offer to fix them.
