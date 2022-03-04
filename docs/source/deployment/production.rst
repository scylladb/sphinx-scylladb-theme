Production deployment
=====================

We use GitHub Pages and GitHub Actions to make the documentation publicly available.

On this page, you will learn:

- How to deploy to GitHub Pages.
- How to set up a custom domain.
- How to read build error messages.
- How to re-run a workflow.
- How to disable GitHub Pages.

.. _available-workflows:

Available workflows
-------------------

The toolchain provides the following workflows under the directory ``.github/workflows``:

.. list-table::
    :widths: 30 70
    :header-rows: 1

    * - Filename
      - Description
    * - ``docs-pages.yaml``
      - Builds multi versioned docs every time the default branch (e.g. ``master``)  receives an update. If the build completes successfully, the workflow publishes the HTML version to GitHub Pages.
    * - ``docs-pr.yaml``
      - Builds the docs when the default branch receives a new pull request or when the pull request receives new commits. The purpose of this workflow is to make sure pull requests do not break the default branch after being merged.
    * - ``docs-links.yaml``
      -  Looks for broken links once a week. If there are broken links, it creates an issue in the same repository with the list of affected links.

.. caution:: If you modify these workflows in your repository, you will need to maintain the changes. So instead, we recommend you to open an issue in the `sphinx-scylladb-theme repository <https://github.com/scylladb/sphinx-scylladb-theme>`_ so that all projects can benefit from the improvements you made.

Installation
------------

To install the workflows:

#. Copy the workflows named ``docs-*.yaml`` from `.github/workflows <https://github.com/scylladb/sphinx-scylladb-theme/blob/master/.github/workflows>`_ to your project. The project's directory structure should look like the following:

    .. code:: console

        project-name/
          ├── .github/
          |   ├── workflows/
          |   |   ├── docs-pages.yaml
          |   |   ├── docs-pr.yaml
          |   |   ├── docs-links.yaml

#. If the default branch is not ``master`` or the docs are not under the ``docs`` folder, the workflows to match the project configuration. For example:

    .. code-block::

        on:
        push:
            branches:
            - master # edit this line
            paths:
            - "docs/**" # edit this line

#. Commit and push the changes to GitHub (default branch).

Once you push the :ref:`workflows <available-workflows>` to the remote repository default branch, GitHub might take a couple of minutes to build and publish the site.

If everything goes well, you will see the docs published under ``https://scylladb.github.io/<repository-slug>``.

.. tip:: You can check the status of the build on GitHub. Under your repository name, click **Actions**.

Setting up a custom domain
--------------------------

.. note:: Setting up a custom domain requieres access to `scylladb.com` DNS configuration. Contact us in Slack ``#scylla-docs`` channel to set this configuration for you.

Follow the following steps to set up a custom domain:

#. In the domain's DNS configuration, create a new CNAME record that points ``<custom-sudomain>.scylladb.com`` to ``scylladb.github.io``.

#. Change ``html_baseurl`` setting in ``conf.py`` for the desired sub-domain name. For instance, we will use ``sphinx-theme.scylladb.com``.

#. Commit and push the changes to GitHub (default branch).

#. Once the DNS changes propagate (<24 h), the docs will be accessible from the custom domain name.

Reading error messages
----------------------

Docs builds usually fail when there is a critical error or warning in the documenation syntax.

To get the specific error message:

#. Hover the |x| that you will see next to the commit message, and click on **Details**.

    .. figure:: images/build-error.png

#. Search for "warning" and "error" in the box you will find at the top right of the screen.

    .. figure:: images/build-log.png

You should see the error messages highlighted.

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
