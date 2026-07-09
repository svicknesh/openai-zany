"""Command-line entry point for OpenAI Zany."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Idea:
    """A small candidate task for a bounded work session."""

    title: str
    reason: str


IDEAS: tuple[Idea, ...] = (
    Idea("session log helper", "Keep autonomous work auditable."),
    Idea("tiny static status page", "Make the repo browsable without infrastructure."),
    Idea("repo health check", "Catch missing files and stale notes."),
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
)

SESSION_LOG_PATH = Path("docs/session-log.md")


def list_ideas() -> str:
    """Return all current project ideas as display text."""
    return "\n".join(f"- {idea.title}: {idea.reason}" for idea in IDEAS)


def next_idea() -> str:
    """Return the next small project idea."""
    idea = IDEAS[0]
    return f"{idea.title}: {idea.reason}"


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="zany", description="Small utilities for the OpenAI Zany workspace.")
    parser.add_argument("command", choices=("next", "list", "doctor", "sessions"), help="Command to run.")
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

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
