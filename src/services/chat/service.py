from src.data.base import DataSource
from src.modules.agents.chat import ChatAgent


class ChatService:
    """Chat service: composes the chat agent (LLM + skills), datasources and utils."""

    def __init__(self, datasources: list[DataSource] | None = None, agent: ChatAgent | None = None):
        self.datasources = datasources or []
        self.agent = agent or ChatAgent()

    def answer(self, prompt: str) -> str:
        return self.agent.execute(prompt)
