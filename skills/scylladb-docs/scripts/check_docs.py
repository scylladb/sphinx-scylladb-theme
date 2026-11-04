#!/usr/bin/env python3
"""Check ScyllaDB documentation changes for common markup and style problems.

Run from the root of a ScyllaDB repository. By default, compares the working tree
(committed and uncommitted changes, plus untracked files) with the merge base of the
upstream default branch, and checks only the lines you added in .rst files under
docs/. In scylladb/scylladb and scylladb/scylla-enterprise, docs/dev/ is skipped,
because it holds unpublished developer notes. Markdown (MyST) pages aren't checked;
they are listed as skipped.

For a change that targets a release branch, pass that branch with --base, so that
the release branch's own content isn't reported as added.

    python check_docs.py                 # check your changes
    python check_docs.py --base upstream/branch-2026.1
    python check_docs.py --all           # check every line of the changed files
    python check_docs.py docs/a.rst ...  # check whole files, without git

Findings are heuristics: confirm each one before fixing it. Exits with 1 if there
are findings, 0 if there are none, and 2 on errors.
"""

import argparse
import fnmatch
import os
import posixpath
import re
import subprocess
import sys

DOCS_PREFIX = "docs/"
DEV_DOCS_PREFIX = "docs/dev/"
# Repositories (by name, so that forks match too) whose docs/dev/ isn't published.
DEV_DOCS_REPOS = {"scylladb", "scylla", "scylla-enterprise"}

ADORNMENT = re.compile(r"^([=\-~.^*#\"+`'_:])\1{2,}\s*$")
CODE_DIRECTIVE = re.compile(r"^(\s*)\.\.\s+(code-block|code|sourcecode)::\s*(\S*)")
IMAGE_DIRECTIVE = re.compile(r"^(\s*)\.\.\s+(image|figure)::")
TOCTREE_DIRECTIVE = re.compile(r"^(\s*)\.\.\s+toctree::")
INCLUDE_DIRECTIVE = re.compile(r"^\s*\.\.\s+include::\s*(\S+)")
NAMED_URL_TARGET = re.compile(r"^\s*\.\.\s+_([^:]+):\s*(\S+)")
UNSUPPORTED_ADMONITION = re.compile(
    r"^\s*\.\.\s+(important|attention|danger|error|hint|seealso|admonition)::"
)
VERSION_DIRECTIVE = re.compile(r"^\s*\.\.\s+(versionadded|versionchanged|deprecated)::")
TITLE_LINK = re.compile(r"(?<![\w:`])`([^`<>]+?)`_(?!_)")
INLINE_LITERAL = re.compile(r"``.+?``")
LINK_TARGET = re.compile(r"<[^<>]*>")
URL = re.compile(r"https?://\S+")
SUBSTITUTION = re.compile(r"\|[\w.-]+\|")
DOC_ROLE = re.compile(r":doc:`([^`]+)`")
REF_ROLE = re.compile(r":ref:`([^`]+)`")
ANCHOR = re.compile(r"^\s*\.\.\s+_([^:`]+):\s*$")

DISCOURAGED_TERMS = [
    (re.compile(r"\bScylla\b(?![-_/.]\w)"), "Use 'ScyllaDB', not 'Scylla'."),
    (re.compile(r"\bkey space", re.I), "Use 'keyspace'."),
    (re.compile(r"\b(Sstable|ssTable)"), "Use 'SSTable'."),
    (re.compile(r"\bdata centers?\b", re.I), "Use 'datacenter'."),
    (re.compile(r"\bmulti[- ]DCs?\b"), "Use 'multi-datacenter'."),
    (re.compile(r"\bmulti-cloud\b", re.I), "Use 'multicloud'."),
    (re.compile(r"\bcode base\b", re.I), "Use 'codebase'."),
]


class Finding:
    def __init__(self, path, line, message):
        self.path = path
        self.line = line
        self.message = message


def git(repo, *args):
    result = subprocess.run(
        ["git", "-c", "core.quotepath=off", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


def in_scope(path, skip_dev_docs):
    if skip_dev_docs and path.startswith(DEV_DOCS_PREFIX):
        return False
    return path.startswith(DOCS_PREFIX)


def has_unpublished_dev_docs(repo):
    """Return True if a remote points to scylladb/scylladb, scylla-enterprise, or a fork."""
    names = set()
    for row in git(repo, "remote", "-v").splitlines():
        url = row.split()[1] if len(row.split()) > 1 else ""
        name = re.sub(r"\.git$", "", url.rstrip("/").rsplit("/", 1)[-1].split(":")[-1])
        names.add(name)
    return bool(names & DEV_DOCS_REPOS)


def read_lines(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read().splitlines()


def find_merge_base(repo, base):
    if base:
        candidates = [base]
    else:
        candidates = []
        try:
            head = git(repo, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD")
            candidates.append(head.strip().replace("refs/remotes/", ""))
        except RuntimeError:
            pass
        candidates += [
            "upstream/master",
            "upstream/main",
            "origin/master",
            "origin/main",
            "master",
            "main",
        ]
    for ref in candidates:
        try:
            return git(repo, "merge-base", ref, "HEAD").strip(), ref
        except RuntimeError:
            continue
    raise RuntimeError(
        "Could not find the upstream default branch. Pass it with --base, "
        "for example --base upstream/master."
    )


def changed_files(repo, merge_base):
    """Return a list of (status, old_path, new_path) compared with the working tree."""
    changes = []
    for row in git(repo, "diff", "-M", "--name-status", merge_base).splitlines():
        parts = row.split("\t")
        status = parts[0][0]
        if status == "R":
            changes.append(("R", parts[1], parts[2]))
        elif status == "D":
            changes.append(("D", parts[1], None))
        else:
            changes.append((status, None, parts[1]))
    untracked = git(repo, "ls-files", "--others", "--exclude-standard", "--", "docs")
    for path in untracked.splitlines():
        changes.append(("A", None, path))
    return changes


def added_line_numbers(repo, merge_base, path):
    """Return the 1-based numbers of lines added in path since merge_base."""
    numbers = set()
    diff = git(repo, "diff", "-U0", merge_base, "--", path)
    current = None
    for row in diff.splitlines():
        hunk = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", row)
        if hunk:
            current = int(hunk.group(1))
        elif current is not None and row.startswith("+") and not row.startswith("+++"):
            numbers.add(current)
            current += 1
    return numbers


def code_lines(lines):
    """Map 0-based indexes of lines inside literal blocks to the block language."""
    code = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        match = CODE_DIRECTIVE.match(line)
        if match:
            indent, language = len(match.group(1)), match.group(3)
        elif (
            line.strip()
            and line.rstrip().endswith("::")
            and not line.lstrip().startswith("..")
        ):
            indent, language = len(line) - len(line.lstrip()), "literal"
        else:
            i += 1
            continue
        j = i + 1
        while j < len(lines):
            if not lines[j].strip():
                j += 1
                continue
            if len(lines[j]) - len(lines[j].lstrip()) <= indent:
                break
            code[j] = language
            j += 1
        i = j
    return code


def prose(line):
    """Strip literals, link targets, and URLs so that only reader-visible text stays."""
    line = INLINE_LITERAL.sub("", line)
    line = URL.sub("", line)
    return LINK_TARGET.sub("", line)


def check_lines(path, lines, selected):
    """Run line-level checks on the 0-based indexes in selected."""
    findings = []
    code = code_lines(lines)
    url_targets = set()
    for line in lines:
        match = NAMED_URL_TARGET.match(line)
        if match and ("://" in match.group(2) or "/" in match.group(2)):
            url_targets.add(match.group(1).strip().lower())

    def add(index, message):
        findings.append(Finding(path, index + 1, message))

    for i in sorted(selected):
        if i >= len(lines):
            continue
        line = lines[i]
        stripped = line.strip()

        if i in code:
            if stripped.startswith("$ "):
                add(i, "Command has a '$' prompt. Remove it so that copying works.")
            continue

        if re.match(r"^\s*\.\.\s+(code-block|sourcecode|code)::\s*$", line):
            add(i, "Code block has no language. Add one, for example 'cql' or 'none'.")

        match = IMAGE_DIRECTIVE.match(line)
        if match:
            indent = len(match.group(1))
            has_alt = False
            for option in lines[i + 1 :]:
                opt = option.strip()
                if not opt or len(option) - len(option.lstrip()) <= indent:
                    break
                if not opt.startswith(":"):
                    break
                if re.match(r":alt:\s*\S", opt):
                    has_alt = True
            if not has_alt:
                add(i, f"{match.group(2).capitalize()} has no :alt: text.")

        match = UNSUPPORTED_ADMONITION.match(line)
        if match:
            hint = " Use '.. note::' instead." if match.group(1) == "important" else ""
            add(
                i,
                f"'.. {match.group(1)}::' isn't a supported admonition. Allowed: "
                f"note, tip, caution, warning.{hint}",
            )

        match = VERSION_DIRECTIVE.match(line)
        if match:
            add(
                i,
                f"Don't use '.. {match.group(1)}::'. State version information once, "
                "in prose.",
            )

        if re.match(r"^\s*\.\.\s+contents::", line):
            add(i, "Remove '.. contents::'. The theme generates the On This Page menu.")

        if re.match(r"^:orphan:", line):
            add(i, "':orphan:' hides the page from navigation. Add it to a toctree.")

        if stripped.startswith(".. ") or stripped.startswith(":"):
            continue

        for match in TITLE_LINK.finditer(INLINE_LITERAL.sub("", line)):
            if match.group(1).strip().lower() in url_targets:
                continue
            add(
                i,
                f"Link `{match.group(1)}`_ may point to a section title. Add an anchor "
                "and use :ref: instead.",
            )

        text = prose(line)
        for pattern, message in DISCOURAGED_TERMS:
            if pattern.search(text):
                add(i, message)

    return findings


def check_headings(path, lines, selected):
    findings = []
    code = code_lines(lines)
    for i in range(len(lines) - 1):
        text, under = lines[i], lines[i + 1]
        if i in code or not text.strip() or text[0].isspace():
            continue
        if ADORNMENT.match(text) or text.startswith(".."):
            continue
        if not ADORNMENT.match(under):
            continue
        # An adornment above the text is an overline only if it isn't itself the
        # underline of a heading directly above.
        overline = None
        if i > 0 and ADORNMENT.match(lines[i - 1]):
            if i == 1 or not lines[i - 2].strip():
                overline = lines[i - 1]
        touched = {i, i + 1} | ({i - 1} if overline else set())
        if not touched & selected:
            continue
        width = len(text.rstrip())
        if len(under.rstrip()) < width:
            findings.append(
                Finding(
                    path,
                    i + 2,
                    f"Heading underline is shorter than the heading text "
                    f"({len(under.rstrip())} < {width}).",
                )
            )
        if overline and len(overline.rstrip()) != len(under.rstrip()):
            findings.append(
                Finding(path, i, "Title overline and underline lengths differ.")
            )
        if SUBSTITUTION.search(text):
            findings.append(
                Finding(path, i + 1, "Don't use substitutions in headings.")
            )
    return findings


def source_root(repo):
    for candidate in ("docs/source", "docs"):
        if os.path.isfile(os.path.join(repo, candidate, "conf.py")):
            return candidate
    return "docs"


def walk_rst(repo, root):
    for dirpath, dirnames, filenames in os.walk(os.path.join(repo, root)):
        dirnames[:] = [
            d for d in dirnames if d not in ("_build", ".venv", "node_modules")
        ]
        for name in filenames:
            if name.endswith(".rst"):
                full = os.path.join(dirpath, name)
                yield os.path.relpath(full, repo).replace(os.sep, "/")


def docname(path, root):
    rel = posixpath.relpath(path, root)
    return rel[:-4] if rel.endswith(".rst") else rel


def normalize(target, current_doc):
    target = target.strip()
    if target.endswith(".rst"):
        target = target[:-4]
    if target.endswith("/"):
        target += "index"
    if target.startswith("/"):
        return posixpath.normpath(target.lstrip("/"))
    return posixpath.normpath(posixpath.join(posixpath.dirname(current_doc), target))


class References:
    """Navigation entries, links, and anchors found in the docs source tree."""

    def __init__(self):
        self.entries = set()  # pages listed in a toctree
        self.patterns = set()  # toctree :glob: patterns
        self.includes = set()  # files pulled in with .. include::
        self.doc_links = {}  # page name -> files that list or link to it
        self.anchors = set()  # explicit anchors defined anywhere
        self.ref_links = {}  # anchor -> files that link to it with :ref:


def role_target(text):
    target = re.match(r"^.*<(.+)>$", text.strip())
    return (target.group(1) if target else text).strip()


def referenced_docs(repo, root):
    """Collect toctree entries, includes, links, and anchors, ignoring code samples."""
    refs = References()
    for path in walk_rst(repo, root):
        current = docname(path, root)
        lines = read_lines(os.path.join(repo, path))
        code = code_lines(lines)
        for i, line in enumerate(lines):
            if i in code:
                continue
            for match in DOC_ROLE.finditer(line):
                target = normalize(role_target(match.group(1)).split("#")[0], current)
                refs.doc_links.setdefault(target, set()).add(path)
            for match in REF_ROLE.finditer(line):
                anchor = role_target(match.group(1)).lower()
                refs.ref_links.setdefault(anchor, set()).add(path)
            match = ANCHOR.match(line)
            if match:
                refs.anchors.add(match.group(1).strip().lower())
            match = INCLUDE_DIRECTIVE.match(line)
            if match:
                refs.includes.add(normalize(match.group(1), current))
            match = TOCTREE_DIRECTIVE.match(line)
            if not match:
                continue
            indent = len(match.group(1))
            glob = False
            for entry in lines[i + 1 :]:
                stripped = entry.strip()
                if not stripped:
                    continue
                if len(entry) - len(entry.lstrip()) <= indent:
                    break
                if stripped.startswith(":"):
                    glob = glob or stripped == ":glob:"
                    continue
                target = role_target(stripped)
                if "://" in target or target == "self":
                    continue
                resolved = normalize(target, current)
                if glob and "*" in target:
                    refs.patterns.add(resolved)
                else:
                    refs.entries.add(resolved)
                refs.doc_links.setdefault(resolved, set()).add(path)
    return refs


def check_new_pages(repo, new_pages, root, refs):
    findings = []
    for path in new_pages:
        name = docname(path, root)
        if name == "index" or path.startswith(".."):
            continue
        if any(
            part.startswith("_") or part == "rst_include" for part in name.split("/")
        ):
            continue
        if name in refs.includes or name in refs.entries:
            continue
        if any(fnmatch.fnmatch(name, pattern) for pattern in refs.patterns):
            continue
        full = os.path.join(repo, path)
        if os.path.isfile(full) and any(
            line.startswith(":orphan:") for line in read_lines(full)
        ):
            continue
        findings.append(
            Finding(path, 1, "New page isn't in any toctree, so the build fails.")
        )
    return findings


def redirect_sources(repo):
    """Return the old paths (the keys) in docs/_utils/redirects.yaml."""
    path = os.path.join(repo, "docs", "_utils", "redirects.yaml")
    if not os.path.isfile(path):
        return []
    sources = []
    for line in read_lines(path):
        line = line.strip()
        if line and not line.startswith("#") and ":" in line:
            sources.append(line.split(":", 1)[0].strip().strip("'\""))
    return sources


def removed_anchors(repo, merge_base, path):
    """Return the explicit anchors that the removed page defined."""
    try:
        lines = git(repo, "show", f"{merge_base}:{path}").splitlines()
    except RuntimeError:
        return set()
    code = code_lines(lines)
    return {
        match.group(1).strip().lower()
        for i, line in enumerate(lines)
        if i not in code and (match := ANCHOR.match(line))
    }


def check_removed_pages(repo, root, merge_base, removed, refs):
    findings = []
    sources = redirect_sources(repo)
    for path, new_path in removed:
        name = docname(path, root)
        stems = {name}
        if name.endswith("/index"):
            stems.add(name[: -len("/index")])
        found = any(
            re.search(re.escape("/" + stem) + r"(\.html|\.rst|\.md)?/?$", source)
            for stem in stems
            for source in sources
        )
        action = f"was renamed to {new_path}" if new_path else "was deleted"
        if not found:
            findings.append(
                Finding(
                    path,
                    0,
                    f"Page {action} but has no entry in docs/_utils/redirects.yaml.",
                )
            )
        for other in sorted(refs.doc_links.get(name, ())):
            findings.append(Finding(other, 0, f"Still links to the old page '{name}'."))
        for anchor in sorted(removed_anchors(repo, merge_base, path) - refs.anchors):
            for other in sorted(refs.ref_links.get(anchor, ())):
                findings.append(
                    Finding(
                        other,
                        0,
                        f"Links to anchor '{anchor}', which was defined on the removed "
                        f"page {path}.",
                    )
                )
    return findings


def run_git_mode(repo, args):
    merge_base, ref = find_merge_base(repo, args.base)
    print(f"Comparing with {ref} (merge base {merge_base[:12]}).")
    root = source_root(repo)
    skip_dev = has_unpublished_dev_docs(repo)
    if skip_dev:
        print(f"Skipping {DEV_DOCS_PREFIX}, which isn't published in this repository.")
    findings, new_pages, removed, skipped, checked = [], [], [], [], 0
    for status, old, new in changed_files(repo, merge_base):
        if status in ("D", "R") and old and old.endswith(".rst"):
            if in_scope(old, skip_dev):
                removed.append((old, new))
        if not new or not in_scope(new, skip_dev):
            continue
        if new.endswith(".md"):
            skipped.append(new)
            continue
        if not new.endswith(".rst"):
            continue
        full = os.path.join(repo, new)
        if not os.path.isfile(full):
            continue
        lines = read_lines(full)
        if status == "A" or args.all:
            selected = set(range(len(lines)))
        else:
            selected = {n - 1 for n in added_line_numbers(repo, merge_base, new)}
        if status in ("A", "R"):
            new_pages.append(new)
        findings += check_lines(new, lines, selected)
        findings += check_headings(new, lines, selected)
        checked += 1
    if new_pages or removed:
        refs = referenced_docs(repo, root)
        findings += check_new_pages(repo, new_pages, root, refs)
        findings += check_removed_pages(repo, root, merge_base, removed, refs)
    report_skipped(skipped)
    return findings, checked


def report_skipped(skipped):
    if skipped:
        print(f"Skipped {len(skipped)} non-.rst file(s); the checker covers .rst only:")
        for path in skipped:
            print(f"  {path}")


def run_file_mode(paths):
    findings, skipped = [], [p for p in paths if not p.endswith(".rst")]
    paths = [p for p in paths if p.endswith(".rst")]
    report_skipped(skipped)
    for path in paths:
        lines = read_lines(path)
        selected = set(range(len(lines)))
        findings += check_lines(path, lines, selected)
        findings += check_headings(path, lines, selected)
    return findings, len(paths)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="*", help="check these whole files, without git")
    parser.add_argument("--base", help="branch to compare with (default: autodetect)")
    parser.add_argument(
        "--all", action="store_true", help="check all lines of the changed files"
    )
    args = parser.parse_args()

    try:
        if args.files:
            findings, checked = run_file_mode(args.files)
        else:
            repo = git(".", "rev-parse", "--show-toplevel").strip()
            findings, checked = run_git_mode(repo, args)
    except (RuntimeError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    findings.sort(key=lambda f: (f.path, f.line))
    current = None
    for finding in findings:
        if finding.path != current:
            current = finding.path
            print(f"\n{current}")
        location = f"{finding.line:>5}" if finding.line else "    -"
        print(f"{location}  {finding.message}")
    print(f"\nChecked {checked} file(s), {len(findings)} finding(s).")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
