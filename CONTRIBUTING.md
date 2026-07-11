# Contributing

Keep changes small, auditable, and easy to reverse.

## Before editing

- Choose one coherent task that can be completed in a short session.
- Read `AGENTS.md`, `README.md`, and the latest entry in `docs/session-log.md`.
- Confirm the change stays inside this repository and does not require secrets.

## While editing

- Prefer the smallest implementation that solves the stated problem.
- Add or update focused tests when behavior changes.
- Avoid unrelated cleanup, broad refactors, and generated-file hand edits.
- Keep public commands and documentation consistent.

## Before stopping

- Run `pytest`.
- Run `zany generate-docs` after changing generated-document inputs.
- Run `zany freshness` and confirm it reports `CURRENT`.
- Review the diff for accidental, secret, or unrelated changes.
- Update `docs/session-log.md` with the task, validation, limitations, and next useful step.

## Commit quality

- Use a concise imperative commit message.
- Keep each commit limited to one understandable change where practical.
- Do not claim tests passed unless they were actually executed.
