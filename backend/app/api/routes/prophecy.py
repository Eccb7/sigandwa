"""
API routes for prophecy operations.
"""

from fastapi import APIRouter, Query
from typing import Optional, List, Dict, Any
from sqlalchemy import text
from app.database import engine

router = APIRouter()


@router.get("/")
async def list_prophecies(
    prophet: Optional[str] = Query(None, description="Filter by prophet name"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
) -> List[Dict[str, Any]]:
    """List all prophecies from the database."""
    try:
        with engine.connect() as conn:
            # Build query
            query = """
                SELECT 
                    id,
                    reference,
                    text,
                    prophet,
                    year_declared,
                    prophecy_type,
                    scope,
                    interpretation_notes,
                    elements
                FROM prophecy_texts
            """
            
            params = {}
            if prophet:
                query += " WHERE prophet = :prophet"
                params["prophet"] = prophet
            
            query += " ORDER BY id LIMIT :limit OFFSET :offset"
            params["limit"] = limit
            params["offset"] = offset
            
            result = conn.execute(text(query), params)
            
            prophecies = []
            for row in result:
                prophecies.append({
                    "id": row[0],
                    "reference": row[1],
                    "text": row[2],
                    "prophet": row[3],
                    "year_declared": row[4],
                    "prophecy_type": row[5],
                    "scope": row[6],
                    "interpretation_notes": row[7],
                    "elements": row[8]
                })
            
            return prophecies
    except Exception as e:
        # Log error and return empty list
        print(f"Error fetching prophecies: {e}")
        return []


@router.get("/stats")
async def get_prophecy_stats() -> Dict[str, Any]:
    """Get statistics about prophecies."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(DISTINCT prophet) as prophet_count,
                    COUNT(DISTINCT prophecy_type) as type_count
                FROM prophecy_texts
            """))
            row = result.fetchone()
            
            # Get counts by prophet
            prophet_result = conn.execute(text("""
                SELECT prophet, COUNT(*) as count
                FROM prophecy_texts
                GROUP BY prophet
                ORDER BY count DESC
            """))
            
            by_prophet = {row[0]: row[1] for row in prophet_result}
            
            return {
                "total": row[0] if row else 0,
                "prophet_count": row[1] if row else 0,
                "type_count": row[2] if row else 0,
                "by_prophet": by_prophet
            }
    except Exception as e:
        print(f"Error fetching prophecy stats: {e}")
        return {
            "total": 0,
            "prophet_count": 0,
            "type_count": 0,
            "by_prophet": {}
        }
