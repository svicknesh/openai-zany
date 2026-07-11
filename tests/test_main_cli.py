from openai_zany import main_cli


def test_registered_commands_adds_integrated_commands_once(monkeypatch):
    monkeypatch.setattr(main_cli.cli, "COMMANDS", (main_cli.cli.CommandInfo("doctor", "Check."),))

    commands = main_cli.registered_commands()

    assert [command.name for command in commands] == ["doctor", "docs-diff", "sessions-json"]


def test_main_routes_next_to_maintained_backlog(monkeypatch, capsys):
    monkeypatch.setattr(main_cli.backlog, "next_report", lambda: "Next idea: maintained task")
    monkeypatch.setattr(main_cli.backlog.DEFAULT_IDEAS_PATH, "is_file", lambda: True)

    result = main_cli.main(["next"])

    assert result == 0
    assert capsys.readouterr().out.strip() == "Next idea: maintained task"


def test_main_routes_list_to_maintained_backlog(monkeypatch, capsys):
    monkeypatch.setattr(main_cli.backlog, "list_report", lambda: "- maintained task")
    monkeypatch.setattr(main_cli.backlog.DEFAULT_IDEAS_PATH, "is_file", lambda: True)

    result = main_cli.main(["list"])

    assert result == 0
    assert capsys.readouterr().out.strip() == "- maintained task"


def test_main_routes_docs_diff_options(monkeypatch):
    received = []
    monkeypatch.setattr(main_cli.docs_diff, "main", lambda argv: received.append(argv) or 1)

    result = main_cli.main(["docs-diff", "--root", "/tmp/repo", "--format", "json"])

    assert result == 1
    assert received == [["--root", "/tmp/repo", "--format", "json"]]


def test_main_routes_console_arguments(monkeypatch):
    received = []
    monkeypatch.setattr(main_cli.sys, "argv", ["zany", "docs-diff", "--format", "json"])
    monkeypatch.setattr(main_cli.docs_diff, "main", lambda argv: received.append(argv) or 1)

    result = main_cli.main()

    assert result == 1
    assert received == [["--root", ".", "--format", "json"]]


def test_main_routes_sessions_json_options(monkeypatch):
    received = []
    monkeypatch.setattr(main_cli.session_json, "main", lambda argv: received.append(argv) or 0)

    result = main_cli.main(["sessions-json", "--path", "/tmp/session-log.md", "--limit", "3"])

    assert result == 0
    assert received == [["--path", "/tmp/session-log.md", "--limit", "3"]]


def test_main_routes_sessions_json_defaults(monkeypatch):
    received = []
    monkeypatch.setattr(main_cli.session_json, "main", lambda argv: received.append(argv) or 0)

    result = main_cli.main(["sessions-json"])

    assert result == 0
    assert received == [["--path", "docs/session-log.md"]]


def test_main_delegates_existing_commands_with_augmented_reference(monkeypatch):
    received = []
    monkeypatch.setattr(main_cli.cli, "COMMANDS", (main_cli.cli.CommandInfo("doctor", "Check."),))
    monkeypatch.setattr(main_cli.cli, "main", lambda argv: received.append(argv) or 0)

    result = main_cli.main(["doctor"])

    assert result == 0
    assert received == [["doctor"]]
    assert [command.name for command in main_cli.cli.COMMANDS] == ["doctor", "docs-diff", "sessions-json"]
