"""
Database seeding script.
Populates the chronology with Biblical and historical events.
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.chronology import ChronologyEra, EventType
from app.chronology.engine import ChronologyEngine

# Import seed data
from biblical_timeline import BIBLICAL_EVENTS
from historical_continuation import HISTORICAL_CONTINUATION


def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created")


def seed_events(db: Session):
    """Seed chronology events."""
    engine = ChronologyEngine(db)

    print("\nSeeding Biblical events...")
    for event_data in BIBLICAL_EVENTS:
        try:
            # Convert string enums to enum types
            event_data["era"] = ChronologyEra[event_data["era"]]
            event_data["event_type"] = EventType[event_data["event_type"]]

            engine.add_event(**event_data)
            print(f"  ✓ Added: {event_data['name']} ({event_data['year_start']})")
        except Exception as e:
            print(f"  ✗ Failed to add {event_data['name']}: {e}")

    print(f"\n✓ Seeded {len(BIBLICAL_EVENTS)} Biblical events")

    print("\nSeeding historical continuation events...")
    for event_data in HISTORICAL_CONTINUATION:
        try:
            event_data["era"] = ChronologyEra[event_data["era"]]
            event_data["event_type"] = EventType[event_data["event_type"]]

            engine.add_event(**event_data)
            print(f"  ✓ Added: {event_data['name']} ({event_data['year_start']})")
        except Exception as e:
            print(f"  ✗ Failed to add {event_data['name']}: {e}")

    print(f"\n✓ Seeded {len(HISTORICAL_CONTINUATION)} historical events")


def main():
    """Main seeding function."""
    print("=" * 60)
    print("Sigandwa Database Seeding")
    print("=" * 60)

    # Create tables (safe if they already exist)
    create_tables()

    # Get database session
    db = SessionLocal()

    try:
        seed_events(db)
        print("\n" + "=" * 60)
        print("✓ Database seeding completed successfully")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Seeding failed: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
