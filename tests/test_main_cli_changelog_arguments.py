import pytest

from openai_zany import main_cli


def test_changelog_rejects_unexpected_arguments(monkeypatch):
    def unexpected_report():
        raise AssertionError("invalid arguments must be rejected before reading session records")

    monkeypatch.setattr(main_cli.session_reports, "changelog_report", unexpected_report)

    with pytest.raises(SystemExit) as exc_info:
        main_cli.main(["changelog", "unexpected"])

    assert exc_info.value.code == 2
