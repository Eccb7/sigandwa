"""
API routes for pattern recognition and analysis.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.patterns.library import PatternLibrary
from app.models.chronology import Pattern

router = APIRouter()


@router.get("/", response_model=List[Dict[str, Any]])
def get_patterns(
    pattern_type: str = Query(None, description="Filter by pattern type"),
    db: Session = Depends(get_db),
):
    """
    Get all defined patterns.
    Optionally filter by pattern type.
    """
    library = PatternLibrary(db)
    patterns = library.get_all_patterns()

    if pattern_type:
        patterns = [p for p in patterns if p.pattern_type == pattern_type]

    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "pattern_type": p.pattern_type,
            "typical_duration_years": p.typical_duration_years,
            "biblical_basis": p.biblical_basis,
            "preconditions": p.preconditions,
            "indicators": p.indicators,
            "outcomes": p.outcomes,
        }
        for p in patterns
    ]


@router.get("/{pattern_id}")
def get_pattern(pattern_id: int, db: Session = Depends(get_db)):
    """Get a specific pattern by ID."""
    library = PatternLibrary(db)
    pattern = library.get_pattern_by_id(pattern_id)

    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    return {
        "id": pattern.id,
        "name": pattern.name,
        "description": pattern.description,
        "pattern_type": pattern.pattern_type,
        "typical_duration_years": pattern.typical_duration_years,
        "biblical_basis": pattern.biblical_basis,
        "preconditions": pattern.preconditions,
        "indicators": pattern.indicators,
        "outcomes": pattern.outcomes,
    }


@router.get("/{pattern_id}/instances")
def get_pattern_instances(pattern_id: int, db: Session = Depends(get_db)):
    """
    Get all historical instances where this pattern occurred.
    Returns events that exemplify the pattern.
    """
    library = PatternLibrary(db)

    # Verify pattern exists
    pattern = library.get_pattern_by_id(pattern_id)
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    instances = library.find_pattern_instances(pattern_id)

    return {
        "pattern_id": pattern_id,
        "pattern_name": pattern.name,
        "total_instances": len(instances),
        "instances": instances,
    }


@router.get("/{pattern_id}/analysis")
def analyze_pattern(pattern_id: int, db: Session = Depends(get_db)):
    """
    Analyze pattern recurrence across eras.
    Returns frequency, era distribution, and intervals.
    """
    library = PatternLibrary(db)

    # Verify pattern exists
    pattern = library.get_pattern_by_id(pattern_id)
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    analysis = library.analyze_pattern_recurrence(pattern_id)

    return {
        "pattern_id": pattern_id,
        "pattern_name": pattern.name,
        **analysis,
    }


@router.post("/detect")
def detect_patterns_in_event(
    event_id: int,
    db: Session = Depends(get_db),
):
    """
    Detect which patterns an event might exemplify.
    Uses keyword analysis on event data.
    """
    library = PatternLibrary(db)

    detected = library.detect_pattern_in_event(event_id)

    return {
        "event_id": event_id,
        "detected_patterns": detected,
        "count": len(detected),
    }


@router.post("/seed")
def seed_core_patterns(db: Session = Depends(get_db)):
    """
    Seed the database with the 6 core Biblical patterns.
    This is idempotent - won't create duplicates.
    """
    library = PatternLibrary(db)
    created = library.seed_core_patterns()

    return {
        "message": f"Seeded {len(created)} core patterns",
        "patterns": [p.name for p in created],
    }


@router.post("/{pattern_id}/link/{event_id}")
def link_pattern_to_event(
    pattern_id: int,
    event_id: int,
    strength: int = Query(5, ge=1, le=10, description="Pattern strength (1-10)"),
    db: Session = Depends(get_db),
):
    """
    Manually link a pattern to an event with a strength rating.
    Strength: 1 = weak match, 10 = perfect exemplar.
    """
    library = PatternLibrary(db)

    # Verify pattern and event exist
    pattern = library.get_pattern_by_id(pattern_id)
    if not pattern:
        raise HTTPException(status_code=404, detail="Pattern not found")

    from app.models.chronology import ChronologyEvent

    event = db.query(ChronologyEvent).filter(ChronologyEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Create link
    library.match_pattern_to_event(event, pattern, strength)

    return {
        "message": "Pattern linked to event",
        "pattern_id": pattern_id,
        "event_id": event_id,
        "strength": strength,
    }
