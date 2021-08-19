Deployment
==========

The theme uses GitHub Pages and GitHub Actions to make the documentation publicly available.

On this page, you’ll learn:

- How to configure the workflows.
- How to deploy to GitHub Pages.
- How to set up a custom domain.
- How to re-run a workflow.
- How to disable GitHub Pages.

.. _available-workflows:

Available workflows
-------------------

The toolchain provides the following GitHub Actions under the directory ``.github/workflows``:

.. list-table::
    :widths: 30 70
    :header-rows: 1

    * - Filename
      - Description
    * - ``docs-pages.yaml``
      - Builds multi versioned docs every time the default branch (e.g. ``master``)  receives an update. If the build completes successfully, the workflow publishes the HTML version to GitHub Pages.
    * - ``docs-pr.yaml``
      - Builds the docs when the default branch receives a new pull request or when the pull request receives new commits. The purpose of this workflow is to make sure pull requests do not break the default branch after being merged.

Configuring the workflows
-------------------------

To configure the workflows:

#. Ensure you have the :ref:`workflows <available-workflows>` in your project under ``.github/workflows``. If you have followed :doc:`Getting Started <../getting-started/installation>` to install the project, the workflows are already included in the documentation project by default. If this is not the case, you can download them from `this link <https://github.com/scylladb/sphinx-scylladb-theme/blob/master/.github/workflows>`_.

#. Edit the workflows to match the project configuration if the default branch is not ``master`` or the docs are not under the ``docs`` folder. For example:

    .. code-block:

        on:
        push:
            branches:
            - master # edit this line
            paths:
            - "docs/**" # edit this line

#. Commit and push the changes to GitHub (default branch).

Enabling GitHub Pages
---------------------

Once you push the :ref:`workflows <available-workflows>`  to the remote repository default branch, GitHub might take a couple of minutes to build and publish the site.

You can check the status of the build on GitHub. Under your repository name, click **Actions**.

If everything goes well, you will see the docs published under ``https://scylladb.github.io/<repository-slug>``.


Setting up a custom domain
--------------------------

Follow the following steps to set up a custom domain:

.. note::To set up a custom domain, you need access scylladb.com DNS configuration.

#. In the domain's DNS configuration, create a new CNAME record that points ``<custom-sudomain>.scylladb.com`` to ``scylladb.github.io``.

#. Change ``html_baseurl`` setting in ``conf.py`` for the desired sub-domain name. For instance, we will use ``sphinx-theme.scylladb.com``.

#. Commit and push the changes to GitHub (default branch).

#. Once the DNS changes propagate (<24 h), the docs will be accessible from the custom domain name.


Re-running a workflow
---------------------

Re-running workflows is useful when:

- The theme received an update. By re-running the last build manually, the documentation project will receive the latest version. Otherwise, the theme will be automatically updated when the default branch gets an update.

- A previous version (branch or a tag) received a patch. Otherwise, the changes will not be reflected in production until the master branch gets an update.

To re-run a workflow see, `Re-running a workflow <https://docs.github.com/en/actions/managing-workflow-runs/re-running-a-workflow>`_.

Disabling GitHub Pages
----------------------

To disable the docs deployment temporarily:

#. Delete the :ref:`workflows <available-workflows>` from ``.github/workflows``, and push the changes.

#. Disable GitHub Pages from the repository settings. For more information, see  `Unpublishing a GitHub Pages Site <https://help.github.com/en/github/working-with-github-pages/unpublishing-a-github-pages-site#unpublishing-a-project-site>`_.
