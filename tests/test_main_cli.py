from openai_zany import main_cli


def test_registered_commands_adds_integrated_commands_once(monkeypatch):
    monkeypatch.setattr(main_cli.cli, "COMMANDS", (main_cli.cli.CommandInfo("doctor", "Check."),))

    commands = main_cli.registered_commands()

    assert [command.name for command in commands] == [
        "doctor",
        "docs-diff",
        "sessions-json",
        "session-log-check",
    ]


def test_main_routes_next_to_maintained_backlog(monkeypatch, capsys, tmp_path):
    ideas_path = tmp_path / "ideas.md"
    ideas_path.write_text("# Ideas\n\n## Candidate tasks\n\n- maintained task\n", encoding="utf-8")
    monkeypatch.setattr(main_cli.backlog, "DEFAULT_IDEAS_PATH", ideas_path)
    monkeypatch.setattr(main_cli.backlog, "next_report", lambda: "Next idea: maintained task")

    result = main_cli.main(["next"])

    assert result == 0
    assert capsys.readouterr().out.strip() == "Next idea: maintained task"


def test_main_routes_list_to_maintained_backlog(monkeypatch, capsys, tmp_path):
    ideas_path = tmp_path / "ideas.md"
    ideas_path.write_text("# Ideas\n\n## Candidate tasks\n\n- maintained task\n", encoding="utf-8")
    monkeypatch.setattr(main_cli.backlog, "DEFAULT_IDEAS_PATH", ideas_path)
    monkeypatch.setattr(main_cli.backlog, "list_report", lambda: "- maintained task")

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
    assert received == [["--path", "docs/sessions"]]


def test_main_delegates_existing_commands_without_mutating_registry(monkeypatch):
    received = []
    original_commands = (main_cli.cli.CommandInfo("doctor", "Check."),)
    monkeypatch.setattr(main_cli.cli, "COMMANDS", original_commands)

    def delegated_main(argv):
        received.append(argv)
        assert [command.name for command in main_cli.cli.COMMANDS] == [
            "doctor",
            "docs-diff",
            "sessions-json",
            "session-log-check",
        ]
        return 0

    monkeypatch.setattr(main_cli.cli, "main", delegated_main)

    result = main_cli.main(["doctor"])

    assert result == 0
    assert received == [["doctor"]]
    assert main_cli.cli.COMMANDS == original_commands


def test_main_restores_command_registry_when_delegation_fails(monkeypatch):
    original_commands = (main_cli.cli.CommandInfo("doctor", "Check."),)
    monkeypatch.setattr(main_cli.cli, "COMMANDS", original_commands)

    def delegated_main(_argv):
        raise RuntimeError("delegation failed")

    monkeypatch.setattr(main_cli.cli, "main", delegated_main)

    try:
        main_cli.main(["doctor"])
    except RuntimeError as error:
        assert str(error) == "delegation failed"
    else:
        raise AssertionError("expected delegated failure")

    assert main_cli.cli.COMMANDS == original_commands
