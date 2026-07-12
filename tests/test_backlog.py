from openai_zany.backlog import candidate_tasks, list_report, next_report, section_bullets


def test_section_bullets_reads_only_requested_section():
    markdown = "# Ideas\n\n## Completed\n\n- Done\n\n## Candidate tasks\n\n- First\n- Second\n"
    assert section_bullets(markdown, "Candidate tasks") == ["First", "Second"]


def test_section_bullets_ignores_nested_subsection_bullets():
    markdown = (
        "# Ideas\n\n## Candidate tasks\n\n- Executable task\n\n"
        "### Context\n\n- Explanation only\n\n## Selection rule\n\n- Not a task\n"
    )
    assert section_bullets(markdown, "Candidate tasks") == ["Executable task"]


def test_section_bullets_ignores_deeper_subsection_bullets():
    markdown = (
        "# Ideas\n\n## Candidate tasks\n\n- Executable task\n\n"
        "#### Implementation notes\n\n- Explanation only\n\n## Selection rule\n\n- Not a task\n"
    )
    assert section_bullets(markdown, "Candidate tasks") == ["Executable task"]


def test_section_bullets_stops_at_top_level_heading():
    markdown = (
        "# Ideas\n\n## Candidate tasks\n\n- Executable task\n\n"
        "# Archived notes\n\n- Historical note\n"
    )
    assert section_bullets(markdown, "Candidate tasks") == ["Executable task"]


def test_candidate_tasks_reads_maintained_ideas_file(tmp_path):
    ideas_path = tmp_path / "ideas.md"
    ideas_path.write_text("# Ideas\n\n## Candidate tasks\n\n- Build useful thing\n", encoding="utf-8")
    assert candidate_tasks(ideas_path) == ["Build useful thing"]
    assert next_report(ideas_path) == "Next idea: Build useful thing"
    assert list_report(ideas_path) == "- Build useful thing"


def test_backlog_reports_missing_file(tmp_path):
    ideas_path = tmp_path / "missing.md"
    assert "Idea backlog: MISSING" in next_report(ideas_path)
    assert "Idea backlog: MISSING" in list_report(ideas_path)


def test_backlog_reports_empty_candidate_section(tmp_path):
    ideas_path = tmp_path / "ideas.md"
    ideas_path.write_text("# Ideas\n\n## Candidate tasks\n", encoding="utf-8")
    assert "Idea backlog: EMPTY" in next_report(ideas_path)
    assert "Idea backlog: EMPTY" in list_report(ideas_path)
