# Style reference

This file covers language, word choice, version information, and the errors in the
current docs. It is based on the ScyllaDB style guide
(https://github.com/scylladb/scylladb-docs-homepage/blob/main/STYLEGUIDE.md) and the
ScyllaDB Cloud docs conventions.

## Contents

1. Audience
2. Voice and tone
3. Grammar and spelling
4. Formatting in text
5. Word list
6. Static documentation
7. Writing about versions
8. Errors in the current docs

---

## 1. Audience

The primary readers are developers and database administrators. Some readers aren't
technical, for example executives who read overview pages.

Don't assume that the reader:

- has NoSQL experience
- knows Apache Cassandra
- uses AWS
- runs a single node

## 2. Voice and tone

| Do | Example | Instead of |
|---|---|---|
| Address the reader as "you". | Enter your credentials. | The user must enter credentials. |
| Use active voice. | ScyllaDB supports the following versions: | The following versions are supported by ScyllaDB. |
| Use present tense. | The page opens. | The page will open. |
| Use imperative mood for instructions. | Install ScyllaDB from the download center. | If you want to install ScyllaDB, go to the download center. |
| Name things clearly instead of using pronouns that could refer to two things. | If you type text in the field, the text doesn't change. | If you type text in the field, it doesn't change. |

- Be friendly, natural, and concise. Prefer short, direct sentences.
- Use contractions where they read naturally, for example "don't" or "isn't".
- Prefer clarity over formality.

## 3. Grammar and spelling

- **Use American English,** for example *analyze*, *behavior*, *license*, *color*.
- **Use the Oxford comma:** "consistency, availability, and partition tolerance."
- **Punctuate consistently:** start sentences with a capital letter, end them with a
  period, and put a colon before a list.

## 4. Formatting in text

- **Bold UI elements,** without quotation marks: Click **Options**, not Click
  "Options".
- **Italicize a new term the first time you introduce it:** A *node* is a unit of
  storage.
- **Format code as code** with double backticks: commands, file names, paths,
  parameters, and CQL keywords used as code.

## 5. Word list

| Use | Don't use |
|---|---|
| ScyllaDB | Scylla |
| keyspace | key space |
| SSTable | Sstable, ssTable |
| datacenter | data center, DC (in prose) |
| multi-datacenter | multi-DC, multi DC |
| multicloud | multi-cloud |
| codebase | code base |
| vnode | Vnode (except at the start of a sentence) |
| click (for UI) | press |
| select (a checkbox or option) | check, mark |

"Scylla" remains correct only in literal names, such as package names, binaries,
services, and config files: `scylla.yaml`, `scylla-server`, `scylla_setup`.

## 6. Static documentation

Documentation describes the product as it is now:

- **Don't pre-announce features or promise fixes.** Don't write "This option will be
  supported in the next release" or "We will add a workaround soon." Document a
  feature when it ships.
- **Avoid temporary wording** such as "currently", "at the moment", "new", or "recently
  added", because it goes stale without anyone noticing.

**Exception:** compatibility notes are fine. Examples are differences from Apache
Cassandra, or from DynamoDB for Alternator. They describe how the product behaves
today; they aren't roadmap items.

## 7. Writing about versions

**In all projects:**

- Don't use the `versionadded`, `versionchanged`, or `deprecated` directives.
- Don't put version availability or roadmap items in an admonition box.
- Don't document what is planned for a future version.

**Cloud only (scylladb/scylla-cloud-doc):**

ScyllaDB Cloud users don't choose their ScyllaDB version directly. Clusters are
upgraded some time after a release: an LTS cluster can stay on the same version for up
to a year, and other clusters for months. A version requirement is therefore worth
recording, but not worth repeating.

- Describe what the product does, not what each version does.
- When availability genuinely matters, state it once. Either write it in prose where
  the feature is introduced, or add it to a single table that collects the version
  requirements for a feature set. Don't repeat it in every section that mentions the
  feature.
- An FAQ entry about version requirements is fine, because readers do ask. Keep the
  answer short, and point to the prose or the table instead of repeating the details.

Avoid:

```rst
.. note::

   Full text search requires **ScyllaDB 2026.3.0 or later**.

.. note::

   Returning BM25 relevance scores in query results is planned for ScyllaDB
   2026.4.0.
```

Instead, write the requirement once, as an ordinary sentence in the prerequisites or as
a row in the feature's version table. Remove the roadmap note completely.

## 8. Errors in the current docs

The existing docs aren't a reliable template. When you copy a pattern from a
neighboring page, check it against this skill first. These are the common problems in
the current docs:

- **Title-based links** (`` `Section Title`_ ``). There are dozens in
  scylladb/scylladb. Use an anchor with `:ref:` instead.
- **Inconsistent headings:** a title with no overline, `=` followed by `^`, or skipped
  levels. The heading example in `docs/README.md` in scylladb/scylladb (`-----` above
  and below "Prerequisites") doesn't match the theme convention either.
- **Unsupported admonitions** such as `important` and `seealso`, and boxes that hold
  ordinary information, which belongs in a paragraph.
- **Images without alt text,** which is most of them in scylladb/scylladb.
- **`$` prompts in code blocks.**
- **Old wording:** "Scylla" instead of "ScyllaDB", "data center" instead of
  "datacenter", and "will" for present behavior.
- **Mini-TOCs (`.. contents::`).** The theme's own TOC example page still recommends
  them, but the "On This Page" sidebar has replaced them.
- **Build instructions that don't match the Makefile:** a README can name a different
  package manager than the project actually uses. For example, the scylladb/scylladb
  README mentions Poetry, but its `docs/Makefile` uses `uv`. Trust `docs/Makefile`.

When you edit a page, fix problems like these in the lines you change. Leave the rest of
the page alone unless the user asks for a cleanup. Large mechanical cleanups belong in
their own PR, so that reviewers can check them separately from content changes.
