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

app.include_router(chat_router, prefix="/api")
app.include_router(memory_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Agent Rocky Backend is Live! Please use the frontend app to interact."}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
