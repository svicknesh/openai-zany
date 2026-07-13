import pytest

from openai_zany import main_cli


def test_freshness_rejects_unexpected_arguments_before_reading_documents(monkeypatch):
    monkeypatch.setattr(
        main_cli.generated_docs,
        "freshness_report",
        lambda: pytest.fail("freshness report should not be read"),
    )

    with pytest.raises(SystemExit) as error:
        main_cli.main(["freshness", "unexpected"])

    assert error.value.code == 2
