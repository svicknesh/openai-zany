"""Command-line entry point for OpenAI Zany."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from html import escape
from pathlib import Path


@dataclass(frozen=True)
class Idea:
    """A small candidate task for a bounded work session."""

    title: str
    reason: str


@dataclass(frozen=True)
class CommandInfo:
    """Documented CLI command."""

    name: str
    description: str


IDEAS: tuple[Idea, ...] = (
    Idea("session log helper", "Keep autonomous work auditable."),
    Idea("tiny static status page", "Make the repo browsable without infrastructure."),
    Idea("repo health check", "Catch missing files and stale notes."),
)

COMMANDS: tuple[CommandInfo, ...] = (
    CommandInfo("next", "Show the next small candidate task."),
    CommandInfo("list", "Show the current idea backlog."),
    CommandInfo("doctor", "Check whether expected scaffold files are present."),
    CommandInfo("sessions", "Summarize the session log and latest recorded session."),
    CommandInfo("changelog", "Generate a compact changelog from recent session-log entries."),
    CommandInfo("status-page", "Write docs/status.html from the session log."),
    CommandInfo("commands", "Print this command reference as Markdown."),
    CommandInfo("roadmap", "Show completed and candidate tasks from docs/ideas.md."),
)

EXPECTED_FILES: tuple[str, ...] = (
    "README.md",
    "AGENTS.md",
    "pyproject.toml",
    "src/openai_zany/__init__.py",
    "src/openai_zany/cli.py",
    "tests/test_cli.py",
    "docs/session-log.md",
    "docs/ideas.md",
    "docs/development.md",
    "docs/status.html",
    "docs/commands.md",
)

SESSION_LOG_PATH = Path("docs/session-log.md")
STATUS_PAGE_PATH = Path("docs/status.html")
IDEAS_PATH = Path("docs/ideas.md")


def list_ideas() -> str:
    """Return all current project ideas as display text."""
    return "\n".join(f"- {idea.title}: {idea.reason}" for idea in IDEAS)


def next_idea() -> str:
    """Return the next small project idea."""
    idea = IDEAS[0]
    return f"{idea.title}: {idea.reason}"


def command_names() -> tuple[str, ...]:
    """Return supported command names."""
    return tuple(command.name for command in COMMANDS)


def command_reference() -> str:
    """Return a Markdown command reference table."""
    rows = ["# Commands", "", "| Command | Description |", "| --- | --- |"]
    rows.extend(f"| `zany {command.name}` | {command.description} |" for command in COMMANDS)
    return "\n".join(rows)


def markdown_section_bullets(markdown: str, heading: str) -> list[str]:
    """Return top-level bullets below a second-level heading."""
    bullets: list[str] = []
    in_section = False

    for line in markdown.splitlines():
        if line.startswith("## "):
            in_section = line.removeprefix("## ").strip() == heading
            continue
        if in_section and line.startswith("- "):
            bullets.append(line.removeprefix("- ").strip())

    return bullets


def roadmap_report(ideas_path: Path | str = IDEAS_PATH) -> str:
    """Return completed and candidate tasks from the project ideas document."""
    path = Path(ideas_path)
    if not path.is_file():
        return f"Roadmap: MISSING\nExpected path: {path}"

    markdown = path.read_text(encoding="utf-8")
    completed = markdown_section_bullets(markdown, "Completed")
    candidates = markdown_section_bullets(markdown, "Candidate tasks")

    lines = ["# Roadmap", "", "## Completed"]
    lines.extend(f"- {item}" for item in completed or ["No completed tasks recorded."])
    lines.extend(["", "## Candidate tasks"])
    lines.extend(f"- {item}" for item in candidates or ["No candidate tasks recorded."])
    return "\n".join(lines)


def missing_expected_files(root: Path | str = ".") -> list[str]:
    """Return expected project files that are missing below root."""
    project_root = Path(root)
    return [path for path in EXPECTED_FILES if not (project_root / path).is_file()]


def doctor_report(root: Path | str = ".") -> str:
    """Return a short repository health report."""
    missing = missing_expected_files(root)

    if not missing:
        return "Repository health: OK\nAll expected files are present."

    missing_lines = "\n".join(f"- {path}" for path in missing)
    return f"Repository health: ATTENTION\nMissing expected files:\n{missing_lines}"


def session_titles(log_text: str) -> list[str]:
    """Return second-level Markdown headings from the session log."""
    return [line.removeprefix("## ").strip() for line in log_text.splitlines() if line.startswith("## ")]


def session_summary(log_path: Path | str = SESSION_LOG_PATH) -> str:
    """Return a short summary of recorded work sessions."""
    path = Path(log_path)

    if not path.is_file():
        return f"Session log: MISSING\nExpected path: {path}"

    titles = session_titles(path.read_text(encoding="utf-8"))

    if not titles:
        return f"Session log: EMPTY\nPath: {path}"

    return f"Session log: OK\nTotal sessions: {len(titles)}\nLatest session: {titles[0]}"


def session_blocks(log_text: str) -> list[tuple[str, list[str]]]:
    """Return session headings and their body lines from a Markdown session log."""
    blocks: list[tuple[str, list[str]]] = []
    current_title: str | None = None
    current_lines: list[str] = []

    for line in log_text.splitlines():
        if line.startswith("## "):
            if current_title is not None:
                blocks.append((current_title, current_lines))
            current_title = line.removeprefix("## ").strip()
            current_lines = []
            continue

        if current_title is not None:
            current_lines.append(line)

    if current_title is not None:
        blocks.append((current_title, current_lines))

    return blocks


def bullet_lines(lines: list[str]) -> list[str]:
    """Return top-level Markdown bullet lines without the bullet marker."""
    return [line.removeprefix("- ").strip() for line in lines if line.startswith("- ")]


def changelog_report(log_path: Path | str = SESSION_LOG_PATH, limit: int = 5) -> str:
    """Return a compact changelog generated from recent session-log entries."""
    path = Path(log_path)

    if not path.is_file():
        return f"Changelog: MISSING\nExpected path: {path}"

    blocks = session_blocks(path.read_text(encoding="utf-8"))

    if not blocks:
        return f"Changelog: EMPTY\nPath: {path}"

    sections: list[str] = ["# Changelog", ""]
    for title, lines in blocks[:limit]:
        sections.append(f"## {title}")
        bullets = bullet_lines(lines)

        if bullets:
            sections.extend(f"- {bullet}" for bullet in bullets[:6])
        else:
            sections.append("- No bullet summary recorded.")

        sections.append("")

    return "\n".join(sections).rstrip()


def status_page_html(log_path: Path | str = SESSION_LOG_PATH) -> str:
    """Return a static HTML status page for the repository."""
    summary = session_summary(log_path)
    changelog = changelog_report(log_path, limit=3)
    summary_html = "<br>".join(escape(line) for line in summary.splitlines())
    changelog_html = escape(changelog)

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>OpenAI Zany Status</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 840px; margin: 3rem auto; padding: 0 1rem; line-height: 1.5; }}
    code, pre {{ background: #f6f8fa; border-radius: 0.4rem; }}
    pre {{ padding: 1rem; overflow-x: auto; }}
    .card {{ border: 1px solid #d0d7de; border-radius: 0.75rem; padding: 1rem; margin: 1rem 0; }}
  </style>
</head>
<body>
  <h1>OpenAI Zany Status</h1>
  <p>Generated from the repository session log.</p>
  <section class=\"card\">
    <h2>Session Summary</h2>
    <p>{summary_html}</p>
  </section>
  <section class=\"card\">
    <h2>Recent Changelog</h2>
    <pre>{changelog_html}</pre>
  </section>
</body>
</html>
"""


def write_status_page(output_path: Path | str = STATUS_PAGE_PATH, log_path: Path | str = SESSION_LOG_PATH) -> Path:
    """Write the static status page and return its path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(status_page_html(log_path), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="zany", description="Small utilities for the OpenAI Zany workspace.")
    parser.add_argument("command", choices=command_names(), help="Command to run.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "next":
        print(next_idea())
        return 0

    if args.command == "list":
        print(list_ideas())
        return 0

    if args.command == "doctor":
        print(doctor_report())
        return 0 if not missing_expected_files() else 1

    if args.command == "sessions":
        print(session_summary())
        return 0 if SESSION_LOG_PATH.is_file() else 1

    if args.command == "changelog":
        print(changelog_report())
        return 0 if SESSION_LOG_PATH.is_file() else 1

    if args.command == "status-page":
        path = write_status_page()
        print(f"Wrote status page: {path}")
        return 0

    if args.command == "commands":
        print(command_reference())
        return 0

    if args.command == "roadmap":
        print(roadmap_report())
        return 0 if IDEAS_PATH.is_file() else 1

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
