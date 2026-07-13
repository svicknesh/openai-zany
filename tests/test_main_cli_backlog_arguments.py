import pytest

from openai_zany import main_cli


@pytest.mark.parametrize(("command", "report_name"), (("next", "next_report"), ("list", "list_report")))
def test_backlog_commands_reject_unexpected_arguments(monkeypatch, command, report_name):
    def unexpected_report():
        raise AssertionError("invalid arguments must be rejected before reading the backlog")

    monkeypatch.setattr(main_cli.backlog, report_name, unexpected_report)

    with pytest.raises(SystemExit) as exc_info:
        main_cli.main([command, "unexpected"])

    assert exc_info.value.code == 2
