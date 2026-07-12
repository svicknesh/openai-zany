from openai_zany import main_cli


def test_main_routes_session_log_check_options(monkeypatch):
    received = []
    monkeypatch.setattr(main_cli.session_check, "main", lambda argv: received.append(argv) or 1)

    result = main_cli.main(
        ["session-log-check", "--path", "/tmp/session-log.md", "--format", "json"]
    )

    assert result == 1
    assert received == [["--path", "/tmp/session-log.md", "--format", "json"]]


def test_main_routes_session_log_check_defaults(monkeypatch):
    received = []
    monkeypatch.setattr(main_cli.session_check, "main", lambda argv: received.append(argv) or 0)

    result = main_cli.main(["session-log-check"])

    assert result == 0
    assert received == [["--path", "docs/session-log.md", "--format", "text"]]
