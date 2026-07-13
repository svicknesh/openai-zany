import pytest

from openai_zany import main_cli, session_json


def test_session_json_rejects_negative_limit(capsys):
    with pytest.raises(SystemExit) as exc_info:
        session_json.main(["--limit", "-1"])

    assert exc_info.value.code == 2
    assert "must be zero or greater" in capsys.readouterr().err


def test_integrated_sessions_json_rejects_negative_limit_before_delegating(monkeypatch):
    delegated = False

    def unexpected_delegate(argv):
        nonlocal delegated
        delegated = True
        return 0

    monkeypatch.setattr(session_json, "main", unexpected_delegate)

    with pytest.raises(SystemExit) as exc_info:
        main_cli.main(["sessions-json", "--limit", "-1"])

    assert exc_info.value.code == 2
    assert delegated is False
