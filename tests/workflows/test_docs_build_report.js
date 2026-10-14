const assert = require('node:assert/strict');
const test = require('node:test');
const { diagnostics, renderReport, reportPullRequest } = require('../../.github/scripts/docs-build-report.js');

const run = {
  id: 123, run_attempt: 1, workflow_id: 9, event: 'pull_request',
  path: '.github/workflows/docs-pr.yaml',
  conclusion: 'failure', head_sha: 'abcdef123456', head_branch: 'docs-change',
  html_url: 'https://github.com/example/docs/actions/runs/123',
  head_repository: { id: 7, owner: { login: 'contributor' } },
  pull_requests: [{ number: 17 }],
};

function fixture({ previous, success = false, newer = false, attempt = false,
  stale = false, closed = false, fork = false, unavailable = false } = {}) {
  const current = { ...run, conclusion: success ? 'success' : 'failure',
    pull_requests: fork ? [] : run.pull_requests };
  const calls = [];
  const pr = { number: 17, state: closed ? 'closed' : 'open',
    head: { sha: stale ? 'different-commit' : run.head_sha } };
  const github = {
    rest: {
      pulls: { list() {}, get: async args => {
        assert.equal(args.pull_number, 17);
        return { data: pr };
      } },
      actions: {
        listWorkflowRuns: async () => ({ data: { workflow_runs: [{ ...current,
          id: newer ? 124 : current.id, run_attempt: attempt ? 2 : 1 }] } }),
        listJobsForWorkflowRunAttempt() {},
        downloadJobLogsForWorkflowRun: async () => {
          if (unavailable) throw new Error('Expired logs');
          return { data: "2026-10-09T10:00:00.000Z docs/network.md: WARNING: document isn't included in any toctree [toc.not_included]\n" };
        },
      },
      issues: {
        listComments() {},
        updateComment: async args => calls.push({ update: args }),
        createComment: async args => calls.push({ create: args }),
        deleteComment: async args => calls.push({ delete: args }),
      },
    },
    paginate: async (method, args) => {
      if (method === github.rest.pulls.list) {
        assert.equal(args.head, 'contributor:docs-change');
        return [pr];
      }
      if (method === github.rest.actions.listJobsForWorkflowRunAttempt) {
        assert.equal(args.attempt_number, 1);
        return [{ id: 88, name: 'build', steps: [{ name: 'Test docs', conclusion: 'failure' }] }];
      }
      return previous ? [{ id: 99, user: { login: 'github-actions[bot]' },
        body: '<!-- docs-build-report -->\nOld failure' }] : [];
    },
  };
  return { github, calls, context: { repo: { owner: 'example', repo: 'docs' },
    payload: { workflow_run: current } }, core: { warning() {} } };
}

test('reports preserve the original warning wording and severity', () => {
  const text = "docs/alternator/network.md: WARNING: document isn't included in any toctree [toc.not_included]";
  const body = renderReport(run, text);
  assert.ok(body.includes('<pre>' + text + '</pre>'));
});

test('diagnostics strip timestamps and colors and omit the log tail when diagnostics exist', () => {
  const line = '2026-10-09T10:00:00.000Z \x1b[31mdocs/page.md: WARNING: missing reference\x1b[0m';
  const text = diagnostics('', [line, line, 'error: dependency install failed'].join('\n'), true);
  assert.equal(text.split('Build log tail:')[0].match(/WARNING:/g).length, 1);
  assert.doesNotMatch(text, /\x1b|2026-10-09T/);
  assert.match(text, /dependency install failed/);
  assert.doesNotMatch(text, /Build log tail/);
});

test('the log tail is a fallback for failures without diagnostics', () => {
  const log = [...Array(30).fill('progress'), 'process unexpectedly stopped'].join('\n');
  const text = diagnostics('', log, true);
  assert.match(text, /^Build log tail:/);
  assert.match(text, /process unexpectedly stopped/);
  assert.equal(diagnostics('', log, false), '');
});

test('diagnostics are grouped by severity with one code block per issue', () => {
  const text = 'Failed step: Build docs\n\n'
    + '/home/runner/work/docs/docs/docs/source/page.rst:10: ERROR: Unknown directive.\n'
    + '\n.. invalid-directive::\n\n   offending source\n'
    + '/home/runner/work/docs/docs/docs/source/page.rst:20: WARNING: missing reference\n'
    + 'docs/source/page.rst:30: ERROR: Second error.\n\n   second source\n'
    + 'docs/source/page.rst:40: WARNING: second warning\n'
    + 'docs/source/page.rst:50: WARNING: third warning';
  const body = renderReport(run, text);
  assert.match(body, /Docs \/ Build PR failed/);
  assert.match(body, /\*\*2 errors\*\* and \*\*3 warnings\*\*/);
  assert.equal(body.match(/<pre>/g).length, 5);
  const [errors, warnings] = body.split('#### Warnings');
  assert.match(errors, /#### Errors/);
  assert.equal(errors.match(/<pre>/g).length, 2);
  assert.equal(warnings.match(/<pre>/g).length, 3);
  assert.match(errors, /<pre>docs\/source\/page.rst:10: ERROR:/);
  assert.match(errors, /offending source<\/pre>/);
  assert.match(warnings, /<pre>docs\/source\/page.rst:20: WARNING:/);
  assert.doesNotMatch(body, /<ol>|<li>/);
  assert.doesNotMatch(body, /\/home\/runner\/work\//);
});

test('many diagnostic blocks still fit in a GitHub comment', () => {
  const body = renderReport(run, Array(1000).fill('WARNING: &'.repeat(3)).join('\n'));
  assert.ok(body.length < 65_536);
  assert.equal(body.match(/<pre>/g).length, 20);
  assert.match(body, /Report truncated/);
});

test('warnings file retains multiline diagnostic context', () => {
  assert.equal(diagnostics('WARNING: bad directive\n  offending source\n', 'progress', false),
    'WARNING: bad directive\n  offending source');
});

test('warnings do not hide errors earlier in the build log', () => {
  const warning = 'WARNING: missing reference';
  const log = ['ERROR: early failure', warning, ...Array(30).fill('progress')].join('\n');
  const text = diagnostics(warning, log, true);
  const messages = text.split('Build log tail:')[0];
  assert.match(messages, /ERROR: early failure/);
  assert.equal(messages.match(/WARNING: missing reference/g).length, 1);
});

test('PR reports preserve the complete multiline diagnostics repeated by the summary step', () => {
  const log = 'Build output\nDocs build diagnostics\nWARNING: invalid directive\n'
    + 'unknown option: example\n\n.. code-block:: text\n   :example: true\n'
    + 'End of docs build diagnostics\nPost-job cleanup';
  assert.equal(diagnostics('', log, true), 'WARNING: invalid directive\n'
    + 'unknown option: example\n\n.. code-block:: text\n   :example: true');
});

test('untrusted diagnostic text cannot escape the preformatted block or mention users', () => {
  const body = renderReport(run, '</pre><script>alert(1)</script> @someone ```');
  assert.doesNotMatch(body, /<script>|@someone/);
  assert.match(body, /&lt;\/pre&gt;/);
  assert.match(body, /&#64;someone/);
});

test('even escaped oversized diagnostics fit in a GitHub comment', () => {
  const body = renderReport(run, '&'.repeat(100_000));
  assert.ok(body.length < 65_536);
  assert.match(body, /Report truncated/);
});

test('failed fork builds create a report using GitHub PR metadata', async () => {
  const data = fixture({ fork: true });
  await reportPullRequest(data);
  assert.equal(data.calls.length, 1);
  assert.equal(data.calls[0].create.issue_number, 17);
  assert.match(data.calls[0].create.body, /Failed step: Test docs/);
});

test('subsequent failures update the existing report', async () => {
  const data = fixture({ previous: true });
  await reportPullRequest(data);
  assert.equal(data.calls.length, 1);
  assert.equal(data.calls[0].update.comment_id, 99);
});

test('successful builds delete the existing report and never post a success comment', async () => {
  const data = fixture({ previous: true, success: true });
  await reportPullRequest(data);
  assert.equal(data.calls.length, 1);
  assert.equal(data.calls[0].delete.comment_id, 99);
  const clean = fixture({ success: true });
  await reportPullRequest(clean);
  assert.equal(clean.calls.length, 0);
});

for (const option of ['stale', 'closed', 'newer', 'attempt']) {
  test(`${option} runs cannot overwrite the current PR report`, async () => {
    const data = fixture({ [option]: true });
    await reportPullRequest(data);
    assert.equal(data.calls.length, 0);
  });
}

test('another workflow cannot post a report by copying the docs workflow name', async () => {
  const data = fixture();
  data.context.payload.workflow_run.path = '.github/workflows/other.yaml';
  await reportPullRequest(data);
  assert.equal(data.calls.length, 0);
});

test('unavailable logs still produce a report linking to the failed build', async () => {
  const data = fixture({ unavailable: true });
  await reportPullRequest(data);
  assert.match(data.calls[0].create.body, /Build log unavailable/);
  assert.match(data.calls[0].create.body, /actions\/runs\/123/);
});
