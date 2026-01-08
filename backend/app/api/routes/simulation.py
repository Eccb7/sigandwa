"""
Simulation API Endpoints
Handles scenario modeling, forecasting, and risk assessment.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field

from app.database import get_db
from app.simulation.engine import SimulationEngine
from app.models.simulation import WorldIndicator, SimulationScenario

router = APIRouter()


# ============================================================================
# Response Models (Pydantic schemas)
# ============================================================================


class CreateScenarioRequest(BaseModel):
    """Request model for creating a scenario."""
    name: str = Field(..., description="Scenario name")
    description: str = Field(..., description="Scenario description")
    indicator_ids: Optional[List[int]] = Field(None, description="List of indicator IDs to include")
    pattern_ids: Optional[List[int]] = Field(None, description="List of pattern IDs to consider")
    assumptions: Optional[dict] = Field(None, description="Additional assumptions")


class IndicatorResponse(BaseModel):
    id: int
    indicator_name: str
    category: str
    value: Optional[float] = None
    description: Optional[str] = None
    timestamp: Optional[str] = None

    class Config:
        from_attributes = True


class IndicatorAssessmentResponse(BaseModel):
    total_indicators: int
    categories: dict
    by_category: dict
    latest_timestamp: Optional[str] = None


class PreconditionMatchResponse(BaseModel):
    pattern_id: int
    pattern_name: str
    pattern_type: str
    total_preconditions: int
    matched_preconditions: List[str]
    missing_preconditions: List[str]
    match_score: float
    risk_level: str
    typical_duration_years: Optional[int] = None


class TrajectoryProjectionResponse(BaseModel):
    pattern_id: int
    pattern_name: str
    pattern_type: str
    historical_instances: int
    average_interval_years: float
    last_occurrence: Optional[int] = None
    years_since_last: Optional[int] = None
    progress_through_cycle: Optional[str] = None
    estimated_next_occurrence: Optional[int] = None
    years_until_next: Optional[int] = None
    likelihood: str
    confidence: float
    trajectory_phases: List[dict]


class ScenarioResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    input_indicators: List[dict]
    matched_patterns: List[dict]
    trajectory: dict
    confidence_score: Optional[float] = None
    created_at: str

    class Config:
        from_attributes = True


class RiskScoreResponse(BaseModel):
    overall_risk_score: float
    risk_level: str
    total_patterns_assessed: int
    patterns_with_matches: int
    top_risks: List[dict]
    risk_categories: dict


class PropheticAnalysisResponse(BaseModel):
    total_prophecies: int
    complete: int
    partial: int
    pending: int
    pending_prophecies: List[dict]
    partial_prophecies: List[dict]
    eschatological_outlook: str


# ============================================================================
# Endpoints
# ============================================================================


@router.get("/indicators", response_model=IndicatorAssessmentResponse)
def assess_indicators(
    category: Optional[str] = Query(
        None, description="Filter by category (political, economic, military, social, religious)"
    ),
    db: Session = Depends(get_db),
):
    """
    Assess current world indicators and their implications.

    Categories: political, economic, military, social, religious
    """
    engine = SimulationEngine(db)
    assessment = engine.assess_current_indicators(indicator_category=category)

    return IndicatorAssessmentResponse(**assessment)


@router.get("/patterns/{pattern_id}/preconditions", response_model=PreconditionMatchResponse)
def check_preconditions(pattern_id: int, db: Session = Depends(get_db)):
    """
    Check if current indicators match pattern preconditions.

    Returns match score (0.0-1.0) and risk level assessment.
    """
    engine = SimulationEngine(db)
    analysis = engine.detect_pattern_preconditions(pattern_id)

    if "error" in analysis:
        raise HTTPException(status_code=404, detail=analysis["error"])

    return PreconditionMatchResponse(**analysis)


@router.get("/patterns/{pattern_id}/trajectory", response_model=TrajectoryProjectionResponse)
def project_trajectory(
    pattern_id: int,
    current_year: int = Query(2026, description="Starting year for projection"),
    db: Session = Depends(get_db),
):
    """
    Project future trajectory based on pattern recurrence.

    Uses historical pattern intervals to forecast next occurrence and phases.
    """
    engine = SimulationEngine(db)
    projection = engine.project_pattern_trajectory(pattern_id, current_year)

    if "error" in projection:
        raise HTTPException(status_code=404, detail=projection["error"])

    if "projection" in projection:
        # Insufficient data case
        raise HTTPException(status_code=400, detail=projection["projection"])

    return TrajectoryProjectionResponse(**projection)


@router.post("/historical-analogs")
def find_analogs(
    keywords: List[str] = Query(..., description="Keywords describing current conditions"),
    categories: Optional[List[str]] = Query(
        None, description="Event categories to search"
    ),
    db: Session = Depends(get_db),
):
    """
    Find historical events analogous to current conditions.

    Returns top 10 most similar historical events with similarity scores.
    """
    engine = SimulationEngine(db)
    current_conditions = {"keywords": keywords, "categories": categories or []}

    analogs = engine.find_historical_analogs(current_conditions)

    return {"total_analogs": len(analogs), "analogs": analogs}


@router.get("/scenarios", response_model=List[ScenarioResponse])
def list_scenarios(db: Session = Depends(get_db)):
    """List all simulation scenarios."""
    engine = SimulationEngine(db)
    scenarios = engine.get_all_scenarios()

    return [
        ScenarioResponse(
            id=s.id,
            name=s.name,
            description=s.description,
            input_indicators=s.input_indicators or [],
            matched_patterns=s.matched_patterns or [],
            trajectory=s.trajectory or {},
            confidence_score=s.confidence_score,
            created_at=s.created_at.isoformat() if s.created_at else None,
        )
        for s in scenarios
    ]


@router.get("/scenarios/{scenario_id}", response_model=ScenarioResponse)
def get_scenario(scenario_id: int, db: Session = Depends(get_db)):
    """Get a specific simulation scenario."""
    engine = SimulationEngine(db)
    scenario = engine.get_scenario_by_id(scenario_id)

    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")

    return ScenarioResponse(
        id=scenario.id,
        name=scenario.name,
        description=scenario.description,
        input_indicators=scenario.input_indicators or [],
        matched_patterns=scenario.matched_patterns or [],
        trajectory=scenario.trajectory or {},
        confidence_score=scenario.confidence_score,
        created_at=scenario.created_at.isoformat() if scenario.created_at else None,
    )


@router.post("/scenarios", response_model=ScenarioResponse)
def create_scenario(
    request: CreateScenarioRequest,
    db: Session = Depends(get_db),
):
    """
    Create a new simulation scenario.

    Combines indicators and patterns to generate trajectory forecast.
    """
    engine = SimulationEngine(db)

    scenario = engine.create_scenario(
        name=request.name,
        description=request.description,
        indicator_ids=request.indicator_ids,
        pattern_ids=request.pattern_ids,
        assumptions=request.assumptions,
    )

    return ScenarioResponse(
        id=scenario.id,
        name=scenario.name,
        description=scenario.description,
        input_indicators=scenario.input_indicators or [],
        matched_patterns=scenario.matched_patterns or [],
        trajectory=scenario.trajectory or {},
        confidence_score=scenario.confidence_score,
        created_at=scenario.created_at.isoformat() if scenario.created_at else None,
    )



@router.get("/risk-assessment", response_model=RiskScoreResponse)
def assess_risk(db: Session = Depends(get_db)):
    """
    Calculate overall civilization risk score.

    Analyzes all patterns against current indicators to assess systemic risk.
    Returns risk level: critical, high, moderate, or low.
    """
    engine = SimulationEngine(db)
    risk_assessment = engine.calculate_civilization_risk_score()

    return RiskScoreResponse(**risk_assessment)


@router.get("/prophetic-timeline", response_model=PropheticAnalysisResponse)
def analyze_prophetic_timeline(db: Session = Depends(get_db)):
    """
    Analyze prophetic timeline for pending fulfillments.

    Reviews all prophecies to identify:
    - Complete fulfillments
    - Partial fulfillments (in progress)
    - Pending fulfillments (not yet started)

    Provides eschatological outlook based on fulfillment status.
    """
    engine = SimulationEngine(db)
    analysis = engine.analyze_prophetic_timeline()

    return PropheticAnalysisResponse(**analysis)


@router.post("/indicators", response_model=IndicatorResponse)
def create_indicator(
    indicator_name: str = Query(..., description="Indicator name"),
    category: str = Query(..., description="Category (political, economic, military, social, religious)"),
    value: Optional[float] = Query(None, description="Quantitative value"),
    description: Optional[str] = Query(None, description="Indicator description"),
    data_source: Optional[str] = Query(None, description="Data source"),
    db: Session = Depends(get_db),
):
    """
    Add a new world indicator.

    Categories: political, economic, military, social, religious
    """
    from datetime import datetime

    indicator = WorldIndicator(
        indicator_name=indicator_name,
        category=category,
        value=value,
        description=description,
        data_source=data_source,
        timestamp=datetime.utcnow(),
    )

    db.add(indicator)
    db.commit()
    db.refresh(indicator)

    return IndicatorResponse(
        id=indicator.id,
        indicator_name=indicator.indicator_name,
        category=indicator.category,
        value=indicator.value,
        description=indicator.description,
        timestamp=indicator.timestamp.isoformat() if indicator.timestamp else None,
    )
