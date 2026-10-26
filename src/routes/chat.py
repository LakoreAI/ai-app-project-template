from fastapi import APIRouter, HTTPException, Request
from openai import OpenAIError

from src.models import ChatRequest, ChatResponse
from src.services.chat import ChatService
from src.utils import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest, request: Request) -> ChatResponse:
    service: ChatService = request.app.state.chat
    try:
        return ChatResponse(answer=service.answer(req.prompt))
    except OpenAIError as e:
        logger.error("LLM call failed: %s", e)
        raise HTTPException(status_code=502, detail="LLM provider error") from e
