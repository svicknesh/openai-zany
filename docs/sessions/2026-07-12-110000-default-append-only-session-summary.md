# Session: Default human session summary to append-only records

Date: 2026-07-12T11:00:00+08:00

## Changes made

- Changed `zany sessions` to read `docs/sessions/` by default.
- Added append-only session-title parsing ordered by sortable filename, newest first.
- Preserved direct legacy-file support through the reusable `session_summary(path)` function.
- Added focused tests for append-only title parsing and directory summary output.
- Updated README usage and migration notes.

## Validation

- The implementation and focused tests were reviewed through the GitHub connector.
- GitHub Actions will run the full test suite and generated-document freshness check on push.
- No generated renderer output changed, so managed documentation was not regenerated.

## Next useful task

- Migrate `zany changelog` to aggregate append-only session records by default.
