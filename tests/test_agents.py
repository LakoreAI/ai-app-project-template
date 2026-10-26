import pytest

from src.modules.agents.base import BaseAgent
from src.modules.agents.chat import ChatAgent
from src.modules.agents.prompts import load_prompt_template
from src.modules.agents.skills import list_skills, load_skill
from tests.test_chat import FakeLLM


def test_list_and_load_skills():
    assert {"summarize", "answer-with-sources"} <= set(list_skills())
    body = load_skill("summarize")
    assert body.startswith("# Summarize")
    assert "name:" not in body


@pytest.mark.parametrize("name", ["missing", "../services"])
def test_unknown_skill(name):
    with pytest.raises(KeyError):
        load_skill(name)


def test_agent_without_skills_uses_its_prompt_template():
    assert BaseAgent().system_prompt == load_prompt_template("default")
    assert ChatAgent(llm=FakeLLM()).system_prompt == load_prompt_template("chat")


def test_unknown_prompt_template():
    with pytest.raises(KeyError):
        load_prompt_template("../skills/summarize/SKILL")


def test_agent_system_prompt_includes_its_skills():
    llm = FakeLLM()
    agent = ChatAgent(llm=llm, skills=["summarize"])
    agent.execute("text")
    system = llm.messages[0]["content"]
    assert system.startswith(load_prompt_template("chat"))
    assert "# Summarize" in system


def test_agent_unknown_skill_fails_at_build():
    with pytest.raises(KeyError):
        ChatAgent(llm=FakeLLM(), skills=["nope"])
