"""Primary CLI router for OpenAI Zany."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from . import cli, docs_diff

DOCS_DIFF_COMMAND = cli.CommandInfo(
    "docs-diff",
    "Preview generated-document changes without writing files.",
)


def registered_commands() -> tuple[cli.CommandInfo, ...]:
    """Return core commands plus commands routed by this module."""
    if any(command.name == DOCS_DIFF_COMMAND.name for command in cli.COMMANDS):
        return cli.COMMANDS
    return (*cli.COMMANDS, DOCS_DIFF_COMMAND)


def docs_diff_parser() -> argparse.ArgumentParser:
    """Return the parser for the integrated docs-diff command."""
    parser = argparse.ArgumentParser(
        prog="zany docs-diff",
        description=DOCS_DIFF_COMMAND.description,
    )
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. JSON is useful for automation.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Route integrated commands, then delegate established commands."""
    arguments = list(argv) if argv is not None else sys.argv[1:]
    if arguments and arguments[0] == DOCS_DIFF_COMMAND.name:
        args = docs_diff_parser().parse_args(arguments[1:])
        return docs_diff.main(["--root", args.root, "--format", args.format])

    cli.COMMANDS = registered_commands()
    return cli.main(arguments)


if __name__ == "__main__":
    raise SystemExit(main())
