GitHub Pages
============

The theme uses GitHub Pages and GitHub Actions to make the documentation publicly available.
Projects using this toolchain build and deploy a new site every time the default branch (master) receives an update.

On this page, you’ll learn:

- How to enable GitHub Pages
- How to set up a custom domain.
- How to re-run a workflow.
- How to disable GitHub Pages

Enabling GitHub Pages
---------------------

#. Create a file named ``.github/pages.yaml`` in the project's root repository.

#. Copy the contents from `this file <https://github.com/scylladb/sphinx-scylladb-theme/blob/master/.github/workflows/pages.yml>`_ into ``.github/pages.yaml``.

#. (Optional) If the repository default branch is not ``master``, edit the configuration file to use the default branch name instead.

#. Commit and push the changes to GitHub (default branch).

#. Wait a couple of minutes; it might take a while until GitHub builds the site. If everything goes well, you will see the docs published under ``https://scylladb.github.io/<repository-slug>``.

Setting up a custom domain
--------------------------

.. note:: To set up a custom domain, you need access scylladb.com DNS configuration.

Follow the next steps to set up a custom domain:

#. In the domain's DNS configuration, create a new CNAME record that points ``<custom-sudomain>.scylladb.com`` to ``scylladb.github.io``.

#. Change ``html_baseurl`` setting in ``conf.py`` for the desired sub-domain name. For instance, we will use ``sphinx-theme.scylladb.com``.

#. Once the DNS changes propagate (<24 h), the docs will be accessible from the custom domain name.

Re-running a workflow
---------------------

Re-running workflows is useful when:

- The theme received an update. By re-running the last build manually, the documentation project will receive the latest version. Otherwise, the theme will be automatically updated when the default branch gets an update.

- A previous version (branch or a tag) received a patch. Otherwise, the changes will not be reflected in production until the master branch gets an update.

To re-run a workflow see, `Re-running a workflow <https://docs.github.com/en/actions/managing-workflow-runs/re-running-a-workflow>`_.

Disabling GitHub Pages
----------------------

To disable the docs deployment temporarily, see `Unpublishing a GitHub Pages Site <https://help.github.com/en/github/working-with-github-pages/unpublishing-a-github-pages-site#unpublishing-a-project-site>`_.
