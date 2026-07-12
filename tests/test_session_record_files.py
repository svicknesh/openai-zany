import re
from datetime import datetime
from pathlib import Path


SESSIONS_PATH = Path("docs/sessions")
SESSION_FILENAME = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{6}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


def test_committed_session_records_are_canonical_and_sortable():
    records = sorted(path for path in SESSIONS_PATH.glob("*.md") if path.name.casefold() != "readme.md")

    assert records, "expected at least one immutable session record"
    for record in records:
        assert SESSION_FILENAME.fullmatch(record.name), f"non-canonical session filename: {record.name}"

        lines = record.read_text(encoding="utf-8").splitlines()
        assert lines[0].startswith("# Session: "), f"missing canonical session title: {record.name}"

        filename_timestamp = datetime.strptime(record.name[:17], "%Y-%m-%d-%H%M%S")
        date_line = next((line for line in lines if line.startswith("Date: ")), None)
        assert date_line is not None, f"missing session date: {record.name}"
        recorded_timestamp = datetime.strptime(date_line.removeprefix("Date: "), "%Y-%m-%dT%H:%M:%SZ")
        assert recorded_timestamp == filename_timestamp, f"session date does not match filename: {record.name}"
