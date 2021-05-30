# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.23] - 22 Apr 2021

### Removed

- Top-bar for Scylla University live (#152)

## [0.1.22] - 14 Apr 2021

### Added

- Top-bar for Scylla University live (#152)
- Contribution guidelines (#146)
- `*-substring_removed` settings in `conf` overrides part of the version name in the multiversion dropdown. (#110)

### Fixed

- Create intermediate directories for redirections (#153)

## [0.1.21] - 24 Jan 2021

### Added

- `smv_rename_latest_version` setting in `conf.py` overrides the latest version output directory (#121).

### Changed

- Moved `smv_latest_version` from `github/workflows/pages.yaml` to `conf.py` (#121).

### Removed

- `_utils/redirects.sh` file (#121).

### Fixed

- `make multiversionpreview` redirects automatically to the latest version (#121).

## [0.1.20] - 19 Jan 2021

### Added

- Unstable version warning (#111).

### Changed

- Disable Scylla Summit banner (#106).
- Documentation moved to docs folder (#108).

## [0.1.19] - 07 Jan 2021

### Added

- Sphinx and theme version in the footer (#98).

### Changed

- Show multiversion label always (#100).

### Fixed

- Report button when title has inlines (#103).

## [0.1.18] - 31 Dec 2020

### Added

- Custom domain support for multiversion builds (#95).
- make multiversionpreview command (#92).
- Stable tag (#89).

## [0.1.16] - 24 Nov 2020

### Added

- Add Scylla Summit Banner (#84).

### Changed

- Update copyright year automatically (#83).

### Fixed

- Warning when not reading the latest version (#78).

## [0.1.15] - 17 Nov 2020

### Added

- Warning when not reading the latest version (#78).

## [0.1.14] - 28 Oct 2020

### Changed

- Overwrites the Sphinx classification for external and internal links (#72).
- Description configurable per project (#71).

## [0.1.13] - 20 Oct 2020

### Added

- External links and download links are now followed by an icon (#65).
- Code blocks can now include substitutions (#53).

### Changed

- The 404 page sports a new design (#64)

### Fixed

- Redirections on multiversion builds were not working properly with GitHub Pages (#69)

### Removed

- pipx dependency (#68)

## [0.1.12] - 01 Oct 2020

### Added

- The 404 page is now loaded from the theme (#58, #59)
- The redirection scripts are now part of the theme (#58)

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
