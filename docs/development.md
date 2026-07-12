# Development Notes

This repository is a bounded playground for small assistant-built utilities. Keep each change narrow, reversible, and easy to inspect.

## Project structure

- `src/openai_zany/` contains the Python package and CLI implementation.
- `tests/` contains pytest coverage for CLI helpers and generated output.
- `docs/sessions/` contains the canonical append-only record for completed bounded work sessions.
- `docs/session-log.md` is the surviving legacy aggregate and must not be replaced by connector-driven runs.
- `docs/ideas.md` tracks completed and candidate tasks.
- `docs/commands.md` documents the current CLI surface.
- `docs/status.html` is a stable generated status page that points readers to live CLI reports.
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

Preview generated-document drift without writing files:

```bash
zany docs-diff
```

Regenerate every managed document when its renderer changes:

```bash
zany generate-docs
```

Confirm the generated files are current:

```bash
zany freshness
```

## Change rules

- Prefer one coherent task per session.
- Add or update tests when behavior changes.
- Keep generated files in sync with their renderers.
- Create one new immutable record under `docs/sessions/` after completed work.
- Never replace `docs/session-log.md` during connector-driven autonomous runs.
- Record the next smallest useful task for the following session.
