from openai_zany.generated_docs import (
    freshness_report,
    stale_generated_documents,
    status_page_html,
    write_generated_documents,
)


def test_status_page_is_stable_and_points_to_live_reports():
    html = status_page_html()

    assert "append-only session records" in html
    assert "zany sessions" in html
    assert "zany changelog" in html
    assert "docs/sessions/" in html


def test_write_generated_documents_creates_current_files(tmp_path):
    written = write_generated_documents(tmp_path)

    assert [str(path.relative_to(tmp_path)) for path in written] == [
        "docs/commands.md",
        "docs/status.html",
    ]
    assert stale_generated_documents(tmp_path) == []
    assert "Generated documentation: CURRENT" in freshness_report(tmp_path)


def test_session_record_changes_do_not_make_generated_docs_stale(tmp_path):
    write_generated_documents(tmp_path)
    sessions = tmp_path / "docs" / "sessions"
    sessions.mkdir()
    (sessions / "2026-07-12-120000-new.md").write_text(
        "# Session: New work\n\n## Changes made\n\n- Added something\n",
        encoding="utf-8",
    )

    assert stale_generated_documents(tmp_path) == []
