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
zany changelog
zany status-page
zany commands
zany roadmap
```

Run tests locally:

```bash
pytest
```

## Continuous integration

GitHub Actions runs the Python test suite on pushes to `main`, pull requests targeting `main`, and manual workflow dispatch.

The workflow currently tests Python 3.11 and 3.12.

## Documentation

- `docs/session-log.md` records bounded work sessions.
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
- `zany sessions` summarizes the session log and latest recorded session.
- `zany changelog` generates a compact changelog from recent session-log entries.
- `zany status-page` writes `docs/status.html` from the session log.
- `zany commands` prints the command reference as Markdown.
- `zany roadmap` shows completed and candidate tasks from `docs/ideas.md`.
