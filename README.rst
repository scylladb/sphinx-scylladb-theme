##########################
Scylla Documentation Theme
##########################

The base Sphinx theme for ScyllaDB documentation projects.

************
Requirements
************

The theme is available on `PyPI <https://pypi.org/project/sphinx-scylladb-theme/>`_ and has been tested with Sphinx 2.4.4 and Fedora 32.
To build and preview the theme locally, you will need to install the following software:

- `Git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_
- `Poetry 1.0.5 <https://python-poetry.org/docs/basic-usage/>`_
- `Python 3.7 <https://www.python.org/downloads/>`_
- `pip <https://pip.pypa.io/en/stable/installing/>`_
- `pipx <https://pipxproject.github.io/pipx/>`_

*******************************
Setting up a new Sphinx Project
*******************************

Are you creating a Sphinx project from scratch? Follow the next steps to set up the new documentation project.

1\. Create a file named ``pyproject.toml`` under the project root folder. Edit the new file and add the contents from the `pyproject.toml template <docs/_utils/pyproject_template.toml>`_. Change the title, version, and package description.

2\. Copy the ``docs`` and ``.github`` directories to your new project root folder. The directory structure should look like:

.. code:: console

    project-name/
    ├── .github/
    ├── docs/
    │   ├── _utils/
    │   ├── source/
    │   ├── Makefile

3\. The documentation project lives under ``docs/source``.
Edit the file ``conf.py`` to suit your project needs (e.g., install new extensions, edit navigation links, ...).

***************************************
Adding the theme to an existing project
***************************************

If you are installing the theme as a dependency of an existing Sphinx project, follow the next steps:

1\. Add the dependency to the new Sphinx documentation project.
Open a console prompt and run the following command in the root documentation folder.

.. code:: console

    poetry add sphinx-scylladb-theme

2\. Add the following configuration in the documentation's ``conf.py`` file.

.. code:: console

    html_theme = 'sphinx_scylladb_theme'
    extensions = [
        ...,
        'sphinx_scylladb_theme'
    ]

3\. Finally, comment out the static paths to use the assets already included in the theme.

.. code:: console

    # templates_path = ['_templates']
    # html_theme_path = ['theme']
    # html_static_path = ['_static']

********************************
Customizing the navigation links
********************************

Edit the ``conf.py`` file under ``docs/source`` and overwrite the ``html_theme_options`` property.
You can customize the navigation bar and set the GitHub repository to report documentation issues.

.. code:: console

    html_theme_options = {
        'header_links': [
        ('Scylla Cloud', 'https://docs.scylladb.com/scylla-cloud/'),
        ('Scylla University', 'https://university.scylladb.com/'),
        ('ScyllaDB Home', 'https://www.scylladb.com/')],
        'github_issues_repository': 'scylladb/scylla-doc-issues',
        'show_sidebar_index': True,
    }

*******************
Previewing the docs
*******************

Run the following command to build the docs.

.. code:: console

    cd docs
    make preview

Once the command completes processing, open http://127.0.0.1:5500/ with your preferred browser.

*******************
Publishing the docs
*******************

The ``.github`` folder contains a script that builds and publishes to GitHub Pages new docs releases.
The workflow runs automatically every time:

- The master branch adds new commits.
- The repository gets a new release tag.

To enable GitHub Pages in your Sphinx Project, see `How to configure GitHub Pages <https://github.com/scylladb/python-driver/wiki/Documentation-notes#how-to-configure-github-pages>`_.

********************
Multiversion support
********************

The theme supports the extension ``sphinx-multiversion@0.2.3``, which allows building self-hosted versioned documentation.

By default, the sample doc project has multiversion enabled.
The dropdown is only shown if:

* The sphinx project has installed the sphinx-multiversion extension, and
* ``smv_tag_whitelist`` is not ``None`` or undefined, and
* ``smv_tag_whitelist`` matches at least one version in GitHub releases.

You can disable multiversion setting the property ``smv_tag_whitelist`` under ``docs/source/conf.py`` to ``None``.

To generate multiple versions of the documentation, you can run:

.. code:: console

    cd docs
    make multiversion

*Note:* The command ``make multiversion`` is aimed to be used by GitHub Actions CI.
While documenting new features, it is not advised to run ``make multiversion`` but ``make preview`` instead.
Versions are retrieved from GitHub tagged releases, hence previous docs cannot be edited.

Then, open ``docs/_build/dirhtml/<version>/index.html`` with your preferred browser.

*Note:* If you only can see docs generated for the master branch, try to run ``git fetch --tags`` to download the latest tags from remote.

Defining supported versions
===========================

The property ``smv_tag_whitelist`` under ``docs/source/conf.py`` defines a regular expression with the pattern for tags supported.

If you only want to support a subset of versions, you can define a list of tags modifying the regular expression. For example,``smv_tag_whitelist = r'\b(3.22.0-scylla|3.21.0-scylla)\b'`` would only build the documentation for the tags ``3.22.0-scylla``, ``3.21.0-scylla`` and ``master`` branch.

The extension allows configuring extra parameters. To know more about them, refer to [sphinx-multiversion documentation](https://holzhaus.github.io/sphinx-multiversion/master/configuration.html).

**************************
Notes for theme developers
**************************

Previewing the theme locally
============================

The ``docs`` folder contains a sample project with the Sphinx theme already installed.

To preview the theme locally, follow the next steps:

1\. Open a new console prompt and clone the theme project.

.. code:: console

    git clone https://github.com/scylladb/sphinx-scylladb-theme.git

2\. Run the following command to build the docs.

.. code:: console

    cd docs
    make preview

If everything goes well, the previous command should generate a ``docs/_build/dirhtml`` directory.

3\. Open http://127.0.0.1:5500/ with your preferred browser and preview the docs.

Publishing the theme to PyPi
============================

To upload a new version of the theme to PyPi, follow the next steps:

1\. Open the file ``pyproject.toml`` with a text editor and increase the project's version number.

.. code:: console

    [tool.poetry]
    name = "sphinx-scylladb-theme"
    version = "0.1.1"
    ...

2\. After saving your changes, run the command to build the package in a command prompt. The current directory should be the ``sphinx-scylla-theme`` project source code.

.. code:: console

    poetry build

3\. Publish the package to PyPi. The command prompt will ask you for the PyPi username and password.

.. code:: console

    poetry publish

After publishing the package, you should see the new release listed on  `PyPI <https://pypi.org/project/sphinx-scylladb-theme/#history>`_.
