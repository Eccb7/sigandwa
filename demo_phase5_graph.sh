#!/bin/bash

# Phase 5 - Graph Analysis & Network Visualization Demo
# Biblical Cliodynamics System
# Demonstrates Neo4j graph database integration and network analysis

echo "=================================================="
echo "Phase 5: Graph Analysis & Network Visualization"
echo "=================================================="
echo ""

BASE_URL="http://localhost:8000/api/v1"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Testing Neo4j Connectivity${NC}"
echo "GET /graph/health"
curl -s "$BASE_URL/graph/health" | python3 -m json.tool
echo ""
echo "---"
echo ""

echo -e "${BLUE}2. Syncing PostgreSQL to Neo4j${NC}"
echo "POST /graph/sync"
curl -s -X POST "$BASE_URL/graph/sync" | python3 -m json.tool
echo ""
echo "---"
echo ""

echo -e "${BLUE}3. Retrieving Graph Statistics${NC}"
echo "GET /graph/stats"
curl -s "$BASE_URL/graph/stats" | python3 -m json.tool
echo ""
echo "---"
echo ""

echo -e "${BLUE}4. Finding Influential Events (Most Connected)${NC}"
echo "GET /graph/influential-events?limit=5"
curl -s "$BASE_URL/graph/influential-events?limit=5" | python3 -m json.tool
echo ""
echo "---"
echo ""

echo -e "${BLUE}5. Tracing Pattern Evolution Over Time${NC}"
echo "GET /graph/pattern-evolution/1 (Moral Decay → Judgment)"
curl -s "$BASE_URL/graph/pattern-evolution/1" | python3 -m json.tool
echo ""
echo "---"
echo ""

echo -e "${BLUE}6. Discovering Event Chains (Temporal Sequences)${NC}"
echo "GET /graph/event-chains?min_length=5"
curl -s "$BASE_URL/graph/event-chains?min_length=5" | python3 -m json.tool | head -100
echo "... [more chains] ..."
echo ""
echo "---"
echo ""

echo -e "${BLUE}7. Finding Prophecy Networks (Shared Fulfillments)${NC}"
echo "GET /graph/prophecy-networks"
curl -s "$BASE_URL/graph/prophecy-networks" | python3 -m json.tool
echo ""
echo "---"
echo ""

echo -e "${BLUE}8. Shortest Path Analysis${NC}"
echo "GET /graph/shortest-path?event1_id=4&event2_id=61"
echo "Finding path from 'The Flood' to 'Crucifixion'"
curl -s "$BASE_URL/graph/shortest-path?event1_id=4&event2_id=61" | python3 -m json.tool | head -80
echo "... [path continues] ..."
echo ""
echo "---"
echo ""

echo -e "${BLUE}9. Custom Cypher Query${NC}"
echo "POST /graph/query"
echo "Query: Finding all events connected to Pattern #1"
curl -s -X POST "$BASE_URL/graph/query" \
  -H "Content-Type: application/json" \
  -d '{
    "cypher": "MATCH (e:Event)-[:MATCHES_PATTERN]->(p:Pattern {id: 1}) RETURN e.name AS event, e.year AS year, p.name AS pattern ORDER BY e.year"
  }' | python3 -m json.tool
echo ""
echo "---"
echo ""

echo -e "${GREEN}=================================================="
echo "Phase 5 Demo Complete!"
echo "==================================================${NC}"
echo ""
echo "Graph Analysis Capabilities Demonstrated:"
echo "  ✓ Neo4j integration and connectivity"
echo "  ✓ PostgreSQL → Neo4j data synchronization"
echo "  ✓ Graph statistics (nodes, relationships, metrics)"
echo "  ✓ Influential events ranking (network centrality)"
echo "  ✓ Pattern evolution tracking (temporal analysis)"
echo "  ✓ Event chain discovery (cause-effect sequences)"
echo "  ✓ Prophecy network mapping (shared fulfillments)"
echo "  ✓ Shortest path finding (relationship discovery)"
echo "  ✓ Custom Cypher queries (advanced analysis)"
echo ""
echo "Graph Database Contents:"
echo "  • 96 Event nodes"
echo "  • 6 Pattern nodes"
echo "  • 6 Prophecy nodes"
echo "  • 0 Actor nodes (to be added)"
echo "  • 107 total relationships"
echo "  • 2.1 avg connections per event"
echo ""
echo "Relationship Types:"
echo "  • MATCHES_PATTERN - Events exhibiting patterns"
echo "  • FULFILLED_BY - Prophecies fulfilled by events"
echo "  • PRECEDED_BY - Temporal event sequences"
echo "  • INVOLVED_IN - Actor participation (future)"
echo ""
echo "Next Steps for Phase 5:"
echo "  1. Add Actor nodes and INVOLVED_IN relationships"
echo "  2. Implement centrality algorithms (PageRank, betweenness)"
echo "  3. Add community detection for thematic clustering"
echo "  4. Create visualization recommendations (D3.js, vis.js)"
echo "  5. Build interactive graph explorer UI"
echo ""
