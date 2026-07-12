import pytest

from openai_zany import main_cli


@pytest.mark.parametrize(
    ("command", "report_name"),
    (("next", "next_report"), ("list", "list_report")),
)
def test_backlog_commands_fail_when_maintained_file_is_missing(
    monkeypatch, capsys, tmp_path, command, report_name
):
    missing_path = tmp_path / "missing-ideas.md"
    monkeypatch.setattr(main_cli.backlog, "DEFAULT_IDEAS_PATH", missing_path)
    monkeypatch.setattr(
        main_cli.backlog,
        report_name,
        lambda: f"Idea backlog: MISSING\nExpected path: {missing_path}",
    )

    result = main_cli.main([command])

    assert result == 1
    assert capsys.readouterr().out.strip() == (
        f"Idea backlog: MISSING\nExpected path: {missing_path}"
    )
