# Session: Default changelog to append-only records

Date: 2026-07-12T11:20:00+08:00

## Changes made

- Added `openai_zany.session_reports` for append-only and legacy human-readable session reporting.
- Routed `zany changelog` through `docs/sessions/` by default.
- Preserved reusable legacy-log changelog support.
- Added focused tests for ordering, legacy compatibility, invalid records, and primary CLI routing.
- Updated README usage and smoke-test documentation.

## Validation

- Focused tests were added for the new behavior.
- GitHub Actions will execute the full suite and generated-document freshness check.

## Next useful task

- Migrate the status-page renderer and generated-document freshness pipeline to append-only session records.
