============
Installation
============

This guide walks you through the steps required to add the documentation toolchain to a ScyllaDB project hosted on GitHub.

Prerequisites
-------------

Before adding the documentation toolchain to a project, you will need to have installed:

- A Unix-based terminal. For Windows, use `Windows Subsystem for Linux <https://learn.microsoft.com/en-us/windows/wsl/install>`_.
- `Python 3.10 or 3.12 <https://www.python.org/downloads/>`_.
- `Poetry 1.8.1 <https://python-poetry.org/docs/master/>`_.
- `Make <https://www.gnu.org/software/make/>`_.
- `Git <https://git-scm.com/>`_.

Step 1: Download the sample project
-----------------------------------

#. Copy the ``docs`` directory from the repository `scylladb/sphinx-scylladb-theme <https://github.com/scylladb/sphinx-scylladb-theme>`_  to the root directory of the project where you want to set up docs. The project's directory structure should look like the following:

   .. code-block:: console

      project-name/
         ├── docs/
         │   ├── _utils/
         │   |   ├── redirects.yaml
         │   |   ├── deploy.sh
         │   ├── source/
         │   |   ├── conf.py
         │   |   ├── index.rst
         │   ├── Makefile

   .. note:: If you already have docs in the project under an existing ``docs`` directory, move the doc files to ``docs/source`` directory.

#. In the newly created ``docs`` folder, create a ``pyproject.toml`` file and copy the contents from the `pyproject.toml template <https://github.com/scylladb/sphinx-scylladb-theme/blob/master/docs/_utils/pyproject_template.toml>`_.

#. Create the file ``.github/dependabot.yml``. Copy the contents from the `dependabot.yml template <https://github.com/scylladb/sphinx-scylladb-theme/blob/master/docs/_utils/dependabot_template.yml>`_.

Step 2: Configure the theme
---------------------------

#. Edit the file ``docs/source/conf.py`` file to suit the project needs (e.g., edit the project name and site description, install new extensions, ...).
   For more information, see :doc:`Configuration <../configuration/index>`.

#. If you don't already have a ``.gitignore`` file in the project, place one in the root directory and include ``/docs/_build`` and ``/source/.doctrees`` in it.
   If you already have a ``.gitignore`` file, add both paths to the file.

Step 3: Preview the site locally
--------------------------------

#. Delete or adapt the sample documentation files under ``docs/source``.

#. From the command line, run ``make preview`` within the ``docs`` folder:

    .. code-block:: console

        cd docs
        make preview

    .. tip:: For troubleshooting, refer to the :ref:`preview command <Make_Preview>` documentation.

#. Fix any warnings raised by Sphinx.

#. Once the docs build without errors, open ``http://127.0.0.1:5500/`` to preview the generated site.

Step 4: Deploy to GitHub Pages
------------------------------

To deploy the documentation site, see :doc:`GitHub Pages Configuration <../deployment/production>`.
