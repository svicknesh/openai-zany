from openai_zany.cli import list_ideas, next_idea


def test_next_idea_has_text():
    assert "session log helper" in next_idea()


def test_list_ideas_has_entries():
    text = list_ideas()
    assert "session log helper" in text
    assert "repo health check" in text
