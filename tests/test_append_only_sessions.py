from openai_zany.cli import append_only_session_titles


def test_append_only_session_titles_ignores_metadata_and_malformed_records(tmp_path):
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    (sessions / "README.md").write_text("# Session: Documentation\n", encoding="utf-8")
    (sessions / "2026-07-12-100000-malformed.md").write_text(
        "# Not a session record\n\n## Changes made\n\n- Missing canonical title.\n",
        encoding="utf-8",
    )
    (sessions / "2026-07-12-110000-valid.md").write_text(
        "# Session: Valid record\n\n## Changes made\n\n- Recorded work.\n",
        encoding="utf-8",
    )

    assert append_only_session_titles(sessions) == ["Valid record"]
