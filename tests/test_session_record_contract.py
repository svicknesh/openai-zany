from pathlib import Path


SESSION_RECORD_INSTRUCTIONS = Path("docs/sessions/README.md")


def test_session_record_instructions_preserve_append_only_contract():
    instructions = SESSION_RECORD_INSTRUCTIONS.read_text(encoding="utf-8")

    assert "# Session Records" in instructions
    assert "YYYY-MM-DD-HHMMSS-short-slug.md" in instructions
    assert "After creation, a session file should not normally be edited." in instructions
    assert "`docs/session-log.md` is a legacy archive." in instructions
    assert "Do not replace it during autonomous connector-driven runs." in instructions
