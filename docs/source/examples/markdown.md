# Markdown Support

The theme supports writing documents in MarkDown thanks to the extension [recommonmark](https://github.com/readthedocs/recommonmark).

## MarkDown Cheatsheet

For Markdown syntax reference, you can use this [Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet>).

## Using directives in MarkDown

You can use all restructuredText directives with the `eval_rst` code block. Here's an example:

````rst
    ```eval_rst
    .. autoclass:: recommonmark.transform.AutoStructify
        :show-inheritance:
    ```
````
