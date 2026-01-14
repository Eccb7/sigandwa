#!/bin/bash
# Phase 4 Demonstration Script
# Shows the Simulation Engine capabilities

echo "================================================================================"
echo " PHASE 4: SIMULATION ENGINE DEMONSTRATION"
echo "================================================================================"
echo ""

echo "📊 1. ASSESSING CURRENT WORLD INDICATORS (25 indicators)"
echo "--------------------------------------------------------------------------------"
curl -s http://localhost:8000/api/v1/simulation/indicators | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Total Indicators: {data['total_indicators']}\")
print(f\"Categories: {', '.join(data['categories'].keys())}\")
for cat, count in data['categories'].items():
    print(f\"  - {cat}: {count} indicators\")
"
echo ""

echo "⚠️  2. CIVILIZATION RISK ASSESSMENT"
echo "--------------------------------------------------------------------------------"
curl -s http://localhost:8000/api/v1/simulation/risk-assessment | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Overall Risk Score: {data['overall_risk_score']:.3f}/1.0\")
print(f\"Risk Level: {data['risk_level'].upper()}\")
print(f\"Patterns Assessed: {data['total_patterns_assessed']}\")
print(f\"Patterns with Matches: {data['patterns_with_matches']}\")
print(\"\nTop 3 Risks:\")
for i, risk in enumerate(data['top_risks'][:3], 1):
    print(f\"  {i}. {risk['pattern_name']}\")
    print(f\"     Match Score: {risk['match_score']:.2f}\")
    print(f\"     Matched: {', '.join(risk['matched_preconditions'])}\")
"
echo ""

echo "🎯 3. PATTERN PRECONDITION DETECTION: Moral Decay → Judgment"
echo "--------------------------------------------------------------------------------"
curl -s http://localhost:8000/api/v1/simulation/patterns/1/preconditions | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Pattern: {data['pattern_name']}\")
print(f\"Match Score: {data['match_score']:.2f} ({data['match_score']*100:.0f}%)\")
print(f\"Risk Level: {data['risk_level'].upper()}\")
print(f\"Matched Preconditions: {', '.join(data['matched_preconditions'])}\")
if data['missing_preconditions']:
    print(f\"Missing Preconditions: {', '.join(data['missing_preconditions'])}\")
else:
    print('Missing Preconditions: None (ALL CONDITIONS MET!)')
print(f\"Typical Duration: {data['typical_duration_years']} years\")
"
echo ""

echo "📈 4. TRAJECTORY PROJECTION: Moral Decay → Judgment"
echo "--------------------------------------------------------------------------------"
curl -s "http://localhost:8000/api/v1/simulation/patterns/1/trajectory?current_year=2026" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Pattern: {data['pattern_name']}\")
print(f\"Historical Instances: {data['historical_instances']}\")
print(f\"Average Interval: {data['average_interval_years']:.0f} years\")
print(f\"Last Occurrence: {data['last_occurrence']} (Sodom & Gomorrah)\")
print(f\"Years Since Last: {data['years_since_last']}\")
print(f\"Progress Through Cycle: {data['progress_through_cycle']}\")
print(f\"Likelihood: {data['likelihood']}\")
print(f\"Confidence: {data['confidence']:.2f}\")
"
echo ""

echo "📅 5. PROPHETIC TIMELINE ANALYSIS"
echo "--------------------------------------------------------------------------------"
curl -s http://localhost:8000/api/v1/simulation/prophetic-timeline | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Total Prophecies: {data['total_prophecies']}\")
print(f\"Complete: {data['complete']}\")
print(f\"Partial: {data['partial']}\")
print(f\"Pending: {data['pending']}\")
print(f\"\nEschatological Outlook:\")
print(f\"  {data['eschatological_outlook']}\")
print(f\"\nPending Prophecies:\")
for prophecy in data['pending_prophecies']:
    print(f\"  - {prophecy['reference']} ({prophecy['prophecy_type']})\")
"
echo ""

echo "🎬 6. CREATING SIMULATION SCENARIO"
echo "--------------------------------------------------------------------------------"
curl -s -X POST http://localhost:8000/api/v1/simulation/scenarios \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Phase 4 Demo Scenario",
    "description": "Demonstration of simulation capabilities",
    "pattern_ids": [1, 3, 4]
  }' | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Scenario ID: {data['id']}\")
print(f\"Name: {data['name']}\")
print(f\"Patterns Analyzed: {len(data['matched_patterns'])}\")
print(f\"Confidence Score: {data['confidence_score']:.3f}\")
print(f\"\nMatched Patterns:\")
for pattern in data['matched_patterns']:
    print(f\"  - {pattern['pattern_name']}\")
    print(f\"    Match Score: {pattern['match_score']:.2f}\")
    print(f\"    Risk Level: {pattern['risk_level'].upper()}\")
"
echo ""

echo "================================================================================"
echo " ✅ PHASE 4 DEMONSTRATION COMPLETE"
echo "================================================================================"
echo ""
echo "System Status: FULLY OPERATIONAL"
echo ""
echo "Documentation:"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Phase 4 Report: PHASE_4_COMPLETION.md"
echo "  - System Docs: SYSTEM_DOCUMENTATION.md"
echo ""
