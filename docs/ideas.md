# Ideas

Small tasks suitable for bounded sessions.

## Completed

- Added `zany doctor` to check expected files.
- Added GitHub Actions for Python tests.
- Added `zany sessions` to summarize the session log.
- Added `zany changelog` to generate a compact changelog from the session log.
- Added `zany status-page` and `docs/status.html` for a static repository status view.
- Added `zany commands` and `docs/commands.md` for CLI command reference.
- Added `docs/autonomous-checklist.md` for future autonomous session quality gates.
- Added `docs/development.md` to explain the repository structure and local workflow.
- Added `zany roadmap` to show completed and candidate tasks from `docs/ideas.md`.
- Added `docs/release-notes-template.md` for consistent, auditable release summaries.
- Added the release notes template to the `zany doctor` repository health check.
- Added a read-only CLI smoke-test procedure to the README.
- Added `zany freshness` to detect missing or stale generated documentation.
- Added CI coverage for generated documentation freshness.
- Added `zany generate-docs` to regenerate every managed document in one step.
- Added `CONTRIBUTING.md` with a compact change checklist.
- Added `zany-sessions-json` for machine-readable session summaries.
- Added `zany-docs-diff` to preview generated-document changes without writing files.
- Routed `zany next` and `zany list` to the maintained candidate backlog in this file.
- Added `zany session-log-check` to validate session-log structure without modifying it.
- Added JSON output to `zany session-log-check` for CI and editor integrations.
- Added `sessions-json` and `docs-diff` to the read-only CLI smoke test.
- Documented `session-log-check` and why it is not yet in the passing smoke test or CI.

## Candidate tasks

- Repair or migrate the incomplete legacy session-log tail, then add `session-log-check` to the read-only CLI smoke test.
- Remove the obsolete hard-coded idea records from `openai_zany.cli` after compatibility review.
- Add `session-log-check` to CI after the historical log satisfies the validator.

## Selection rule

Choose tasks that can be completed, tested, and logged in one short session.
