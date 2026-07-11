"""Validate the repository session log structure."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Sequence
from pathlib import Path

DEFAULT_LOG_PATH = Path("docs/session-log.md")
DATE_HEADING = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _section_bullets(lines: list[str], heading: str) -> list[str]:
    """Return top-level bullets below a named body heading."""
    bullets: list[str] = []
    in_section = False
    for line in lines:
        stripped = line.strip()
        if stripped.endswith(":") and not line.startswith("- "):
            in_section = stripped == heading
            continue
        if in_section and line.startswith("- "):
            bullets.append(line[2:].strip())
    return bullets


def validate_session_log_text(markdown: str) -> list[str]:
    """Return human-readable structural problems in session-log Markdown."""
    lines = markdown.splitlines()
    errors: list[str] = []
    first_content = next((line.strip() for line in lines if line.strip()), "")
    if first_content != "# Session Log":
        errors.append("first non-empty line must be '# Session Log'")

    blocks: list[tuple[int, str, list[str]]] = []
    current_line = 0
    current_title: str | None = None
    current_body: list[str] = []
    for number, line in enumerate(lines, start=1):
        if line.startswith("## "):
            if current_title is not None:
                blocks.append((current_line, current_title, current_body))
            current_line = number
            current_title = line[3:].strip()
            current_body = []
        elif current_title is not None:
            current_body.append(line)
    if current_title is not None:
        blocks.append((current_line, current_title, current_body))

    if not blocks:
        errors.append("at least one '## YYYY-MM-DD' session entry is required")
        return errors

    for line_number, title, body in blocks:
        prefix = f"line {line_number} ({title or 'empty heading'})"
        if not DATE_HEADING.fullmatch(title):
            errors.append(f"{prefix}: heading must use YYYY-MM-DD")
        meaningful = [line.strip() for line in body if line.strip()]
        if not meaningful or meaningful[0] in {"Changes made:", "Notes:"}:
            errors.append(f"{prefix}: add a one-line session summary before sections")
        if "Changes made:" not in meaningful:
            errors.append(f"{prefix}: missing 'Changes made:' section")
        elif not _section_bullets(body, "Changes made:"):
            errors.append(f"{prefix}: 'Changes made:' must contain a top-level bullet")
        if "Notes:" not in meaningful:
            errors.append(f"{prefix}: missing 'Notes:' section")
        elif not _section_bullets(body, "Notes:"):
            errors.append(f"{prefix}: 'Notes:' must contain a top-level bullet")
    return errors


def session_log_check_result(path: Path | str = DEFAULT_LOG_PATH) -> dict[str, object]:
    """Return a stable machine-readable validation result."""
    log_path = Path(path)
    if not log_path.is_file():
        return {
            "path": str(log_path),
            "status": "missing",
            "valid": False,
            "errors": [f"expected session log at {log_path}"],
        }

    errors = validate_session_log_text(log_path.read_text(encoding="utf-8"))
    return {
        "path": str(log_path),
        "status": "valid" if not errors else "invalid",
        "valid": not errors,
        "errors": errors,
    }


def session_log_check_report(path: Path | str = DEFAULT_LOG_PATH) -> str:
    """Return a concise validation report for a session log."""
    result = session_log_check_result(path)
    if result["status"] == "missing":
        return f"Session log structure: MISSING\nExpected path: {result['path']}"
    if result["valid"]:
        return "Session log structure: VALID\nAll session entries follow the expected format."
    details = "\n".join(f"- {error}" for error in result["errors"])
    return f"Session log structure: INVALID\n{details}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="zany session-log-check",
        description="Validate docs/session-log.md structure without modifying it.",
    )
    parser.add_argument("--path", default=str(DEFAULT_LOG_PATH), help="Session-log path.")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. JSON is useful for automation.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = session_log_check_result(args.path)
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(session_log_check_report(args.path))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())