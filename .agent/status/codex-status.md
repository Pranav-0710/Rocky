STATUS: COMPLETE
TASK: T004
WHAT I BUILT: Added dotenv support, .env.example/.env, gitignore protection for backend/.env, real Gemini service wiring, real ChromaDB PersistentClient memory storage/query, route wiring to real services, and env-based CORS via FRONTEND_URL.
FILES CHANGED: backend/requirements.txt, backend/app/main.py, backend/app/routes/chat.py, backend/app/routes/memory.py, backend/app/services/llm.py, backend/app/services/vector_db.py, backend/.env.example, backend/.env, .gitignore, .agent/status/codex-status.md
INTEGRATION NOTES: Backend restarted at http://127.0.0.1:8000. /health works. Memory upload and query_memory verified with ChromaDB. /api/chat now requires a real GEMINI_API_KEY; backend/.env currently contains placeholder value.
BLOCKERS: None
