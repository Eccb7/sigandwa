"""
Prophecy API Endpoints
Handles prophecy-fulfillment mapping operations.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.prophecy.library import ProphecyLibrary
from app.models.prophecy import ProphecyText, ProphecyFulfillment, FulfillmentType

router = APIRouter()


# ============================================================================
# Response Models (Pydantic schemas)
# ============================================================================


from pydantic import BaseModel, Field


class ProphecyResponse(BaseModel):
    id: int
    reference: str
    text: str
    prophet: Optional[str] = None
    year_declared: Optional[int] = None
    prophecy_type: Optional[str] = None
    scope: Optional[str] = None
    elements: Optional[List[dict]] = None

    class Config:
        from_attributes = True


class FulfillmentResponse(BaseModel):
    id: int
    prophecy_id: int
    event_id: int
    fulfillment_type: str
    confidence_score: Optional[float] = None
    explanation: str
    elements_fulfilled: Optional[List[str]] = None

    class Config:
        from_attributes = True


class FulfillmentWithEventResponse(BaseModel):
    fulfillment: FulfillmentResponse
    event_name: str
    event_year: Optional[int] = None
    event_description: Optional[str] = None


class TimelineAnalysisResponse(BaseModel):
    prophecy_id: int
    reference: str
    year_declared: Optional[int] = None
    total_fulfillments: int
    fulfillment_types: dict
    years_to_first_fulfillment: Optional[int] = None
    timeline: List[dict]


class FulfillmentCandidateResponse(BaseModel):
    event_id: int
    event_name: str
    event_year: Optional[int] = None
    confidence: float
    matched_keywords: List[str]


class SeedResultResponse(BaseModel):
    total_prophecies: int
    seeded: int
    skipped: int
    seeded_references: List[str]
    skipped_references: List[str]


# ============================================================================
# Endpoints
# ============================================================================


@router.get("/", response_model=List[ProphecyResponse])
def list_prophecies(
    prophecy_type: Optional[str] = Query(None, description="Filter by prophecy type"),
    scope: Optional[str] = Query(None, description="Filter by scope"),
    db: Session = Depends(get_db),
):
    """
    List all prophecies with optional filtering.

    Filters:
    - prophecy_type: messianic, judgment, restoration, kingdom_succession, etc.
    - scope: local, national, international, eschatological
    """
    library = ProphecyLibrary(db)
    prophecies = library.get_all_prophecies(prophecy_type=prophecy_type, scope=scope)

    return [
        ProphecyResponse(
            id=p.id,
            reference=p.reference,
            text=p.text,
            prophet=p.prophet,
            year_declared=p.year_declared,
            prophecy_type=p.prophecy_type,
            scope=p.scope,
            elements=p.elements,
        )
        for p in prophecies
    ]


@router.get("/{prophecy_id}", response_model=ProphecyResponse)
def get_prophecy(prophecy_id: int, db: Session = Depends(get_db)):
    """Get a specific prophecy by ID."""
    library = ProphecyLibrary(db)
    prophecy = library.get_prophecy_by_id(prophecy_id)

    if not prophecy:
        raise HTTPException(status_code=404, detail="Prophecy not found")

    return ProphecyResponse(
        id=prophecy.id,
        reference=prophecy.reference,
        text=prophecy.text,
        prophet=prophecy.prophet,
        year_declared=prophecy.year_declared,
        prophecy_type=prophecy.prophecy_type,
        scope=prophecy.scope,
        elements=prophecy.elements,
    )


@router.get("/{prophecy_id}/fulfillments", response_model=List[FulfillmentWithEventResponse])
def get_fulfillments(
    prophecy_id: int,
    fulfillment_type: Optional[str] = Query(
        None, description="Filter by fulfillment type"
    ),
    db: Session = Depends(get_db),
):
    """
    Get all fulfillments for a prophecy.

    Fulfillment types: complete, partial, repeated, conditional, pending, symbolic
    """
    library = ProphecyLibrary(db)

    # Verify prophecy exists
    prophecy = library.get_prophecy_by_id(prophecy_id)
    if not prophecy:
        raise HTTPException(status_code=404, detail="Prophecy not found")

    # Convert fulfillment_type string to enum if provided
    ft_enum = None
    if fulfillment_type:
        try:
            ft_enum = FulfillmentType(fulfillment_type)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid fulfillment type. Valid types: {[ft.value for ft in FulfillmentType]}",
            )

    fulfillments = library.get_fulfillments(prophecy_id, fulfillment_type=ft_enum)

    from app.models.chronology import ChronologyEvent

    result = []
    for f in fulfillments:
        event = db.query(ChronologyEvent).filter(ChronologyEvent.id == f.event_id).first()

        result.append(
            FulfillmentWithEventResponse(
                fulfillment=FulfillmentResponse(
                    id=f.id,
                    prophecy_id=f.prophecy_id,
                    event_id=f.event_id,
                    fulfillment_type=f.fulfillment_type.value,
                    confidence_score=f.confidence_score,
                    explanation=f.explanation,
                    elements_fulfilled=f.elements_fulfilled,
                ),
                event_name=event.name if event else "Unknown",
                event_year=event.year_start if event else None,
                event_description=event.description if event else None,
            )
        )

    return result


@router.get("/{prophecy_id}/timeline", response_model=TimelineAnalysisResponse)
def analyze_timeline(prophecy_id: int, db: Session = Depends(get_db)):
    """
    Analyze the timeline of fulfillments for a prophecy.

    Returns statistical analysis including:
    - Total fulfillments
    - Distribution by fulfillment type
    - Years from prophecy to first fulfillment
    - Chronological timeline of all fulfillments
    """
    library = ProphecyLibrary(db)

    # Verify prophecy exists
    prophecy = library.get_prophecy_by_id(prophecy_id)
    if not prophecy:
        raise HTTPException(status_code=404, detail="Prophecy not found")

    analysis = library.analyze_fulfillment_timeline(prophecy_id)

    return TimelineAnalysisResponse(**analysis)


@router.post("/detect-candidates/{prophecy_id}", response_model=List[FulfillmentCandidateResponse])
def detect_candidates(
    prophecy_id: int,
    confidence_threshold: float = Query(
        0.5, ge=0.0, le=1.0, description="Minimum confidence score (0.0-1.0)"
    ),
    db: Session = Depends(get_db),
):
    """
    Detect potential events that might fulfill a prophecy based on keyword matching.

    Returns candidates with confidence scores based on keyword overlap.
    """
    library = ProphecyLibrary(db)

    # Verify prophecy exists
    prophecy = library.get_prophecy_by_id(prophecy_id)
    if not prophecy:
        raise HTTPException(status_code=404, detail="Prophecy not found")

    candidates = library.detect_fulfillment_candidates(
        prophecy_id, confidence_threshold=confidence_threshold
    )

    return [
        FulfillmentCandidateResponse(
            event_id=c["event"].id,
            event_name=c["event"].name,
            event_year=c["event"].year_start,
            confidence=c["confidence"],
            matched_keywords=c["matched_keywords"],
        )
        for c in candidates
    ]


@router.post("/seed", response_model=SeedResultResponse)
def seed_prophecies(db: Session = Depends(get_db)):
    """
    Seed core Biblical prophecies into the database.

    Idempotent operation - safe to run multiple times.

    Seeds 6 core prophecies:
    - Daniel 2 (Four Kingdoms)
    - Daniel 7 (Four Beasts)
    - Daniel 9 (70 Weeks)
    - Isaiah 53 (Suffering Servant)
    - Jeremiah 25 (70 Years)
    - Isaiah 44-45 (Cyrus Named)
    """
    library = ProphecyLibrary(db)
    result = library.seed_core_prophecies()

    return SeedResultResponse(**result)


@router.post("/{prophecy_id}/link/{event_id}", response_model=FulfillmentResponse)
def link_fulfillment(
    prophecy_id: int,
    event_id: int,
    fulfillment_type: str = Query(..., description="Type of fulfillment"),
    confidence_score: float = Query(..., ge=0.0, le=1.0, description="Confidence (0.0-1.0)"),
    explanation: str = Query(..., description="How the event fulfills the prophecy"),
    elements: Optional[List[str]] = Query(
        None, description="List of prophecy element IDs fulfilled"
    ),
    db: Session = Depends(get_db),
):
    """
    Manually link a prophecy to an event as a fulfillment.

    Fulfillment types: complete, partial, repeated, conditional, pending, symbolic
    """
    from app.models.chronology import ChronologyEvent

    library = ProphecyLibrary(db)

    # Verify prophecy exists
    prophecy = library.get_prophecy_by_id(prophecy_id)
    if not prophecy:
        raise HTTPException(status_code=404, detail="Prophecy not found")

    # Verify event exists
    event = db.query(ChronologyEvent).filter(ChronologyEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Convert fulfillment_type string to enum
    try:
        ft_enum = FulfillmentType(fulfillment_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid fulfillment type. Valid types: {[ft.value for ft in FulfillmentType]}",
        )

    fulfillment = library.link_fulfillment(
        prophecy=prophecy,
        event=event,
        fulfillment_type=ft_enum,
        confidence_score=confidence_score,
        explanation=explanation,
        elements_fulfilled=elements,
    )

    return FulfillmentResponse(
        id=fulfillment.id,
        prophecy_id=fulfillment.prophecy_id,
        event_id=fulfillment.event_id,
        fulfillment_type=fulfillment.fulfillment_type.value,
        confidence_score=fulfillment.confidence_score,
        explanation=explanation,
        elements_fulfilled=fulfillment.elements_fulfilled,
    )
