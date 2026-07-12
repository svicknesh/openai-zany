import re
from pathlib import Path


SESSIONS_PATH = Path("docs/sessions")
SESSION_FILENAME = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{6}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


def test_committed_session_records_are_canonical_and_sortable():
    records = sorted(path for path in SESSIONS_PATH.glob("*.md") if path.name.casefold() != "readme.md")

    assert records, "expected at least one immutable session record"
    for record in records:
        assert SESSION_FILENAME.fullmatch(record.name), f"non-canonical session filename: {record.name}"
        first_line = record.read_text(encoding="utf-8").splitlines()[0]
        assert first_line.startswith("# Session: "), f"missing canonical session title: {record.name}"
