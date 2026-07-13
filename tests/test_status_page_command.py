import pytest

from openai_zany import main_cli


def test_status_page_writes_only_status_document(monkeypatch, capsys, tmp_path):
    status_path = tmp_path / "docs" / "status.html"
    monkeypatch.setattr(main_cli.generated_docs, "STATUS_PAGE_PATH", status_path)

    def fail_if_all_documents_are_written():
        raise AssertionError("status-page must not regenerate every managed document")

    monkeypatch.setattr(
        main_cli.generated_docs,
        "write_generated_documents",
        fail_if_all_documents_are_written,
    )

    result = main_cli.main(["status-page"])

    assert result == 0
    assert status_path.read_text(encoding="utf-8") == main_cli.generated_docs.status_page_html()
    assert capsys.readouterr().out.strip() == f"Wrote status page: {status_path}"


def test_status_page_rejects_unexpected_arguments(monkeypatch, tmp_path):
    status_path = tmp_path / "docs" / "status.html"
    monkeypatch.setattr(main_cli.generated_docs, "STATUS_PAGE_PATH", status_path)

    with pytest.raises(SystemExit) as error:
        main_cli.main(["status-page", "unexpected"])

    assert error.value.code == 2
    assert not status_path.exists()
