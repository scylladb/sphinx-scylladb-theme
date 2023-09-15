# sphinx-multiversion

Fork of https://github.com/Holzhaus/sphinx-multiversion for the ScyllaDB Project.

Sphinx extension for building self-hosted versioned docs.

Original documentation can be found at: https://holzhaus.github.io/sphinx-multiversion/

## Fork additions

### Prebuild and postbuild commands

The fork introduces the possibility to run custom commands before and after building the docs with the option `--pre-build` and `--post-build`.

This could be useful to prepare the docs repository before running `sphinx-build`, debug the execution, or even generate versioned documentation using other builders.

For example, imagine that you want to build versioned docs written in Sphinx, but the API reference is generated with JavaDoc. This option enables the generation of both versioned docs to host them under the same folder using GitHub Pages.

Here's an example showing the directory where the build command is running:

```
sphinx-multiversion docs build/html --pre-build pw
```

You can pass multiple commands by adding extra `--pre-build` or `--post-build` options. The commands run in order, from left to right:

```
sphinx-multiversion docs build/html --pre-build pwd --pre-build ls --post-build "cat file.txt"
```

### Rename latest version URL

The `smv_latest_version` setting determines which is the latest version.
Setting this option could be useful to show a warning when users are not reading the latest version.

You can override the latest version output directory with `smv_rename_latest_version`.

Here's an example:

```
smv_latest_version = 'x.y.z'         # Use the branch/tag name
smv_rename_latest_version = 'latest' # Use the commit hash
```

### Add support for custom tags

See https://github.com/dgarcia360/sphinx-multiversion/pull/4

### Fix Git LFS error

See https://github.com/scylladb/scylla-enterprise/issues/3414


## Maintenance

This fork will be maintained until the following issues are solved:

- https://github.com/Holzhaus/sphinx-multiversion/issues/45
- https://github.com/Holzhaus/sphinx-multiversion/issues/65

## License

BSD 2-Clause License

Copyright (c) 2020, Jan Holthuis <jan.holthuis@ruhr-uni-bochum.de>
All rights reserved.

Modifications (see "Fork Additions") 2020, David Garcia <hi@davidgarcia.dev>
