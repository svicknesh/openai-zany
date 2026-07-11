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
- Run `zany-docs-diff` before regeneration to review exactly what managed documentation will change.
- Use `zany-docs-diff --format json` when a machine-readable review artifact is useful.
- Run `zany generate-docs` after changing generated-document inputs.
- Run `zany freshness` and confirm it reports `CURRENT`.
- Review the final diff for accidental, secret, or unrelated changes.
- Update `docs/session-log.md` with the task, validation, limitations, and next useful step.

## Generated-document sequence

Use this order so generated changes remain inspectable rather than appearing as unexplained file churn:

```bash
zany-docs-diff
zany generate-docs
zany freshness
```

The first command is read-only and exits with status 1 when it finds pending changes. That status means regeneration is required; it is not an execution failure.

## Commit quality

- Use a concise imperative commit message.
- Keep each commit limited to one understandable change where practical.
- Do not claim tests passed unless they were actually executed.
