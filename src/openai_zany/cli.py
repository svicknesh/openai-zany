"""Command-line entry point for OpenAI Zany."""

from __future__ import annotations

import argparse
from dataclasses import dataclass


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


def list_ideas() -> str:
    """Return all current project ideas as display text."""
    return "\n".join(f"- {idea.title}: {idea.reason}" for idea in IDEAS)


def next_idea() -> str:
    """Return the next small project idea."""
    idea = IDEAS[0]
    return f"{idea.title}: {idea.reason}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="zany", description="Small utilities for the OpenAI Zany workspace.")
    parser.add_argument("command", choices=("next", "list"), help="Command to run.")
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

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
