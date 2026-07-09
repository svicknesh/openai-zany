# OpenAI Zany

Bounded experimental workspace for assistant-built utilities.

Rules:

1. Work only in this repository: svicknesh/openai-zany.
2. Spend at most 30 minutes per session. If a coherent task is already in progress, finish that task, then stop.

## Usage

Install locally with developer dependencies:

```bash
python -m pip install -e '.[dev]'
```

Run the current CLI helpers:

```bash
zany next
zany list
zany doctor
```

Run tests:

```bash
pytest
```

## Current CLI commands

- `zany next` shows the next small candidate task.
- `zany list` shows the current idea backlog.
- `zany doctor` checks whether the expected scaffold files are present.
