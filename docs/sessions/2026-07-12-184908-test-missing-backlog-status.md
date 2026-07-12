# Session: Test missing backlog command status

Date: 2026-07-12T18:49:08Z

## Changes made

- Added focused regression coverage for the `zany next` and `zany list` exit status when the maintained ideas file is missing.
- Verified both commands report the missing backlog path and return status 1.

## Validation

- Reviewed the parameterized test against the current primary CLI routing behavior.
- Full test execution was unavailable through the repository connector.
- No managed-document renderer or generated document changed, so regeneration was not required.

## Notes

- Work stayed inside `svicknesh/openai-zany`.
- `docs/session-log.md` was not modified.
- The change is isolated, reversible, and adds no runtime behavior.
