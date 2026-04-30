STATUS: COMPLETE
TASK: T003
WHAT I BUILT: Pytest suite for /api/chat and /api/memory/upload with mocked LLM/vector DB. Antigravity resolved shell blocker by adding anyio[trio], pytest-anyio deps and conftest.py.
FILES CHANGED: backend/tests/test_routes.py, backend/tests/conftest.py, backend/requirements.txt
INTEGRATION NOTES: Run with PYTHONPATH=backend. 2/2 tests PASSED.
BLOCKERS: None — resolved by Antigravity.
