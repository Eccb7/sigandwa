"""
Chronology Engine: Core timeline management system.

This engine maintains the authoritative Biblical-to-present timeline,
handles uncertainty ranges, and provides temporal indexing operations.
"""

from typing import List, Optional, Tuple
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.chronology import ChronologyEvent, ChronologyEra, EventType


class ChronologyEngine:
    """
    The Chronology Engine is the foundational system for all temporal operations.

    It treats the Biblical timeline (Ussher-based) as continuous from Creation
    to the present, providing a single authoritative time index for all events.

    Key capabilities:
    - Query events by year, era, or range
    - Handle uncertainty in dates
    - Calculate temporal distances between events
    - Identify contemporaneous events across different regions
    """

    def __init__(self, db: Session):
        self.db = db

    def get_event_by_year(self, year: int, tolerance: int = 0) -> List[ChronologyEvent]:
        """
        Retrieve all events occurring in a specific year.

        Args:
            year: Year in Ussher chronology (negative for BC, positive for AD)
            tolerance: Years of flexibility (e.g., tolerance=5 finds events within 5 years)

        Returns:
            List of events occurring in or near the specified year
        """
        query = self.db.query(ChronologyEvent).filter(
            and_(
                ChronologyEvent.year_start >= year - tolerance,
                or_(
                    ChronologyEvent.year_end.is_(None),
                    ChronologyEvent.year_end <= year + tolerance,
                ),
            )
        )
        return query.all()

    def get_events_in_range(
        self, year_start: int, year_end: int, include_uncertain: bool = True
    ) -> List[ChronologyEvent]:
        """
        Retrieve all events within a year range.

        Args:
            year_start: Beginning of range (Ussher chronology)
            year_end: End of range (Ussher chronology)
            include_uncertain: Whether to include events with uncertain dates that
                             might fall within range

        Returns:
            List of events in the specified range
        """
        base_query = self.db.query(ChronologyEvent).filter(
            or_(
                # Event starts within range
                and_(
                    ChronologyEvent.year_start >= year_start,
                    ChronologyEvent.year_start <= year_end,
                ),
                # Event ends within range
                and_(
                    ChronologyEvent.year_end.isnot(None),
                    ChronologyEvent.year_end >= year_start,
                    ChronologyEvent.year_end <= year_end,
                ),
                # Event spans entire range
                and_(
                    ChronologyEvent.year_start <= year_start,
                    or_(
                        ChronologyEvent.year_end.is_(None),
                        ChronologyEvent.year_end >= year_end,
                    ),
                ),
            )
        )

        if include_uncertain:
            # Also include events where uncertainty bounds overlap with range
            # Use union_all and distinct() to avoid JSON equality issues
            uncertain_query = self.db.query(ChronologyEvent).filter(
                or_(
                    and_(
                        ChronologyEvent.year_start_min.isnot(None),
                        ChronologyEvent.year_start_min <= year_end,
                        ChronologyEvent.year_start_max >= year_start,
                    ),
                    and_(
                        ChronologyEvent.year_end_min.isnot(None),
                        ChronologyEvent.year_end_min <= year_end,
                        ChronologyEvent.year_end_max >= year_start,
                    ),
                )
            )
            # Get IDs from both queries and fetch unique events
            base_ids = {e.id for e in base_query.all()}
            uncertain_ids = {e.id for e in uncertain_query.all()}
            all_ids = base_ids | uncertain_ids
            
            if all_ids:
                return self.db.query(ChronologyEvent).filter(
                    ChronologyEvent.id.in_(all_ids)
                ).order_by(ChronologyEvent.year_start).all()
            return []

        return base_query.all()

    def get_events_by_era(self, era: ChronologyEra) -> List[ChronologyEvent]:
        """Retrieve all events within a specific chronological era."""
        return self.db.query(ChronologyEvent).filter(ChronologyEvent.era == era).all()

    def calculate_temporal_distance(self, event1_id: int, event2_id: int) -> Optional[int]:
        """
        Calculate years between two events.

        Returns:
            Number of years between events (negative if event1 is later than event2)
            None if either event doesn't exist
        """
        event1 = self.db.query(ChronologyEvent).filter(ChronologyEvent.id == event1_id).first()
        event2 = self.db.query(ChronologyEvent).filter(ChronologyEvent.id == event2_id).first()

        if not event1 or not event2:
            return None

        return event2.year_start - event1.year_start

    def find_contemporaneous_events(
        self, event_id: int, window_years: int = 10
    ) -> List[ChronologyEvent]:
        """
        Find events occurring around the same time as a given event.

        This is useful for identifying correlations between events in different regions
        or domains (e.g., political upheaval coinciding with religious reformation).

        Args:
            event_id: ID of the reference event
            window_years: Years before and after to search

        Returns:
            List of contemporaneous events (excluding the reference event itself)
        """
        event = self.db.query(ChronologyEvent).filter(ChronologyEvent.id == event_id).first()

        if not event:
            return []

        return (
            self.db.query(ChronologyEvent)
            .filter(
                and_(
                    ChronologyEvent.id != event_id,
                    ChronologyEvent.year_start >= event.year_start - window_years,
                    ChronologyEvent.year_start <= event.year_start + window_years,
                )
            )
            .all()
        )

    def add_event(
        self,
        name: str,
        year_start: int,
        era: ChronologyEra,
        event_type: EventType,
        description: Optional[str] = None,
        year_end: Optional[int] = None,
        year_start_min: Optional[int] = None,
        year_start_max: Optional[int] = None,
        biblical_source: Optional[str] = None,
        historical_source: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> ChronologyEvent:
        """
        Add a new event to the chronology.

        This is the primary method for building and extending the timeline.
        """
        event = ChronologyEvent(
            name=name,
            description=description,
            year_start=year_start,
            year_end=year_end,
            year_start_min=year_start_min,
            year_start_max=year_start_max,
            era=era,
            event_type=event_type,
            biblical_source=biblical_source,
            historical_source=historical_source,
            metadata=metadata,
        )

        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)

        return event

    def get_timeline_summary(
        self, start_year: Optional[int] = None, end_year: Optional[int] = None
    ) -> dict:
        """
        Generate a summary of the timeline, optionally bounded by years.

        Returns:
            Dictionary containing timeline statistics and key events
        """
        query = self.db.query(ChronologyEvent)

        if start_year is not None:
            query = query.filter(ChronologyEvent.year_start >= start_year)
        if end_year is not None:
            query = query.filter(ChronologyEvent.year_start <= end_year)

        events = query.all()

        # Calculate statistics
        event_count = len(events)
        era_distribution = {}
        type_distribution = {}

        for event in events:
            era_distribution[event.era.value] = era_distribution.get(event.era.value, 0) + 1
            type_distribution[event.event_type.value] = (
                type_distribution.get(event.event_type.value, 0) + 1
            )

        return {
            "total_events": event_count,
            "era_distribution": era_distribution,
            "type_distribution": type_distribution,
            "year_range": {
                "start": start_year or (min([e.year_start for e in events]) if events else None),
                "end": end_year or (max([e.year_start for e in events]) if events else None),
            },
        }
