from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str
    skill: str | None = None


class ChatResponse(BaseModel):
    answer: str
