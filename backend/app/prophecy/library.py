"""
Prophecy Library - Core prophecy-fulfillment mapping logic.
Manages Biblical prophecies and tracks their historical fulfillments.
"""

from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Any
from app.models.prophecy import ProphecyText, ProphecyFulfillment, FulfillmentType
from app.models.chronology import ChronologyEvent


class ProphecyLibrary:
    """
    Central repository for prophecy-fulfillment tracking.
    Manages core Biblical prophecies and their historical realizations.
    """

    # Core Biblical prophecies with detailed breakdown
    CORE_PROPHECIES = {
        "daniel_2": {
            "reference": "Daniel 2:31-45",
            "prophet": "Daniel",
            "year_declared": -603,
            "prophecy_type": "kingdom_succession",
            "scope": "international",
            "text": "Nebuchadnezzar's dream of a great statue with head of gold, chest of silver, belly of bronze, legs of iron, feet of iron and clay. A stone cut without hands destroys the statue and becomes a great mountain filling the earth.",
            "elements": [
                {
                    "id": "head_gold",
                    "description": "Head of gold - Babylonian Empire",
                    "keywords": ["babylon", "nebuchadnezzar", "gold"],
                },
                {
                    "id": "chest_silver",
                    "description": "Chest/arms of silver - Medo-Persian Empire",
                    "keywords": ["persia", "medes", "cyrus"],
                },
                {
                    "id": "belly_bronze",
                    "description": "Belly/thighs of bronze - Greek Empire",
                    "keywords": ["greece", "alexander", "hellenistic"],
                },
                {
                    "id": "legs_iron",
                    "description": "Legs of iron - Roman Empire",
                    "keywords": ["rome", "roman", "caesar"],
                },
                {
                    "id": "feet_mixed",
                    "description": "Feet of iron and clay - Divided kingdoms",
                    "keywords": ["divided", "fragmented", "unstable"],
                },
                {
                    "id": "stone_kingdom",
                    "description": "Stone cut without hands - Messianic Kingdom",
                    "keywords": ["messiah", "kingdom of god", "eternal"],
                },
            ],
        },
        "daniel_7": {
            "reference": "Daniel 7:1-28",
            "prophet": "Daniel",
            "year_declared": -553,
            "prophecy_type": "kingdom_succession",
            "scope": "international",
            "text": "Vision of four beasts: lion with eagle's wings (Babylon), bear raised on one side (Medo-Persia), leopard with four heads (Greece), terrifying beast with iron teeth and ten horns (Rome/Final Empire). Ancient of Days gives dominion to Son of Man.",
            "elements": [
                {
                    "id": "lion_beast",
                    "description": "Lion with eagle's wings - Babylon",
                    "keywords": ["babylon", "nebuchadnezzar"],
                },
                {
                    "id": "bear_beast",
                    "description": "Bear raised on one side - Medo-Persia",
                    "keywords": ["persia", "medes"],
                },
                {
                    "id": "leopard_beast",
                    "description": "Leopard with four wings and four heads - Greece",
                    "keywords": ["greece", "alexander", "four kingdoms"],
                },
                {
                    "id": "terrifying_beast",
                    "description": "Terrifying beast with iron teeth and ten horns - Rome/Final Empire",
                    "keywords": ["rome", "ten kings", "antichrist"],
                },
                {
                    "id": "little_horn",
                    "description": "Little horn that speaks boastfully",
                    "keywords": ["antichrist", "persecution", "blasphemy"],
                },
                {
                    "id": "ancient_of_days",
                    "description": "Ancient of Days judges, gives kingdom to Son of Man",
                    "keywords": ["judgment", "messiah", "eternal kingdom"],
                },
            ],
        },
        "daniel_9": {
            "reference": "Daniel 9:24-27",
            "prophet": "Daniel",
            "year_declared": -538,
            "prophecy_type": "messianic_timeline",
            "scope": "national",
            "text": "Seventy 'sevens' are decreed for Israel: 69 sevens until Messiah comes, then Messiah cut off, city and sanctuary destroyed. Final seven: covenant with many, abomination causing desolation.",
            "elements": [
                {
                    "id": "decree_rebuild",
                    "description": "Decree to restore and rebuild Jerusalem",
                    "keywords": ["artaxerxes", "nehemiah", "decree"],
                },
                {
                    "id": "sixty_nine_sevens",
                    "description": "69 sevens (483 years) until Messiah",
                    "keywords": ["messiah", "anointed one", "483 years"],
                },
                {
                    "id": "messiah_cut_off",
                    "description": "Messiah cut off and have nothing",
                    "keywords": ["crucifixion", "death", "rejected"],
                },
                {
                    "id": "city_destroyed",
                    "description": "City and sanctuary destroyed by people of the prince",
                    "keywords": ["jerusalem", "temple", "destruction", "70 ad"],
                },
                {
                    "id": "final_seven",
                    "description": "Final seven: covenant with many, abomination",
                    "keywords": ["tribulation", "antichrist", "covenant"],
                },
            ],
        },
        "isaiah_53": {
            "reference": "Isaiah 53:1-12",
            "prophet": "Isaiah",
            "year_declared": -700,
            "prophecy_type": "messianic",
            "scope": "international",
            "text": "Suffering Servant: despised and rejected, wounded for our transgressions, led like lamb to slaughter, bore sins of many, numbered with transgressors, poured out soul to death.",
            "elements": [
                {
                    "id": "despised_rejected",
                    "description": "Despised and rejected by men",
                    "keywords": ["rejected", "despised", "sorrows"],
                },
                {
                    "id": "wounded_sins",
                    "description": "Wounded for our transgressions, bruised for iniquities",
                    "keywords": ["atonement", "sacrifice", "sins"],
                },
                {
                    "id": "silent_suffering",
                    "description": "Oppressed, silent before accusers like lamb to slaughter",
                    "keywords": ["silent", "lamb", "no defense"],
                },
                {
                    "id": "death_burial",
                    "description": "Assigned grave with wicked, with rich in death",
                    "keywords": ["death", "burial", "tomb"],
                },
                {
                    "id": "justified_many",
                    "description": "By knowledge of him shall many be justified",
                    "keywords": ["justification", "righteousness", "salvation"],
                },
            ],
        },
        "jeremiah_25": {
            "reference": "Jeremiah 25:8-14",
            "prophet": "Jeremiah",
            "year_declared": -605,
            "prophecy_type": "judgment",
            "scope": "national",
            "text": "Judah will serve Babylon 70 years. After 70 years, God will punish Babylon and make it desolate forever.",
            "elements": [
                {
                    "id": "seventy_years",
                    "description": "Judah will serve Babylon 70 years",
                    "keywords": ["70 years", "captivity", "exile"],
                },
                {
                    "id": "babylon_punished",
                    "description": "After 70 years, Babylon will be punished",
                    "keywords": ["babylon", "judgment", "fall"],
                },
                {
                    "id": "desolation",
                    "description": "Babylon will become everlasting desolation",
                    "keywords": ["desolate", "ruins", "perpetual"],
                },
            ],
        },
        "isaiah_44_45": {
            "reference": "Isaiah 44:28-45:1",
            "prophet": "Isaiah",
            "year_declared": -700,
            "prophecy_type": "restoration",
            "scope": "national",
            "text": "God will raise up Cyrus by name 150 years before his birth to rebuild Jerusalem and the temple. Cyrus will be God's shepherd and anointed one.",
            "elements": [
                {
                    "id": "cyrus_named",
                    "description": "Cyrus named 150 years before birth",
                    "keywords": ["cyrus", "named", "prophecy"],
                },
                {
                    "id": "temple_rebuilt",
                    "description": "Cyrus will rebuild Jerusalem and temple",
                    "keywords": ["rebuild", "temple", "jerusalem"],
                },
                {
                    "id": "gods_shepherd",
                    "description": "Cyrus called God's shepherd and anointed",
                    "keywords": ["shepherd", "anointed", "chosen"],
                },
            ],
        },
    }

    def __init__(self, db: Session):
        """Initialize the library with a database session."""
        self.db = db

    def get_all_prophecies(
        self, prophecy_type: Optional[str] = None, scope: Optional[str] = None
    ) -> List[ProphecyText]:
        """
        Retrieve all prophecies, optionally filtered.

        Args:
            prophecy_type: Filter by type (messianic, judgment, restoration, etc.)
            scope: Filter by scope (local, national, international, eschatological)

        Returns:
            List of prophecy texts
        """
        query = self.db.query(ProphecyText)

        if prophecy_type:
            query = query.filter(ProphecyText.prophecy_type == prophecy_type)

        if scope:
            query = query.filter(ProphecyText.scope == scope)

        return query.all()

    def get_prophecy_by_id(self, prophecy_id: int) -> Optional[ProphecyText]:
        """Get a specific prophecy by ID."""
        return self.db.query(ProphecyText).filter(ProphecyText.id == prophecy_id).first()

    def get_prophecy_by_reference(self, reference: str) -> Optional[ProphecyText]:
        """Get prophecy by Biblical reference."""
        return self.db.query(ProphecyText).filter(ProphecyText.reference == reference).first()

    def create_prophecy(self, prophecy_data: Dict[str, Any]) -> ProphecyText:
        """
        Create a new prophecy entry.

        Args:
            prophecy_data: Dictionary with prophecy details

        Returns:
            Created ProphecyText instance
        """
        prophecy = ProphecyText(**prophecy_data)
        self.db.add(prophecy)
        self.db.commit()
        self.db.refresh(prophecy)
        return prophecy

    def link_fulfillment(
        self,
        prophecy: ProphecyText,
        event: ChronologyEvent,
        fulfillment_type: FulfillmentType,
        confidence_score: float,
        explanation: str,
        elements_fulfilled: Optional[List[str]] = None,
    ) -> ProphecyFulfillment:
        """
        Link a prophecy to an event as a fulfillment.

        Args:
            prophecy: ProphecyText instance
            event: ChronologyEvent instance
            fulfillment_type: Type of fulfillment
            confidence_score: 0.0-1.0 confidence level
            explanation: How the event fulfills the prophecy
            elements_fulfilled: List of element IDs from prophecy that are fulfilled

        Returns:
            Created ProphecyFulfillment instance
        """
        fulfillment = ProphecyFulfillment(
            prophecy_id=prophecy.id,
            event_id=event.id,
            fulfillment_type=fulfillment_type,
            confidence_score=confidence_score,
            explanation=explanation,
            elements_fulfilled=elements_fulfilled or [],
        )

        self.db.add(fulfillment)
        self.db.commit()
        self.db.refresh(fulfillment)
        return fulfillment

    def get_fulfillments(
        self, prophecy_id: int, fulfillment_type: Optional[FulfillmentType] = None
    ) -> List[ProphecyFulfillment]:
        """
        Get all fulfillments for a prophecy.

        Args:
            prophecy_id: Prophecy ID
            fulfillment_type: Optional filter by fulfillment type

        Returns:
            List of fulfillments with related events
        """
        query = self.db.query(ProphecyFulfillment).filter(
            ProphecyFulfillment.prophecy_id == prophecy_id
        )

        if fulfillment_type:
            query = query.filter(ProphecyFulfillment.fulfillment_type == fulfillment_type)

        return query.all()

    def analyze_fulfillment_timeline(self, prophecy_id: int) -> Dict[str, Any]:
        """
        Analyze the timeline of fulfillments for a prophecy.

        Args:
            prophecy_id: Prophecy ID

        Returns:
            Dictionary with timeline analysis
        """
        prophecy = self.get_prophecy_by_id(prophecy_id)
        if not prophecy:
            return {}

        fulfillments = self.get_fulfillments(prophecy_id)

        if not fulfillments:
            return {
                "prophecy_id": prophecy_id,
                "reference": prophecy.reference,
                "year_declared": prophecy.year_declared,
                "total_fulfillments": 0,
                "fulfillment_types": {},
                "timeline": [],
            }

        # Gather fulfillment events
        events = []
        fulfillment_types = {}

        for fulfillment in fulfillments:
            event = (
                self.db.query(ChronologyEvent)
                .filter(ChronologyEvent.id == fulfillment.event_id)
                .first()
            )

            if event:
                events.append(
                    {
                        "event_id": event.id,
                        "name": event.name,
                        "year_start": event.year_start,
                        "fulfillment_type": fulfillment.fulfillment_type.value,
                        "confidence_score": fulfillment.confidence_score,
                        "elements_fulfilled": fulfillment.elements_fulfilled,
                    }
                )

                # Count fulfillment types
                ft = fulfillment.fulfillment_type.value
                fulfillment_types[ft] = fulfillment_types.get(ft, 0) + 1

        # Sort events by year
        events.sort(key=lambda e: e["year_start"] or 0)

        # Calculate years from prophecy to first fulfillment
        years_to_fulfillment = None
        if events and prophecy.year_declared:
            first_fulfillment_year = events[0]["year_start"]
            if first_fulfillment_year:
                years_to_fulfillment = first_fulfillment_year - prophecy.year_declared

        return {
            "prophecy_id": prophecy_id,
            "reference": prophecy.reference,
            "year_declared": prophecy.year_declared,
            "total_fulfillments": len(events),
            "fulfillment_types": fulfillment_types,
            "years_to_first_fulfillment": years_to_fulfillment,
            "timeline": events,
        }

    def detect_fulfillment_candidates(
        self, prophecy_id: int, confidence_threshold: float = 0.5
    ) -> List[ChronologyEvent]:
        """
        Detect potential events that might fulfill a prophecy based on keywords.

        Args:
            prophecy_id: Prophecy ID
            confidence_threshold: Minimum confidence score (0.0-1.0)

        Returns:
            List of candidate events
        """
        prophecy = self.get_prophecy_by_id(prophecy_id)
        if not prophecy or not prophecy.elements:
            return []

        # Extract keywords from all prophecy elements
        keywords = set()
        for element in prophecy.elements:
            keywords.update(element.get("keywords", []))

        # Search for events matching keywords in name or description
        candidates = []
        events = self.db.query(ChronologyEvent).all()

        for event in events:
            search_text = f"{event.name} {event.description or ''}".lower()
            matches = sum(1 for kw in keywords if kw.lower() in search_text)

            if matches > 0:
                # Simple confidence: ratio of matched keywords
                confidence = min(matches / len(keywords), 1.0)

                if confidence >= confidence_threshold:
                    candidates.append(
                        {
                            "event": event,
                            "confidence": confidence,
                            "matched_keywords": [
                                kw for kw in keywords if kw.lower() in search_text
                            ],
                        }
                    )

        # Sort by confidence descending
        candidates.sort(key=lambda c: c["confidence"], reverse=True)

        return candidates

    def seed_core_prophecies(self) -> Dict[str, Any]:
        """
        Seed the core Biblical prophecies into the database.
        Idempotent - checks if prophecies already exist.

        Returns:
            Dictionary with seeding results
        """
        seeded = []
        skipped = []

        for prophecy_key, prophecy_data in self.CORE_PROPHECIES.items():
            # Check if prophecy already exists
            existing = self.get_prophecy_by_reference(prophecy_data["reference"])

            if existing:
                skipped.append(prophecy_data["reference"])
                continue

            # Create prophecy
            prophecy = ProphecyText(
                reference=prophecy_data["reference"],
                text=prophecy_data["text"],
                prophet=prophecy_data["prophet"],
                year_declared=prophecy_data["year_declared"],
                prophecy_type=prophecy_data["prophecy_type"],
                scope=prophecy_data["scope"],
                elements=prophecy_data["elements"],
            )

            self.db.add(prophecy)
            seeded.append(prophecy_data["reference"])

        self.db.commit()

        return {
            "total_prophecies": len(self.CORE_PROPHECIES),
            "seeded": len(seeded),
            "skipped": len(skipped),
            "seeded_references": seeded,
            "skipped_references": skipped,
        }
