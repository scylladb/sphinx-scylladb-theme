# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## 1.8.10 - 3 December 2025

### Fixed

- [#1541](https://github.com/scylladb/sphinx-scylladb-theme/pull/1541): Fixed breadcrumbs and hero content being hidden behind the fixed header on mobile when the promo banner is disabled.


## 1.8.9 - 21 November 2025

### Added

- [#1516](https://github.com/scylladb/sphinx-scylladb-theme/pull/1516): Added styling for API reference documentation, including Python autodoc, Doxygen/Breathe, and REST API documentation.
- [#1516](https://github.com/scylladb/sphinx-scylladb-theme/pull/1516): Added support for three navigation levels in the right sidebar with options to control depth per page and project.
- [#1507](https://github.com/scylladb/sphinx-scylladb-theme/pull/1507): Added documentation example for embedding videos in documentation pages.

### Updated

- [#1513](https://github.com/scylladb/sphinx-scylladb-theme/issues/1513): Updated driver links in the header navigation.

### Fixed

- [#1498](https://github.com/scylladb/sphinx-scylladb-theme/pull/1498): Fixed announcement banner display issues on mobile devices.

## 1.8.8 - 2 September 2025

### Added

- [#1485](https://github.com/scylladb/sphinx-scylladb-theme/pull/1485): Added Ask AI button in the header and hero box component for easier access to AI-powered documentation assistance.
- [#1476](https://github.com/scylladb/sphinx-scylladb-theme/pull/1476): Introduced support for defining MyST substitutions per version in multiversion builds.

### Updated

- [#1463](https://github.com/scylladb/sphinx-scylladb-theme/pull/1463): Updated download link in the header navigation.

### Fixed

- [#1458](https://github.com/scylladb/sphinx-scylladb-theme/pull/1458): Fixed highlight color rendering issues in dark mode.


## 1.8.7 - 1 July 2025

### Added

- [89315d4](https://github.com/scylladb/sphinx-scylladb-theme/commit/89315d4483559a1423d8fb33ad75b885a1df1bad): Introduced a new `grid` directive for flexible page layouts.
- [#1443](https://github.com/scylladb/sphinx-scylladb-theme/pull/1443): Added support for additional icons.
- [#1452](https://github.com/scylladb/sphinx-scylladb-theme/pull/1452): Enabled the Ask AI bot by default across all documentation projects.

### Updated

- [89315](https://github.com/scylladb/sphinx-scylladb-theme/commit/89315d4483559a1423d8fb33ad75b885a1df1bad): Improved support for cards, making them available on inner pages.
- [#1442](https://github.com/scylladb/sphinx-scylladb-theme/pull/1442): Updated navbar links to direct users to the latest manual documentation.
- [#1441](https://github.com/scylladb/sphinx-scylladb-theme/pull/1441): Restyled the left sidebar to better identify nested elements.

### Fixed

- [#1428](https://github.com/scylladb/sphinx-scylladb-theme/pull/1428): Restored the ability to retain scroll position when reloading or navigating between pages.
- [#1417](https://github.com/scylladb/sphinx-scylladb-theme/pull/1417): Fixed code line highlighting in dark mode.
- [cd88d37](https://github.com/scylladb/sphinx-scylladb-theme/commit/cd88d37ef43bb657ce32d5020eeb3df69919ec0c): Removed unnecessary scroll behavior from search results.

## 1.8.6 - 1 Apr 2025

### Added

- [#1354](https://github.com/scylladb/sphinx-scylladb-theme/pull/1354): Integrated an AI-powered chatbot to assist users with documentation queries.

### Updated

- [#1379](https://github.com/scylladb/sphinx-scylladb-theme/pull/1379): Updated server link in the header to point to `docs.scylladb.com/manual`.
- [#1368](https://github.com/scylladb/sphinx-scylladb-theme/pull/1368): Added a link to tutorials in the footer and updated the privacy policy disclaimer.

### Fixed

- [#1361](https://github.com/scylladb/sphinx-scylladb-theme/pull/1361): Adjusted hero box spacing on mobile for projects using a landing page.
- [#1369](https://github.com/scylladb/sphinx-scylladb-theme/pull/1369): Fixed an issue with copying anchor links on nested pages.

## 1.8.5 - 17 Jan 2025

### Fixed

- [#1336](https://github.com/scylladb/sphinx-scylladb-theme/pull/1336): Fixed an issue where the sidebar menu overlapped the project title.

## 1.8.4 - 17 Jan 2025

### Added

- [#1277](https://github.com/scylladb/sphinx-scylladb-theme/pull/1289): Added a troubleshooting note for users encountering issues with keyring and Poetry.
- [#1302](https://github.com/scylladb/sphinx-scylladb-theme/pull/1302): Introduced Mermaid.js support for rendering diagrams from text.
- [#1303](https://github.com/scylladb/sphinx-scylladb-theme/pull/1303): Implemented a helper to fetch multiversion data from a remote URL.
- [#1314](https://github.com/scylladb/sphinx-scylladb-theme/pull/1314): Updated the user interface, including the homepage, sidebars, and breadcrumbs.
- [#1316](https://github.com/scylladb/sphinx-scylladb-theme/pull/1316): Added a license banner to announce changes to ScyllaDB’s licensing and versioning policy.
- [#1316](https://github.com/scylladb/sphinx-scylladb-theme/pull/1316): Added an option to copy the anchor link when hovering over a heading.
- [#1330](https://github.com/scylladb/sphinx-scylladb-theme/pull/1329): Added an option to override the multiversion redirect for the main domain, enabling redirection of `docs.scylladb.com/manual` to `docs.scylladb.com/manual/stable` instead of `docs.scylladb.com/stable`.

### Fixed

- [#1330](https://github.com/scylladb/sphinx-scylladb-theme/pull/1330): Resolved an issue with the alert banner position.

## 1.8.3 - 25 Oct 2024

### Added

- [#1277](https://github.com/scylladb/sphinx-scylladb-theme/pull/1277): Documentation on Dependabot support, explaining configuration, update frequency, and handling vulnerability alerts.

### Fixed

- [#1277](https://github.com/scylladb/sphinx-scylladb-theme/pull/1277): Updated cookie configuration to ensure cookies are available across all `.scylladb.com` subdomains.
- [#1277](https://github.com/scylladb/sphinx-scylladb-theme/pull/1277): Corrected Dependabot ignore property that was unintentionally excluding all dependencies, now allowing only specified dependencies to receive updates.

## 1.8.2 - 22 Oct 2024

### Added

- [#1257](https://github.com/scylladb/sphinx-scylladb-theme/pull/1257): The theme now respects browser and system preferences for dark mode by default.

### Updated

- [#1257](https://github.com/scylladb/sphinx-scylladb-theme/pull/1257): Switched from localStorage to cache for storing settings such as dark mode and announcement preferences. This allows for shared preferences across projects.

### Fixed

- [#1246](https://github.com/scylladb/sphinx-scylladb-theme/pull/1246): Tooltips now correctly render glossary entries without relying on whether the glossary file was pre-loaded by Sphinx.
- [#1260](https://github.com/scylladb/sphinx-scylladb-theme/pull/1260): Fixed a brief flash of light mode when navigating between pages in dark mode.
- [#1258](https://github.com/scylladb/sphinx-scylladb-theme/pull/1258): Styled legacy panel boxes defined inside raw HTML directives to display correctly in dark mode.

### Removed

- [#1267](https://github.com/scylladb/sphinx-scylladb-theme/pull/1267): Removed the previous icon library.
- [#1266](https://github.com/scylladb/sphinx-scylladb-theme/pull/1266): Completely dropped Font Awesome support, removed the latest icons, and cleaned up the dependency.


## 1.8.1 - 24 Sept 2024

### Added

- [#1163](https://github.com/scylladb/sphinx-scylladb-theme/pull/1163): Introduced a new component to display tooltips in the documentation. This feature supports both glossary entries and custom text.
- [#1180](https://github.com/scylladb/sphinx-scylladb-theme/pull/1180): Documented how to create links to configuration parameters.
- [#1210](https://github.com/scylladb/sphinx-scylladb-theme/pull/1210): Added dark theme support.
- [#1210](https://github.com/scylladb/sphinx-scylladb-theme/pull/1210): Introduced a new custom library for icons.

### Updated

- [#1175](https://github.com/scylladb/sphinx-scylladb-theme/pull/1175): Adjusted script loading order so that Google Tag Manager scripts load before generic scripts.
- [#1186](https://github.com/scylladb/sphinx-scylladb-theme/pull/1186): Recommend including the poetry lock file in the repository to ensure consistent dependencies are installed in the CI/CD pipeline.
- [#1190](https://github.com/scylladb/sphinx-scylladb-theme/pull/1190): Updated the ScyllaDB logo and mascots.

### Fixed

- [#1206](https://github.com/scylladb/sphinx-scylladb-theme/pull/1206): Pinned `sphinx-autobuild` version to avoid a known issue.

### Removed

- [#1189](https://github.com/scylladb/sphinx-scylladb-theme/pull/1189): Removed the newsletter from the footer.

- [#1217](https://github.com/scylladb/sphinx-scylladb-theme/pull/1217): Dropped Font Awesome libary support for icons.

## 1.7.4 - 30 Jul 2024

### Fixed

- [#1157](https://github.com/scylladb/sphinx-scylladb-theme/pull/1157) Set `sphinx-notfound-page` to `0.1.2` to fix the issue raised by the latest version of the extension. More details in https://github.com/readthedocs/sphinx-notfound-page/issues/240

## 1.7.3 - 25 Jun 2024

### Updated

- [#1123](https://github.com/scylladb/sphinx-scylladb-theme/pull/1123): Compatibility with Python 3.12.
- [#1123](https://github.com/scylladb/sphinx-scylladb-theme/pull/1123): Replaced Flake8 with Ruff for faster code linting.

### Removed

- [#1123](https://github.com/scylladb/sphinx-scylladb-theme/pull/1123): Deprecate Prettier for code linting (pre-commit).

## 1.7.2 - 30 Apr 2024

### Added

- [#1093](https://github.com/scylladb/sphinx-scylladb-theme/pull/1093): Option to override the "Create an issue" label per project.

### Fixed

- [#1092](https://github.com/scylladb/sphinx-scylladb-theme/pull/1092): Right sidebar scroll highlighting.


## 1.7.1 - 12 Apr 2024

### Added

- [#1023](https://github.com/scylladb/sphinx-scylladb-theme/pull/1023): Added functionality to trigger documentation publications when updates are made to previous versions.
- [#1058](https://github.com/scylladb/sphinx-scylladb-theme/pull/1058): Added new button styles to the hero box.
- [#1059](https://github.com/scylladb/sphinx-scylladb-theme/pull/1059): Introduced an option to open topic boxes in the same tab.
- [#1069](https://github.com/scylladb/sphinx-scylladb-theme/pull/1069): Adds the option to exclude ``doctools.js`` per page to make the theme compatible with Swagger UI.

### Updated

- [#972](https://github.com/scylladb/sphinx-scylladb-theme/commit/9dffad3eff41caadec25de0649abcaf5ad811027): Updated configuration to set `myst_heading_anchors` to 6 for compatibility purposes.
- [#1036](https://github.com/scylladb/sphinx-scylladb-theme/pull/1036): Made the project name in the sidebar clickable, enhancing navigation.
- [#1051](https://github.com/scylladb/sphinx-scylladb-theme/pull/1051): Improved the sidebar functionality to auto-scroll to the current page.

### Fixed

- [#1051](https://github.com/scylladb/sphinx-scylladb-theme/pull/1051): Adjusted the sidebar height to prevent the footer from overlapping

### Removed

- [#1053](https://github.com/scylladb/sphinx-scylladb-theme/pull/1053): Discontinued Amplify support for page previews in favor of a custom Jenkins pipeline.

## 1.6.6 - 5 Jan 2024

### Updated

- [#949](https://github.com/scylladb/sphinx-scylladb-theme/pull/949): Enhanced Zendesk verification tag support.

## 1.6.5 - 18 Dec 2023

### Fixed

- [#962](https://github.com/scylladb/sphinx-scylladb-theme/pull/962): `pkg_resources` is deprecated in favor of  `importlib.metadata`.

## 1.6.2 - 6 Dec 2023

### Added

- [#949](https://github.com/scylladb/sphinx-scylladb-theme/pull/949): Separated global scripts from local scripts, allowing for customization of tags and scripts at the individual project level.

## 1.6.1 - 10 Oct 2023

### Added

- [#891](https://github.com/scylladb/sphinx-scylladb-theme/pull/891): Introduced parallel builds for enhanced performance.
- [#890](https://github.com/scylladb/sphinx-scylladb-theme/pull/890): Implemented support for repositories utilizing Git Large File Storage (LFS).

### Updated

- [#891](https://github.com/scylladb/sphinx-scylladb-theme/pull/891): Upgraded to Sphinx 7.2.4, requiring Python 3.9 or higher for compatibility.
- [#867](https://github.com/scylladb/sphinx-scylladb-theme/pull/867): Updated the header link to direct users to the most current open-source documentation site.
- [#827](https://github.com/scylladb/sphinx-scylladb-theme/pull/827): Enhanced the guide on building multiversioned documentation locally.

### Fixed

- [#904](https://github.com/scylladb/sphinx-scylladb-theme/issues/904): Fixed the style of admonitions with bullet points.
- [#889](https://github.com/scylladb/sphinx-scylladb-theme/issues/889): Optimized top scroll padding, ensuring a similar behaviour across different component types.

### Removed

- [#867](https://github.com/scylladb/sphinx-scylladb-theme/pull/867): For Windows users: We have discontinued support for Git Bash, recommending users to transition to Windows Subsystem for Linux (WSL).
- [#912](https://github.com/scylladb/sphinx-scylladb-theme/pull/912): The Windows-specific variables previously found in the `docs/Makefile` have been removed. Windows users are now advised to ensure that Poetry is added to the system's PATH for seamless command execution and script running.

## 1.5.1 - 31 May 2023

### Added

- [#781](https://github.com/scylladb/sphinx-scylladb-theme/pull/781): The footer now includes an option to like or dislike the current page.
- [#803](https://github.com/scylladb/sphinx-scylladb-theme/pull/803): Promote the use of MyST parser instead of recommonmark for new projects.
- [#764](https://github.com/scylladb/sphinx-scylladb-theme/pull/764): The footer now links to ScyllaDB University.

### Updated

- [#802](https://github.com/scylladb/sphinx-scylladb-theme/pull/802): Upgraded certain icons to a higher resolution.
- [#803](https://github.com/scylladb/sphinx-scylladb-theme/pull/803): The deployment process documentation was updated to use GitHub Actions.

### Fixed

- [#775](https://github.com/scylladb/sphinx-scylladb-theme/pull/775): The sitemap links were not working properly.

## 1.4.3 - 04 April 2023

### Added

- [#741](https://github.com/scylladb/sphinx-scylladb-theme/pull/741): Option to skip custom theme warnings.

### Updated

- Add specific Google Tag Manager ID for the Scylla docs.

## 1.4.1 - 13 March 2023

**IMPORTANT**: For more information on how to update, see [Migrating from 1.3 to 1.4](https://sphinx-theme.scylladb.com/stable/upgrade/1-3-to-1-4.html).

### Added

- [#652](https://github.com/scylladb/sphinx-scylladb-theme/pull/652): The docs builds now raises a warning if a RST or MD file has underscores in the filename.
- [#696](https://github.com/scylladb/sphinx-scylladb-theme/pull/696): The announcement banner can be managed from Google Tag Manager.

### Fixed

- [#720](https://github.com/scylladb/sphinx-scylladb-theme/pull/720): In 1.3.5, we introduced a bug that caused some breadcrumbs to not have a link. This is now fixed.

## 1.3.5 - 24 Feb 2023

### Updated

- [#694](https://github.com/scylladb/sphinx-scylladb-theme/pull/694): The sidebar highlights the current project you are viewing.
- [#694](https://github.com/scylladb/sphinx-scylladb-theme/pull/694): The breadcrumbs now add a link to the root site docs.scylladb.com.
- [#694](https://github.com/scylladb/sphinx-scylladb-theme/pull/694): The navigation bar links to the new enteprise docs site.

## 1.3.4 - 13 Dec 2022

### Added

- [#646](https://github.com/scylladb/sphinx-scylladb-theme/pull/646): The footer now adds a link to the community forum.
- [#651](https://github.com/scylladb/sphinx-scylladb-theme/pull/651): The preference to keep the promotional banner closed now expires after 30 days.

### Updated

- [#643](https://github.com/scylladb/sphinx-scylladb-theme/pull/643): The "Edit this page" now opens default branch instead of the current branch of the docs you are viewing.
- [#647](https://github.com/scylladb/sphinx-scylladb-theme/pull/647): Change "Scylla" occurrences to "ScyllaDB".
- [#649](https://github.com/scylladb/sphinx-scylladb-theme/pull/649): Remove the Scylla Cloud app from the header. Now the header only points to the Scylla Cloud docs.

## 1.3.3 - 29 Nov 2022

### Added

- [#661](https://github.com/scylladb/sphinx-scylladb-theme/pull/611): Maintainers can now add custom text after the content. This is useful for projects requiring a license notice on every documentation page.

### Fixed

- [#624](https://github.com/scylladb/sphinx-scylladb-theme/pull/624): Label roles are now hidden on the right sidebar.

## 1.3.2 - 28 Oct 2022

### Added

- [#590](https://github.com/scylladb/sphinx-scylladb-theme/pull/590): Create a new "label" role to differenciate between enterprise and open-source features.
- [#599](https://github.com/scylladb/sphinx-scylladb-theme/pull/599): Zendesk verification tag.

### Updated

- [#555](https://github.com/scylladb/sphinx-scylladb-theme/pull/555): Now the multiversion extension is mantained on this repository.
- dependabot: We've updated all the JavaScript and Python dependencies to the latest version.

### Removed

- [#556]: Removed the `_utils/deploy.sh` script. Now the logic to deploy the docs is in the GitHub Actions workflow.

## 1.3.1 - 19 Aug 2022

**IMPORTANT**: For more information on how to update, see [Migrating from 1.2 to 1.3](https://sphinx-theme.scylladb.com/stable/upgrade/1-2-to-1-3.html).

### Added

- [#525](https://github.com/scylladb/sphinx-scylladb-theme/issues/525): When a user clicks on **Create an issue** button, the issue is now created with the prefix `docs:` and the label `documentation`.
- [#531](https://github.com/scylladb/sphinx-scylladb-theme/pull/531): Adds instructions to trigger pull requests previews with Amplify only when there are updates within the `docs` folder.
- We added a quickstart guide to create your first documentation page, list it in the table of contents, and preview the site locally.
- [#551](https://github.com/scylladb/sphinx-scylladb-theme/pull/551): Adds an option to hide the multiversion selector for projects for projects that only build one version.

### Changed

- [#509](https://github.com/scylladb/sphinx-scylladb-theme/pull/509): We redesigned the home page search box to make it more visible.
- [#515](https://github.com/scylladb/sphinx-scylladb-theme/pull/515): Before, redirects were part of the theme. This means that, for every version, the same redirects were being created, giving us little control if we wanted to redirect a page from the previous version to a different URL. Now, we are using a separate third-party package to create redirections. Also, instead of creating the same redirections for each version, we generate them at the end once the docs are built. This allows us to have better control of the redirects per version.
- [#533](https://github.com/scylladb/sphinx-scylladb-theme/pull/533): We improved the build time of docs previews by 80%.
- [#536](https://github.com/scylladb/sphinx-scylladb-theme/pull/546): The multiversion version dropdown is now always displayed, even if there is only one version.

## 1.2.2 - 17 May 2022

### Added

- [#472](https://github.com/scylladb/sphinx-scylladb-theme/pull/472): The hero box directive now can display the search box with a new option.
- [#452](https://github.com/scylladb/sphinx-scylladb-theme/pull/452): Various improvements on the search page UI.

### Changed

- [#447](https://github.com/scylladb/sphinx-scylladb-theme/pull/447): We've replaced Netlify for AWS Amplify to automatically build pull requests previews for docs.

### Fixed

- [#406](https://github.com/scylladb/sphinx-scylladb-theme/pull/406): Pages built with the `make html` builder were displaying an incorrect canonical URL.

## 1.2.1 - 29 March 2022

### Added

- [#422](https://github.com/scylladb/sphinx-scylladb-theme/pull/422): The theme generates a `sitemap.xml` by default.

### Fixed

- [#421](https://github.com/scylladb/sphinx-scylladb-theme/pull/421): Show always contribute buttons.
- [#425](https://github.com/scylladb/sphinx-scylladb-theme/pull/425): CSS for the 404 page was not loading.

## 1.2 - 22 March 2022

**IMPORTANT**: For more information on how to update, see [Migrating from 1.1 to 1.2](https://sphinx-theme.scylladb.com/stable/upgrade/1-1-to-1-2.html).

### Added

- [#379](https://github.com/scylladb/sphinx-scylladb-theme/pull/379): We've added Netlify support to automatically build pull requests previews for docs. This feature is in beta for a reduced number of projects.
- [#390](https://github.com/scylladb/sphinx-scylladb-theme/pull/390): Once a week, a GitHub Action finds for broken links in Markdown and restructuredText files. If there are broken links, the action will create a new issue in the same repository with the links that have to be fixed.
- [#401](https://github.com/scylladb/sphinx-scylladb-theme/pull/401): We've added new warning messages when previewing a non-stable version of the documentation.
- [#402](https://github.com/scylladb/sphinx-scylladb-theme/pull/402): Now, you can create landing pages with sidebars.
- [#402](https://github.com/scylladb/sphinx-scylladb-theme/pull/402): The theme includes a GitHub Action that runs the theme tests automatically when some of the theme files are edited.

### Changed

- [#359](https://github.com/scylladb/sphinx-scylladb-theme/pull/359): We've updated all the JavaScript and Python dependencies to the latest version.
- [#361](https://github.com/scylladb/sphinx-scylladb-theme/pull/361): Tables were redesigned to make them more readable.
- [#371](https://github.com/scylladb/sphinx-scylladb-theme/pull/371): We've moved the contribute buttons to the right sidebar.
- [#372](https://github.com/scylladb/sphinx-scylladb-theme/pull/372): The substitutions extension is now installed as a third-party dependency.
- [#403](https://github.com/scylladb/sphinx-scylladb-theme/pull/403): The theme does not show the multiversion dropdown in the sidebar if there is only one item.
- [#404](https://github.com/scylladb/sphinx-scylladb-theme/pull/404): Now, topic box images are hidden in responsive view.
- [#410](https://github.com/scylladb/sphinx-scylladb-theme/pull/410): We've improved the search component load time.

### Fixed

- [#357](https://github.com/scylladb/sphinx-scylladb-theme/issues/357): The copy button displayed an empty circle on hover.
- [#362](https://github.com/scylladb/sphinx-scylladb-theme/pull/362): The zoom option for images was only working with SVG images. Now, this feature is compatible with other formats such as PNG and JPG.
- [#382](https://github.com/scylladb/sphinx-scylladb-theme/pull/382): When the top bar was closed, it continued appearing for milliseconds when the page was refreshed.
- [#389](https://github.com/scylladb/sphinx-scylladb-theme/pull/389): We've increased the breadcrumbs spacing.
- [#406](https://github.com/scylladb/sphinx-scylladb-theme/pull/406): Various pages shared the same canonical URL. Now, we point to the URL of the latest stable version of the document.

## 1.1.1 - 02 February 2022

### Fixed

- [#344](https://github.com/scylladb/sphinx-scylladb-theme/pull/344): Fixes the error `TypeError: 'CQLLexer' object is not callable`.

## 1.1 - 01 February 2022

**IMPORTANT**: For more information on how to update, see [Migrating from 1.0 to 1.1](https://sphinx-theme.scylladb.com/stable/upgrade/1-0-to-1-1).

### Added

- [#323](https://github.com/scylladb/sphinx-scylladb-theme/pull/323): The theme includes a new directive to collapse long content and redundant information.
- [#300](https://github.com/scylladb/sphinx-scylladb-theme/pull/300) : Support for Sphinx 4.x.
- [#263](https://github.com/scylladb/sphinx-scylladb-theme/pull/263): We use dependabot to receive automatic notifications when there are new dependency updates.
- [#229](https://github.com/scylladb/sphinx-scylladb-theme/issues/229): New file-wide metadata options.

### Changed

- [#263](https://github.com/scylladb/sphinx-scylladb-theme/pull/263): Update JavaScript and Python dependencies to the latest version.
- [#307](https://github.com/scylladb/sphinx-scylladb-theme/issues/307): Before, poetry was installed as a dependency. From this release, you must install Poetry as a prerequisite.

### Fixed

- [#301](https://github.com/scylladb/sphinx-scylladb-theme/pull/301): Tables with headings were not styled.
- [#309](https://github.com/scylladb/sphinx-scylladb-theme/pull/309): Expertrec added a new component for projects in the search box page. We've re-styled the page to match the theme's look and feel.

## 1.0.6 - 08 December 2021

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

## 1.0.5 - 27 October 2021

### Added

- [#213](https://github.com/scylladb/sphinx-scylladb-theme/pull/213): We've added guides to help maintainers to migrate to ScyllaDB Sphinx Theme 1.0 and 1.1.
- [#236](https://github.com/scylladb/sphinx-scylladb-theme/pull/236): Added documentation to install the toolchain for Windows users.

### Changed

- [#214](https://github.com/scylladb/sphinx-scylladb-theme/pull/214): Breadcrumbs now highlight the project's name. With this change, readers will know which documentation site they are navigating.
- [#231](https://github.com/scylladb/sphinx-scylladb-theme/pull/231): All external links include an external link icon, and they now open on a new page.
- [#240](https://github.com/scylladb/sphinx-scylladb-theme/pull/240): We've removed transparency from the home page mascot.

### Fixed

- [#214](https://github.com/scylladb/sphinx-scylladb-theme/pull/214): Breadcrumbs links to internal pages were not working.

## 1.0 - 01 September 2021

**IMPORTANT**: For more information on how to update, see [Migrating from 0.x to 1.0](https://sphinx-theme.scylladb.com/stable/upgrade/0-x-to-1-0).

### Added

- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): We’ve made a number of updates to the look and feel of the theme to improve the overall user experience.
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): The static front end files (CSS, JS, and images) are now managed with `webpack`. For more information, see [Contribute to the Theme](https://sphinx-theme.scylladb.com/stable/contribute/contribute-theme.html).
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): The promo banner now supports icons with the option theme option `banner_icon_path`. For more information, see [Template Options](https://sphinx-theme.scylladb.com/stable/configuration/template.html).
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): The contribute button adds the option "Edit on GitHub". To configure your project to support this option, read [Template Options](https://sphinx-theme.scylladb.com/stable/configuration/template.html).
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): We run hooks on every commit to automatically point out linting issues.
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): The new workflow `docs-pr` runs on pull requests to make sure docs build without warnings before being merged. For more information, see [Deployment](https://sphinx-theme.scylladb.com/branch-1.0/github-pages.html).

### Changed

- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): Topics boxes (cards) can be used in other sections, and not just on the home page. We now have different layouts to suit most projects' needs. Check them out at [Topic Boxes](https://sphinx-theme.scylladb.com/stable/examples/topic-box)

### Fixed

- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): We've added more unit tests to the project, especially to extensions.
- [#201](https://github.com/scylladb/sphinx-scylladb-theme/pull/201): We've fixed JavaScript warnings and errors raised by the console.

## 0.1.25 - 05 July 2021

### Fixed

- [#194](https://github.com/scylladb/sphinx-scylladb-theme/pull/194): FontAwesome 5.0 backwards compatibility.

## 0.1.24 - 17 June 2021

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

## 0.1.23 - 22 Apr 2021

### Removed

- [#152](https://github.com/scylladb/sphinx-scylladb-theme/issues/152): Top-bar for ScyllaDB University live.

## 0.1.22 - 14 Apr 2021

### Added

- [#152](https://github.com/scylladb/sphinx-scylladb-theme/issues/152): Top-bar for ScyllaDB University live.
- [#146](https://github.com/scylladb/sphinx-scylladb-theme/issues/146): Guidelines for project maintainers.
- [#110](https://github.com/scylladb/sphinx-scylladb-theme/issues/110): Theme option to override part of the version name in the multiversion dropdown.

### Fixed

- [#153](https://github.com/scylladb/sphinx-scylladb-theme/issues/153): Create intermediate directories for redirections.

## 0.1.21 - 24 Jan 2021

### Added

- [#121](https://github.com/scylladb/sphinx-scylladb-theme/issues/121): `smv_rename_latest_version` setting in `conf.py` overrides the latest version output directory.

### Changed

- [#121](https://github.com/scylladb/sphinx-scylladb-theme/issues/121): Moved `smv_latest_version` from `github/workflows/pages.yml` to `conf.py`.

### Removed

- [#121](https://github.com/scylladb/sphinx-scylladb-theme/issues/121): `_utils/redirects.sh` script.

### Fixed

- [#121](https://github.com/scylladb/sphinx-scylladb-theme/issues/121): `make multiversionpreview` was not redirecting automatically to the latest version.

## 0.1.20 - 19 Jan 2021

### Added

- [#111](https://github.com/scylladb/sphinx-scylladb-theme/issues/111): Show a warning if the latest version is not stable.

### Changed

- [#106](https://github.com/scylladb/sphinx-scylladb-theme/issues/106): Disable ScyllaDB Summit banner (#106).
- [#108](https://github.com/scylladb/sphinx-scylladb-theme/issues/108): Documentation of the project moved under docs folder.

## 0.1.19 - 07 Jan 2021

### Added

- [#98](https://github.com/scylladb/sphinx-scylladb-theme/issues/98): Show Sphinx & Theme version in the footer.

### Changed

- [#100](https://github.com/scylladb/sphinx-scylladb-theme/issues/100): Show the multiversion label when there is only one version.

### Fixed

- [#103](https://github.com/scylladb/sphinx-scylladb-theme/issues/103): Report button does not break when the page title has inlines.

## 0.1.18 - 31 Dec 2020

### Added

- [#84](https://github.com/scylladb/sphinx-scylladb-theme/issues/84): Banner for ScyllaDB Summit.
- [#95](https://github.com/scylladb/sphinx-scylladb-theme/issues/95): Support for custom domain.
- [#92](https://github.com/scylladb/sphinx-scylladb-theme/issues/92): Command to preview multiversion build.
- [#89](https://github.com/scylladb/sphinx-scylladb-theme/issues/89): Rename the latest version URL automatically to stable.

## 0.1.16 - 24 Nov 2020

### Added

- [#84](https://github.com/scylladb/sphinx-scylladb-theme/issues/84): Banner for ScyllaDB Summit.

### Changed

- [#83](https://github.com/scylladb/sphinx-scylladb-theme/issues/83): Copyright year in the footer is now updated automatically.

## 0.1.15 - 17 Nov 2020

### Added

- [#78](https://github.com/scylladb/sphinx-scylladb-theme/issues/78): Show a warning when the user is not reading not reading the latest version.

## 0.1.14 - 28 Oct 2020

### Changed

- [#72](https://github.com/scylladb/sphinx-scylladb-theme/issues/72): Overwrite the Sphinx classification for external and internal links.
- [#71](https://github.com/scylladb/sphinx-scylladb-theme/issues/71): Site description is now configurable per project.

## 0.1.13 - 20 Oct 2020

### Added

- [#65](https://github.com/scylladb/sphinx-scylladb-theme/issues/65): External links and download links are now followed by an icon.
- [#53](https://github.com/scylladb/sphinx-scylladb-theme/issues/53): Now code blocks can include substitutions.

### Changed

- [#64](https://github.com/scylladb/sphinx-scylladb-theme/issues/64): The 404 page sports a new design.

### Fixed

- [#69](https://github.com/scylladb/sphinx-scylladb-theme/issues/69): Redirections on multiversion builds were not working

### Removed

- [#68](https://github.com/scylladb/sphinx-scylladb-theme/issues/68): PIPX dependency.

## 0.1.12 - 01 Oct 2020

### Added

- [#59](https://github.com/scylladb/sphinx-scylladb-theme/issues/59): All projects now share a 404 page.
- [#58](https://github.com/scylladb/sphinx-scylladb-theme/issues/58): Support for redirections.
