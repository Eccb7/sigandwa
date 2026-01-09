"""
Pydantic schemas for chronology API requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

from app.models.chronology import ChronologyEra, EventType


class ChronologyEventBase(BaseModel):
    """Base schema for chronology events."""

    name: str = Field(..., description="Event name")
    description: Optional[str] = Field(None, description="Detailed description")
    year_start: int = Field(..., description="Start year (negative for BC, positive for AD)")
    year_end: Optional[int] = Field(None, description="End year if event has duration")
    year_start_min: Optional[int] = Field(None, description="Earliest possible start year")
    year_start_max: Optional[int] = Field(None, description="Latest possible start year")
    year_end_min: Optional[int] = Field(None, description="Earliest possible end year")
    year_end_max: Optional[int] = Field(None, description="Latest possible end year")
    era: ChronologyEra = Field(..., description="Chronological era")
    event_type: EventType = Field(..., description="Primary event classification")
    biblical_source: Optional[str] = Field(None, description="Biblical reference (e.g., Genesis 7)")
    historical_source: Optional[str] = Field(None, description="Historical source references")
    extra_data: Optional[Dict[str, Any]] = Field(None, description="Additional structured data")


class ChronologyEventCreate(ChronologyEventBase):
    """Schema for creating new chronology events."""

    pass


class ChronologyEventResponse(ChronologyEventBase):
    """Schema for chronology event responses."""

    id: int

    class Config:
        from_attributes = True


class TimelineSummaryResponse(BaseModel):
    """Schema for timeline summary statistics."""

    total_events: int
    era_distribution: Dict[str, int]
    type_distribution: Dict[str, int]
    year_range: Dict[str, Optional[int]]
