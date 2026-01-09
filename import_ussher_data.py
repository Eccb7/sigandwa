#!/usr/bin/env python3
"""
Import Ussher's Annals data into the database
Run this after the system is started
"""

import sys
import asyncio
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models.chronology import ChronologyEvent, EventType, ChronologyEra
from data.seed.ussher_annals_seed import USSHER_ANNALS_EVENTS


def import_events():
    """Import all Ussher Annals events into the database"""
    
    print("\n" + "="*70)
    print("  IMPORTING USSHER'S ANNALS OF THE WORLD DATA")
    print("="*70 + "\n")
    
    from app.database import SessionLocal
    db = SessionLocal()
    
    try:
        # Check how many events already exist
        existing_count = db.query(ChronologyEvent).count()
        print(f"📊 Current events in database: {existing_count}")
        
        imported_count = 0
        skipped_count = 0
        
        for event_data in USSHER_ANNALS_EVENTS:
            # Check if event already exists by name and year
            existing = db.query(ChronologyEvent).filter(
                ChronologyEvent.name == event_data["name"],
                ChronologyEvent.year_start == event_data["year_start"]
            ).first()
            
            if existing:
                print(f"⏭️  Skipping (already exists): {event_data['name']}")
                skipped_count += 1
                continue
            
            # Create new event
            # Merge key_actors and source_references into extra_data
            extra_data = event_data.get("extra_data", {}).copy()
            if "key_actors" in event_data:
                extra_data["key_actors"] = event_data["key_actors"]
            if "source_references" in event_data:
                extra_data["source_references"] = event_data["source_references"]
            
            event = ChronologyEvent(
                name=event_data["name"],
                description=event_data["description"],
                year_start=event_data["year_start"],
                year_end=event_data.get("year_end"),
                year_start_min=event_data.get("year_start_min"),
                year_start_max=event_data.get("year_start_max"),
                era=event_data["era"],  # Already a string matching enum values
                event_type=event_data["event_type"],  # Already a string matching enum values
                biblical_source=event_data.get("biblical_source"),
                extra_data=extra_data
            )
            
            db.add(event)
            print(f"✅ Imported: {event_data['name']} ({event_data['year_start']} BC/AD)")
            imported_count += 1
        
        # Commit all changes
        db.commit()
        
        print("\n" + "-"*70)
        print(f"✨ Import complete!")
        print(f"   • New events imported: {imported_count}")
        print(f"   • Events skipped: {skipped_count}")
        print(f"   • Total events in database: {existing_count + imported_count}")
        print("-"*70 + "\n")
        
        # Show some statistics
        print("📈 Event breakdown by era:")
        for era in ChronologyEra:
            count = db.query(ChronologyEvent).filter(
                ChronologyEvent.era == era
            ).count()
            if count > 0:
                print(f"   • {era.value}: {count} events")
        
        print("\n📈 Event breakdown by type:")
        for event_type in EventType:
            count = db.query(ChronologyEvent).filter(
                ChronologyEvent.event_type == event_type
            ).count()
            if count > 0:
                print(f"   • {event_type.value}: {count} events")
        
    except Exception as e:
        print(f"\n❌ Error during import: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import_events()
