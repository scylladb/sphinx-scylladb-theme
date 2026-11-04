Documentation dependency updates
================================

The optional **Docs / Update dependencies** workflow updates the Python dependencies used to build your documentation.

How it works
------------

The workflow runs every Monday at 08:00 UTC and opens a pull request with the updated ``uv.lock`` after the vulnerability
audit and documentation build pass.

Updates skip PyPI files uploaded less than seven days ago, except for ``sphinx-scylladb-theme`` and ``sphinx-multiversion-scylla``.
The seven-day window gives maintainers time to detect and remove compromised releases before they are selected for an update.

Enable the workflow
-------------------

#. Copy `docs-dependencies.yaml <https://github.com/scylladb/sphinx-scylladb-theme/blob/master/.github/workflows/docs-dependencies.yaml>`_
   into ``.github/workflows/`` and adjust the Python version and docs paths.
#. Enable **Allow GitHub Actions to create and approve pull requests** in the
   repository's Actions settings.
#. Copy the ``UPDATE_EXCLUDE_NEWER`` variable and the ``update`` and ``audit``
   targets from the theme's `docs/Makefile <https://github.com/scylladb/sphinx-scylladb-theme/blob/master/docs/Makefile>`_
   into your project's ``docs/Makefile``.

The workflow runs ``make -C docs update``, ``make -C docs audit``, and ``make -C docs test``.
An audit finding or build failure stops the run before a pull request is opened.

Run an update manually
----------------------

#. Open **Actions > Docs / Update dependencies > Run workflow** in your repository.
#. Select the repository's default branch.
#. Run the workflow with the checkbox left unchecked to keep the seven-day window.

To take an urgent release immediately, select **Allow dependency releases uploaded less than seven days ago** before running the workflow.
