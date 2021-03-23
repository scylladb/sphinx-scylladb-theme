GitHub Pages
============

The theme uses GitHub Pages and GitHub Actions to make the documentation publicly available.
The file `.github/pages.yaml <https://github.com/scylladb/sphinx-scylladb-theme/blob/master/.github/workflows/pages.yaml>`_ in your project defines how docs are published using GitHub Pages.

Most projects build and deploy a new site every time the default branch (master) receives an update.
When :ref:`multiversion <multiversion>` is enabled, GitHub Pages builds docs for all versions listed in the file ``conf.py``.

Enabling GitHub Pages
---------------------

.. note:: You need to be logged in GitHub with Admin or Maintain repo permissions. If this is not the case, please ask the repo owner to `invite you as a collaborator <https://help.github.jp/enterprise/2.11/user/articles/inviting-collaborators-to-a-personal-repository/>`_. 

#. Change ``html_baseurl`` setting in ``docs/conf.py`` for the future public URL of your site. For instance, we will use ``https://scylladb.github.io/sphinx-scylladb-theme``.

#. Create a new ``gh-pages`` empty branch. Run the commands in the root directory.

    .. code:: console

        git checkout --orphan gh-pages
        # Warning: Be careful; the next command deletes all files inside the folder.
        git rm -rf .
        touch .nojekyll
        git add .
        git commit -m "Setup GitHub Pages"
        git push origin gh-pages
    
#. Open the repository `Settings <https://github.com/scylladb/sphinx-scylladb-theme/settings>`_ and scroll down to the "GitHub Pages" section.

#. Select ``gh-pages`` branch.

#. Wait a couple of minutes; it might take a while until GitHub applies the changes. If everything goes well, you will see the docs published under ``https://scylladb.github.io/<repository-slug>``.

Disabling GitHub Pages
----------------------

To disable the docs deployment temporarily, see `Unpublishing a GitHub Pages Site <https://help.github.com/en/github/working-with-github-pages/unpublishing-a-github-pages-site#unpublishing-a-project-site>`_.

Setting up a custom domain
--------------------------

.. note:: You need access to the domain DNS configuration.

Follow the next steps to set up a custom domain:

#. In the domain's DNS configuration, create a new CNAME record that points ``<custom-sudomain>.scylladb.com`` to ``scylladb.github.io``.

#. Change ``html_baseurl`` setting in ``docs/conf.py`` for the desired sub-domain name. For instance, we will use ``sphinx-theme.scylladb.com``.

#. Once the DNS changes propagate (<24 h), the docs will be accessible from the custom domain name.
