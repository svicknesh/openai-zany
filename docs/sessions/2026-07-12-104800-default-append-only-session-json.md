# Session: Default machine-readable summaries to append-only records

Date: 2026-07-12T10:48:00+08:00

## Changes made

- Changed `openai_zany.session_json.DEFAULT_LOG_PATH` from `docs/session-log.md` to `docs/sessions`.
- Kept explicit legacy-log access through `--path docs/session-log.md`.
- Updated primary CLI routing coverage to expect the append-only directory default.
- Updated README usage, compatibility, and session-record documentation.

## Validation

- Existing directory parsing and ordering tests cover the append-only storage format.
- Primary CLI routing now has a regression assertion for `docs/sessions`.
- Managed document renderers were not changed, so `docs/commands.md` and `docs/status.html` should remain current.

## Notes

- Work stayed inside `svicknesh/openai-zany`.
- The legacy aggregate log was not modified.
- Next useful task: migrate human-readable `zany sessions`, changelog, and status-page generation to the append-only session directory.
