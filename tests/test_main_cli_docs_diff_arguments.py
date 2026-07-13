import pytest

from openai_zany import main_cli


def test_docs_diff_rejects_unexpected_arguments_before_delegating(monkeypatch):
    monkeypatch.setattr(
        main_cli.docs_diff,
        "main",
        lambda argv: pytest.fail("docs-diff should not be delegated"),
    )

    with pytest.raises(SystemExit) as error:
        main_cli.main(["docs-diff", "unexpected"])

    assert error.value.code == 2
