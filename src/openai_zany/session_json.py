"""Machine-readable summaries for the OpenAI Zany session log."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_LOG_PATH = Path("docs/session-log.md")


def parse_sessions(log_text: str) -> list[dict[str, object]]:
    """Parse second-level session headings and top-level bullets."""
    sessions: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for line in log_text.splitlines():
        if line.startswith("## "):
            current = {"title": line.removeprefix("## ").strip(), "items": []}
            sessions.append(current)
        elif current is not None and line.startswith("- "):
            items = current["items"]
            assert isinstance(items, list)
            items.append(line.removeprefix("- ").strip())
    return sessions


def session_summary_data(log_path: Path | str = DEFAULT_LOG_PATH, limit: int | None = None) -> dict[str, object]:
    """Return a JSON-serializable session summary."""
    path = Path(log_path)
    if not path.is_file():
        return {"status": "missing", "path": str(path), "total_sessions": 0, "sessions": []}
    sessions = parse_sessions(path.read_text(encoding="utf-8"))
    selected = sessions if limit is None else sessions[:limit]
    return {
        "status": "ok" if sessions else "empty",
        "path": str(path),
        "total_sessions": len(sessions),
        "sessions": selected,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print the Zany session log as JSON.")
    parser.add_argument("--path", type=Path, default=DEFAULT_LOG_PATH, help="Session-log path.")
    parser.add_argument("--limit", type=int, default=None, help="Maximum recent sessions to include.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.limit is not None and args.limit < 0:
        raise SystemExit("--limit must be zero or greater")
    data = session_summary_data(args.path, args.limit)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0 if data["status"] != "missing" else 1


if __name__ == "__main__":
    raise SystemExit(main())
