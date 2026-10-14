const fs = require('node:fs');
const path = require('node:path');

const MARKER = '<!-- docs-build-report -->';
const MAX_LOG = 2_000_000;
const MAX_REPORT = 12_000;
const MAX_DIAGNOSTICS = 20;
const DIAGNOSTIC = /^(?:\S.*?:\s*)?(WARNING|ERROR|CRITICAL):|^(error):/i;

function limitLog(text) {
  return text.length > MAX_LOG ? text.slice(0, MAX_LOG) + '\n[Log truncated]\n'
    + text.slice(-32_000) : text;
}

function clean(text) {
  return text.replace(/\x1b\[[0-9;]*[a-zA-Z]/g, '')
    .replace(/^\d{4}-\d{2}-\d{2}T\S+\s?/gm, '')
    .replace(/\/home\/runner\/work\/[^/\s]+\/[^/\s]+\//g, '');
}

function diagnostics(warnings, log, failed) {
  const plain = clean(log);
  // The summary step repeats the complete diagnostics, including multiline errors.
  const start = plain.lastIndexOf('\nDocs build diagnostics\n');
  const end = plain.indexOf('\nEnd of docs build diagnostics', start);
  if (!warnings.trim() && start >= 0 && end > start) {
    return plain.slice(start + '\nDocs build diagnostics\n'.length, end);
  }
  const lines = plain.split('\n');
  const warningText = clean(warnings).trim();
  const known = new Set(warningText.split('\n'));
  const additional = [...new Set(lines.filter(line =>
    DIAGNOSTIC.test(line)
  ))].filter(line => !known.has(line));
  const messages = [warningText, ...additional].filter(Boolean).join('\n');
  if (messages) return messages;
  const tail = failed ? lines.filter(line => line.trim()).slice(-25).join('\n') : '';
  return tail ? 'Build log tail:\n' + tail : '';
}

function splitDiagnostics(text) {
  const entries = [];
  const prefix = [];
  for (const line of text.split('\n')) {
    const match = line.match(DIAGNOSTIC);
    if (match) {
      const severity = (match[1] || match[2]).toUpperCase() === 'WARNING' ? 'warning' : 'error';
      entries.push({ severity, text: line });
    } else if (entries.length) entries[entries.length - 1].text += '\n' + line;
    else prefix.push(line);
  }
  return { entries, prefix: prefix.join('\n').trim() };
}

function escape(text) {
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/@/g, '&#64;');
}

function renderReport(run, text) {
  const status = { success: 'passed', failure: 'failed' }[run.conclusion] || run.conclusion;
  const displayed = clean(text).slice(0, MAX_REPORT);
  const { entries, prefix } = splitDiagnostics(displayed);
  const shortened = text.length > MAX_REPORT || entries.length > MAX_DIAGNOSTICS;
  const output = [MARKER, `### Docs / Build PR ${status}`, ''];
  if (run.conclusion === 'success') output.push('The documentation check passed.', '');
  else if (entries.length) {
    const counts = ['error', 'warning'].map(severity => {
      const count = entries.filter(entry => entry.severity === severity).length;
      return count ? `**${count} ${severity}${count === 1 ? '' : 's'}**` : '';
    }).filter(Boolean).join(' and ');
    output.push(`The documentation check reported ${counts}. Warnings also fail this check.`, '');
  } else output.push('No documentation diagnostics were captured. Check the failed step in the build log.', '');
  output.push(`Commit: \`${run.head_sha.slice(0, 7)}\`. [Build log](${run.html_url}).`, '');
  if (entries.length) {
    if (prefix) output.push('<p>' + escape(prefix) + '</p>', '');
    let remaining = MAX_DIAGNOSTICS;
    for (const severity of ['error', 'warning']) {
      const group = entries.filter(entry => entry.severity === severity).slice(0, remaining);
      if (!group.length) continue;
      output.push(severity === 'error' ? '#### Errors' : '#### Warnings', '');
      for (const entry of group) output.push('<pre>' + escape(entry.text.trim()) + '</pre>', '');
      remaining -= group.length;
    }
  } else if (displayed.trim()) output.push('<pre>' + escape(displayed) + '</pre>', '');
  if (shortened) output.push('Report truncated. See the build log for all diagnostics.', '');
  return output.join('\n');
}

function readLog(filename) {
  if (!fs.existsSync(filename)) return '';
  return limitLog(fs.readFileSync(filename, 'utf8'));
}

async function writeSummary({ core }) {
  const directory = process.env.RUNNER_TEMP;
  const outcome = process.env.DOCS_BUILD_OUTCOME;
  const warnings = readLog(path.join(directory, 'docs-warnings.log'));
  const log = readLog(path.join(directory, 'docs-build.log'));
  const text = diagnostics(warnings, log, outcome === 'failure');
  const run = {
    conclusion: outcome === 'skipped' ? 'not run' : outcome,
    head_sha: process.env.GITHUB_SHA,
    html_url: `${process.env.GITHUB_SERVER_URL}/${process.env.GITHUB_REPOSITORY}`
      + `/actions/runs/${process.env.GITHUB_RUN_ID}`,
  };
  core.info('\nDocs build diagnostics\n' + (text.trim()
    || (outcome === 'success' ? 'No warnings or errors found.' : 'No diagnostics captured.'))
    + '\nEnd of docs build diagnostics');
  await core.summary.addRaw(renderReport(run, text)).write();
}

async function readBuildDiagnostics({ github, repository, run, core }) {
  const jobs = await github.paginate(github.rest.actions.listJobsForWorkflowRunAttempt, {
    ...repository, run_id: run.id, attempt_number: run.run_attempt, per_page: 100,
  });
  const build = jobs.find(job => job.name === 'build');
  if (!build) return '';
  const failed = (build.steps || []).find(step => step.conclusion === 'failure');
  const prefix = failed ? `Failed step: ${failed.name}\n\n` : '';
  try {
    const { data } = await github.rest.actions.downloadJobLogsForWorkflowRun({
      ...repository, job_id: build.id,
    });
    const log = typeof data === 'string' ? data : Buffer.from(data).toString('utf8');
    return prefix + diagnostics('', limitLog(log), true);
  } catch (error) {
    core.warning(`Could not read the build log: ${error.message}`);
    return prefix + 'Build log unavailable. Use the link above to inspect the failed step.';
  }
}

async function reportPullRequest({ github, context, core }) {
  const run = context.payload.workflow_run;
  const repository = context.repo;
  if (run.event !== 'pull_request' || run.path !== '.github/workflows/docs-pr.yaml') return;
  // Resolve the PR from GitHub metadata, never from PR-controlled files or logs.
  let candidates = run.pull_requests || [];
  if (!candidates.length && run.head_repository) {
    candidates = await github.paginate(github.rest.pulls.list, {
      ...repository, state: 'open',
      head: `${run.head_repository.owner.login}:${run.head_branch}`, per_page: 100,
    });
  }
  for (const candidate of candidates) {
    const { data: pr } = await github.rest.pulls.get({
      ...repository, pull_number: candidate.number,
    });
    if (pr.state !== 'open' || pr.head.sha !== run.head_sha) continue;
    const { data: latest } = await github.rest.actions.listWorkflowRuns({
      ...repository, workflow_id: run.workflow_id, event: 'pull_request',
      head_sha: run.head_sha, per_page: 100,
    });
    if (latest.workflow_runs.some(other =>
      other.head_repository?.id === run.head_repository?.id
      && other.head_branch === run.head_branch
      && (other.id > run.id || (other.id === run.id && other.run_attempt > run.run_attempt))
    )) continue;
    const comments = await github.paginate(github.rest.issues.listComments, {
      ...repository, issue_number: pr.number, per_page: 100,
    });
    const previous = comments.find(comment =>
      comment.user?.login === 'github-actions[bot]' && (comment.body || '').startsWith(MARKER)
    );
    if (run.conclusion === 'success') {
      if (previous) await github.rest.issues.deleteComment({
        ...repository, comment_id: previous.id,
      });
      continue;
    }
    const text = await readBuildDiagnostics({ github, repository, run, core });
    const body = renderReport(run, text);
    if (previous) await github.rest.issues.updateComment({
      ...repository, comment_id: previous.id, body,
    });
    else await github.rest.issues.createComment({
      ...repository, issue_number: pr.number, body,
    });
  }
}

module.exports = { clean, diagnostics, renderReport, writeSummary, reportPullRequest };
