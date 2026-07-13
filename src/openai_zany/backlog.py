"""File-backed task backlog helpers for bounded work sessions."""

from __future__ import annotations

from pathlib import Path

DEFAULT_IDEAS_PATH = Path("docs/ideas.md")
CANDIDATE_HEADING = "Candidate tasks"
BULLET_MARKERS = ("- ", "* ", "+ ")


def section_bullets(markdown: str, heading: str) -> list[str]:
    """Return non-empty top-level bullets below a second-level Markdown heading."""
    bullets: list[str] = []
    in_section = False
    in_nested_section = False
    for line in markdown.splitlines():
        if line.startswith("# "):
            in_section = False
            in_nested_section = False
            continue
        if line.startswith("## "):
            in_section = line.removeprefix("## ").strip() == heading
            in_nested_section = False
            continue
        if in_section and line.startswith("###") and line.lstrip("#").startswith(" "):
            in_nested_section = True
            continue
        if in_section and not in_nested_section:
            marker = next((candidate for candidate in BULLET_MARKERS if line.startswith(candidate)), None)
            if marker is not None:
                bullet = line.removeprefix(marker).strip()
                if bullet:
                    bullets.append(bullet)
    return bullets


def candidate_tasks(ideas_path: Path | str = DEFAULT_IDEAS_PATH) -> list[str]:
    """Return candidate tasks from the maintained ideas document."""
    path = Path(ideas_path)
    if not path.is_file():
        return []
    return section_bullets(path.read_text(encoding="utf-8"), CANDIDATE_HEADING)


def list_report(ideas_path: Path | str = DEFAULT_IDEAS_PATH) -> str:
    """Return the maintained candidate backlog as display text."""
    path = Path(ideas_path)
    if not path.is_file():
        return f"Idea backlog: MISSING\nExpected path: {path}"
    tasks = candidate_tasks(path)
    if not tasks:
        return f"Idea backlog: EMPTY\nPath: {path}"
    return "\n".join(f"- {task}" for task in tasks)


def next_report(ideas_path: Path | str = DEFAULT_IDEAS_PATH) -> str:
    """Return the first maintained candidate task."""
    path = Path(ideas_path)
    if not path.is_file():
        return f"Idea backlog: MISSING\nExpected path: {path}"
    tasks = candidate_tasks(path)
    if not tasks:
        return f"Idea backlog: EMPTY\nPath: {path}"
    return f"Next idea: {tasks[0]}"
