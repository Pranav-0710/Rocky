# Codex Inbox

## Active Task
**TASK ID:** T004
**PRIORITY:** HIGH — Debate Room Round 1 fixes
**DESCRIPTION:**

The Debate Room flagged 4 issues. Fix them in this exact order:

### Fix 1 — Add `.env` support (SECURITY)
1. Add `python-dotenv` to `requirements.txt`
2. In `backend/app/main.py`, add at the very top:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```
3. Create `backend/.env.example` (NOT `.env`) with:
   ```
   GEMINI_API_KEY=your_key_here
   CHROMA_DB_DIR=./chroma_store
   FRONTEND_URL=http://localhost:5173
   ```
4. Create `backend/.env` (add to `.gitignore` — never commit this)

### Fix 2 — Wire real Gemini API into `services/llm.py`
Replace the mock with a real Gemini call:
```python
import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

def get_reply(message: str, context: str = "") -> str:
    system = f"You are Rocky, a loyal personal AI companion. You are warm, sharp, and always helpful.\n\nContext about the user:\n{context}"
    response = model.generate_content(f"{system}\n\nUser: {message}")
    return response.text
```

### Fix 3 — Wire real ChromaDB into `services/vector_db.py`
```python
import os
import chromadb

def get_client():
    path = os.environ.get("CHROMA_DB_DIR", "./chroma_store")
    return chromadb.PersistentClient(path=path)

async def store_file(file) -> int:
    contents = await file.read()
    text = contents.decode("utf-8", errors="ignore")
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    client = get_client()
    collection = client.get_or_create_collection("rocky_memory")
    for i, chunk in enumerate(chunks):
        collection.add(documents=[chunk], ids=[f"{file.filename}_{i}"])
    return len(chunks)

def query_memory(prompt: str, n: int = 3) -> str:
    client = get_client()
    collection = client.get_or_create_collection("rocky_memory")
    results = collection.query(query_texts=[prompt], n_results=n)
    docs = results.get("documents", [[]])[0]
    return "\n".join(docs)
```

### Fix 4 — Update `routes/chat.py` and `routes/memory.py` to use real services
- `routes/chat.py`: call `query_memory(request.message)` first, then pass result as `context` to `get_reply()`
- `routes/memory.py`: replace `mock_store_file` with `store_file` from `vector_db.py`

### Fix 5 — Update CORS in `main.py`
```python
import os
allow_origins = [os.environ.get("FRONTEND_URL", "http://localhost:5173")]
```

**WHEN DONE:** Update `.agent/status/codex-status.md`
