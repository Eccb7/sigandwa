#!/usr/bin/env python3
"""
Link Prophecies to Historical Events
Establishes prophecy-fulfillment relationships based on historical data.
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = str(Path(__file__).parent / "backend")
sys.path.insert(0, backend_path)
print(f"Added to path: {backend_path}")

from app.database import SessionLocal
from app.models.prophecy import ProphecyText, FulfillmentType
from app.models.chronology import ChronologyEvent
from app.prophecy.library import ProphecyLibrary


def link_prophecy_fulfillments():
    """Link core prophecies to their historical fulfillments."""
    db = SessionLocal()
    library = ProphecyLibrary(db)

    print("🔗 Linking prophecies to fulfillment events...")

    # Mapping: (prophecy_reference, event_name_pattern, fulfillment_type, confidence, explanation, elements)
    fulfillment_mappings = [
        # Daniel 2:31-45 - Four Kingdoms
        (
            "Daniel 2:31-45",
            "Fall of Babylon",
            FulfillmentType.COMPLETE,
            0.95,
            "Babylonian Empire (head of gold) falls to Medo-Persian Empire (chest of silver)",
            ["head_gold", "chest_silver"],
        ),
        (
            "Daniel 2:31-45",
            "Cyrus Decree",
            FulfillmentType.COMPLETE,
            0.90,
            "Medo-Persian Empire establishes dominance under Cyrus",
            ["chest_silver"],
        ),
        (
            "Daniel 2:31-45",
            "Alexander the Great",
            FulfillmentType.COMPLETE,
            0.95,
            "Greek Empire (belly of bronze) conquers known world under Alexander",
            ["belly_bronze"],
        ),
        (
            "Daniel 2:31-45",
            "Roman Republic",
            FulfillmentType.PARTIAL,
            0.85,
            "Roman Empire (legs of iron) begins its dominance",
            ["legs_iron"],
        ),
        # Daniel 9:24-27 - 70 Weeks
        (
            "Daniel 9:24-27",
            "Decree of Artaxerxes",
            FulfillmentType.COMPLETE,
            0.90,
            "Decree to rebuild Jerusalem starts the 70 weeks prophecy countdown",
            ["decree_rebuild"],
        ),
        (
            "Daniel 9:24-27",
            "Crucifixion",
            FulfillmentType.COMPLETE,
            0.95,
            "Messiah cut off after 69 weeks (483 years from decree)",
            ["sixty_nine_sevens", "messiah_cut_off"],
        ),
        (
            "Daniel 9:24-27",
            "Fall of Jerusalem",
            FulfillmentType.COMPLETE,
            0.95,
            "City and sanctuary destroyed by Romans (people of the prince)",
            ["city_destroyed"],
        ),
        # Isaiah 53 - Suffering Servant
        (
            "Isaiah 53:1-12",
            "Crucifixion",
            FulfillmentType.COMPLETE,
            0.98,
            "Jesus fulfills suffering servant prophecy through crucifixion",
            [
                "despised_rejected",
                "wounded_sins",
                "silent_suffering",
                "death_burial",
                "justified_many",
            ],
        ),
        # Jeremiah 25 - 70 Years
        (
            "Jeremiah 25:8-14",
            "Fall of Jerusalem",
            FulfillmentType.COMPLETE,
            0.95,
            "Judah enters 70 years of Babylonian captivity",
            ["seventy_years"],
        ),
        (
            "Jeremiah 25:8-14",
            "Fall of Babylon",
            FulfillmentType.COMPLETE,
            0.95,
            "After 70 years, Babylon falls to Medo-Persian Empire",
            ["babylon_punished", "seventy_years"],
        ),
        (
            "Jeremiah 25:8-14",
            "Cyrus Decree",
            FulfillmentType.COMPLETE,
            0.90,
            "End of 70 years captivity, Jews return to rebuild",
            ["seventy_years"],
        ),
        # Isaiah 44-45 - Cyrus Named
        (
            "Isaiah 44:28-45:1",
            "Cyrus Decree",
            FulfillmentType.COMPLETE,
            0.95,
            "Cyrus, named 150 years before birth, decrees temple rebuilding",
            ["cyrus_named", "temple_rebuilt", "gods_shepherd"],
        ),
    ]

    linked_count = 0
    skipped_count = 0

    for (
        prophecy_ref,
        event_pattern,
        fulfillment_type,
        confidence,
        explanation,
        elements,
    ) in fulfillment_mappings:
        # Get prophecy
        prophecy = library.get_prophecy_by_reference(prophecy_ref)
        if not prophecy:
            print(f"⚠️  Prophecy not found: {prophecy_ref}")
            skipped_count += 1
            continue

        # Find matching event
        events = (
            db.query(ChronologyEvent)
            .filter(ChronologyEvent.name.ilike(f"%{event_pattern}%"))
            .all()
        )

        if not events:
            print(f"⚠️  Event not found matching: {event_pattern}")
            skipped_count += 1
            continue

        event = events[0]  # Take first match

        # Check if fulfillment already exists
        existing = (
            db.query(
                db.query(library.db.query(ProphecyText).filter_by(id=prophecy.id))
                .join(ProphecyText.fulfillments)
                .filter_by(event_id=event.id)
                .first()
            )
            if False
            else None
        )

        # Simple duplicate check
        from app.models.prophecy import ProphecyFulfillment

        existing = (
            db.query(ProphecyFulfillment)
            .filter(
                ProphecyFulfillment.prophecy_id == prophecy.id,
                ProphecyFulfillment.event_id == event.id,
            )
            .first()
        )

        if existing:
            print(
                f"  ⏭️  Skipping existing link: {prophecy_ref} -> {event.name}"
            )
            skipped_count += 1
            continue

        # Link prophecy to event
        library.link_fulfillment(
            prophecy=prophecy,
            event=event,
            fulfillment_type=fulfillment_type,
            confidence_score=confidence,
            explanation=explanation,
            elements_fulfilled=elements,
        )

        linked_count += 1
        print(
            f"  ✅ Linked: {prophecy_ref} -> {event.name} ({fulfillment_type.value}, {confidence:.0%} confidence)"
        )

        if linked_count % 5 == 0:
            print(f"     Progress: {linked_count} fulfillments linked...")

    db.close()

    print(f"\n✅ Linked {linked_count} prophecy fulfillments")
    print(f"⏭️  Skipped {skipped_count} (already linked or not found)")


if __name__ == "__main__":
    link_prophecy_fulfillments()
