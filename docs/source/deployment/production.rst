=====================
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
    * - ``docs-links.yaml`` (optional)
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

#. If the default branch is not ``master`` or the docs are not located under the ``docs`` folder, modify the workflows to align with the project configuration. For example:

    .. code-block::

        on:
        push:
            branches:
            - master # edit this line
            paths:
            - "docs/**" # edit this line

#. In the repository's **Settings**, navigate to the **Pages** section and select **GitHub Actions** as the deployment source.

    .. figure:: images/pages-configuration.png

#. Commit and push the changes to your GitHub repository. Make sure to push these changes to the default branch.

Once you push the :ref:`workflows <available-workflows>` to the remote repository default branch, GitHub might take a couple of minutes to build and publish the site.

.. tip:: To monitor the progress of the build, look for the **Actions** tab below your repository name on GitHub.

If everything goes well, you will see the docs published under ``https://scylladb.github.io/<repository-slug>``.


Setting up a custom domain
--------------------------

.. note:: Setting up a custom domain requieres access to `scylladb.com` DNS configuration. Contact us in Slack ``#scylla-docs`` channel to set this configuration for you.

Follow the following steps to set up a custom domain:

#. In the domain's DNS configuration, create a new CNAME record that points ``<custom-sudomain>.scylladb.com`` to ``scylladb.github.io``.

#. Change ``html_baseurl`` setting in ``conf.py`` for the desired sub-domain name. For instance, we will use ``sphinx-theme.scylladb.com``.

#. Commit and push the changes to your GitHub repository. Make sure to push these changes to the default branch.

#. In the repository's **Settings**, navigate to the **Pages** section and make sure the custom domain name is set under **Custom domain** and **Enforce HTTPS** is enabled.

  .. figure:: images/pages-custom-domain.png

#. Verify the domain name to restrict its usage only on ScyllaDB organization repositories. To do so, follow the steps in `Verifying your domain with GitHub <https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages#verifying-a-domain-for-your-organization-site>`_.

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

Publishing the docs manually
----------------------------

If you need to manually trigger a documentation build and publish the latest changes, follow the steps below. This might be necessary if automatic triggers fail.

To manually rerun the last build, follow these steps:

1. Navigate to your repository's **Actions** tab on GitHub.

2. In the list of workflows, locate and select the ``docs-pages.yaml`` workflow.

3. On the workflow's page, click the **Run workflow** button. For more details, see `Manually running a workflow <https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/manually-running-a-workflow>`_.

4. **IMPORTANT:** When prompted, ensure you select the default branch (usually `master` or `main`). This ensures the workflow runs using the latest version of the configuration file, which contains information about which branches to build.

5. Confirm the action and wait for the workflow to complete.


Disabling GitHub Pages
----------------------

To disable the docs deployment temporarily:

#. Delete the :ref:`workflows <available-workflows>` from ``.github/workflows``.

#. Disable GitHub Pages from the repository settings. For more information, see  `Unpublishing a GitHub Pages Site <https://help.github.com/en/github/working-with-github-pages/unpublishing-a-github-pages-site#unpublishing-a-project-site>`_.
