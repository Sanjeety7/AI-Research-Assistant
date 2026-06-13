# backend/app/api/health.py
"""Health check API."""
from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def health_check():
    """Service health check."""
    return {"status": "healthy", "version": "1.0.0"}
