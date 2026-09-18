"""
Catches redirects merged to master whose target has not yet been
released to ``/stable/``, which would otherwise leave real users on
the current stable version hitting a 404.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

import yaml

EXTERNAL_URL_RE = re.compile(r"^[a-z][a-z0-9+.-]*://", re.IGNORECASE)

ADVICE = """
These redirects would send real users to a 404 after deploy.

This usually means the target page was added on master but the version
that its URL prefix references has not been re-released yet.

Recommended fix:
  1. Remove the affected entries from redirects.yaml in this PR.
  2. Open a follow-up PR that only adds those entries.
  3. Merge the follow-up PR AFTER the version containing the target
     page is released and deployed.
""".strip()

_HTTP_TIMEOUT = 10


def load_redirects(yaml_path: Path) -> dict[str, str]:
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


def _default_http_head(url: str) -> int | None:
    """Returns the HTTP status code, or None on network error."""
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=_HTTP_TIMEOUT) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except (urllib.error.URLError, TimeoutError, ConnectionError):
        return None


def target_is_live(base_url: str, target: str, http_head=None) -> bool | None:
    if EXTERNAL_URL_RE.match(target):
        return True

    head = http_head or _default_http_head
    url = base_url.rstrip("/") + target
    status = head(url)
    if status is None:
        return None
    return 200 <= status < 300


def check_live(
    yaml_path: Path,
    base_url: str,
    prefix: str = "stable",
    http_head=None,
) -> list[tuple[str, str]]:
    entries = load_redirects(yaml_path)
    marker = f"/{prefix.strip('/')}/"
    missing = []
    for old, new in entries.items():
        target = str(new)
        if not target.startswith(marker):
            continue
        result = target_is_live(base_url, target, http_head=http_head)
        if result is False:
            missing.append((old, new))
    return missing


def read_base_url(confdir: Path) -> str:
    from sphinx.config import eval_config_file
    from sphinx.util.tags import Tags

    # eval_config_file chdirs into filename.parent then reads filename,
    # so filename must be absolute or the read fails after the chdir.
    namespace = eval_config_file((confdir / "conf.py").resolve(), Tags())
    url = str(namespace.get("html_baseurl") or "").strip()
    if not url:
        raise ValueError(
            f"html_baseurl is not set in {confdir}/conf.py; "
            f"cannot determine the live site to check against"
        )
    return url.rstrip("/")


def _report_missing(missing: list[tuple[str, str]], where: str) -> int:
    print(
        f"error: {len(missing)} redirect target(s) missing from {where}:",
        file=sys.stderr,
    )
    for old, new in missing:
        print(f"  {new}  (from {old})", file=sys.stderr)
    print("", file=sys.stderr)
    print(ADVICE, file=sys.stderr)
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--yaml", required=True, type=Path, help="Path to redirects.yaml"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--conf",
        type=Path,
        help=(
            "Read html_baseurl from the Sphinx conf.py in this directory "
            "and check every /<stable-prefix>/ target is reachable on it."
        ),
    )
    mode.add_argument(
        "--stable-base-url",
        help="Explicit live-site URL, mainly for tests and edge cases.",
    )
    parser.add_argument(
        "--stable-prefix",
        default="stable",
        help='URL prefix that maps to the rolling latest release (default: "stable").',
    )
    args = parser.parse_args(argv)

    if not args.yaml.is_file():
        print(f"error: redirects file not found: {args.yaml}", file=sys.stderr)
        return 2

    if args.conf is not None:
        if not (args.conf / "conf.py").is_file():
            print(f"error: conf.py not found in {args.conf}", file=sys.stderr)
            return 2
        try:
            base_url = read_base_url(args.conf)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
    else:
        base_url = args.stable_base_url

    missing = check_live(args.yaml, base_url, args.stable_prefix)
    if missing:
        return _report_missing(missing, base_url)
    print(f"ok: all /{args.stable_prefix}/ redirect target(s) return 2xx on {base_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
