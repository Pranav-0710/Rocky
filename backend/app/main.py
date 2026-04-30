from dotenv import load_dotenv
load_dotenv()

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router
from app.routes.memory import router as memory_router


app = FastAPI(title="Agent Rocky API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("FRONTEND_URL", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app.include_router(chat_router, prefix="/api")
app.include_router(memory_router, prefix="/api")

# Serve the static React app
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")

if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Allow API routes to pass through (though they are mounted earlier, this handles fallbacks)
        if full_path.startswith("api/"):
            return {"detail": "Not Found"}
            
        # Serve specific requested files in the root (like logo.png, manifest.json)
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
            
        # For all other paths, serve React's index.html (SPA routing)
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "Agent Rocky Backend is Live! Build the frontend to see the UI."}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
