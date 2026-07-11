"""Primary CLI router for OpenAI Zany."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from . import backlog, cli, docs_diff, session_check, session_json

DOCS_DIFF_COMMAND = cli.CommandInfo(
    "docs-diff",
    "Preview generated-document changes without writing files.",
)
SESSIONS_JSON_COMMAND = cli.CommandInfo(
    "sessions-json",
    "Print structured session-log data as JSON.",
)
SESSION_LOG_CHECK_COMMAND = cli.CommandInfo(
    "session-log-check",
    "Validate the session log structure without modifying it.",
)
INTEGRATED_COMMANDS = (DOCS_DIFF_COMMAND, SESSIONS_JSON_COMMAND, SESSION_LOG_CHECK_COMMAND)


def registered_commands() -> tuple[cli.CommandInfo, ...]:
    """Return core commands plus commands routed by this module."""
    registered = list(cli.COMMANDS)
    known_names = {command.name for command in registered}
    registered.extend(command for command in INTEGRATED_COMMANDS if command.name not in known_names)
    return tuple(registered)


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


def sessions_json_parser() -> argparse.ArgumentParser:
    """Return the parser for the integrated sessions-json command."""
    parser = argparse.ArgumentParser(
        prog="zany sessions-json",
        description=SESSIONS_JSON_COMMAND.description,
    )
    parser.add_argument("--path", default=str(session_json.DEFAULT_LOG_PATH), help="Session-log path.")
    parser.add_argument("--limit", type=int, default=None, help="Maximum recent sessions to include.")
    return parser


def session_log_check_parser() -> argparse.ArgumentParser:
    """Return the parser for the integrated session-log-check command."""
    parser = argparse.ArgumentParser(
        prog="zany session-log-check",
        description=SESSION_LOG_CHECK_COMMAND.description,
    )
    parser.add_argument("--path", default=str(session_check.DEFAULT_LOG_PATH), help="Session-log path.")
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
    if arguments and arguments[0] == "next":
        print(backlog.next_report())
        return 0 if backlog.DEFAULT_IDEAS_PATH.is_file() else 1
    if arguments and arguments[0] == "list":
        print(backlog.list_report())
        return 0 if backlog.DEFAULT_IDEAS_PATH.is_file() else 1
    if arguments and arguments[0] == DOCS_DIFF_COMMAND.name:
        args = docs_diff_parser().parse_args(arguments[1:])
        return docs_diff.main(["--root", args.root, "--format", args.format])
    if arguments and arguments[0] == SESSIONS_JSON_COMMAND.name:
        args = sessions_json_parser().parse_args(arguments[1:])
        forwarded = ["--path", args.path]
        if args.limit is not None:
            forwarded.extend(["--limit", str(args.limit)])
        return session_json.main(forwarded)
    if arguments and arguments[0] == SESSION_LOG_CHECK_COMMAND.name:
        args = session_log_check_parser().parse_args(arguments[1:])
        return session_check.main(["--path", args.path, "--format", args.format])

    cli.COMMANDS = registered_commands()
    return cli.main(arguments)


if __name__ == "__main__":
    raise SystemExit(main())