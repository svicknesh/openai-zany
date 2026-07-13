# Session: Document CLI compatibility boundary

Date: 2026-07-13T06:45:26Z

## Changes made

- Added a CLI compatibility-boundary section to `docs/development.md`.
- Recorded that the installed `zany` entry point is `openai_zany.main_cli:main` and that backlog-backed `next` and `list` routing occurs there.
- Identified the legacy hard-coded idea objects in `openai_zany.cli` as internal leftovers and documented the command metadata and regression coverage that must be preserved when they are removed.

## Validation

- Reviewed `pyproject.toml`, `src/openai_zany/main_cli.py`, `src/openai_zany/cli.py`, and the current CLI tests to confirm the documented routing and compatibility boundary.
- GitHub reported no combined status checks or workflow runs for the pre-change commit, so CI status was unknown rather than confirmed passing.
- This was a documentation-only change; runtime behavior and managed-document renderer inputs were unchanged, so tests and generated-document regeneration were not required.

## Notes

- Work stayed inside `svicknesh/openai-zany`.
- `docs/session-log.md` was not modified.
- The next smallest useful task is to remove `Idea`, `IDEAS`, `next_idea()`, and `list_ideas()` from `openai_zany.cli` while retaining `next` and `list` command metadata and router-level regression coverage.