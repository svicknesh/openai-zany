import pytest

from openai_zany import main_cli


def test_generate_docs_rejects_unexpected_arguments_before_writing_documents(monkeypatch):
    monkeypatch.setattr(
        main_cli.generated_docs,
        "write_generated_documents",
        lambda: pytest.fail("generated documents should not be written"),
    )

    with pytest.raises(SystemExit) as error:
        main_cli.main(["generate-docs", "unexpected"])

    assert error.value.code == 2
