# Session Records

This directory is the canonical write target for new autonomous-session records.

Each completed session creates one new immutable Markdown file instead of replacing a shared log. This avoids history loss when a connector can create files safely but cannot patch or append to a large existing file.

## File naming

Use a sortable, collision-resistant name:

```text
YYYY-MM-DD-HHMMSS-short-slug.md
```

Use UTC unless the session explicitly records another timezone.

## Required structure

```markdown
# Session: Short summary

Date: YYYY-MM-DDTHH:MM:SSZ

## Changes made

- One or more concrete changes.

## Validation

- Tests, CI status, or an honest statement that validation was unavailable.

## Notes

- Work stayed inside `svicknesh/openai-zany`.
- Relevant limitations or risks.
- Next smallest useful task.
```

## Immutability

After creation, a session file should not normally be edited. Corrections belong in a new session file that references the earlier record.

## Legacy aggregate

`docs/session-log.md` is a legacy archive. Do not replace it during autonomous connector-driven runs. A later generator may rebuild an aggregate view from this directory plus the surviving legacy archive.
