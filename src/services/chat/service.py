from src.data.base import DataSource
from src.modules.skill_module import SkillModule
from src.services.chat.modules.llm import LLM
from src.services.chat.utils.prompts import DEFAULT_SYSTEM_PROMPT


class ChatService:
    """Chat service: composes modules (llm, skills), datasources and utils."""

    def __init__(
        self,
        datasources: list[DataSource] | None = None,
        llm: LLM | None = None,
        skills: SkillModule | None = None,
    ) -> None:
        self.datasources = datasources or []
        self.llm = llm or LLM()
        self.skills = skills or SkillModule()

    def answer(self, prompt: str, skill: str | None = None) -> str:
        """Answer `prompt`; `skill` (a name in assets/skills) replaces the default system prompt."""
        system = self.skills.load(skill) if skill else DEFAULT_SYSTEM_PROMPT
        return self.llm.complete(
            [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ]
        )
