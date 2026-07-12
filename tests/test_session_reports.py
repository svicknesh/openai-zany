from openai_zany import main_cli
from openai_zany.session_reports import changelog_report, session_entries


def test_session_entries_reads_append_only_records_newest_first(tmp_path):
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    (sessions / "README.md").write_text("# Session Records\n", encoding="utf-8")
    (sessions / "2026-07-12-090000-old.md").write_text(
        "# Session: Older\n\n## Changes made\n\n- Old change\n",
        encoding="utf-8",
    )
    (sessions / "2026-07-12-100000-new.md").write_text(
        "# Session: Newer\n\n## Changes made\n\n- New change\n",
        encoding="utf-8",
    )

    assert session_entries(sessions) == [
        ("Newer", ["New change"]),
        ("Older", ["Old change"]),
    ]


def test_changelog_report_supports_legacy_log(tmp_path):
    log = tmp_path / "session-log.md"
    log.write_text("# Session Log\n\n## First\n\n- Added one\n", encoding="utf-8")

    report = changelog_report(log)

    assert "# Changelog" in report
    assert "## First" in report
    assert "- Added one" in report


def test_changelog_report_ignores_invalid_records(tmp_path):
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    (sessions / "invalid.md").write_text("# Not a session\n", encoding="utf-8")

    assert changelog_report(sessions).startswith("Changelog: EMPTY")


def test_main_routes_changelog_to_append_only_report(monkeypatch, capsys, tmp_path):
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    monkeypatch.setattr(main_cli.session_reports, "DEFAULT_SESSIONS_PATH", sessions)
    monkeypatch.setattr(main_cli.session_reports, "changelog_report", lambda: "# Changelog\n\n## Latest")

    result = main_cli.main(["changelog"])

    assert result == 0
    assert capsys.readouterr().out.strip() == "# Changelog\n\n## Latest"
