from typing import Any

from pydantic import BaseModel, Field
from fastapi import APIRouter

from app.services.llm import get_reply
from app.services.vector_db import query_memory


router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    actions: list[Any] = Field(default_factory=list)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    context = query_memory(request.message)
    return ChatResponse(reply=get_reply(request.message, context=context), actions=[])
