"""
Tests for chronology engine functionality.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.chronology.engine import ChronologyEngine
from app.models.chronology import ChronologyEra, EventType

TEST_DATABASE_URL = "sqlite:///./test_chronology.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create test database session."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_add_event(db_session):
    """Test adding an event to chronology."""
    engine_instance = ChronologyEngine(db_session)

    event = engine_instance.add_event(
        name="Fall of Jerusalem",
        year_start=-586,
        era=ChronologyEra.EXILE,
        event_type=EventType.MILITARY,
        description="Babylonian conquest",
    )

    assert event.id is not None
    assert event.name == "Fall of Jerusalem"
    assert event.year_start == -586


def test_get_events_in_range(db_session):
    """Test querying events within a year range."""
    engine_instance = ChronologyEngine(db_session)

    # Add test events
    engine_instance.add_event(
        name="Event 1", year_start=-1000, era=ChronologyEra.UNITED_MONARCHY, event_type=EventType.POLITICAL
    )
    engine_instance.add_event(
        name="Event 2", year_start=-900, era=ChronologyEra.DIVIDED_KINGDOM, event_type=EventType.MILITARY
    )
    engine_instance.add_event(
        name="Event 3", year_start=-800, era=ChronologyEra.DIVIDED_KINGDOM, event_type=EventType.RELIGIOUS
    )

    # Query range
    events = engine_instance.get_events_in_range(-950, -850)

    assert len(events) == 1
    assert events[0].name == "Event 2"


def test_calculate_temporal_distance(db_session):
    """Test calculating years between events."""
    engine_instance = ChronologyEngine(db_session)

    event1 = engine_instance.add_event(
        name="Exodus", year_start=-1491, era=ChronologyEra.EXODUS_TO_JUDGES, event_type=EventType.POLITICAL
    )
    event2 = engine_instance.add_event(
        name="Solomon's Temple", year_start=-1005, era=ChronologyEra.UNITED_MONARCHY, event_type=EventType.RELIGIOUS
    )

    distance = engine_instance.calculate_temporal_distance(event1.id, event2.id)

    assert distance == 486  # 1491 - 1005 = 486 years


def test_find_contemporaneous_events(db_session):
    """Test finding events that occurred around the same time."""
    engine_instance = ChronologyEngine(db_session)

    # Create reference event
    ref_event = engine_instance.add_event(
        name="Reference Event",
        year_start=-700,
        era=ChronologyEra.DIVIDED_KINGDOM,
        event_type=EventType.POLITICAL,
    )

    # Create nearby events
    engine_instance.add_event(
        name="Nearby Event 1", year_start=-705, era=ChronologyEra.DIVIDED_KINGDOM, event_type=EventType.MILITARY
    )
    engine_instance.add_event(
        name="Nearby Event 2", year_start=-695, era=ChronologyEra.DIVIDED_KINGDOM, event_type=EventType.RELIGIOUS
    )
    engine_instance.add_event(
        name="Far Event", year_start=-500, era=ChronologyEra.EXILE, event_type=EventType.POLITICAL
    )

    # Find contemporaneous events within 10 years
    contemporaneous = engine_instance.find_contemporaneous_events(ref_event.id, window_years=10)

    assert len(contemporaneous) == 2
    names = [e.name for e in contemporaneous]
    assert "Nearby Event 1" in names
    assert "Nearby Event 2" in names
    assert "Far Event" not in names
