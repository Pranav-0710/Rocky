STATUS: COMPLETE
TASK: T006 + T008
WHAT I BUILT: Added chat history support on /api/chat and updated LLM call path to build Groq-style message arrays (system + history + latest user message). Updated route tests to patch current LLM/vector services and added coverage for GET /api/memory/debug.
FILES CHANGED: backend/app/routes/chat.py, backend/app/services/llm.py, backend/tests/test_routes.py
INTEGRATION NOTES: Tests passed with `cmd /c "set PYTHONPATH=backend&& backend\.venv\Scripts\python.exe -m pytest backend/tests -q"` (3 passed).
BLOCKERS: None for implementation/tests. Commit not created yet.
