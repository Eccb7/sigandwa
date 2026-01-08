"""
API routes for simulation operations.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_simulations():
    """List all simulations (placeholder)."""
    return {"message": "Simulation endpoint - to be implemented"}
