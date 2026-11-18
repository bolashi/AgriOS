from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import GEMINI_API_KEY
from .services.model_registry import ModelRegistry
from .routers import detect, insights, assistant, voice
import os

app = FastAPI(title="AgriOS API", version="0.1.0")
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])
registry = ModelRegistry()
app.include_router(detect.router, prefix="/api")
app.include_router(insights.router, prefix="/api")
app.include_router(assistant.router, prefix="/api")
app.include_router(voice.router, prefix="/api")

@app.get("/api/health")
def health():
    return {"status": "ok", "version": "0.1.0",
            "model": {"status": registry.status, "error": registry.error},
            "gemini_configured": bool(GEMINI_API_KEY)}

@app.get("/api/model/info")
def model_info():
    return registry.info()
