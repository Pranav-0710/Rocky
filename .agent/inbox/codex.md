# Codex Inbox

## Active Task
**TASK ID:** T005
**PRIORITY:** CRITICAL — Rocky's memory retrieval is broken
**DESCRIPTION:**

Rocky has data in Qdrant Cloud (verified: 5 points including "My best friend is Arjun"), but when the user asks "who is my best friend", the `query_memory()` function returns empty context. The LLM then says "I don't have that information."

### Root Cause Investigation
The `query_memory()` function in `backend/app/services/vector_db.py` has a bare `except Exception` that silently swallows errors. The likely cause is:
1. The `fastembed` model download fails or times out on Render's free tier
2. OR the Qdrant collection search fails silently
3. OR the embedding vectors don't match (different model used for store vs query)

### What To Fix

#### Fix 1 — Add logging to `query_memory()` in `backend/app/services/vector_db.py`
- Import `logging` at the top
- Create a logger: `logger = logging.getLogger(__name__)`
- In the `except Exception` block, change from silent pass to: `logger.error(f"Memory query failed: {e}", exc_info=True)`
- Add a `logger.info(f"Memory context retrieved: {len(results)} results")` after the search succeeds

#### Fix 2 — Add logging to `store_file()` as well
- Log how many chunks were stored and the collection name
- Log any errors during embedding or upsert

#### Fix 3 — Add a debug endpoint to `backend/app/routes/memory.py`
Add a new GET endpoint:
```python
@router.get("/memory/debug")
async def debug_memory():
    """Returns the current state of Rocky's memory for debugging."""
    from app.services.vector_db import get_client, get_embedder, COLLECTION_NAME, query_memory
    try:
        client = get_client()
        count = client.count(collection_name=COLLECTION_NAME).count
        # Test a sample query
        test_context = query_memory("best friend")
        return {
            "collection": COLLECTION_NAME,
            "total_points": count,
            "sample_query": "best friend",
            "sample_result": test_context[:500] if test_context else "EMPTY — THIS IS THE BUG",
            "embedder_status": "ok"
        }
    except Exception as e:
        return {"error": str(e)}
```

#### Fix 4 — Ensure the embedder is cached properly
In `vector_db.py`, the `_embedder` global might not survive across Render's worker processes. Make sure `get_embedder()` handles re-initialization gracefully.

### Files To Change
- `backend/app/services/vector_db.py`
- `backend/app/routes/memory.py`

### Success Criteria
After your changes, hitting `https://rocky-bafn.onrender.com/api/memory/debug` should return:
```json
{
  "total_points": 5,
  "sample_result": "... Arjun ..."
}
```

**WHEN DONE:** Update `.agent/status/codex-status.md` and push to GitHub with message "Fix memory retrieval logging and debug endpoint"
