"""
Pattern Recognition Library for Biblical Cliodynamic Analysis.

Identifies recurring patterns across historical events and eras.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.chronology import ChronologyEvent, Pattern, EventPattern, ChronologyEra
from app.models.prophecy import PropheticalPattern
import json


class PatternLibrary:
    """
    Core pattern recognition and analysis engine.
    Identifies recurrence of historical templates across eras.
    """

    def __init__(self, db: Session):
        self.db = db

    # Core pattern templates based on Biblical framework
    CORE_PATTERNS = {
        "moral_decay_judgment": {
            "name": "Moral Decay → Divine Judgment",
            "description": "Societies experiencing moral decline followed by judgment (conquest, plague, exile)",
            "preconditions": ["moral_relativism", "covenant_unfaithfulness", "injustice"],
            "indicators": ["social_corruption", "idolatry", "oppression_of_poor"],
            "outcomes": ["military_defeat", "plague", "exile", "political_collapse"],
            "biblical_examples": ["Flood", "Sodom", "Northern Kingdom Fall", "Judah Exile"],
            "duration_years": [10, 100],
        },
        "pride_fall": {
            "name": "Pride → Humbling/Fall",
            "description": "Leaders or nations experiencing hubris followed by humiliation",
            "preconditions": ["military_success", "economic_prosperity", "self_deification"],
            "indicators": ["boasting", "overreach", "violation_of_sacred_boundaries"],
            "outcomes": ["sudden_reversal", "assassination", "madness", "empire_fragmentation"],
            "biblical_examples": ["Tower of Babel", "Pharaoh", "Nebuchadnezzar", "Belshazzar", "Herod Agrippa"],
            "duration_years": [1, 40],
        },
        "exile_restoration": {
            "name": "Exile → Restoration",
            "description": "Dispersion of a people followed by eventual return or regathering",
            "preconditions": ["covenant_unfaithfulness", "military_defeat"],
            "indicators": ["displacement", "loss_of_land", "foreign_domination"],
            "outcomes": ["return_to_homeland", "temple_rebuilding", "national_renewal"],
            "biblical_examples": ["Babylonian Exile → Return", "Modern Israel 1948"],
            "duration_years": [70, 2000],
        },
        "persecution_growth": {
            "name": "Persecution → Growth",
            "description": "Intense persecution of faith communities leading to expansion",
            "preconditions": ["religious_distinctiveness", "state_hostility"],
            "indicators": ["martyrdom", "scattering", "underground_networks"],
            "outcomes": ["numerical_growth", "geographic_spread", "cultural_penetration"],
            "biblical_examples": ["Early Church persecution → spread", "Reformation persecution → Protestantism spread"],
            "duration_years": [10, 300],
        },
        "unity_fragmentation": {
            "name": "Unity → Fragmentation",
            "description": "United political or religious entities splitting into rival factions",
            "preconditions": ["succession_crisis", "doctrinal_disputes", "resource_competition"],
            "indicators": ["civil_war", "schism", "rival_claimants"],
            "outcomes": ["multiple_successor_states", "weakened_power", "vulnerability_to_conquest"],
            "biblical_examples": ["United Monarchy → Divided Kingdom", "Western/Eastern Church", "Roman Empire split"],
            "duration_years": [1, 50],
        },
        "delayed_fulfillment": {
            "name": "Promise Delayed → Eventually Fulfilled",
            "description": "Long delay between promise and fulfillment, testing faith",
            "preconditions": ["divine_promise_given", "immediate_fulfillment_fails"],
            "indicators": ["waiting_period", "apparent_impossibility", "faithful_remnant"],
            "outcomes": ["sudden_fulfillment", "vindication_of_faithful", "unexpected_means"],
            "biblical_examples": ["Abraham's son", "Messiah coming", "Land promise to Israel"],
            "duration_years": [25, 2000],
        },
    }

    def get_all_patterns(self) -> List[Pattern]:
        """Retrieve all defined patterns from database."""
        return self.db.query(Pattern).all()

    def get_pattern_by_id(self, pattern_id: int) -> Optional[Pattern]:
        """Retrieve a specific pattern."""
        return self.db.query(Pattern).filter(Pattern.id == pattern_id).first()

    def get_pattern_by_name(self, name: str) -> Optional[Pattern]:
        """Retrieve a pattern by name."""
        return self.db.query(Pattern).filter(Pattern.name == name).first()

    def create_pattern(
        self,
        name: str,
        description: str,
        pattern_type: str,
        preconditions: Dict[str, Any],
        indicators: Dict[str, Any],
        outcomes: Dict[str, Any],
        biblical_basis: Optional[str] = None,
        typical_duration_years: Optional[int] = None,
    ) -> Pattern:
        """Create a new pattern definition."""
        pattern = Pattern(
            name=name,
            description=description,
            pattern_type=pattern_type,
            preconditions=preconditions,
            indicators=indicators,
            outcomes=outcomes,
            biblical_basis=biblical_basis,
            typical_duration_years=typical_duration_years,
        )
        self.db.add(pattern)
        self.db.commit()
        self.db.refresh(pattern)
        return pattern

    def match_pattern_to_event(
        self, event: ChronologyEvent, pattern: Pattern, strength: int = 5
    ) -> EventPattern:
        """
        Link an event to a pattern with a strength rating (1-10).
        """
        event_pattern = EventPattern(
            event_id=event.id, pattern_id=pattern.id, strength=strength
        )
        self.db.add(event_pattern)
        self.db.commit()
        return event_pattern

    def find_pattern_instances(self, pattern_id: int) -> List[Dict[str, Any]]:
        """
        Find all historical instances of a given pattern.
        Returns events with their era and temporal context.
        """
        pattern = self.get_pattern_by_id(pattern_id)
        if not pattern:
            return []

        # Get events linked to this pattern
        instances = (
            self.db.query(ChronologyEvent, EventPattern.strength)
            .join(EventPattern, ChronologyEvent.id == EventPattern.event_id)
            .filter(EventPattern.pattern_id == pattern_id)
            .order_by(ChronologyEvent.year_start)
            .all()
        )

        result = []
        for event, strength in instances:
            result.append(
                {
                    "event_id": event.id,
                    "name": event.name,
                    "description": event.description,
                    "year_start": event.year_start,
                    "year_end": event.year_end,
                    "era": event.era.value,
                    "strength": strength,
                    "biblical_source": event.biblical_source,
                    "historical_source": event.historical_source,
                }
            )

        return result

    def analyze_pattern_recurrence(self, pattern_id: int) -> Dict[str, Any]:
        """
        Analyze how often and across which eras a pattern recurs.
        """
        instances = self.find_pattern_instances(pattern_id)

        if not instances:
            return {
                "pattern_id": pattern_id,
                "total_instances": 0,
                "era_distribution": {},
                "average_interval_years": None,
            }

        # Calculate era distribution
        era_counts = {}
        for instance in instances:
            era = instance["era"]
            era_counts[era] = era_counts.get(era, 0) + 1

        # Calculate average interval between instances
        years = sorted([i["year_start"] for i in instances])
        intervals = [years[i + 1] - years[i] for i in range(len(years) - 1)]
        avg_interval = sum(intervals) / len(intervals) if intervals else None

        return {
            "pattern_id": pattern_id,
            "total_instances": len(instances),
            "era_distribution": era_counts,
            "average_interval_years": avg_interval,
            "first_occurrence": years[0],
            "most_recent_occurrence": years[-1],
            "instances": instances,
        }

    def detect_pattern_in_event(self, event_id: int) -> List[Dict[str, Any]]:
        """
        Analyze an event to detect which patterns it might exemplify.
        Uses keyword matching on extra_data, description, and context.
        """
        event = self.db.query(ChronologyEvent).filter(ChronologyEvent.id == event_id).first()
        if not event:
            return []

        detected_patterns = []

        # Get all patterns
        all_patterns = self.get_all_patterns()

        # Analyze event text
        event_text = f"{event.name} {event.description or ''}"
        extra_data = event.extra_data or {}
        extra_data_str = json.dumps(extra_data).lower()

        for pattern in all_patterns:
            score = 0

            # Check if pattern keywords appear in event
            preconditions = pattern.preconditions or {}
            indicators = pattern.indicators or {}
            outcomes = pattern.outcomes or {}

            # Simple keyword matching (can be enhanced with NLP)
            for condition in preconditions:
                if isinstance(condition, str) and condition.lower() in extra_data_str:
                    score += 2

            for indicator in indicators:
                if isinstance(indicator, str) and indicator.lower() in event_text.lower():
                    score += 3

            for outcome in outcomes:
                if isinstance(outcome, str) and outcome.lower() in event_text.lower():
                    score += 2

            # If score exceeds threshold, add to detected patterns
            if score >= 3:
                detected_patterns.append(
                    {
                        "pattern_id": pattern.id,
                        "pattern_name": pattern.name,
                        "confidence_score": min(score / 10.0, 1.0),  # Normalize to 0-1
                        "matched_indicators": score,
                    }
                )

        return sorted(detected_patterns, key=lambda x: x["confidence_score"], reverse=True)

    def seed_core_patterns(self) -> List[Pattern]:
        """
        Seed the database with the 6 core Biblical patterns.
        Should be run once during initialization.
        """
        created_patterns = []

        for pattern_key, pattern_data in self.CORE_PATTERNS.items():
            # Check if pattern already exists
            existing = self.get_pattern_by_name(pattern_data["name"])
            if existing:
                continue

            pattern = self.create_pattern(
                name=pattern_data["name"],
                description=pattern_data["description"],
                pattern_type="biblical_template",
                preconditions=pattern_data["preconditions"],
                indicators=pattern_data["indicators"],
                outcomes=pattern_data["outcomes"],
                biblical_basis=", ".join(pattern_data["biblical_examples"]),
                typical_duration_years=pattern_data["duration_years"][1]
                if len(pattern_data["duration_years"]) > 1
                else None,
            )

            created_patterns.append(pattern)

        return created_patterns
