import json

from openai_zany.docs_diff import generated_document_diffs, main
from openai_zany.generated_docs import write_generated_documents


def test_diffs_are_empty_when_documents_match(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()

    write_generated_documents(tmp_path)

    assert generated_document_diffs(tmp_path) == []


def test_diffs_preview_changes_without_writing(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    target = docs / "commands.md"
    target.write_text("old\n", encoding="utf-8")

    diffs = generated_document_diffs(tmp_path)

    assert diffs[0]["path"] == "docs/commands.md"
    assert diffs[0]["status"] == "stale"
    assert "--- docs/commands.md" in diffs[0]["diff"]
    assert "+# Commands" in diffs[0]["diff"]
    assert target.read_text(encoding="utf-8") == "old\n"


def test_missing_document_uses_dev_null(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()

    diffs = generated_document_diffs(tmp_path)

    assert diffs[0]["status"] == "missing"
    assert "--- /dev/null" in diffs[0]["diff"]
    assert "+++ docs/commands.md" in diffs[0]["diff"]


def test_main_returns_nonzero_for_pending_changes(tmp_path, capsys):
    docs = tmp_path / "docs"
    docs.mkdir()

    assert main(["--root", str(tmp_path)]) == 1
    assert "+++ docs/commands.md" in capsys.readouterr().out


def test_json_output_is_machine_readable(tmp_path, capsys):
    docs = tmp_path / "docs"
    docs.mkdir()

    assert main(["--root", str(tmp_path), "--format", "json"]) == 1

    payload = json.loads(capsys.readouterr().out)
    assert payload["current"] is False
    assert payload["documents"][0]["path"] == "docs/commands.md"
    assert payload["documents"][0]["status"] == "missing"
    assert payload["documents"][0]["diff"].startswith("--- /dev/null")
