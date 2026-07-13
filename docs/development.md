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

## CLI compatibility boundary

- The installed `zany` command enters through `openai_zany.main_cli:main`, as declared in `pyproject.toml`.
- `main_cli` owns routing for the maintained backlog-backed `next` and `list` commands before delegating established commands to `openai_zany.cli`.
- The legacy `Idea`, `IDEAS`, `next_idea()`, and `list_ideas()` objects in `openai_zany.cli` are internal leftovers rather than part of the installed CLI contract.
- Removing those leftovers should preserve the `next` and `list` command metadata in `cli.COMMANDS` because the primary parser and generated command reference still use that shared registry.
- Direct imports of the legacy helpers are not covered by the documented public interface; removal should nevertheless include a focused test that the installed router continues to serve backlog-backed `next` and `list` output.

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