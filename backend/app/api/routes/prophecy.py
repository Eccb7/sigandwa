"""
API routes for prophecy operations.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_prophecies():
    """List all prophecies (placeholder)."""
    return {"message": "Prophecy endpoint - to be implemented"}
