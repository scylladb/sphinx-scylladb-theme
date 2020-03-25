Getting Started
===============

Installing the Theme
--------------------

At this moment theme is only available as a Git repository.
In the nearest future it will become a Python package, installable with pip or other tools.

To test the theme with a Sphinx docs project, clone it to a subdirectory of your project.
Don't use git submodules, as in the future you won't need to keep the submodule.

Configuring a Sphinx Project
----------------------------

Make sure you've cloned the theme to a project's subdirectory before configuring it.

To configure a Sphinx project for using this theme, change several parts of its ``conf.py`` file:


#.  Change the ``html_theme`` value.
    Add a ``html_theme_path`` variable with path to directory where you cloned the theme.
    (It has ``sphinx_scylla_theme`` inside it.)

    ..  code-block:: python

        html_theme = 'sphinx_scylla_theme'
        html_theme_path = ["<path to theme>"]

    Once theme will be installable as a Python package, ``html_theme_path`` will become obsolete.

#.  Change the ``html_sidebars`` value:

    ..  code-block:: python

        html_sidebars = {'**': ['side-nav.html']}


Now your project is configured to use the ScyllaDB theme.

Using the Extensions
--------------------

If you want to also use the ``topic-box`` and ``panel-box`` extensions,
add some more lines to ``conf.py`` file:

#.  On top of the file, after the imports, add the path to extensions directory.

    ..  code-block:: python

        sys.path.insert(0, os.path.abspath('<path to theme>/sphinx_scylla_theme/extensions'))

#.  Update the list of extensions:

    ..  code-block:: python

        extensions = [
            # ...
            'topic-box',
            'panel-box',
            ]

Now you can use the extensions in your documentation sources.
