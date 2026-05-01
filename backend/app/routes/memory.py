from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel

from app.services.vector_db import COLLECTION_NAME, get_client, query_memory, store_file


router = APIRouter()


class MemoryUploadResponse(BaseModel):
    status: str
    chunks_added: int


@router.post("/memory/upload", response_model=MemoryUploadResponse)
async def upload_memory(file: UploadFile = File(...)) -> MemoryUploadResponse:
    chunks_added = await store_file(file)
    return MemoryUploadResponse(status="success", chunks_added=chunks_added)


@router.get("/memory/debug")
async def debug_memory():
    """Returns the current state of Rocky's memory for debugging."""
    try:
        client = get_client()
        count = client.count(collection_name=COLLECTION_NAME, exact=True).count
        test_context = query_memory("best friend")
        return {
            "collection": COLLECTION_NAME,
            "total_points": count,
            "sample_query": "best friend",
            "sample_result": test_context[:500] if test_context else "EMPTY — THIS IS THE BUG",
            "embedder_status": "ok",
        }
    except Exception as e:
        return {"error": str(e)}
