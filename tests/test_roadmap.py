from openai_zany.cli import markdown_section_bullets, roadmap_report


def test_markdown_section_bullets_reads_only_requested_section():
    markdown = "# Ideas\n\n## Completed\n\n- Done\n\n## Candidate tasks\n\n- Next\n"

    assert markdown_section_bullets(markdown, "Completed") == ["Done"]
    assert markdown_section_bullets(markdown, "Candidate tasks") == ["Next"]


def test_roadmap_report_handles_missing_ideas_file(tmp_path):
    report = roadmap_report(tmp_path / "missing.md")

    assert "Roadmap: MISSING" in report


def test_roadmap_report_separates_completed_and_candidate_tasks(tmp_path):
    ideas_path = tmp_path / "ideas.md"
    ideas_path.write_text(
        "# Ideas\n\n"
        "## Completed\n\n- Added one\n\n"
        "## Candidate tasks\n\n- Add two\n\n"
        "## Selection rule\n\nChoose bounded work.\n",
        encoding="utf-8",
    )

    report = roadmap_report(ideas_path)

    assert "# Roadmap" in report
    assert "## Completed\n- Added one" in report
    assert "## Candidate tasks\n- Add two" in report
    assert "Choose bounded work." not in report
