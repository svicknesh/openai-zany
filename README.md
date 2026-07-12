# OpenAI Zany

Bounded experimental workspace for assistant-built utilities.

Rules:

1. Work only in this repository: svicknesh/openai-zany.
2. Spend at most 30 minutes per session. If a coherent task is already in progress, finish that task, then stop.

## Usage

Install locally with developer dependencies:

```bash
python -m pip install -e '.[dev]'
```

Run the current CLI helpers:

```bash
zany next
zany list
zany doctor
zany sessions
zany sessions-json
zany changelog
zany status-page
zany commands
zany roadmap
zany freshness
zany generate-docs
zany docs-diff
```

Human-readable summaries, machine-readable summaries, and changelogs now default to the append-only session-record directory. The JSON command also supports an optional result limit and explicit legacy-file access:

```bash
zany sessions
zany sessions-json
zany sessions-json --limit 5
zany sessions-json --path docs/session-log.md
zany sessions-json --path docs/sessions --limit 5
zany changelog
```

Directory results are ordered by sortable session filename, newest first. Files without a `# Session:` heading are ignored.

The standalone `zany-sessions-json` executable remains available for compatibility.

Run tests locally:

```bash
pytest
```

## CLI smoke test

After installation, run this small read-only check from the repository root:

```bash
set -eu
zany doctor
zany commands | grep -F '| `zany doctor` |'
zany roadmap | grep -F '## Candidate tasks'
zany sessions
zany sessions-json --path docs/sessions --limit 1 | grep -F '"sessions"'
zany changelog | grep -F '# Changelog'
zany docs-diff
```

A successful run exits with status 0 and prints the repository health report, a command-reference row, the roadmap candidate heading, human-readable and machine-readable append-only session results, and a changelog. It also confirms that generated documentation has no pending differences. The smoke test does not regenerate or modify repository files.

## Session records

New autonomous work is recorded as one immutable Markdown file per session under `docs/sessions/`. This append-only model prevents connector-driven runs from truncating shared history.

`docs/session-log.md` remains a legacy archive used only for compatibility. `zany sessions`, `zany sessions-json`, and `zany changelog` read `docs/sessions/` by default; `zany sessions-json` can still read the legacy file through `--path docs/session-log.md`. Autonomous connector runs must not replace the legacy archive. See `docs/sessions/README.md` for naming and structure rules.

## Generated documentation

Preview pending generated-document changes without writing files:

```bash
zany docs-diff
zany docs-diff --format json
```

Exit status 1 means pending changes were found and displayed.

Check whether managed documentation matches the current renderers:

```bash
zany freshness
```

Regenerate every managed document in one step:

```bash
zany generate-docs
```

The refresh command currently writes `docs/commands.md` and `docs/status.html`.

## Continuous integration

GitHub Actions runs the Python test suite and verifies generated-document freshness on pushes to `main`, pull requests targeting `main`, and manual workflow dispatch.

The workflow currently tests Python 3.11 and 3.12. A stale `docs/commands.md` or `docs/status.html` fails the workflow with guidance to regenerate the affected file.

## Documentation

- `CONTRIBUTING.md` provides the compact checklist for code and documentation changes.
- `docs/sessions/` contains canonical append-only autonomous-session records.
- `docs/session-log.md` is the surviving legacy aggregate session archive.
- `docs/ideas.md` tracks completed and candidate tasks.
- `docs/development.md` explains the repository structure and local workflow.
- `docs/status.html` provides a static repository status page.
- `docs/commands.md` provides the CLI command reference.
- `docs/autonomous-checklist.md` provides the pre-stop checklist for autonomous sessions.
- `docs/release-notes-template.md` provides a small, auditable release-notes structure.

## Current CLI commands

- `zany next` shows the next small candidate task.
- `zany list` shows the current idea backlog.
- `zany doctor` checks whether the expected scaffold files are present.
- `zany sessions` summarizes append-only session records and the latest recorded session.
- `zany sessions-json` prints structured append-only session-record data by default, with legacy-file support through `--path`.
- `zany changelog` generates a compact changelog from recent append-only session records.
- `zany status-page` writes `docs/status.html` from the session log.
- `zany commands` prints the command reference as Markdown.
- `zany roadmap` shows completed and candidate tasks from `docs/ideas.md`.
- `zany freshness` checks whether generated documentation matches current renderers.
- `zany generate-docs` regenerates all managed documentation files.
- `zany docs-diff` previews generated-document changes without writing files.
