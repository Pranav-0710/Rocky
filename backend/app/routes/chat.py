from typing import Any, Literal

from pydantic import BaseModel, Field
from fastapi import APIRouter

from app.services import llm as llm_service
from app.services import vector_db as vector_db_service


router = APIRouter()


class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[HistoryMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str
    actions: list[Any] = Field(default_factory=list)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    context = vector_db_service.query_memory(request.message)
    history = [item.model_dump() for item in request.history]
    return ChatResponse(
        reply=llm_service.get_reply(request.message, context=context, history=history),
        actions=[],
    )
