/**
 * Copyright (c) 2022 - present David Garcia (@dgarcia360)
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
const core = require("@actions/core");
const github = require("@actions/github");
const { Octokit } = require("octokit");

async function main() {
  // Authenticate
  const octokit = new Octokit({
    auth: process.env.TOKEN,
  });

  // Search the Amplify URL
  const url = bodyComment.split("Access this pull request here: ")[1];

  // Get the pull request files modified
  const request = {
    owner: github.context.repo.owner,
    repo: github.context.repo.repo,
    pull_number: github.context.issue.number,
  };

  let changedFiles;
  try {
    const result = await octokit.request(
      `GET /repos/${request.owner}/${request.repo}/pulls/${github.context.issue.number}/files`,
      request,
    );
    changedFiles = result.data;
  } catch (err) {
    core.setFailed(`Request failed with error ${err}`);
  }

  // For each changed file, get the files under **/docs, .md or .rst files
  const acceptedFilesStatus = ["created", "modified"];
  let docFiles = [];
  changedFiles.forEach((file) => {
    if (
      acceptedFilesStatus.includes(file.status) &&
      file.filename.startsWith("docs/") &&
      !file.filename.includes("docs/dev") &&
      (file.filename.endsWith(".rst") || file.filename.endsWith(".md"))
    ) {
      const baseFilename = file.filename
        .replace("docs/source/", "")
        .replace("docs/", "")
        .split(".")
        .slice(0, -1)
        .join(".");
      docFiles.push(`- ${file.filename} ${url}/${baseFilename}\n`);
    }
  });

  if (docFiles.length == 0) {
    // Delete the comment
    try {
      await octokit.rest.issues.deleteComment({
        owner: github.context.repo.owner,
        repo: github.context.repo.repo,
        comment_id: github.context.payload.comment.id,
      });
    } catch (err) {
      core.setFailed(`Delete comment failed with error ${err}`);
    }
  } else {
    // Update the original comment of the pull request to add the list of modified files
    try {
      await octokit.rest.issues.updateComment({
        owner: github.context.repo.owner,
        repo: github.context.repo.repo,
        comment_id: github.context.payload.comment.id,
        body: `${bodyComment}\n\nFiles changed:\n${docFiles.join("")}`,
      });
    } catch (err) {
      core.setFailed(`Comment failed with error ${err}`);
    }
  }
}

const bodyComment = github.context.payload.comment.body;
const amplifyComment = `${bodyComment}`.includes(
  "This pull request is automatically being deployed by Amplify Hosting",
);
if (github.context.payload.issue.pull_request && amplifyComment) {
  main();
}
