"""
API routes for chronology operations.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.chronology.engine import ChronologyEngine
from app.models.chronology import ChronologyEra, EventType
from app.schemas.chronology import (
    ChronologyEventResponse,
    ChronologyEventCreate,
    TimelineSummaryResponse,
)

router = APIRouter()


@router.get("/events", response_model=List[ChronologyEventResponse])
async def get_events(
    year_start: Optional[int] = Query(None, description="Start year (negative for BC)"),
    year_end: Optional[int] = Query(None, description="End year (negative for BC)"),
    era: Optional[ChronologyEra] = Query(None, description="Filter by era"),
    event_type: Optional[EventType] = Query(None, description="Filter by event type"),
    limit: int = Query(100, le=1000, description="Maximum number of events to return"),
    db: Session = Depends(get_db),
):
    """
    Retrieve events from the chronology.

    Supports filtering by year range, era, and event type.
    """
    engine = ChronologyEngine(db)

    if year_start and year_end:
        events = engine.get_events_in_range(year_start, year_end)
    elif era:
        events = engine.get_events_by_era(era)
    else:
        # Default: get recent historical events
        events = engine.get_events_in_range(-4000, 2026)

    # Apply type filter if specified
    if event_type:
        events = [e for e in events if e.event_type == event_type]

    return events[:limit]


@router.get("/events/{event_id}", response_model=ChronologyEventResponse)
async def get_event_by_id(event_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific event by ID."""
    from app.models.chronology import ChronologyEvent

    event = db.query(ChronologyEvent).filter(ChronologyEvent.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@router.post("/events", response_model=ChronologyEventResponse)
async def create_event(event: ChronologyEventCreate, db: Session = Depends(get_db)):
    """
    Add a new event to the chronology.

    This endpoint allows extending the timeline with new historical or Biblical events.
    """
    engine = ChronologyEngine(db)

    new_event = engine.add_event(
        name=event.name,
        year_start=event.year_start,
        era=event.era,
        event_type=event.event_type,
        description=event.description,
        year_end=event.year_end,
        year_start_min=event.year_start_min,
        year_start_max=event.year_start_max,
        biblical_source=event.biblical_source,
        historical_source=event.historical_source,
        metadata=event.metadata,
    )

    return new_event


@router.get("/events/{event_id}/contemporaneous", response_model=List[ChronologyEventResponse])
async def get_contemporaneous_events(
    event_id: int,
    window_years: int = Query(10, description="Years before/after to search"),
    db: Session = Depends(get_db),
):
    """
    Find events occurring around the same time as the specified event.

    Useful for identifying correlations and patterns across different domains.
    """
    engine = ChronologyEngine(db)
    events = engine.find_contemporaneous_events(event_id, window_years)

    return events


@router.get("/summary", response_model=TimelineSummaryResponse)
async def get_timeline_summary(
    start_year: Optional[int] = Query(None, description="Start year for summary"),
    end_year: Optional[int] = Query(None, description="End year for summary"),
    db: Session = Depends(get_db),
):
    """
    Get statistical summary of the timeline.

    Returns event counts, distribution by era and type, and year range.
    """
    engine = ChronologyEngine(db)
    summary = engine.get_timeline_summary(start_year, end_year)

    return summary
