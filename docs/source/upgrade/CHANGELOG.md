# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1] - 01 February 2022

**IMPORTANT**: For more information on how to update, see [Migrating from 1.0 to 1.1](https://sphinx-theme.scylladb.com/stable/upgrade/1-0-to-1-1).

### Added

- [#323](https://github.com/scylladb/sphinx-scylladb-theme/pull/323): The theme includes a new directive to collapse long content and redundant information.
- [#300](https://github.com/scylladb/sphinx-scylladb-theme/pull/300) : Support for Sphinx 4.x.
- [#263](https://github.com/scylladb/sphinx-scylladb-theme/pull/263): We use dependabot to receive automatic notifications when there are new dependency updates.
- [#229](https://github.com/scylladb/sphinx-scylladb-theme/issues/229): New file-wide metadata options.

## Updated

- [#263](https://github.com/scylladb/sphinx-scylladb-theme/pull/263): Update JavaScript and Python dependencies to the latest version.
- [#307](https://github.com/scylladb/sphinx-scylladb-theme/issues/307): Before, poetry was installed as a dependency. From this release, you must install Poetry as a prerequisite.

### Fixed

- [#301](https://github.com/scylladb/sphinx-scylladb-theme/pull/301): Tables with headings were not styled.
- [#309](https://github.com/scylladb/sphinx-scylladb-theme/pull/309): Expertrec added a new component for projects in the search box page. We have re-styled the page to match the theme's look and feel.

## [1.0.6] - 08 December 2021

### Added

- [#187](https://github.com/scylladb/sphinx-scylladb-theme/issues/187): When a reader clicks on an image that has been resized, this now opens in full width.
- [#193](https://github.com/scylladb/sphinx-scylladb-theme/issues/193): We've added a button to hide the sidebar. With this feature, our readers can read the documentation with fewer distractions.

### Changed

- [#206](https://github.com/scylladb/sphinx-scylladb-theme/issues/206): We've updated jQuery dependency to 3.6.0.
- [#246](https://github.com/scylladb/sphinx-scylladb-theme/pull/246): The contribute button is more noticeable.
- [#247](https://github.com/scylladb/sphinx-scylladb-theme/issues/247): The sidebar's dropdown icons sport a new design.
- [#245](https://github.com/scylladb/sphinx-scylladb-theme/pull/245): The panel box component sports a new design.
- [#252](https://github.com/scylladb/sphinx-scylladb-theme/issues/252): We've reviewed the warning that appears when the user is not reading the latest stable version of the documentation. Now, the warning also considers branches that are still under active development.
- [#259](https://github.com/scylladb/sphinx-scylladb-theme/issues/259): The sidebar's scrollbar is now thinner and in line with the new design.

## [1.0.5] - 27 October 2021

### Added

- [#213](https://github.com/scylladb/sphinx-scylladb-theme/pull/213): We've added guides to help Scylla developers to migrate to Scylla Sphinx Theme 1.0 and 1.1.
- [#236](https://github.com/scylladb/sphinx-scylladb-theme/pull/236): Added documentation to install the toolchain for Windows users.

### Changed

- [#214](https://github.com/scylladb/sphinx-scylladb-theme/pull/214): Breadcrumbs now highlight the project's name. With this change, readers will know which documentation site they are navigating.
- [#231](https://github.com/scylladb/sphinx-scylladb-theme/pull/231): All external links include an external link icon, and they now open on a new page.
- [#240](https://github.com/scylladb/sphinx-scylladb-theme/pull/240): We've removed transparency from the home page mascot.

### Fixed

- [#214](https://github.com/scylladb/sphinx-scylladb-theme/pull/214): Breadcrumbs links to internal pages were not working.

## [1.0] - 01 September 2021

**IMPORTANT**: For more information on how to update, see [Migrating from 0.x to 1.0](https://sphinx-theme.scylladb.com/stable/upgrade/0-x-to-1-0).

### Added

- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): We’ve made a number of updates to the look and feel of the theme to improve the overall user experience.
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): The static front end files (CSS, JS, and images) are now managed with `webpack`. For more information, see [Contribute to the Theme](https://sphinx-theme.scylladb.com/stable/contribute/contribute-theme.html).
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): The promo banner now supports icons with the option theme option `banner_icon_path`. For more information, see [Template Options](https://sphinx-theme.scylladb.com/stable/configuration/template.html).
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): The contribute button adds the option "Edit on GitHub". To configure your project to support this option, read [Template Options](https://sphinx-theme.scylladb.com/stable/configuration/template.html).
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): We run hooks on every commit to automatically point out linting issues.
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): The new workflow `docs-pr` runs on pull requests to make sure docs build without warnings before being merged. For more information, see [Deployment](https://sphinx-theme.scylladb.com/stable/deployment/production.html).

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

[1.1]: https://github.com/scylladb/sphinx-scylladb-theme/compare/1.0.6...1.1.0
[1.0.6]: https://github.com/scylladb/sphinx-scylladb-theme/compare/1.0.5...1.0.6
[1.0.5]: https://github.com/scylladb/sphinx-scylladb-theme/compare/1.0.4...1.0.5
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
