from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel

from app.services.vector_db import store_file


router = APIRouter()


class MemoryUploadResponse(BaseModel):
    status: str
    chunks_added: int


@router.post("/memory/upload", response_model=MemoryUploadResponse)
async def upload_memory(file: UploadFile = File(...)) -> MemoryUploadResponse:
    chunks_added = await store_file(file)
    return MemoryUploadResponse(status="success", chunks_added=chunks_added)
