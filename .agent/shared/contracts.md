# Contracts — Single Source of Truth

## File Structure
/backend (Python FastAPI)
  /app
    main.py
    /routes
      chat.py
      memory.py
    /services
      llm.py
      vector_db.py
  requirements.txt
/frontend (React Vite PWA)
  /src
    App.tsx
    /components
      ChatInterface.tsx
      Planner.tsx
    /pages
  package.json

## API Endpoints
- `POST /api/chat`
  - Request: `{ "message": "string" }`
  - Response: `{ "reply": "string", "actions": [] }`
- `POST /api/memory/upload`
  - Request: `multipart/form-data (file)`
  - Response: `{ "status": "success", "chunks_added": int }`
- `GET /api/planner/reminders`
  - Request: `none`
  - Response: `{ "reminders": [] }`

## Shared Data Schemas
- `Reminder`: `{ id: string, title: string, time: datetime, status: string }`
- `MemoryChunk`: `{ id: string, content: string, metadata: dict }`

## Environment Variables
- `GEMINI_API_KEY`: Google Gemini key
- `CHROMA_DB_DIR`: Local path for ChromaDB storage

## Integration Points
- Frontend React app calls FastAPI on `http://localhost:8000/api`
