from openai_zany import main_cli


def test_registered_commands_preserves_existing_integrated_command_once(monkeypatch):
    existing = main_cli.cli.CommandInfo("docs-diff", "Custom docs diff description.")
    monkeypatch.setattr(
        main_cli.cli,
        "COMMANDS",
        (
            main_cli.cli.CommandInfo("doctor", "Check."),
            existing,
        ),
    )

    commands = main_cli.registered_commands()

    assert [command.name for command in commands] == [
        "doctor",
        "docs-diff",
        "sessions-json",
        "session-log-check",
    ]
    assert commands[1] is existing
