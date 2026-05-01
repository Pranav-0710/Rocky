# Copilot CLI Inbox

## Active Task
**TASK ID:** T006 + T008
**PRIORITY:** HIGH — Add conversation history & Update Tests
**DESCRIPTION:**

Codex is currently unavailable, so you are taking over the backend feature implementation. We are using Groq + Qdrant (not Gemini/ChromaDB).

### Part 1: Add conversation history (T006)
Right now Rocky has no short-term memory. Every message is treated independently. 

#### 1. Add conversation history to the chat endpoint
In `backend/app/routes/chat.py`:
- Change `ChatRequest` to accept an optional `history` field: a list of `{"role": "user"|"assistant", "content": "..."}` objects (or equivalent pydantic models)
- Pass the full history to `get_reply()` instead of just the latest message

#### 2. Update `backend/app/services/llm.py`
- Change `get_reply()` signature to accept `history: list[dict]` (or similar) instead of just `message: str`
- Build the messages array properly for the Groq call:
  - First message: `{"role": "system", "content": system_prompt}` (keep existing system prompt with context)
  - Then append all history messages
  - Final message: `{"role": "user", "content": message}`
- If `history` is empty or not provided, behave exactly as before.

### Part 2: Update the Test Suite (T008)
The test suite is outdated. Update it to reflect the current stack (Groq + Qdrant) and the new endpoints.

#### 1. Update `backend/tests/test_routes.py`
- Mock `app.services.vector_db.query_memory` instead of old ChromaDB mocks
- Mock `app.services.llm.get_reply` instead of old Gemini mocks
- Add a test for the new `GET /api/memory/debug` endpoint
- Ensure the `POST /api/chat` test sends the new `history` field (can be an empty list)

### Files To Change
- `backend/app/routes/chat.py`
- `backend/app/services/llm.py`
- `backend/tests/test_routes.py`

### Success Criteria
1. The backend accepts and processes `history` in the chat payload.
2. All tests pass with the current Groq + Qdrant stack when running:
   `backend\.venv\Scripts\python.exe -m pytest backend/tests -q`

**WHEN DONE:** Update `.agent/status/copilot-status.md` and commit with message "Add conversation history and update tests"
