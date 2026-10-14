import pytest
import yaml

from sphinx_scylladb_theme.cli.redirects_check import (
    check_live,
    main,
    read_base_url,
    target_is_live,
)

# -- read_base_url ----------------------------------------------------------


def test_read_base_url_from_conf(tmp_path):
    (tmp_path / "conf.py").write_text('html_baseurl = "https://docs.example.com/"\n')
    assert read_base_url(tmp_path) == "https://docs.example.com"


def test_read_base_url_missing_raises(tmp_path):
    (tmp_path / "conf.py").write_text("")
    with pytest.raises(ValueError, match="html_baseurl is not set"):
        read_base_url(tmp_path)


# -- CLI plumbing -----------------------------------------------------------


def test_main_missing_yaml(tmp_path, capsys):
    rc = main(
        [
            "--yaml",
            str(tmp_path / "missing.yaml"),
            "--stable-base-url",
            "https://x",
        ]
    )
    assert rc == 2
    assert "not found" in capsys.readouterr().err


def test_main_conf_missing_conf_py(tmp_path, capsys):
    yaml_path = tmp_path / "redirects.yaml"
    yaml_path.write_text("")
    rc = main(["--yaml", str(yaml_path), "--conf", str(tmp_path)])
    assert rc == 2
    assert "conf.py not found" in capsys.readouterr().err


def test_main_conf_and_stable_are_mutually_exclusive(tmp_path):
    yaml_path = tmp_path / "redirects.yaml"
    yaml_path.write_text("")
    with pytest.raises(SystemExit):
        main(
            [
                "--yaml",
                str(yaml_path),
                "--conf",
                str(tmp_path),
                "--stable-base-url",
                "https://example.com",
            ]
        )


def test_main_requires_a_mode(tmp_path):
    yaml_path = tmp_path / "redirects.yaml"
    yaml_path.write_text("")
    with pytest.raises(SystemExit):
        main(["--yaml", str(yaml_path)])


# -- target_is_live / check_live -------------------------------------------


class FakeHTTP:
    """Records requested URLs and returns a scripted status per URL."""

    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def __call__(self, url):
        self.calls.append(url)
        return self.responses.get(url)


def test_target_is_live_2xx_true():
    http = FakeHTTP({"https://x/stable/foo.html": 200})
    assert target_is_live("https://x", "/stable/foo.html", http_head=http) is True


def test_target_is_live_404_false():
    http = FakeHTTP({"https://x/stable/gone.html": 404})
    assert target_is_live("https://x", "/stable/gone.html", http_head=http) is False


def test_target_is_live_network_error_none():
    http = FakeHTTP({"https://x/stable/foo.html": None})
    assert target_is_live("https://x", "/stable/foo.html", http_head=http) is None


def test_target_is_live_external_url_skipped():
    http = FakeHTTP({})
    assert target_is_live("https://x", "https://other/", http_head=http) is True
    assert http.calls == []


def test_target_is_live_strips_trailing_slash_on_base():
    http = FakeHTTP({"https://x/stable/foo.html": 200})
    target_is_live("https://x/", "/stable/foo.html", http_head=http)
    assert http.calls == ["https://x/stable/foo.html"]


def test_check_live_only_checks_stable_prefix(tmp_path):
    yaml_path = tmp_path / "redirects.yaml"
    yaml_path.write_text(
        yaml.safe_dump(
            {
                "/stable/a.html": "/stable/live.html",  # /stable/, 200 -> ok
                "/stable/b.html": "/stable/dead.html",  # /stable/, 404 -> fail
                "/1.7/c.html": "/1.7/anything.html",  # not /stable/ -> skip
                "/stable/d.html": "https://external/",  # external -> skip
            }
        )
    )
    http = FakeHTTP(
        {
            "https://x/stable/live.html": 200,
            "https://x/stable/dead.html": 404,
        }
    )
    missing = check_live(yaml_path, "https://x", http_head=http)
    assert missing == [("/stable/b.html", "/stable/dead.html")]
    assert "https://x/1.7/anything.html" not in http.calls


def test_check_live_network_error_is_skipped(tmp_path):
    yaml_path = tmp_path / "redirects.yaml"
    yaml_path.write_text(yaml.safe_dump({"/stable/a.html": "/stable/x.html"}))
    http = FakeHTTP({"https://x/stable/x.html": None})  # network error
    assert check_live(yaml_path, "https://x", http_head=http) == []


def test_check_live_custom_prefix(tmp_path):
    yaml_path = tmp_path / "redirects.yaml"
    yaml_path.write_text(
        yaml.safe_dump(
            {
                "/latest/a.html": "/latest/dead.html",
                "/stable/b.html": "/stable/dead.html",  # ignored under prefix=latest
            }
        )
    )
    http = FakeHTTP({"https://x/latest/dead.html": 404})
    missing = check_live(yaml_path, "https://x", prefix="latest", http_head=http)
    assert missing == [("/latest/a.html", "/latest/dead.html")]


def test_check_live_empty_yaml(tmp_path):
    yaml_path = tmp_path / "redirects.yaml"
    yaml_path.write_text("")
    assert check_live(yaml_path, "https://x", http_head=FakeHTTP({})) == []
