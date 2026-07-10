# Development Notes

This repository is a bounded playground for small assistant-built utilities. Keep each change narrow, reversible, and easy to inspect.

## Project structure

- `src/openai_zany/` contains the Python package and CLI implementation.
- `tests/` contains pytest coverage for CLI helpers and generated output.
- `docs/session-log.md` records each bounded work session.
- `docs/ideas.md` tracks completed and candidate tasks.
- `docs/commands.md` documents the current CLI surface.
- `docs/status.html` is generated from the session log by `zany status-page`.
- `docs/autonomous-checklist.md` provides the pre-stop checklist for autonomous sessions.

## Local workflow

Install the package with developer dependencies:

```bash
python -m pip install -e '.[dev]'
```

Run the full test suite:

```bash
pytest
```

Regenerate derived documentation when its source changes:

```bash
zany commands > docs/commands.md
zany status-page
```

## Change rules

- Prefer one coherent task per session.
- Add or update tests when behavior changes.
- Keep generated files in sync with their source commands.
- Update `docs/session-log.md` before stopping.
- Record the next smallest useful task for the following session.
