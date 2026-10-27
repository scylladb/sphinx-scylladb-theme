# Skills for Claude Code

This folder contains [Claude Code](https://claude.com/claude-code) skills for
ScyllaDB documentation contributors. Skills aren't part of the theme package, so they
don't affect theme releases.

| Skill | What it does |
|---|---|
| `scylladb-docs` | Helps you write, update, and review ScyllaDB user documentation so that it builds cleanly and follows the theme's markup conventions and the ScyllaDB style guide. It covers reStructuredText (`.rst`) pages; for Markdown (MyST) pages, it applies only the language rules. It applies to `docs/` in any ScyllaDB project, except `docs/dev/` in scylladb/scylladb and scylladb/scylla-enterprise. |

## Install

Copy the skill folder to your personal skills folder. The skill is then available in
every repository you work on. Run these commands from the root of this repository.
They delete any installed copy first, so you can run the same commands again to
update the skill after you pull a newer version. Deleting first also removes files
that newer versions no longer include.

**Linux and macOS:**

```bash
mkdir -p ~/.claude/skills
rm -rf ~/.claude/skills/scylladb-docs
cp -r skills/scylladb-docs ~/.claude/skills/
```

**Windows (PowerShell):**

```powershell
$skills = "$env:USERPROFILE\.claude\skills"
New-Item -ItemType Directory -Force $skills | Out-Null
Remove-Item -Recurse -Force "$skills\scylladb-docs" -ErrorAction SilentlyContinue
Copy-Item -Recurse skills\scylladb-docs "$skills\"
```

On Linux and macOS, you can create a symbolic link instead of a copy. Pulling this
repository then updates the skill automatically:

```bash
mkdir -p ~/.claude/skills
rm -rf ~/.claude/skills/scylladb-docs
ln -s "$PWD/skills/scylladb-docs" ~/.claude/skills/scylladb-docs
```

Restart Claude Code after you install or update the skill.

## Use

Claude Code loads the skill automatically when you work on files under `docs/`. You can
also invoke it explicitly with `/scylladb-docs`. For example:

- "Add a page about configuring client-to-node encryption to the security section."
- "I renamed `backup.rst` to `backup-cluster.rst`. Fix everything that needs fixing."
- "Review my docs changes before I open a PR."

The skill includes a checker script that finds mechanical problems in the lines you
changed. You can also run the checker without Claude, from the root of a ScyllaDB
repository:

```bash
python ~/.claude/skills/scylladb-docs/scripts/check_docs.py
```

The script needs only Python 3.8 or later and Git. Run it with `--help` to see the
options.
