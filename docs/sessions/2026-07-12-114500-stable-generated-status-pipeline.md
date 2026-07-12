# Session: Stabilize generated documentation for append-only sessions

Date: 2026-07-12T11:45:00+08:00

## Changes made

- Added `openai_zany.generated_docs` as the stable generated-document pipeline.
- Replaced the session-dependent status page with a stable page that points to live CLI reports.
- Routed `zany status-page`, `zany freshness`, and `zany generate-docs` through the new pipeline.
- Updated `zany docs-diff` to use the same generated-document source.
- Added regression tests proving that a new append-only session record does not make generated docs stale.
- Updated README documentation.

## Validation

- Generated `docs/status.html` now matches the stable renderer.
- Focused tests were added for the new pipeline and docs-diff integration.
- GitHub Actions will run the complete test suite and freshness check.

## Next useful task

- Migrate or retire remaining legacy session-log validation paths that assume one mutable aggregate file.
