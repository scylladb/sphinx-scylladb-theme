# Markdown support

The theme supports writing documents in Markdown thanks to the extension [recommonmark](https://github.com/readthedocs/recommonmark).

## Installation

See [recommonmark docs](https://recommonmark.readthedocs.io/en/latest/).

## Cheatsheet

For Markdown syntax reference, you can use this [Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet>).

## Using directives in Markdown

Recommonmark lets you use restructuredText directives with the `eval_rst` code block. Here's an example:

````rst
    ```eval_rst
    .. autoclass:: recommonmark.transform.AutoStructify
        :show-inheritance:
    ```
````
