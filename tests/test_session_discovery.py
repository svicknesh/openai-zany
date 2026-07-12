from openai_zany.cli import append_only_session_titles, session_summary


def test_append_only_discovery_ignores_non_session_markdown(tmp_path):
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    (sessions / "README.md").write_text("# Session Records\n", encoding="utf-8")
    (sessions / "notes.md").write_text("# Notes\n\nNo session heading.\n", encoding="utf-8")
    (sessions / "2026-07-12-210000-valid.md").write_text(
        "# Session: Valid record\n\n## Changes made\n\n- Added coverage.\n",
        encoding="utf-8",
    )

    assert append_only_session_titles(sessions) == ["Valid record"]
    assert "Total sessions: 1" in session_summary(sessions)
