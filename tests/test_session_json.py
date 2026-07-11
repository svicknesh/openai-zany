import json

from openai_zany.session_json import main, parse_sessions, session_summary_data


def test_parse_sessions_extracts_titles_and_top_level_bullets():
    text = "# Session Log\n\n## First\n\n- Added one\n  - nested\n\n## Second\n\n- Added two\n"
    assert parse_sessions(text) == [
        {"title": "First", "items": ["Added one"]},
        {"title": "Second", "items": ["Added two"]},
    ]


def test_session_summary_data_applies_limit(tmp_path):
    path = tmp_path / "session-log.md"
    path.write_text("# Session Log\n\n## First\n- One\n\n## Second\n- Two\n", encoding="utf-8")
    data = session_summary_data(path, limit=1)
    assert data["status"] == "ok"
    assert data["total_sessions"] == 2
    assert data["sessions"] == [{"title": "First", "items": ["One"]}]


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
