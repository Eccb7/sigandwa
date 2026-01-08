#!/usr/bin/env python3
"""
Comprehensive System Test
Demonstrates all phases of the Biblical Cliodynamics Analysis System.
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80 + "\n")


def print_json(data: Any):
    """Pretty print JSON data."""
    print(json.dumps(data, indent=2))


def test_phase_1_chronology():
    """Test Phase 1: Chronology Database."""
    print_section("PHASE 1: CHRONOLOGY & HISTORICAL DATABASE")
    
    # Get events count
    print("📊 Database Statistics:")
    response = requests.get(f"{BASE_URL}/chronology/events")
    events = response.json()
    print(f"  - Total Events: {len(events)}")
    
    # Get timeline
    print("\n🕐 Recent Timeline Events:")
    response = requests.get(f"{BASE_URL}/chronology/timeline?limit=5")
    timeline = response.json()
    for event in timeline:
        print(f"  - {event['year']}: {event['name']}")


def test_phase_2_patterns():
    """Test Phase 2: Pattern Recognition."""
    print_section("PHASE 2: PATTERN RECOGNITION SYSTEM")
    
    # List patterns
    print("📋 Biblical Pattern Templates:")
    response = requests.get(f"{BASE_URL}/patterns")
    patterns = response.json()
    for pattern in patterns:
        print(f"  - {pattern['id']}: {pattern['name']} ({pattern['pattern_type']})")
    
    # Get pattern instances
    print("\n🔍 Historical Instances of 'Moral Decay → Judgment':")
    response = requests.get(f"{BASE_URL}/patterns/1/instances")
    instances = response.json()
    print(f"  Total Instances: {instances['total_instances']}")
    for instance in instances['instances']:
        print(f"  - {instance['event_name']} ({instance['event_year']})")


def test_phase_3_prophecies():
    """Test Phase 3: Prophecy-Fulfillment Tracking."""
    print_section("PHASE 3: PROPHECY-FULFILLMENT TRACKING")
    
    # List prophecies
    print("📖 Tracked Prophecies:")
    response = requests.get(f"{BASE_URL}/prophecies")
    prophecies = response.json()
    for prophecy in prophecies:
        print(f"  - {prophecy['reference']}: {prophecy['prophecy_type']}")
        print(f"    Declared: {prophecy['year_declared']}")
    
    # Get prophetic timeline
    print("\n⏰ Prophetic Timeline Status:")
    response = requests.get(f"{BASE_URL}/prophecies/timeline")
    timeline = response.json()
    print(f"  - Complete: {timeline['complete']}/{timeline['total']}")
    print(f"  - Partial: {timeline['partial']}/{timeline['total']}")
    print(f"  - Pending: {timeline['pending']}/{timeline['total']}")
    
    # Get specific fulfillment
    print("\n✅ Daniel 9 (Seventy Weeks) Fulfillment:")
    response = requests.get(f"{BASE_URL}/prophecies/3/fulfillments")
    fulfillments = response.json()
    if fulfillments['fulfillments']:
        fulfillment = fulfillments['fulfillments'][0]
        print(f"  Event: {fulfillment['event_name']}")
        print(f"  Year: {fulfillment['event_year']}")
        print(f"  Confidence: {fulfillment['confidence_score']}%")
        print(f"  Elements Fulfilled: {fulfillment['elements_fulfilled']}")


def test_phase_4_simulation():
    """Test Phase 4: Simulation Engine."""
    print_section("PHASE 4: SIMULATION ENGINE & FORECASTING")
    
    # Assess indicators
    print("🌍 Current World Indicators:")
    response = requests.get(f"{BASE_URL}/simulation/indicators")
    assessment = response.json()
    print(f"  Total Indicators: {assessment['total_indicators']}")
    print(f"  Categories: {', '.join(assessment['categories'].keys())}")
    for category, count in assessment['categories'].items():
        print(f"    - {category}: {count} indicators")
    
    # Risk assessment
    print("\n⚠️  Civilization Risk Assessment:")
    response = requests.get(f"{BASE_URL}/simulation/risk-assessment")
    risk = response.json()
    print(f"  Overall Risk Score: {risk['overall_risk_score']:.3f}")
    print(f"  Risk Level: {risk['risk_level'].upper()}")
    print(f"  Patterns Assessed: {risk['total_patterns_assessed']}")
    print(f"  Patterns with Matches: {risk['patterns_with_matches']}")
    
    print("\n  Top Risks:")
    for i, risk_item in enumerate(risk['top_risks'][:3], 1):
        print(f"    {i}. {risk_item['pattern_name']}")
        print(f"       Match Score: {risk_item['match_score']:.2f}")
        print(f"       Matched Preconditions: {', '.join(risk_item['matched_preconditions'])}")
    
    # Check pattern preconditions
    print("\n🎯 Pattern Precondition Analysis:")
    response = requests.get(f"{BASE_URL}/simulation/patterns/1/preconditions")
    analysis = response.json()
    print(f"  Pattern: {analysis['pattern_name']}")
    print(f"  Match Score: {analysis['match_score']:.2f} ({analysis['match_score']*100:.0f}%)")
    print(f"  Risk Level: {analysis['risk_level'].upper()}")
    print(f"  Matched: {', '.join(analysis['matched_preconditions'])}")
    if analysis['missing_preconditions']:
        print(f"  Missing: {', '.join(analysis['missing_preconditions'])}")
    else:
        print(f"  Missing: None (All preconditions met!)")
    
    # Project trajectory
    print("\n📈 Pattern Trajectory Projection:")
    response = requests.get(f"{BASE_URL}/simulation/patterns/1/trajectory?current_year=2026")
    projection = response.json()
    print(f"  Pattern: {projection['pattern_name']}")
    print(f"  Historical Instances: {projection['historical_instances']}")
    print(f"  Average Interval: {projection['average_interval_years']:.0f} years")
    print(f"  Last Occurrence: {projection['last_occurrence']}")
    print(f"  Years Since Last: {projection['years_since_last']}")
    print(f"  Progress Through Cycle: {projection['progress_through_cycle']}")
    print(f"  Likelihood: {projection['likelihood']}")
    
    # Prophetic timeline
    print("\n📅 Prophetic Timeline Analysis:")
    response = requests.get(f"{BASE_URL}/simulation/prophetic-timeline")
    prophetic = response.json()
    print(f"  Total Prophecies: {prophetic['total_prophecies']}")
    print(f"  Complete: {prophetic['complete']}")
    print(f"  Partial: {prophetic['partial']}")
    print(f"  Pending: {prophetic['pending']}")
    print(f"  Outlook: {prophetic['eschatological_outlook']}")
    
    # Create scenario
    print("\n🎬 Creating Simulation Scenario...")
    response = requests.post(
        f"{BASE_URL}/simulation/scenarios",
        json={
            "name": "System Test Scenario 2026",
            "description": "Comprehensive test of all system capabilities",
            "pattern_ids": [1, 2, 3, 4]
        }
    )
    scenario = response.json()
    print(f"  Scenario ID: {scenario['id']}")
    print(f"  Name: {scenario['name']}")
    print(f"  Patterns Analyzed: {len(scenario['matched_patterns'])}")
    print(f"  Confidence Score: {scenario['confidence_score']:.3f}")
    print(f"  Trajectory Phases: {len(scenario['trajectory'].get('timeline', []))}")


def main():
    """Run all system tests."""
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  Biblical Cliodynamics Analysis System - Complete System Test".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    try:
        test_phase_1_chronology()
        test_phase_2_patterns()
        test_phase_3_prophecies()
        test_phase_4_simulation()
        
        print_section("✅ ALL TESTS COMPLETE")
        print("System Status: FULLY OPERATIONAL")
        print("\nAPI Documentation: http://localhost:8000/docs")
        print("System Documentation: SYSTEM_DOCUMENTATION.md")
        print("Phase Completion Reports:")
        print("  - PHASE_1_COMPLETION.md")
        print("  - PHASE_2_COMPLETION.md")
        print("  - PHASE_3_COMPLETION.md")
        print("  - PHASE_4_COMPLETION.md")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API server")
        print("Please ensure the API is running: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
