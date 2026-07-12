# Agent Instructions

This repository is the only allowed workspace for assistant-driven changes.

## Hard limits

- Work only in `svicknesh/openai-zany`.
- Limit active work to 30 minutes per session.
- If the limit is reached while a coherent task is already underway, finish that task, record the result, then stop.
- Do not add secrets, credentials, tokens, private data, or external production integrations.

## Working style

- Prefer small changes that are easy to inspect.
- Keep the project runnable after each change.
- Add or update tests when behavior changes.
- Record meaningful work by creating one new immutable file under `docs/sessions/`.
- Follow the naming and structure rules in `docs/sessions/README.md`.
- Treat `docs/session-log.md` as a legacy archive; do not replace it during connector-driven autonomous work.
