"""
API routes for event operations.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_events():
    """List all events (placeholder)."""
    return {"message": "Events endpoint - to be implemented"}
