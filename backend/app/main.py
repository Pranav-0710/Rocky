from dotenv import load_dotenv
load_dotenv()

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router
from app.routes.memory import router as memory_router


app = FastAPI(title="Agent Rocky API")

# CORS — allow frontend origin
frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:5173")
origins = [frontend_url, "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")
app.include_router(memory_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Agent Rocky Backend is Live!", "status": "ok"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
