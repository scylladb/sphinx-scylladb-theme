import os
import subprocess
from unittest.mock import MagicMock

import pytest

from sphinx_scylladb_theme.extensions.last_updated import (
    build_dates_map,
    find_repo_root,
    format_timestamp,
    resolve_ref,
    source_prefix,
    update_page_context,
)


def git(repo, *args, env=None):
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        env=env,
    )


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, "init", "-b", "master")
    git(tmp_path, "config", "user.email", "test@test.com")
    git(tmp_path, "config", "user.name", "Test")

    docs = tmp_path / "docs" / "source"
    docs.mkdir(parents=True)

    def commit(filename, timestamp):
        (docs / filename).write_text(f"content {timestamp}")
        git(tmp_path, "add", ".")
        git(
            tmp_path,
            "commit",
            "-m",
            f"edit {filename}",
            env={
                **os.environ,
                "GIT_AUTHOR_DATE": f"@{timestamp} +0000",
                "GIT_COMMITTER_DATE": f"@{timestamp} +0000",
            },
        )

    commit("index.rst", 1000)
    commit("other.rst", 2000)
    commit("index.rst", 3000)
    return tmp_path


def test_find_repo_root(repo):
    assert find_repo_root(str(repo / "docs" / "source")) == str(repo.resolve())


def test_find_repo_root_not_a_repo(tmp_path):
    assert find_repo_root(str(tmp_path)) == ""


def test_find_repo_root_skips_empty_candidates(repo):
    assert find_repo_root("", None, str(repo)) == str(repo.resolve())


def test_build_dates_map_latest_date_wins(repo):
    dates = build_dates_map(str(repo), "HEAD")
    assert dates["docs/source/index.rst"] == 3000
    assert dates["docs/source/other.rst"] == 2000


def test_build_dates_map_with_prefix(repo):
    dates = build_dates_map(str(repo), "HEAD", "docs/source")
    assert dates["docs/source/index.rst"] == 3000


def test_build_dates_map_bad_ref(repo):
    assert build_dates_map(str(repo), "does-not-exist") == {}


def test_resolve_ref(repo):
    assert resolve_ref(str(repo), "master") == "master"
    assert resolve_ref(str(repo), None) == "HEAD"
    assert resolve_ref(str(repo), "unknown-branch") == "HEAD"


def test_format_timestamp():
    assert format_timestamp(0) == "01 January 1970"
    assert format_timestamp(0, "%Y-%m-%d") == "1970-01-01"


def test_source_prefix_inside_repo(repo):
    app = MagicMock()
    app.srcdir = str(repo / "docs" / "source")
    assert source_prefix(app, str(repo)) == "docs/source"


def test_source_prefix_outside_repo_uses_theme_options(repo, tmp_path_factory):
    export = tmp_path_factory.mktemp("export")
    app = MagicMock()
    app.srcdir = str(export / "docs" / "source")
    app.config.html_theme_options = {"conf_py_path": "documentation/source/"}
    app.builder.theme.get_options.side_effect = lambda overrides: {
        "conf_py_path": "docs/source/",
        **overrides,
    }
    assert source_prefix(app, str(repo)) == "documentation/source"


def test_source_prefix_outside_repo_theme_default(repo, tmp_path_factory):
    export = tmp_path_factory.mktemp("export")
    app = MagicMock()
    app.srcdir = str(export / "docs" / "source")
    app.config.html_theme_options = {}
    app.builder.theme.get_options.side_effect = lambda overrides: {
        "conf_py_path": "theme-default/source/",
        **overrides,
    }
    assert source_prefix(app, str(repo)) == "theme-default/source"


def test_source_prefix_outside_repo_no_theme(repo, tmp_path_factory):
    export = tmp_path_factory.mktemp("export")
    app = MagicMock()
    app.srcdir = str(export / "docs" / "source")
    app.config.html_theme_options = {"conf_py_path": "documentation/source/"}
    app.builder = None
    assert source_prefix(app, str(repo)) == "documentation/source"


def make_app(dates, prefix="docs/source", fmt=None):
    app = MagicMock()
    app._git_last_updated = dates
    app._git_last_updated_prefix = prefix
    app.config.html_last_updated_fmt = fmt
    app.env.doc2path.return_value = "index.rst"
    return app


def test_update_page_context_sets_last_updated():
    app = make_app({"docs/source/index.rst": 0})
    context = {}
    update_page_context(app, "index", None, context, None)
    assert context["last_updated"] == "01 January 1970"


def test_update_page_context_respects_format():
    app = make_app({"docs/source/index.rst": 0}, fmt="%Y-%m-%d")
    context = {}
    update_page_context(app, "index", None, context, None)
    assert context["last_updated"] == "1970-01-01"


def test_update_page_context_unknown_page_untouched():
    app = make_app({"docs/source/index.rst": 0})
    app.env.doc2path.return_value = "missing.rst"
    context = {"last_updated": "fallback"}
    update_page_context(app, "missing", None, context, None)
    assert context["last_updated"] == "fallback"


def test_update_page_context_no_dates_untouched():
    app = make_app({})
    context = {}
    update_page_context(app, "index", None, context, None)
    assert context == {}
