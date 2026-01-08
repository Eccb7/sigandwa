"""
SQLAlchemy models for chronology and events.
These define the authoritative timeline from Creation to Present.
"""

from sqlalchemy import Column, Integer, String, Text, Date, Enum, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import date
from typing import Optional
import enum

from app.database import Base


class EventType(str, enum.Enum):
    """
    Event classification based on primary domain of impact.
    Multiple types may apply; primary is recorded here.
    """

    POLITICAL = "political"
    ECONOMIC = "economic"
    RELIGIOUS = "religious"
    MILITARY = "military"
    SOCIAL = "social"
    NATURAL = "natural"  # Floods, droughts, etc.
    PROPHETIC = "prophetic"  # Prophetic declarations


class ChronologyEra(str, enum.Enum):
    """
    Major chronological divisions in Biblical-historical timeline.
    """

    CREATION_TO_FLOOD = "creation_to_flood"
    FLOOD_TO_ABRAHAM = "flood_to_abraham"
    PATRIARCHS = "patriarchs"
    EGYPTIAN_BONDAGE = "egyptian_bondage"
    EXODUS_TO_JUDGES = "exodus_to_judges"
    UNITED_MONARCHY = "united_monarchy"
    DIVIDED_KINGDOM = "divided_kingdom"
    EXILE = "exile"
    POST_EXILE = "post_exile"
    INTERTESTAMENTAL = "intertestamental"
    NEW_TESTAMENT = "new_testament"
    EARLY_CHURCH = "early_church"
    ROMAN_EMPIRE = "roman_empire"
    MEDIEVAL = "medieval"
    REFORMATION = "reformation"
    COLONIAL = "colonial"
    MODERN = "modern"
    CONTEMPORARY = "contemporary"


class ChronologyEvent(Base):
    """
    Core chronology table: the authoritative timeline.
    Every event (Biblical or historical) is indexed here.
    """

    __tablename__ = "chronology_events"

    id = Column(Integer, primary_key=True, index=True)

    # Event identification
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Temporal positioning (Ussher-based absolute dates)
    # Dates are BC (negative) or AD (positive) in Ussher chronology
    year_start = Column(Integer, nullable=False, index=True)
    year_end = Column(Integer, nullable=True)  # For events with duration

    # Uncertainty bounds
    # If event date is uncertain, these define the possible range
    year_start_min = Column(Integer, nullable=True)
    year_start_max = Column(Integer, nullable=True)
    year_end_min = Column(Integer, nullable=True)
    year_end_max = Column(Integer, nullable=True)

    # Classification
    era = Column(Enum(ChronologyEra), nullable=False, index=True)
    event_type = Column(Enum(EventType), nullable=False, index=True)

    # Source metadata
    biblical_source = Column(String(255), nullable=True)  # e.g., "Genesis 7:11-24"
    historical_source = Column(Text, nullable=True)  # Historical references

    # Additional structured data
    extra_data = Column(JSON, nullable=True)  # Flexible schema for extra attributes

    # Relationships
    actors = relationship("Actor", secondary="event_actors", back_populates="events")
    patterns = relationship("Pattern", secondary="event_patterns", back_populates="events")


class Actor(Base):
    """
    Individuals, nations, empires, or institutions involved in events.
    """

    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    actor_type = Column(
        String(50), nullable=False, index=True
    )  # person, nation, empire, institution
    description = Column(Text, nullable=True)
    year_start = Column(Integer, nullable=True)  # When actor emerged
    year_end = Column(Integer, nullable=True)  # When actor ceased to exist

    # Relationships
    events = relationship("ChronologyEvent", secondary="event_actors", back_populates="actors")


class EventActor(Base):
    """Association table linking events to actors."""

    __tablename__ = "event_actors"

    event_id = Column(Integer, ForeignKey("chronology_events.id"), primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id"), primary_key=True)
    role = Column(String(100), nullable=True)  # conqueror, victim, prophet, etc.


class Pattern(Base):
    """
    Reusable historical patterns identified across eras.
    These are the templates for civilizational cycles.
    """

    __tablename__ = "patterns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=False)

    # Pattern characteristics
    pattern_type = Column(
        String(100), nullable=False, index=True
    )  # rise, decline, collapse, recapitulation
    typical_duration_years = Column(Integer, nullable=True)  # Average duration if applicable

    # Conditions and indicators
    preconditions = Column(JSON, nullable=True)  # What conditions trigger this pattern
    indicators = Column(JSON, nullable=True)  # Observable signs during pattern
    outcomes = Column(JSON, nullable=True)  # Typical results

    # Biblical references
    biblical_basis = Column(Text, nullable=True)  # Scriptural foundation for pattern

    # Relationships
    events = relationship("ChronologyEvent", secondary="event_patterns", back_populates="patterns")


class EventPattern(Base):
    """Association table linking events to patterns."""

    __tablename__ = "event_patterns"

    event_id = Column(Integer, ForeignKey("chronology_events.id"), primary_key=True)
    pattern_id = Column(Integer, ForeignKey("patterns.id"), primary_key=True)
    strength = Column(Integer, nullable=True)  # 1-10 scale of pattern match strength
