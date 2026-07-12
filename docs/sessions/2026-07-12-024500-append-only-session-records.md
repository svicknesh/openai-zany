# Session: Append-only session records

Date: 2026-07-12T02:45:00Z

## Changes made

- Added `docs/sessions/README.md` as the canonical session-record specification.
- Changed autonomous guidance to create one immutable file per completed session.
- Reclassified `docs/session-log.md` as a legacy archive that connector-driven runs must not replace.
- Updated the autonomous checklist and README documentation.

## Validation

- Changes are documentation and operating-model updates; no application behavior or generated document changed.
- Existing GitHub Actions remains configured to run `pytest` and `zany freshness`.

## Notes

- Work stayed inside `svicknesh/openai-zany`.
- The append-only model removes the full-file replacement failure mode that truncated historical session records.
- Next smallest useful task: update session-reading commands to aggregate `docs/sessions/*.md` with the legacy archive.
