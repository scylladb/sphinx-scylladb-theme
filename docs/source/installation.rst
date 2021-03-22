============
Installation
============

1. Copy the ``docs`` and ``.github`` directories from the repository `scylladb/sphinx-scylladb-theme <https://github.com/scylladb/sphinx-scylladb-theme>`_
to the project root directory where you want to setup docs. The directory structure should look like this:

.. code:: console

   project-name/
      ├── pyproject.toml
      ├── .github/workflows/pages.yaml
      ├── docs/
      │   ├── _utils/
      │   |   ├── deploy.sh
      │   |   ├── redirect.sh
      │   |   ├── setup.sh
      │   ├── source/
      │   ├── Makefile

.. note:: If you already have docs in the project under an existing ``docs`` directory, move the doc files to the ``docs/source`` directory. 

2. Create the file ``docs/pyproject.toml`` under the new ``docs`` folder. Copy the contents from the `pyproject.toml template <docs/_utils/pyproject_template.toml>`_.

3. Edit the project's ``conf.py`` file to suit the project needs (e.g. install new extensions, edit navigation links, ...).
   For more information about the most common configurable settings, refer to :doc:`Configuration <configuration>`.

4. If you don't already have a ``.gitignore`` file in the project, place one in the root directory and include ``/docs/_build`` and ``/source/.doctrees`` in it.
   If you already have a ``.gitignore`` file, add both paths to the file.