import pytest

from src.modules.skill_module import SkillModule


def test_list_and_load():
    skills = SkillModule()
    assert {"summarize", "answer-with-sources"} <= set(skills.list())
    body = skills.load("summarize")
    assert body.startswith("# Summarize")
    assert "name:" not in body


@pytest.mark.parametrize("name", ["missing", "../services"])
def test_unknown_skill(name):
    with pytest.raises(KeyError):
        SkillModule().load(name)
