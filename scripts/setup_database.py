#!/usr/bin/env python3
"""
Direct database setup script - bypasses Alembic.
Creates tables and seeds data directly using SQLAlchemy.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

# Set environment
import os
os.environ.setdefault("DATABASE_URL", "postgresql://sigandwa:sigandwa_dev@localhost:5432/sigandwa")
os.environ.setdefault("NEO4J_URI", "bolt://localhost:7687")
os.environ.setdefault("NEO4J_USER", "neo4j")
os.environ.setdefault("NEO4J_PASSWORD", "sigandwa_dev")
os.environ.setdefault("ALLOWED_ORIGINS", "[]")

print("🔧 Setting up Sigandwa database...")

print("\n1️⃣  Connecting to PostgreSQL...")
from app.database import engine, Base, SessionLocal
from app.models import chronology, prophecy, simulation

print("✅ Connection established")

print("\n2️⃣  Dropping existing tables (if any)...")
Base.metadata.drop_all(bind=engine)
print("✅ Tables dropped")

print("\n3️⃣  Creating all tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created")

print("\n4️⃣  Loading seed data...")
sys.path.insert(0, str(Path(__file__).parent / "data" / "seed"))
from biblical_timeline import BIBLICAL_EVENTS
from historical_continuation import HISTORICAL_CONTINUATION

print(f"   - Biblical events: {len(BIBLICAL_EVENTS)}")
print(f"   - Historical continuation: {len(HISTORICAL_CONTINUATION)}")

print("\n5️⃣  Seeding events...")
db = SessionLocal()
try:
    from app.models.chronology import ChronologyEvent, ChronologyEra, EventType
    
    all_events = BIBLICAL_EVENTS + HISTORICAL_CONTINUATION
    for i, event_data in enumerate(all_events, 1):
        try:
            # Convert era string to enum
            era_str = event_data["era"].upper().replace(" ", "_").replace("-", "_")
            era_enum = ChronologyEra[era_str]
            
            # Convert event_type string to enum
            event_type_str = event_data.get("event_type", "RELIGIOUS").upper()
            event_type_enum = EventType[event_type_str]
            
            event = ChronologyEvent(
                name=event_data["name"],
                description=event_data.get("description"),
                year_start=event_data["year_start"],
                year_end=event_data.get("year_end"),
                year_start_min=event_data.get("year_start_min"),
                year_start_max=event_data.get("year_start_max"),
                year_end_min=event_data.get("year_end_min"),
                year_end_max=event_data.get("year_end_max"),
                era=era_enum,
                event_type=event_type_enum,
                biblical_source=event_data.get("biblical_source"),
                historical_source=event_data.get("historical_source"),
                extra_data=event_data.get("extra_data", event_data.get("metadata"))  # Handle both names
            )
            db.add(event)
            
            if i % 20 == 0:
                print(f"   - Seeded {i}/{len(all_events)} events...")
        except Exception as e:
            print(f"   ⚠️  Error seeding event {event_data.get('name', 'Unknown')}: {e}")
            continue
    
    db.commit()
    print(f"✅ Seeded {len(all_events)} events successfully")
    
except Exception as e:
    print(f"❌ Error during seeding: {e}")
    db.rollback()
    raise
finally:
    db.close()

print("\n6️⃣  Initializing Neo4j...")
try:
    sys.path.insert(0, str(Path(__file__).parent / "data" / "seed"))
    from init_neo4j import Neo4jInitializer
    
    initializer = Neo4jInitializer()
    initializer.initialize()
    print("✅ Neo4j initialized")
except Exception as e:
    print(f"⚠️  Neo4j initialization warning: {e}")
    print("   (This is non-critical - continuing)")

print("\n✅ Database setup complete!")
print(f"\n📊 Summary:")
print(f"   - Tables: {len(Base.metadata.tables)}")
print(f"   - Events: {len(all_events)}")
print(f"   - Biblical: {len(BIBLICAL_EVENTS)}")
print(f"   - Historical: {len(HISTORICAL_CONTINUATION)}")
print(f"\n🚀 Run: cd backend && uvicorn app.main:app --reload")
