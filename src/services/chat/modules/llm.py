from openai import OpenAI

from src.config import settings
from src.modules.base import BaseModules


class LLM(BaseModules):
    def __init__(self, model: str | None = None, api_key: str | None = None) -> None:
        super().__init__()
        self.model = model or settings.openai_model
        self.api_key = api_key if api_key is not None else settings.openai_api_key
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        # created on first use so the app can start without an API key
        if self._client is None:
            self._client = OpenAI(api_key=self.api_key)
        return self._client

    def complete(self, messages: list[dict[str, str]]) -> str:
        response = self.client.chat.completions.create(model=self.model, messages=messages)
        return response.choices[0].message.content or ""
