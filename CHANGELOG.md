# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0] - 01 September 2021

### Added

- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): We’ve made a number of updates to the look and feel of the theme to improve the overall user experience.
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): The static front end files (CSS, JS, and images) are now managed with `webpack`. For more information, see [Contribute to the Theme](https://sphinx-theme.scylladb.com/stable/contribute/contribute-theme.html).
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): The promo banner now supports icons with the option theme option `banner_icon_path`. For more information, see [Template Options](https://sphinx-theme.scylladb.com/stable/configuration/template.html).
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): The contribute button adds the option "Edit on GitHub". To configure your project to support this option, read [Template Options](https://sphinx-theme.scylladb.com/stable/configuration/template.html).
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): We run hooks on every commit to automatically point out linting issues.
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): The new workflow `docs-pr` runs on pull requests to make sure docs build without warnings before being merged. For more information, see [Deployment](https://sphinx-theme.scylladb.com/stable/github-pages.html).

### Changed

- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): Topics boxes (cards) can be used in other sections, and not just on the home page. We now have different layouts to suit most projects' needs. Check them out at [Topic Boxes](https://sphinx-theme.scylladb.com/stable/examples/topic-box)

### Fixed

- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): We've added more unit tests to the project, especially to extensions.
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): We've fixed JavaScript warnings and errors raised by the console.

## [0.1.25] - 05 July 2021

### Fixed

- [#194](https://github.com/scylladb/sphinx-scylladb-theme/pull/194): FontAwesome 5.0 backwards compatibility.

## [0.1.24] - 17 June 2021

### Added

- [#180](https://github.com/scylladb/sphinx-scylladb-theme/issues/180): Now projects can configure promotional banners.
- [#179](https://github.com/scylladb/sphinx-scylladb-theme/issues/179): Troubleshooting guides for multiversion.
- [#173](https://github.com/scylladb/sphinx-scylladb-theme/issues/173): Dropdown for Contributors with the options to "Report an Issue" and "Learn How to Contribute".
- [#170](https://github.com/scylladb/sphinx-scylladb-theme/issues/170): Option to hide versions from the multiversion dropdown.
- [#174](https://github.com/scylladb/sphinx-scylladb-theme/issues/174): Shared substitutions for all projects.

### Fixed

- [#171](https://github.com/scylladb/sphinx-scylladb-theme/issues/171): Branches name were rendered in ASC order.

### Removed

- [#173](https://github.com/scylladb/sphinx-scylladb-theme/issues/179): Report an issue button from footer.

## [0.1.23] - 22 Apr 2021

### Removed

- [#152](https://github.com/scylladb/sphinx-scylladb-theme/issues/152): Top-bar for Scylla University live.

## [0.1.22] - 14 Apr 2021

### Added

- [#152](https://github.com/scylladb/sphinx-scylladb-theme/issues/152): Top-bar for Scylla University live.
- [#146](https://github.com/scylladb/sphinx-scylladb-theme/issues/146): Guidelines for project maintainers.
- [#110](https://github.com/scylladb/sphinx-scylladb-theme/issues/110): Theme option to override part of the version name in the multiversion dropdown.

### Fixed

- [#153](https://github.com/scylladb/sphinx-scylladb-theme/issues/153): Create intermediate directories for redirections.

## [0.1.21] - 24 Jan 2021

### Added

- [#121](https://github.com/scylladb/sphinx-scylladb-theme/issues/121): `smv_rename_latest_version` setting in `conf.py` overrides the latest version output directory.

### Changed

- [#121](https://github.com/scylladb/sphinx-scylladb-theme/issues/121): Moved `smv_latest_version` from `github/workflows/pages.yml` to `conf.py`.

### Removed

- [#121](https://github.com/scylladb/sphinx-scylladb-theme/issues/121): `_utils/redirects.sh` script.

### Fixed

- [#121](https://github.com/scylladb/sphinx-scylladb-theme/issues/121): `make multiversionpreview` was not redirecting automatically to the latest version.

## [0.1.20] - 19 Jan 2021

### Added

- [#111](https://github.com/scylladb/sphinx-scylladb-theme/issues/111): Show a warning if the latest version is not stable.

### Changed

- [#106](https://github.com/scylladb/sphinx-scylladb-theme/issues/106): Disable Scylla Summit banner (#106).
- [#108](https://github.com/scylladb/sphinx-scylladb-theme/issues/108): Documentation of the project moved under docs folder.

## [0.1.19] - 07 Jan 2021

### Added

- [#98](https://github.com/scylladb/sphinx-scylladb-theme/issues/98): Show Sphinx & Theme version in the footer.

### Changed

- [#100](https://github.com/scylladb/sphinx-scylladb-theme/issues/100): Show the multiversion label when there is only one version.

### Fixed

- [#103](https://github.com/scylladb/sphinx-scylladb-theme/issues/103): Report button does not break when the page title has inlines.

## [0.1.18] - 31 Dec 2020

### Added

- [#84](https://github.com/scylladb/sphinx-scylladb-theme/issues/84): Banner for Scylla Summit.
- [#95](https://github.com/scylladb/sphinx-scylladb-theme/issues/95): Support for custom domain.
- [#92](https://github.com/scylladb/sphinx-scylladb-theme/issues/92): Command to preview multiversion build.
- [#89](https://github.com/scylladb/sphinx-scylladb-theme/issues/89): Rename the latest version URL automatically to stable.

## [0.1.16] - 24 Nov 2020

### Added

- [#84](https://github.com/scylladb/sphinx-scylladb-theme/issues/84): Banner for Scylla Summit.

### Changed

- [#83](https://github.com/scylladb/sphinx-scylladb-theme/issues/83): Copyright year in the footer is now updated automatically.

## [0.1.15] - 17 Nov 2020

### Added

- [#78](https://github.com/scylladb/sphinx-scylladb-theme/issues/78): Show a warning when the user is not reading not reading the latest version.

## [0.1.14] - 28 Oct 2020

### Changed

- [#72](https://github.com/scylladb/sphinx-scylladb-theme/issues/72): Overwrite the Sphinx classification for external and internal links.
- [#71](https://github.com/scylladb/sphinx-scylladb-theme/issues/71): Site description is now configurable per project.

## [0.1.13] - 20 Oct 2020

### Added

- [#65](https://github.com/scylladb/sphinx-scylladb-theme/issues/65): External links and download links are now followed by an icon.
- [#53](https://github.com/scylladb/sphinx-scylladb-theme/issues/53): Now code blocks can include substitutions.

### Changed

- [#64](https://github.com/scylladb/sphinx-scylladb-theme/issues/64): The 404 page sports a new design.

### Fixed

- [#69](https://github.com/scylladb/sphinx-scylladb-theme/issues/69): Redirections on multiversion builds were not working

### Removed

- [#68](https://github.com/scylladb/sphinx-scylladb-theme/issues/68): PIPX dependency.

## [0.1.12] - 01 Oct 2020

### Added

- [#59](https://github.com/scylladb/sphinx-scylladb-theme/issues/59): All projects now share a 404 page.
- [#58](https://github.com/scylladb/sphinx-scylladb-theme/issues/58): Support for redirections.

[1.0]: https://github.com/scylladb/sphinx-scylladb-theme/compare/0.1.25...1.0.4
[0.1.25]: https://github.com/scylladb/sphinx-scylladb-theme/compare/0.1.24...0.1.25
[0.1.24]: https://github.com/scylladb/sphinx-scylladb-theme/compare/0.1.23...0.1.24
[0.1.23]: https://github.com/scylladb/sphinx-scylladb-theme/compare/0.1.22...0.1.23
[0.1.22]: https://github.com/scylladb/sphinx-scylladb-theme/compare/0.1.21...0.1.22
[0.1.21]: https://github.com/scylladb/sphinx-scylladb-theme/compare/0.1.20...0.1.21
[0.1.20]: https://github.com/scylladb/sphinx-scylladb-theme/compare/0.1.19...0.1.20
[0.1.19]: https://github.com/scylladb/sphinx-scylladb-theme/compare/0.1.18...0.1.19
[0.1.18]: https://github.com/scylladb/sphinx-scylladb-theme/compare/0.1.16...0.1.18
[0.1.16]: https://github.com/scylladb/sphinx-scylladb-theme/compare/0.1.15...0.1.16
[0.1.15]: https://github.com/scylladb/sphinx-scylladb-theme/compare/0.1.14...0.1.15
[0.1.14]: https://github.com/scylladb/sphinx-scylladb-theme/compare/0.1.13...0.1.14
[0.1.13]: https://github.com/scylladb/sphinx-scylladb-theme/compare/0.1.12...0.1.13
[0.1.12]: https://github.com/scylladb/sphinx-scylladb-theme/releases/tag/0.1.12
