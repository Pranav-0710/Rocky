STATUS: COMPLETE
TASK: T005
WHAT I BUILT: Added logging to memory store/query paths, switched query_memory to supported Qdrant query API, added `/api/memory/debug`, and kept embedder re-init safe when initialization fails.
FILES CHANGED: backend/app/services/vector_db.py, backend/app/routes/memory.py, .agent/status/codex-status.md
INTEGRATION NOTES: Backend restarted at http://127.0.0.1:8000. `/api/memory/debug` now returns `total_points` and retrieved sample memory text. Memory query no longer fails silently when Qdrant SDK raises.
BLOCKERS: None
