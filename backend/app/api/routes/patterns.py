"""
API routes for pattern operations.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_patterns():
    """List all patterns (placeholder)."""
    return {"message": "Patterns endpoint - to be implemented"}
