import json

from openai_zany.session_json import main, parse_session_record, parse_sessions, session_summary_data


def test_parse_sessions_extracts_titles_and_top_level_bullets():
    text = "# Session Log\n\n## First\n\n- Added one\n  - nested\n\n## Second\n\n- Added two\n"
    assert parse_sessions(text) == [
        {"title": "First", "items": ["Added one"]},
        {"title": "Second", "items": ["Added two"]},
    ]


def test_parse_session_record_extracts_title_and_bullets():
    text = (
        "# Session: Add directory support\n\n"
        "Date: 2026-07-12T02:48:00Z\n\n"
        "## Changes made\n\n- Added one\n  - nested\n\n"
        "## Validation\n\n- Tests passed\n"
    )
    assert parse_session_record(text) == {
        "title": "Add directory support",
        "items": ["Added one", "Tests passed"],
    }


def test_session_summary_data_applies_limit(tmp_path):
    path = tmp_path / "session-log.md"
    path.write_text("# Session Log\n\n## First\n- One\n\n## Second\n- Two\n", encoding="utf-8")
    data = session_summary_data(path, limit=1)
    assert data["status"] == "ok"
    assert data["total_sessions"] == 2
    assert data["sessions"] == [{"title": "First", "items": ["One"]}]


def test_session_summary_data_reads_directory_newest_first(tmp_path):
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    (sessions / "README.md").write_text("# Session Records\n", encoding="utf-8")
    (sessions / "2026-07-11-120000-first.md").write_text(
        "# Session: First\n\n## Changes made\n\n- Older\n",
        encoding="utf-8",
    )
    (sessions / "2026-07-12-120000-second.md").write_text(
        "# Session: Second\n\n## Changes made\n\n- Newer\n",
        encoding="utf-8",
    )
    data = session_summary_data(sessions, limit=1)
    assert data["status"] == "ok"
    assert data["total_sessions"] == 2
    assert data["sessions"] == [{"title": "Second", "items": ["Newer"]}]


def test_session_summary_data_ignores_invalid_directory_records(tmp_path):
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    (sessions / "invalid.md").write_text("# Not a session\n", encoding="utf-8")
    data = session_summary_data(sessions)
    assert data["status"] == "empty"
    assert data["sessions"] == []


def test_session_summary_data_reports_missing_file(tmp_path):
    data = session_summary_data(tmp_path / "missing.md")
    assert data["status"] == "missing"
    assert data["total_sessions"] == 0
    assert data["sessions"] == []


def test_main_prints_json(tmp_path, capsys):
    path = tmp_path / "session-log.md"
    path.write_text("# Session Log\n\n## First\n- One\n", encoding="utf-8")
    assert main(["--path", str(path), "--limit", "1"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["sessions"][0]["title"] == "First"
