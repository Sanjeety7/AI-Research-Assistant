# backend/app/main.py
"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import research, ingest, health

app = FastAPI(
    title="AI Research Assistant",
    description="Multi-model intelligent backend",
    version="1.0.0"
)

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(research.router, prefix="/api/research", tags=["research"])
app.include_router(ingest.router, prefix="/api/ingest", tags=["ingest"])
