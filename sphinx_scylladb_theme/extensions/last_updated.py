"""
Per-page "Last updated" dates from git history.

Overrides the ``last_updated`` template context variable with the date of
the last commit that touched each page's source file.

Works with sphinx-multiversion.

"""

import os
import posixpath
import subprocess
from datetime import datetime, timezone

DEFAULT_DATE_FORMAT = "%d %B %Y"

# Last-resort fallback, matching ``conf_py_path`` in theme.conf. Only used
# when the theme options cannot be resolved at all (non-HTML builders).
DEFAULT_CONF_PY_PATH = "docs/source/"

_GIT_TIMEOUT = 300


def _git(repo, *args):
    """
    Runs a git command in ``repo`` and returns its stdout, or ``None`` on
    any failure (git missing, not a repository, bad ref, timeout).
    """
    try:
        result = subprocess.run(
            ["git", "-C", repo, "-c", "core.quotePath=false", *args],
            capture_output=True,
            text=True,
            timeout=_GIT_TIMEOUT,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return result.stdout


def find_repo_root(*candidates):
    """
    Returns the git top-level directory for the first candidate path that
    is inside a repository, or an empty string.
    """
    for path in candidates:
        if not path:
            continue
        out = _git(path, "rev-parse", "--show-toplevel")
        if out:
            return out.strip()
    return ""


def resolve_ref(repo_root, name):
    """
    Resolves a sphinx-multiversion version name to a usable git ref.
    Branch names may only exist on the remote (e.g. ``origin/stable``).
    Returns ``HEAD`` when the name cannot be resolved.
    """
    if not name:
        return "HEAD"
    for candidate in (name, f"origin/{name}"):
        if _git(repo_root, "rev-parse", "--verify", "--quiet", candidate) is not None:
            return candidate
    return "HEAD"


def build_dates_map(repo_root, ref, prefix=""):
    """
    Builds a map of repo-relative file path -> unix timestamp of the last
    commit that touched the file, in a single history pass.

    :param repo_root: Absolute path to the git repository.
    :param ref: Ref to read history at (e.g. ``HEAD``, ``origin/stable``).
    :param prefix: Optional repo-relative path to limit the walk to.
    """
    args = ["log", ref, "--format=%x00%at", "--name-only"]
    if prefix:
        args += ["--", prefix]
    out = _git(repo_root, *args)
    if not out:
        return {}

    dates = {}
    timestamp = None
    for line in out.splitlines():
        if line.startswith("\x00"):
            timestamp = int(line[1:])
        elif line and timestamp is not None:
            # git log is newest-first: keep the first date seen per file.
            dates.setdefault(line, timestamp)
    return dates


def format_timestamp(timestamp, fmt=None):
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime(
        fmt or DEFAULT_DATE_FORMAT
    )


def source_prefix(app, repo_root):
    """
    Returns the docs source directory relative to the repository root.

    In a regular build the source directory lives inside the repository.
    Under sphinx-multiversion it is a temporary export, so the location is
    taken from the ``conf_py_path`` theme option instead.
    """
    srcdir = os.path.realpath(str(app.srcdir))
    repo_root = os.path.realpath(repo_root)
    if srcdir == repo_root:
        return ""
    if srcdir.startswith(repo_root + os.sep):
        return os.path.relpath(srcdir, repo_root).replace(os.sep, "/")

    return conf_py_path(app).strip("/")


def conf_py_path(app):
    """
    Returns the ``conf_py_path`` theme option, resolved the same way
    templates see it: project overrides in ``html_theme_options`` merged
    over the theme.conf defaults.
    """
    theme_options = getattr(app.config, "html_theme_options", {}) or {}
    theme = getattr(getattr(app, "builder", None), "theme", None)
    if theme is not None:
        try:
            return theme.get_options(theme_options).get(
                "conf_py_path", DEFAULT_CONF_PY_PATH
            )
        except Exception:
            pass
    return theme_options.get("conf_py_path", DEFAULT_CONF_PY_PATH)


def init_dates(app):
    app._git_last_updated = {}
    app._git_last_updated_prefix = ""

    if not getattr(app.config, "git_last_updated_enabled", True):
        return

    # Under sphinx-multiversion, srcdir and the working directory both live
    # in a temporary git-archive export; the output directory is the only
    # path that still points inside the original repository.
    repo_root = find_repo_root(
        str(app.srcdir),
        os.getcwd(),
        os.getenv("SPHINX_MULTIVERSION_OUTPUTDIR"),
    )
    if not repo_root:
        return

    ref = resolve_ref(repo_root, os.getenv("SPHINX_MULTIVERSION_NAME"))
    prefix = source_prefix(app, repo_root)
    app._git_last_updated = build_dates_map(repo_root, ref, prefix)
    app._git_last_updated_prefix = prefix


def update_page_context(app, pagename, templatename, context, doctree):
    dates = getattr(app, "_git_last_updated", None)
    if not dates:
        return

    source = app.env.doc2path(pagename, False)
    repo_path = posixpath.join(app._git_last_updated_prefix, str(source))
    timestamp = dates.get(repo_path)
    if timestamp is None:
        return

    fmt = getattr(app.config, "html_last_updated_fmt", None)
    context["last_updated"] = format_timestamp(timestamp, fmt)


def setup(app):
    app.add_config_value("git_last_updated_enabled", True, "html")
    app.connect("builder-inited", init_dates)
    app.connect("html-page-context", update_page_context)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
