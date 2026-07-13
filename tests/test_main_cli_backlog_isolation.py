import pytest

from openai_zany import main_cli


@pytest.mark.parametrize(
    ("command", "report_name", "report_text"),
    (
        ("next", "next_report", "Next idea: maintained task"),
        ("list", "list_report", "- maintained task"),
    ),
)
def test_backlog_commands_do_not_delegate_to_legacy_cli(
    monkeypatch,
    capsys,
    tmp_path,
    command,
    report_name,
    report_text,
):
    ideas_path = tmp_path / "ideas.md"
    ideas_path.write_text("# Ideas\n\n## Candidate tasks\n\n- maintained task\n", encoding="utf-8")
    monkeypatch.setattr(main_cli.backlog, "DEFAULT_IDEAS_PATH", ideas_path)
    monkeypatch.setattr(main_cli.backlog, report_name, lambda: report_text)

    def unexpected_delegate(_argv):
        raise AssertionError("maintained backlog commands must not delegate to cli.main")

    monkeypatch.setattr(main_cli.cli, "main", unexpected_delegate)

    assert main_cli.main([command]) == 0
    assert capsys.readouterr().out.strip() == report_text
