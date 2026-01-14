#!/usr/bin/env python3
"""
Link historical events to patterns based on extra_data.
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = str(Path(__file__).parent / "backend")
sys.path.insert(0, backend_path)
print(f"Added to path: {backend_path}")

import os
os.environ.setdefault("DATABASE_URL", "postgresql://sigandwa:sigandwa_dev@localhost:5432/sigandwa")
os.environ.setdefault("ALLOWED_ORIGINS", '["http://localhost:3000","http://localhost:8000"]')

from app.database import SessionLocal
from app.models.chronology import ChronologyEvent
from app.patterns.library import PatternLibrary

print("🔗 Linking events to patterns...")

db = SessionLocal()
library = PatternLibrary(db)

# Get all patterns
patterns = {p.name: p for p in library.get_all_patterns()}

# Pattern name mappings (from extra_data to pattern names)
PATTERN_MAPPINGS = {
    "moral_decay_judgment": "Moral Decay → Divine Judgment",
    "pride_humbling": "Pride → Humbling/Fall",
    "pride_fall": "Pride → Humbling/Fall",
    "exile_restoration": "Exile → Restoration",
    "persecution_growth": "Persecution → Growth",
    "unity_fragmentation": "Unity → Fragmentation",
    "delayed_fulfillment": "Promise Delayed → Eventually Fulfilled",
}

# Get all events
events = db.query(ChronologyEvent).all()

links_created = 0

for event in events:
    extra_data = event.extra_data or {}
    pattern_key = extra_data.get("pattern")

    if pattern_key and pattern_key in PATTERN_MAPPINGS:
        pattern_name = PATTERN_MAPPINGS[pattern_key]
        pattern = patterns.get(pattern_name)

        if pattern:
            try:
                # Link with strength 7 (strong match)
                library.match_pattern_to_event(event, pattern, strength=7)
                links_created += 1
                if links_created % 10 == 0:
                    print(f"   - Linked {links_created} events...")
            except Exception as e:
                # Skip if already linked
                continue

db.commit()
db.close()

print(f"✅ Linked {links_created} events to patterns")
