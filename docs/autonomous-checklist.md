# Autonomous Session Checklist

Use this checklist before ending any assistant-driven work session in this repository.

## Preflight

- Confirm the latest known CI state is not failing.
- Confirm managed documentation is not known to be stale.
- If either state cannot support a safe bounded change, make no repository changes.
- Do not manufacture work merely to produce a session record.

## Scope

- Work stayed inside `svicknesh/openai-zany`.
- The task was small enough to inspect.
- The change is reversible without affecting external systems.
- No secrets, credentials, tokens, private data, or production integrations were added.

## Quality

- Code changes include tests where practical.
- Documentation was updated when behavior or usage changed.
- Generated files were refreshed when their source changed.
- The repository should remain installable with `python -m pip install -e '.[dev]'`.

## Before stopping

- Create one new immutable session record under `docs/sessions/` using `docs/sessions/README.md`.
- Do not replace `docs/session-log.md` during connector-driven autonomous work.
- Note any test or CI result that is known.
- Record the next smallest useful task.
- Stop after the coherent task is complete.
