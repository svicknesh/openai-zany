from openai_zany.cli import (
    doctor_report,
    list_ideas,
    missing_expected_files,
    next_idea,
    session_summary,
    session_titles,
)


def test_next_idea_has_text():
    assert "session log helper" in next_idea()


def test_list_ideas_has_entries():
    text = list_ideas()
    assert "session log helper" in text
    assert "repo health check" in text


def test_missing_expected_files_detects_empty_directory(tmp_path):
    missing = missing_expected_files(tmp_path)
    assert "README.md" in missing
    assert "src/openai_zany/cli.py" in missing


def test_doctor_report_is_ok_for_complete_scaffold(tmp_path):
    for relative_path in missing_expected_files(tmp_path):
        file_path = tmp_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text("placeholder\n", encoding="utf-8")

    report = doctor_report(tmp_path)
    assert "Repository health: OK" in report
    assert "All expected files are present." in report


def test_doctor_report_lists_missing_files(tmp_path):
    report = doctor_report(tmp_path)
    assert "Repository health: ATTENTION" in report
    assert "README.md" in report


def test_session_titles_extracts_second_level_headings():
    text = "# Session Log\n\n## 2026-07-09\n\nWork.\n\n## 2026-07-08\n"
    assert session_titles(text) == ["2026-07-09", "2026-07-08"]


def test_session_summary_reports_missing_log(tmp_path):
    report = session_summary(tmp_path / "missing.md")
    assert "Session log: MISSING" in report


def test_session_summary_reports_latest_session(tmp_path):
    log_path = tmp_path / "session-log.md"
    log_path.write_text("# Session Log\n\n## 2026-07-09\n\nWork.\n\n## 2026-07-08\n", encoding="utf-8")

    report = session_summary(log_path)
    assert "Session log: OK" in report
    assert "Total sessions: 2" in report
    assert "Latest session: 2026-07-09" in report
