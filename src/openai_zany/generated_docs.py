"""Stable generated documentation for OpenAI Zany."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from . import cli

COMMANDS_PATH = Path("docs/commands.md")
STATUS_PAGE_PATH = Path("docs/status.html")

INTEGRATED_COMMANDS: tuple[cli.CommandInfo, ...] = (
    cli.CommandInfo("docs-diff", "Preview generated-document changes without writing files."),
    cli.CommandInfo("sessions-json", "Print structured session-record data as JSON."),
    cli.CommandInfo("session-log-check", "Validate the session log structure without modifying it."),
)


@dataclass(frozen=True)
class GeneratedDocument:
    """A generated repository document and its renderer."""

    path: Path
    render: Callable[[], str]


def documented_commands() -> tuple[cli.CommandInfo, ...]:
    """Return core and integrated commands exactly once."""
    commands = list(cli.COMMANDS)
    known_names = {command.name for command in commands}
    commands.extend(command for command in INTEGRATED_COMMANDS if command.name not in known_names)
    return tuple(commands)


def command_reference() -> str:
    """Return the complete Markdown command reference."""
    rows = ["# Commands", "", "| Command | Description |", "| --- | --- |"]
    rows.extend(f"| `zany {command.name}` | {command.description} |" for command in documented_commands())
    return "\n".join(rows)


def status_page_html() -> str:
    """Return a stable status page that does not drift after each session record."""
    return """<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>OpenAI Zany Status</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 840px; margin: 3rem auto; padding: 0 1rem; line-height: 1.5; }
    code, pre { background: #f6f8fa; border-radius: 0.4rem; }
    code { padding: 0.15rem 0.35rem; }
    pre { padding: 1rem; overflow-x: auto; }
    .card { border: 1px solid #d0d7de; border-radius: 0.75rem; padding: 1rem; margin: 1rem 0; }
  </style>
</head>
<body>
  <h1>OpenAI Zany Status</h1>
  <p>This repository uses append-only session records so autonomous work cannot truncate shared history.</p>
  <section class=\"card\">
    <h2>Live repository reports</h2>
    <pre>zany sessions
zany sessions-json --limit 5
zany changelog
zany freshness</pre>
  </section>
  <section class=\"card\">
    <h2>Session source</h2>
    <p>Canonical records live under <code>docs/sessions/</code>. The legacy <code>docs/session-log.md</code> file is retained for compatibility and must not be replaced by autonomous connector runs.</p>
  </section>
</body>
</html>
"""


def generated_documents() -> tuple[GeneratedDocument, ...]:
    """Return all managed generated documents."""
    return (
        GeneratedDocument(COMMANDS_PATH, command_reference),
        GeneratedDocument(STATUS_PAGE_PATH, status_page_html),
    )


def write_generated_documents(root: Path | str = ".") -> list[Path]:
    """Write all managed generated documents below root."""
    project_root = Path(root)
    written: list[Path] = []
    for document in generated_documents():
        path = project_root / document.path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(document.render(), encoding="utf-8")
        written.append(path)
    return written


def stale_generated_documents(root: Path | str = ".") -> list[str]:
    """Return managed documents that are missing or stale."""
    project_root = Path(root)
    stale: list[str] = []
    for document in generated_documents():
        path = project_root / document.path
        if not path.is_file() or path.read_text(encoding="utf-8") != document.render():
            stale.append(str(document.path))
    return stale


def freshness_report(root: Path | str = ".") -> str:
    """Return a generated-document freshness report."""
    stale = stale_generated_documents(root)
    if not stale:
        return "Generated documentation: CURRENT\nAll generated documents are up to date."
    lines = "\n".join(f"- {path}" for path in stale)
    return f"Generated documentation: STALE\nRegenerate these files:\n{lines}"
