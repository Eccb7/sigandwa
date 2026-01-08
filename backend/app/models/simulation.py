"""
Models for simulation inputs and trajectory outputs.
"""

from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Float
from datetime import datetime

from app.database import Base


class WorldIndicator(Base):
    """
    Current world state indicators used as simulation inputs.
    These represent observable conditions that feed into pattern matching.
    """

    __tablename__ = "world_indicators"

    id = Column(Integer, primary_key=True, index=True)
    indicator_name = Column(String(255), nullable=False, index=True)
    category = Column(
        String(100), nullable=False, index=True
    )  # political, economic, military, social, religious
    value = Column(Float, nullable=True)  # Quantitative value if applicable
    description = Column(Text, nullable=True)
    data_source = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Extra data
    extra_data = Column(JSON, nullable=True)


class SimulationScenario(Base):
    """
    Stored simulation scenarios and their trajectories.
    """

    __tablename__ = "simulation_scenarios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Input conditions
    input_indicators = Column(JSON, nullable=False)  # Snapshot of world indicators
    assumptions = Column(JSON, nullable=True)  # Conditional assumptions made

    # Pattern matching
    matched_patterns = Column(JSON, nullable=True)  # Historical patterns that apply
    historical_analogs = Column(JSON, nullable=True)  # Similar historical situations

    # Outputs
    trajectory = Column(JSON, nullable=False)  # Conditional future trajectory
    risk_vectors = Column(JSON, nullable=True)  # Key risk factors identified
    confidence_score = Column(Float, nullable=True)  # 0.0-1.0

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    parameters = Column(JSON, nullable=True)  # Simulation parameters used
