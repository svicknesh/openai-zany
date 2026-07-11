from pathlib import Path

from openai_zany import main_cli, session_check


VALID_LOG = """# Session Log

## 2026-07-11

Added a validation command.

Changes made:

- Added the command.

Notes:

- Work stayed bounded.
"""


def test_validate_session_log_text_accepts_expected_structure():
    assert session_check.validate_session_log_text(VALID_LOG) == []


def test_validate_session_log_text_reports_missing_sections():
    errors = session_check.validate_session_log_text(
        "# Session Log\n\n## not-a-date\n\nChanges made:\n"
    )
    assert any("heading must use YYYY-MM-DD" in error for error in errors)
    assert any("one-line session summary" in error for error in errors)
    assert any("must contain a top-level bullet" in error for error in errors)
    assert any("missing 'Notes:' section" in error for error in errors)


def test_session_log_check_report_handles_missing_file(tmp_path):
    report = session_check.session_log_check_report(tmp_path / "missing.md")
    assert "Session log structure: MISSING" in report


def test_session_log_check_main_returns_nonzero_for_invalid_file(tmp_path, capsys):
    path = tmp_path / "session-log.md"
    path.write_text("# Wrong title\n", encoding="utf-8")
    assert session_check.main(["--path", str(path)]) == 1
    assert "Session log structure: INVALID" in capsys.readouterr().out


def test_primary_cli_routes_session_log_check(monkeypatch):
    captured: list[list[str]] = []

    def fake_main(arguments):
        captured.append(arguments)
        return 0

    monkeypatch.setattr(session_check, "main", fake_main)
    assert main_cli.main(["session-log-check", "--path", "custom.md"]) == 0
    assert captured == [["--path", "custom.md"]]


def test_registered_commands_include_session_log_check():
    assert "session-log-check" in {command.name for command in main_cli.registered_commands()}
