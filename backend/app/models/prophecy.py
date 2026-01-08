"""
Models for prophecy-fulfillment mapping.
Tracks how prophetic texts relate to historical outcomes.
"""

from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class FulfillmentType(str, enum.Enum):
    """
    Classification of how prophecy relates to historical outcome.
    """

    COMPLETE = "complete"  # Fully and definitively fulfilled
    PARTIAL = "partial"  # Partially fulfilled, more may follow
    REPEATED = "repeated"  # Pattern that recurs across eras
    CONDITIONAL = "conditional"  # Conditional; fulfillment depends on response
    PENDING = "pending"  # Not yet fulfilled
    SYMBOLIC = "symbolic"  # Symbolic representation rather than literal


class ProphecyText(Base):
    """
    Prophetic declarations from Biblical texts.
    """

    __tablename__ = "prophecy_texts"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String(255), nullable=False, index=True)  # e.g., "Daniel 2:31-45"
    text = Column(Text, nullable=False)
    prophet = Column(String(100), nullable=True, index=True)

    # Temporal context
    year_declared = Column(Integer, nullable=True)  # When prophecy was given

    # Classification
    prophecy_type = Column(String(100), nullable=True)  # messianic, judgment, restoration, etc.
    scope = Column(
        String(100), nullable=True
    )  # local, national, international, eschatological

    # Structured content
    # Breaking down the prophecy into discrete predictive elements
    elements = Column(JSON, nullable=True)

    # Relationships
    fulfillments = relationship("ProphecyFulfillment", back_populates="prophecy")


class ProphecyFulfillment(Base):
    """
    Links prophecy texts to historical events that fulfill them.
    Supports multiple fulfillments (repeated patterns).
    """

    __tablename__ = "prophecy_fulfillments"

    id = Column(Integer, primary_key=True, index=True)

    # Link to prophecy and event
    prophecy_id = Column(Integer, ForeignKey("prophecy_texts.id"), nullable=False, index=True)
    event_id = Column(
        Integer, ForeignKey("chronology_events.id"), nullable=False, index=True
    )

    # Fulfillment characteristics
    fulfillment_type = Column(Enum(FulfillmentType), nullable=False, index=True)
    confidence_score = Column(
        Float, nullable=True
    )  # 0.0-1.0: How certain is this fulfillment claim

    # Analysis
    explanation = Column(Text, nullable=False)  # How this event fulfills the prophecy
    elements_fulfilled = Column(
        JSON, nullable=True
    )  # Which elements of prophecy are fulfilled

    # Relationships
    prophecy = relationship("ProphecyText", back_populates="fulfillments")
    event = relationship("ChronologyEvent")


class PropheticalPattern(Base):
    """
    Recurring prophetic patterns that repeat across history.
    E.g., "nations that oppress Israel are judged" appears repeatedly.
    """

    __tablename__ = "prophetical_patterns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=False)

    # Pattern definition
    condition = Column(Text, nullable=False)  # What triggers the pattern
    predicted_outcome = Column(Text, nullable=False)  # What the pattern predicts

    # Biblical basis
    foundational_texts = Column(JSON, nullable=True)  # List of prophecy references

    # Historical validation
    # List of historical instances where this pattern manifested
    historical_instances = Column(JSON, nullable=True)
