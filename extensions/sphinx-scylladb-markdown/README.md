# sphinx-scylladb-markdown

The Sphinx ScyllaDB Markdown Extension is specifically designed for projects using [sphinx-multiversion](https://github.com/Holzhaus/sphinx-multiversion). It facilitates a smooth transition from recommonmark to MystParser in Sphinx documentation. 

This extension is particularly useful in scenarios where older documentation versions require recommonmark, which is now [deprecated](https://recommonmark.readthedocs.io/en/latest/), while newer versions can leverage the advanced features of MystParser.

## Installation

To install the Sphinx ScyllaDB Markdown Extension, follow these steps:

1. Run the following command within your Sphinx project directory:

    ```bash
    pip install sphinx-scylladb-markdown
    ```

1. Add the following lines to your ``conf.py`` file in your Sphinx project:

    ```bash
    extensions = [
        ...
        'sphinx_scylladb_markdown',
        ...
    ]
    ```

1. Set the ``scylladb_markdown_enable`` in your ``conf.py``:

    ```python
    scylladb_markdown_enable = True
    ```

1. Optional: If you want to use recommonmark for specific versions, list them in ``scylladb_markdown_recommonmark_versions`` in your `conf.py` file:

    ```python
    scylladb_markdown_recommonmark_versions = ['v1.0', 'v1.1']
    ```

## License

Copyright (c) 2023-present ScyllaDB Licensed under the `Apache License 2.0 <LICENSE>`_.
