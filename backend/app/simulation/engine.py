"""
Simulation Engine - Core scenario modeling and forecasting logic.
Projects future trajectories based on historical patterns and current indicators.
"""

from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
import statistics

from app.models.simulation import WorldIndicator, SimulationScenario
from app.models.chronology import ChronologyEvent, Pattern
from app.models.prophecy import ProphecyText, ProphecyFulfillment
from app.patterns.library import PatternLibrary
from app.prophecy.library import ProphecyLibrary


class SimulationEngine:
    """
    Biblical Cliodynamic simulation engine.
    Models future scenarios based on pattern recurrence and prophetic frameworks.
    """

    # Risk severity levels
    RISK_CRITICAL = "critical"  # Imminent threat
    RISK_HIGH = "high"  # Likely within 5-10 years
    RISK_MODERATE = "moderate"  # Possible within 20-50 years
    RISK_LOW = "low"  # Distant or unlikely

    def __init__(self, db: Session):
        """Initialize the simulation engine with database session."""
        self.db = db
        self.pattern_library = PatternLibrary(db)
        self.prophecy_library = ProphecyLibrary(db)

    def assess_current_indicators(
        self, indicator_category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Assess current world indicators and their implications.

        Args:
            indicator_category: Filter by category (political, economic, military, social, religious)

        Returns:
            Dictionary with indicator analysis
        """
        query = self.db.query(WorldIndicator)

        if indicator_category:
            query = query.filter(WorldIndicator.category == indicator_category)

        indicators = query.order_by(WorldIndicator.timestamp.desc()).all()

        if not indicators:
            return {
                "total_indicators": 0,
                "categories": {},
                "latest_indicators": [],
                "risk_assessment": "No current indicators available",
            }

        # Group by category
        by_category = {}
        for indicator in indicators:
            category = indicator.category
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(
                {
                    "name": indicator.indicator_name,
                    "value": indicator.value,
                    "description": indicator.description,
                    "timestamp": indicator.timestamp.isoformat() if indicator.timestamp else None,
                }
            )

        return {
            "total_indicators": len(indicators),
            "categories": {cat: len(inds) for cat, inds in by_category.items()},
            "by_category": by_category,
            "latest_timestamp": indicators[0].timestamp.isoformat()
            if indicators[0].timestamp
            else None,
        }

    def detect_pattern_preconditions(self, pattern_id: int) -> Dict[str, Any]:
        """
        Check if current indicators match pattern preconditions.

        Args:
            pattern_id: Pattern ID to check

        Returns:
            Dictionary with precondition matching analysis
        """
        pattern = self.pattern_library.get_pattern_by_id(pattern_id)
        if not pattern:
            return {"error": "Pattern not found"}

        # Get current indicators
        indicators = self.db.query(WorldIndicator).order_by(WorldIndicator.timestamp.desc()).all()

        if not indicators:
            return {
                "pattern_id": pattern_id,
                "pattern_name": pattern.name,
                "match_score": 0.0,
                "matched_preconditions": [],
                "missing_preconditions": pattern.preconditions or [],
                "message": "No current indicators available for analysis",
            }

        # Extract keywords from indicators
        indicator_keywords = set()
        for ind in indicators:
            if ind.indicator_name:
                indicator_keywords.update(ind.indicator_name.lower().split())
            if ind.description:
                indicator_keywords.update(ind.description.lower().split())
            if ind.extra_data and isinstance(ind.extra_data, dict):
                for key, val in ind.extra_data.items():
                    if isinstance(val, str):
                        indicator_keywords.update(val.lower().split())

        # Match preconditions
        preconditions = pattern.preconditions or []
        matched = []
        missing = []

        for precondition in preconditions:
            precondition_lower = precondition.lower()
            # Simple keyword matching
            if any(kw in precondition_lower for kw in indicator_keywords):
                matched.append(precondition)
            else:
                missing.append(precondition)

        match_score = len(matched) / len(preconditions) if preconditions else 0.0

        return {
            "pattern_id": pattern_id,
            "pattern_name": pattern.name,
            "pattern_type": pattern.pattern_type,
            "total_preconditions": len(preconditions),
            "matched_preconditions": matched,
            "missing_preconditions": missing,
            "match_score": match_score,
            "risk_level": self._calculate_risk_level(match_score),
            "typical_duration_years": pattern.typical_duration_years,
        }

    def find_historical_analogs(self, current_conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find historical events analogous to current conditions.

        Args:
            current_conditions: Dictionary of current condition keywords/categories

        Returns:
            List of analogous historical events with similarity scores
        """
        keywords = current_conditions.get("keywords", [])
        categories = current_conditions.get("categories", [])

        if not keywords and not categories:
            return []

        # Search for events matching keywords
        events = self.db.query(ChronologyEvent).all()
        analogs = []

        for event in events:
            search_text = f"{event.name} {event.description or ''}".lower()
            matched_keywords = [kw for kw in keywords if kw.lower() in search_text]

            if matched_keywords:
                similarity = len(matched_keywords) / len(keywords) if keywords else 0.0

                analogs.append(
                    {
                        "event_id": event.id,
                        "name": event.name,
                        "year_start": event.year_start,
                        "era": event.era.value if event.era else None,
                        "description": event.description,
                        "similarity_score": similarity,
                        "matched_keywords": matched_keywords,
                    }
                )

        # Sort by similarity descending
        analogs.sort(key=lambda a: a["similarity_score"], reverse=True)

        return analogs[:10]  # Return top 10

    def project_pattern_trajectory(
        self, pattern_id: int, current_year: int = 2026
    ) -> Dict[str, Any]:
        """
        Project future trajectory based on pattern recurrence.

        Args:
            pattern_id: Pattern ID to project
            current_year: Starting year for projection

        Returns:
            Dictionary with trajectory forecast
        """
        pattern = self.pattern_library.get_pattern_by_id(pattern_id)
        if not pattern:
            return {"error": "Pattern not found"}

        # Analyze historical instances
        analysis = self.pattern_library.analyze_pattern_recurrence(pattern_id)

        if analysis["total_instances"] == 0:
            return {
                "pattern_id": pattern_id,
                "pattern_name": pattern.name,
                "projection": "Insufficient historical data for projection",
                "confidence": 0.0,
            }

        # Calculate projection
        avg_interval = analysis.get("average_interval_years", pattern.typical_duration_years or 100)
        last_occurrence = analysis.get("most_recent_occurrence")

        if last_occurrence:
            years_since = current_year - last_occurrence
            progress_ratio = years_since / avg_interval if avg_interval > 0 else 0

            if progress_ratio >= 0.8:
                likelihood = "High - Pattern interval nearing completion"
            elif progress_ratio >= 0.5:
                likelihood = "Moderate - Pattern midway through typical cycle"
            elif progress_ratio >= 0.2:
                likelihood = "Low - Pattern recently occurred"
            else:
                likelihood = "Very Low - Pattern just completed"

            estimated_next = last_occurrence + avg_interval
            years_until = estimated_next - current_year

            return {
                "pattern_id": pattern_id,
                "pattern_name": pattern.name,
                "pattern_type": pattern.pattern_type,
                "historical_instances": analysis["total_instances"],
                "average_interval_years": avg_interval,
                "last_occurrence": last_occurrence,
                "years_since_last": years_since,
                "progress_through_cycle": f"{progress_ratio * 100:.1f}%",
                "estimated_next_occurrence": estimated_next if years_until > 0 else None,
                "years_until_next": years_until if years_until > 0 else None,
                "likelihood": likelihood,
                "confidence": min(analysis["total_instances"] / 5.0, 1.0),  # More instances = higher confidence
                "trajectory_phases": self._generate_trajectory_phases(pattern, years_until),
            }
        else:
            return {
                "pattern_id": pattern_id,
                "pattern_name": pattern.name,
                "projection": "No historical occurrences found",
                "confidence": 0.0,
            }

    def create_scenario(
        self,
        name: str,
        description: str,
        indicator_ids: Optional[List[int]] = None,
        pattern_ids: Optional[List[int]] = None,
        assumptions: Optional[Dict[str, Any]] = None,
    ) -> SimulationScenario:
        """
        Create a new simulation scenario.

        Args:
            name: Scenario name
            description: Scenario description
            indicator_ids: List of indicator IDs to include
            pattern_ids: List of pattern IDs to consider
            assumptions: Additional assumptions

        Returns:
            Created SimulationScenario instance
        """
        # Gather input indicators
        input_indicators = []
        if indicator_ids:
            for ind_id in indicator_ids:
                indicator = self.db.query(WorldIndicator).filter(WorldIndicator.id == ind_id).first()
                if indicator:
                    input_indicators.append(
                        {
                            "id": indicator.id,
                            "name": indicator.indicator_name,
                            "category": indicator.category,
                            "value": indicator.value,
                            "description": indicator.description,
                        }
                    )

        # Match patterns
        matched_patterns = []
        if pattern_ids:
            for pat_id in pattern_ids:
                precondition_match = self.detect_pattern_preconditions(pat_id)
                if precondition_match.get("match_score", 0) > 0:
                    matched_patterns.append(precondition_match)

        # Generate trajectory
        trajectory = self._generate_scenario_trajectory(matched_patterns)

        # Calculate confidence
        confidence = self._calculate_scenario_confidence(matched_patterns, input_indicators)

        # Create scenario
        scenario = SimulationScenario(
            name=name,
            description=description,
            input_indicators=input_indicators,
            assumptions=assumptions or {},
            matched_patterns=matched_patterns,
            trajectory=trajectory,
            confidence_score=confidence,
            created_at=datetime.utcnow(),
        )

        self.db.add(scenario)
        self.db.commit()
        self.db.refresh(scenario)

        return scenario

    def get_all_scenarios(self) -> List[SimulationScenario]:
        """Get all simulation scenarios."""
        return self.db.query(SimulationScenario).order_by(SimulationScenario.created_at.desc()).all()

    def get_scenario_by_id(self, scenario_id: int) -> Optional[SimulationScenario]:
        """Get a specific scenario by ID."""
        return (
            self.db.query(SimulationScenario).filter(SimulationScenario.id == scenario_id).first()
        )

    def analyze_prophetic_timeline(self) -> Dict[str, Any]:
        """
        Analyze prophetic timeline for pending fulfillments.

        Returns:
            Dictionary with prophetic analysis
        """
        prophecies = self.prophecy_library.get_all_prophecies()

        pending_count = 0
        partial_count = 0
        complete_count = 0

        pending_prophecies = []
        partial_prophecies = []

        for prophecy in prophecies:
            fulfillments = self.prophecy_library.get_fulfillments(prophecy.id)

            if not fulfillments:
                pending_count += 1
                pending_prophecies.append(
                    {
                        "id": prophecy.id,
                        "reference": prophecy.reference,
                        "prophecy_type": prophecy.prophecy_type,
                        "year_declared": prophecy.year_declared,
                        "elements": prophecy.elements,
                    }
                )
            else:
                from app.models.prophecy import FulfillmentType

                has_complete = any(f.fulfillment_type == FulfillmentType.COMPLETE for f in fulfillments)
                has_partial = any(f.fulfillment_type == FulfillmentType.PARTIAL for f in fulfillments)
                has_pending = any(f.fulfillment_type == FulfillmentType.PENDING for f in fulfillments)

                if has_pending or (has_partial and not has_complete):
                    partial_count += 1
                    partial_prophecies.append(
                        {
                            "id": prophecy.id,
                            "reference": prophecy.reference,
                            "fulfillments": len(fulfillments),
                            "types": [f.fulfillment_type.value for f in fulfillments],
                        }
                    )
                elif has_complete:
                    complete_count += 1

        return {
            "total_prophecies": len(prophecies),
            "complete": complete_count,
            "partial": partial_count,
            "pending": pending_count,
            "pending_prophecies": pending_prophecies,
            "partial_prophecies": partial_prophecies,
            "eschatological_outlook": self._assess_eschatological_status(
                pending_prophecies, partial_prophecies
            ),
        }

    def calculate_civilization_risk_score(self) -> Dict[str, Any]:
        """
        Calculate overall civilization risk score based on pattern preconditions.

        Returns:
            Dictionary with risk assessment
        """
        patterns = self.pattern_library.get_all_patterns()
        indicators = self.db.query(WorldIndicator).all()

        if not indicators:
            return {
                "overall_risk_score": 0.0,
                "risk_level": self.RISK_LOW,
                "message": "No indicators available for risk assessment",
            }

        pattern_risks = []

        for pattern in patterns:
            precondition_match = self.detect_pattern_preconditions(pattern.id)
            match_score = precondition_match.get("match_score", 0.0)

            if match_score > 0:
                # Weight by pattern severity
                severity_weights = {
                    "decline": 0.8,
                    "collapse": 1.0,
                    "judgment": 0.9,
                    "fall": 0.85,
                    "fragmentation": 0.7,
                    "default": 0.5,
                }

                pattern_type = pattern.pattern_type.lower()
                weight = severity_weights.get(pattern_type, severity_weights["default"])

                weighted_score = match_score * weight

                pattern_risks.append(
                    {
                        "pattern_id": pattern.id,
                        "pattern_name": pattern.name,
                        "pattern_type": pattern.pattern_type,
                        "match_score": match_score,
                        "weighted_risk": weighted_score,
                        "matched_preconditions": precondition_match.get("matched_preconditions", []),
                    }
                )

        # Sort by risk descending
        pattern_risks.sort(key=lambda p: p["weighted_risk"], reverse=True)

        # Calculate overall score
        if pattern_risks:
            overall_score = statistics.mean([p["weighted_risk"] for p in pattern_risks])
        else:
            overall_score = 0.0

        risk_level = self._calculate_risk_level(overall_score)

        return {
            "overall_risk_score": overall_score,
            "risk_level": risk_level,
            "total_patterns_assessed": len(patterns),
            "patterns_with_matches": len(pattern_risks),
            "top_risks": pattern_risks[:5],  # Top 5 risks
            "risk_categories": self._categorize_risks(pattern_risks),
        }

    # Private helper methods

    def _calculate_risk_level(self, match_score: float) -> str:
        """Convert match score to risk level."""
        if match_score >= 0.8:
            return self.RISK_CRITICAL
        elif match_score >= 0.6:
            return self.RISK_HIGH
        elif match_score >= 0.3:
            return self.RISK_MODERATE
        else:
            return self.RISK_LOW

    def _generate_trajectory_phases(
        self, pattern: Pattern, years_until: Optional[int]
    ) -> List[Dict[str, Any]]:
        """Generate trajectory phases for pattern projection."""
        if not years_until or years_until <= 0:
            return []

        phases = []
        indicators = pattern.indicators or []
        outcomes = pattern.outcomes or []

        # Early phase: Preconditions active
        phases.append(
            {
                "phase": "Preconditions Active",
                "timeframe": "Current",
                "characteristics": pattern.preconditions or [],
                "years_range": [0, int(years_until * 0.3)],
            }
        )

        # Middle phase: Indicators manifest
        phases.append(
            {
                "phase": "Indicators Manifesting",
                "timeframe": f"Next {int(years_until * 0.4)} years",
                "characteristics": indicators,
                "years_range": [int(years_until * 0.3), int(years_until * 0.7)],
            }
        )

        # Late phase: Outcomes materialize
        phases.append(
            {
                "phase": "Outcomes Materializing",
                "timeframe": f"Years {int(years_until * 0.7)}-{years_until}",
                "characteristics": outcomes,
                "years_range": [int(years_until * 0.7), years_until],
            }
        )

        return phases

    def _generate_scenario_trajectory(self, matched_patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate trajectory based on matched patterns."""
        if not matched_patterns:
            return {"message": "No patterns matched - trajectory uncertain"}

        # Aggregate pattern outcomes
        all_outcomes = []
        for pattern_match in matched_patterns:
            pattern_id = pattern_match.get("pattern_id")
            pattern = self.pattern_library.get_pattern_by_id(pattern_id)
            if pattern and pattern.outcomes:
                all_outcomes.extend(pattern.outcomes)

        # Create timeline
        timeline = [
            {"phase": "Current State", "year_offset": 0, "events": ["Pattern preconditions detected"]},
            {
                "phase": "Near Term (5 years)",
                "year_offset": 5,
                "events": ["Indicators begin manifesting"],
            },
            {
                "phase": "Medium Term (20 years)",
                "year_offset": 20,
                "events": ["Pattern progression accelerates"],
            },
            {"phase": "Long Term (50 years)", "year_offset": 50, "events": all_outcomes[:5]},
        ]

        return {"timeline": timeline, "projected_outcomes": list(set(all_outcomes))}

    def _calculate_scenario_confidence(
        self, matched_patterns: List[Dict[str, Any]], input_indicators: List[Dict[str, Any]]
    ) -> float:
        """Calculate confidence score for scenario."""
        if not matched_patterns:
            return 0.0

        # Average match scores
        match_scores = [p.get("match_score", 0) for p in matched_patterns]
        avg_match = statistics.mean(match_scores) if match_scores else 0

        # Factor in data availability
        data_factor = min(len(input_indicators) / 10.0, 1.0)  # More indicators = higher confidence

        return (avg_match + data_factor) / 2.0

    def _assess_eschatological_status(
        self, pending_prophecies: List[Dict], partial_prophecies: List[Dict]
    ) -> str:
        """Assess eschatological timeline status."""
        if len(pending_prophecies) > 3:
            return "Many prophecies remain unfulfilled - significant prophetic timeline ahead"
        elif len(partial_prophecies) > 2:
            return "Multiple prophecies in progressive fulfillment - active prophetic period"
        elif len(pending_prophecies) == 0 and len(partial_prophecies) == 0:
            return "All tracked prophecies fulfilled - potential eschatological completion approaching"
        else:
            return "Limited prophecies pending - transitional prophetic phase"

    def _categorize_risks(self, pattern_risks: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize risks by type."""
        categories = {}
        for risk in pattern_risks:
            pattern_type = risk.get("pattern_type", "unknown")
            categories[pattern_type] = categories.get(pattern_type, 0) + 1
        return categories

    def get_all_scenarios(self) -> List[SimulationScenario]:
        """Get all simulation scenarios."""
        return self.db.query(SimulationScenario).order_by(
            SimulationScenario.created_at.desc()
        ).all()

    def get_scenario_by_id(self, scenario_id: int) -> Optional[SimulationScenario]:
        """Get a specific scenario by ID."""
        return self.db.query(SimulationScenario).filter(
            SimulationScenario.id == scenario_id
        ).first()

