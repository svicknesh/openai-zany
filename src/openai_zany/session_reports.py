"""Human-readable reports for append-only session records."""

from __future__ import annotations

from pathlib import Path

DEFAULT_SESSIONS_PATH = Path("docs/sessions")
LEGACY_LOG_PATH = Path("docs/session-log.md")


def _record_title_and_items(record_text: str) -> tuple[str, list[str]] | None:
    """Parse one append-only record into a title and top-level bullets."""
    title: str | None = None
    items: list[str] = []
    for line in record_text.splitlines():
        if title is None and line.startswith("# Session: "):
            title = line.removeprefix("# Session: ").strip()
        elif line.startswith("- "):
            items.append(line.removeprefix("- ").strip())
    if not title:
        return None
    return title, items


def _legacy_blocks(log_text: str) -> list[tuple[str, list[str]]]:
    """Parse legacy aggregate session-log entries."""
    blocks: list[tuple[str, list[str]]] = []
    title: str | None = None
    items: list[str] = []
    for line in log_text.splitlines():
        if line.startswith("## "):
            if title is not None:
                blocks.append((title, items))
            title = line.removeprefix("## ").strip()
            items = []
        elif title is not None and line.startswith("- "):
            items.append(line.removeprefix("- ").strip())
    if title is not None:
        blocks.append((title, items))
    return blocks


def session_entries(path: Path | str = DEFAULT_SESSIONS_PATH) -> list[tuple[str, list[str]]]:
    """Return session entries from an append-only directory or legacy file."""
    source = Path(path)
    if not source.exists():
        return []
    if source.is_file():
        return _legacy_blocks(source.read_text(encoding="utf-8"))

    entries: list[tuple[str, list[str]]] = []
    for record_path in sorted(source.glob("*.md"), reverse=True):
        if record_path.name.casefold() == "readme.md":
            continue
        parsed = _record_title_and_items(record_path.read_text(encoding="utf-8"))
        if parsed is not None:
            entries.append(parsed)
    return entries


def changelog_report(path: Path | str = DEFAULT_SESSIONS_PATH, limit: int = 5) -> str:
    """Return a compact Markdown changelog from session records."""
    source = Path(path)
    if not source.exists():
        return f"Changelog: MISSING\nExpected path: {source}"

    entries = session_entries(source)
    if not entries:
        return f"Changelog: EMPTY\nPath: {source}"

    lines = ["# Changelog", ""]
    for title, items in entries[:limit]:
        lines.append(f"## {title}")
        if items:
            lines.extend(f"- {item}" for item in items[:6])
        else:
            lines.append("- No bullet summary recorded.")
        lines.append("")
    return "\n".join(lines).rstrip()
