# Markdown support

The docs toolchain supports writing documents in Markdown with the help of two extensions: MyST and recommonmark.

For new projects, we recommend using the MyST due to its more extensive features and robust support. However, recommonmark will still be supported for those projects which have yet to migrate.

## MyST parser

### Installation

To install MyST:

1. Install the extension:

   ```console
   poetry add myst-parser
   ```

2. Load the extension in the `conf.py` configuration file:

   ```python
   extensions = ["myst_parser"]
   ```

3. Add the following configuration in the `conf.py` to enable the `colon_fence` extension:

   ```python
   myst_enable_extensions = ["colon_fence"]
   ```

For more details, see the [MyST documentation](https://myst-parser.readthedocs.io/en/latest/intro.html#/).

### Usage

MyST extends the [CommonMark syntax](https://spec.commonmark.org/) specification. For more details, see the [Authoring](https://myst-parser.readthedocs.io/en/latest/syntax/typography.html) section of the MyST documentation.

Additionally, it provides specific support for Sphinx roles and directives. For more details, see the [Roles and directives](https://myst-parser.readthedocs.io/en/latest/syntax/roles-and-directives.html#roles-directives) section of the MyST documentation.

## recommonmark parser

:::{caution}
This extension is deprecated and will be removed in a future release. If you are setting up a new project, we recommend using the MyST parser instead.
:::

See [recommonmark docs](https://recommonmark.readthedocs.io/en/latest/) for more details on how to install and use this parser.
