import json
import os
import subprocess
from pathlib import Path

import pytest
import yaml

REPOSITORY = Path(__file__).resolve().parents[2]


def read_action(name):
    directory = REPOSITORY / ".github/actions" / name
    return directory, yaml.safe_load((directory / "action.yml").read_text())


def test_build_preserves_failure_and_logs_output(tmp_path):
    workflow = yaml.safe_load(
        (REPOSITORY / ".github/workflows/docs-pr.yaml").read_text()
    )
    step = next(
        step
        for step in workflow["jobs"]["build"]["steps"]
        if step.get("id") == "docs-build"
    )
    assert step["shell"] == "bash"
    make = tmp_path / "make"
    make.write_text(
        "#!/bin/sh\n"
        '[ "$1" = "-C" ] && [ "$2" = "docs" ] || exit 97\n'
        "echo 'WARNING: missing reference' >&2\n"
        "echo 'ERROR: build failed' >&2\n"
        "exit 3\n"
    )
    make.chmod(0o755)
    result = subprocess.run(
        ["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", step["run"]],
        env={
            **os.environ,
            "PATH": f"{tmp_path}:{os.environ['PATH']}",
            "RUNNER_TEMP": str(tmp_path),
        },
        capture_output=True,
        text=True,
    )
    assert result.returncode == 3
    assert "WARNING: missing reference" in result.stdout
    assert "ERROR: build failed" in (tmp_path / "docs-build.log").read_text()


@pytest.mark.parametrize("event_name", ["pull_request", "workflow_run"])
def test_report_loads_bundled_helper_outside_the_callers_checkout(tmp_path, event_name):
    directory, action = read_action("docs-report")
    step = action["runs"]["steps"][-1]
    # Run the actual github-script entry point from a different repository.
    # Only the action path should determine which helper is executed.
    report_script = step["env"]["REPORT_SCRIPT"].replace(
        "${{ github.action_path }}", str(directory)
    )
    (tmp_path / "docs-warnings.log").write_text("WARNING: missing reference\n")
    (tmp_path / "docs-build.log").write_text("ERROR: build failed\n")
    runner = r"""
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
let body;
const core = {
  info() {}, warning() {},
  summary: { addRaw(value) { body = value; return this; }, async write() {} },
};
const run = {
  id: 123, run_attempt: 1, workflow_id: 9, event: 'pull_request',
  path: '.github/workflows/docs-pr.yaml',
  conclusion: 'failure', head_sha: 'abcdef123456', pull_requests: [{ number: 17 }],
  html_url: 'https://github.com/example/docs/actions/runs/123',
};
const context = { eventName: process.argv[2], repo: { owner: 'example', repo: 'docs' },
  payload: { workflow_run: run } };
const github = {
  rest: {
    pulls: { get: async () => ({ data: { number: 17, state: 'open', head: { sha: run.head_sha } } }) },
    actions: {
      listWorkflowRuns: async () => ({ data: { workflow_runs: [] } }),
      listJobsForWorkflowRunAttempt() {},
      downloadJobLogsForWorkflowRun: async () => ({ data: 'WARNING: missing reference\nERROR: build failed' }),
    },
    issues: { listComments() {}, createComment: async ({ body: value }) => { body = value; } },
  },
  paginate: async method => method === github.rest.actions.listJobsForWorkflowRunAttempt
    ? [{ id: 88, name: 'build', steps: [] }] : [],
};
new AsyncFunction('require', 'core', 'context', 'github', process.argv[1])(require, core, context, github)
  .then(() => process.stdout.write(JSON.stringify(body)))
  .catch(error => { console.error(error); process.exitCode = 1; });
"""
    result = subprocess.run(
        ["node", "-e", runner, step["with"]["script"], event_name],
        cwd=tmp_path,
        env={
            **os.environ,
            "REPORT_SCRIPT": report_script,
            "RUNNER_TEMP": str(tmp_path),
            "DOCS_BUILD_OUTCOME": "failure",
            "GITHUB_RUN_ID": "123",
            "GITHUB_RUN_ATTEMPT": "1",
            "GITHUB_SHA": "abcdef123456",
            "GITHUB_SERVER_URL": "https://github.com",
            "GITHUB_REPOSITORY": "example/docs",
        },
        capture_output=True,
        text=True,
        check=True,
    )
    body = json.loads(result.stdout)
    assert "Docs / Build PR failed" in body
    assert "WARNING: missing reference" in body
    assert "ERROR: build failed" in body
    assert "https://github.com/example/docs/actions/runs/123" in body
