from src.modules.agents.base import BaseAgent
from src.modules.llm import LLM


class ChatAgent(BaseAgent):
    prompt_template = "chat"

    def __init__(self, llm: LLM | None = None, skills: list[str] | None = None):
        super().__init__(skills)
        self.llm = llm or LLM()

    def execute(self, prompt: str) -> str:
        return self.llm.complete(
            [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ]
        )
