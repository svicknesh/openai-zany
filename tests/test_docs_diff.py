from openai_zany.docs_diff import generated_document_diffs, main


def test_diffs_are_empty_when_documents_match(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "session-log.md").write_text("# Session Log\n\n## First\n\n- Added one\n", encoding="utf-8")

    from openai_zany.cli import write_generated_documents

    write_generated_documents(tmp_path)

    assert generated_document_diffs(tmp_path) == []


def test_diffs_preview_changes_without_writing(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "session-log.md").write_text("# Session Log\n\n## First\n\n- Added one\n", encoding="utf-8")
    target = docs / "commands.md"
    target.write_text("old\n", encoding="utf-8")

    diffs = generated_document_diffs(tmp_path)

    assert "--- docs/commands.md" in diffs[0]
    assert "+# Commands" in diffs[0]
    assert target.read_text(encoding="utf-8") == "old\n"


def test_missing_document_uses_dev_null(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "session-log.md").write_text("# Session Log\n", encoding="utf-8")

    diffs = generated_document_diffs(tmp_path)

    assert "--- /dev/null" in diffs[0]
    assert "+++ docs/commands.md" in diffs[0]


def test_main_returns_nonzero_for_pending_changes(tmp_path, capsys):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "session-log.md").write_text("# Session Log\n", encoding="utf-8")

    assert main(["--root", str(tmp_path)]) == 1
    assert "+++ docs/commands.md" in capsys.readouterr().out
