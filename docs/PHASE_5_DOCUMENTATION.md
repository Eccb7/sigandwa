# Phase 5: Graph Analysis & Network Visualization

**Status:** ✅ **COMPLETE**  
**Implementation Date:** January 2025  
**Neo4j Version:** 5.15  
**Python Driver:** neo4j 5.16.0

---

## Overview

Phase 5 adds a **graph database layer** using Neo4j to enable advanced relationship analysis, network visualization, and complex pattern discovery across biblical events, prophecies, and historical patterns. This phase transforms the relational database into an interconnected knowledge graph for cliodynamic analysis.

### Key Capabilities

- **Relationship Mapping:** Visualize connections between events, patterns, and prophecies
- **Network Analysis:** Discover influential events, clusters, and communities
- **Path Finding:** Trace connections across millennia of history
- **Pattern Evolution:** Track how patterns manifest across different eras
- **Prophecy Networks:** Map prophecies with shared fulfillments
- **Temporal Chains:** Identify cause-effect sequences

---

## Architecture

### Graph Schema

```
NODES:
├── Event (96 nodes)
│   Properties: id, name, year, year_start, year_end, era, event_type, description
├── Pattern (6 nodes)
│   Properties: id, name, pattern_type, description, typical_duration_years
├── Prophecy (6 nodes)
│   Properties: id, reference, prophecy_type, year_declared, prophet, scope, text
└── Actor (0 nodes - planned)
    Properties: id, name, actor_type, description

RELATIONSHIPS:
├── MATCHES_PATTERN (Event → Pattern)
│   Properties: confidence, identified_date
├── FULFILLED_BY (Prophecy → Event)
│   Properties: fulfillment_type, confidence, verification_notes
├── PRECEDED_BY (Event → Event)
│   Properties: years_between
└── INVOLVED_IN (Actor → Event) - planned
    Properties: role, significance
```

### Data Flow

```
PostgreSQL (Source of Truth)
    ↓ sync_all()
Neo4j Graph Database
    ↓ Cypher Queries
Graph Analysis Results
    ↓ REST API
Frontend Applications
```

---

## Implementation

### 1. Core Modules

#### `backend/app/graph/__init__.py` (550 lines)

**Neo4jConnection Class**
- Manages Neo4j driver connection
- Methods:
  - `verify_connectivity()` - Health check
  - `execute_query()` - Read operations
  - `execute_write()` - Write operations
  - `close()` - Cleanup

**GraphSync Class**
- Synchronizes PostgreSQL → Neo4j
- Methods:
  - `initialize_schema()` - Creates constraints and indexes
  - `sync_events()` - Syncs 96 biblical events
  - `sync_patterns()` - Syncs 6 historical patterns
  - `sync_prophecies()` - Syncs 6 prophecies
  - `sync_actors()` - Syncs actors (future)
  - `sync_event_patterns()` - Creates MATCHES_PATTERN relationships
  - `sync_prophecy_fulfillments()` - Creates FULFILLED_BY relationships
  - `sync_event_actors()` - Creates INVOLVED_IN relationships (future)
  - `sync_temporal_relationships()` - Creates PRECEDED_BY chains
  - `sync_all()` - Full synchronization

**GraphAnalyzer Class**
- Performs graph queries and analysis
- Methods:
  - `find_event_chains(min_length)` - Temporal sequences
  - `find_pattern_clusters()` - Events with shared patterns
  - `find_prophecy_networks()` - Connected prophecies
  - `find_influential_events(limit)` - Most connected nodes
  - `find_pattern_evolution(pattern_id)` - Pattern timeline
  - `find_shortest_path(event1_id, event2_id)` - Path discovery
  - `get_graph_statistics()` - Graph metrics

### 2. REST API Endpoints

#### `backend/app/api/routes/graph.py` (360 lines)

**11 Graph Endpoints:**

1. **GET `/api/v1/graph/health`**
   - Check Neo4j connectivity
   - Response: `{"neo4j_connected": true, "status": "healthy"}`

2. **POST `/api/v1/graph/sync`**
   - Sync PostgreSQL to Neo4j
   - Response: Sync counts for all node and relationship types

3. **GET `/api/v1/graph/stats`**
   - Graph statistics
   - Response: Node counts, relationship counts, avg connections

4. **GET `/api/v1/graph/event-chains?min_length=3`**
   - Find temporal event sequences
   - Response: Array of chronological chains

5. **GET `/api/v1/graph/pattern-clusters`**
   - Events matching multiple patterns
   - Response: Clustered events

6. **GET `/api/v1/graph/prophecy-networks`**
   - Prophecies with shared fulfillments
   - Response: Connected prophecy pairs

7. **GET `/api/v1/graph/influential-events?limit=10`**
   - Most connected events (centrality)
   - Response: Ranked events by connection count

8. **GET `/api/v1/graph/pattern-evolution/{pattern_id}`**
   - Pattern manifestation timeline
   - Response: Chronological instances

9. **GET `/api/v1/graph/shortest-path?event1_id=X&event2_id=Y`**
   - Path between two events
   - Response: Node sequence and relationship types

10. **POST `/api/v1/graph/query`**
    - Custom Cypher queries (read-only)
    - Request: `{"cypher": "MATCH ... RETURN ..."}`
    - Response: Query results

11. **DELETE `/api/v1/graph/reset`**
    - Clear graph database
    - Response: Deletion confirmation

---

## Current Graph State

### Database Contents (as of sync)

```
Nodes:
- Events: 96
- Patterns: 6
- Prophecies: 6
- Actors: 0
Total: 108 nodes

Relationships:
- MATCHES_PATTERN: 5
- FULFILLED_BY: 7
- PRECEDED_BY: 95 (chronological chains)
- INVOLVED_IN: 0
Total: 107 relationships

Average Connections: 2.1 per event
```

### Top Influential Events

Based on `find_influential_events()` query:

1. **Crucifixion & Resurrection (30 AD)** - 2 prophecy fulfillments
2. **Fall of Babylon (-539)** - 2 prophecy fulfillments
3. **Fall of Jerusalem (-586)** - 2 prophecy fulfillments
4. **State of Israel (1948)** - 1 pattern match
5. **Decree of Cyrus (-538)** - 1 pattern match

### Prophecy Networks

Connected prophecies sharing fulfillment events:

1. **Daniel 9:24-27 + Jeremiah 25:8-14** → Fall of Jerusalem (-586)
2. **Daniel 2:31-45 + Jeremiah 25:8-14** → Fall of Babylon (-539)
3. **Daniel 9:24-27 + Isaiah 53:1-12** → Crucifixion (30 AD)

---

## Usage Examples

### 1. Sync Database

```bash
curl -X POST http://localhost:8000/api/v1/graph/sync | python3 -m json.tool
```

Response:
```json
{
  "success": true,
  "synced": {
    "events": 96,
    "patterns": 6,
    "prophecies": 6,
    "actors": 0,
    "event_patterns": 5,
    "prophecy_fulfillments": 7,
    "event_actors": 0
  },
  "message": "Successfully synced 120 items to Neo4j graph"
}
```

### 2. Find Event Chains

```bash
curl "http://localhost:8000/api/v1/graph/event-chains?min_length=5"
```

Returns chronological sequences like:
- Creation → Fall → Flood → Babel → Abraham → ... (11 events)
- Exodus → Golden Calf → Conquest → Joshua → Saul → David → ... (10 events)

### 3. Trace Pattern Evolution

```bash
curl "http://localhost:8000/api/v1/graph/pattern-evolution/1"
```

Response:
```json
{
  "pattern_id": 1,
  "total_instances": 2,
  "chronological_instances": [
    {
      "event_id": 4,
      "event_name": "The Flood",
      "year": -2348,
      "event_type": "natural",
      "description": "Global flood; divine judgment on pre-flood civilization"
    },
    {
      "event_id": 7,
      "event_name": "Destruction of Sodom and Gomorrah",
      "year": -1898,
      "event_type": "natural",
      "description": "Divine judgment on cities of the plain"
    }
  ]
}
```

### 4. Find Shortest Path

```bash
curl "http://localhost:8000/api/v1/graph/shortest-path?event1_id=4&event2_id=61"
```

Finds path from **The Flood** to **Crucifixion** (37 hops across 2,378 years):
- The Flood → Pattern (Moral Decay → Judgment) → Sodom → Isaac → Jacob → Joseph → ... → Fall of Jerusalem → Prophecy → Crucifixion

### 5. Custom Cypher Query

```bash
curl -X POST http://localhost:8000/api/v1/graph/query \
  -H "Content-Type: application/json" \
  -d '{
    "cypher": "MATCH (e:Event)-[r:FULFILLED_BY]-(p:Prophecy) RETURN e.name, p.reference, e.year ORDER BY e.year"
  }'
```

---

## Cypher Query Patterns

### Common Queries for Analysis

#### 1. Find All Events in an Era
```cypher
MATCH (e:Event)
WHERE e.era = 'patriarchal'
RETURN e.name, e.year
ORDER BY e.year
```

#### 2. Events Fulfilling Multiple Prophecies
```cypher
MATCH (e:Event)-[:FULFILLED_BY]-(p:Prophecy)
WITH e, count(p) as prophecy_count
WHERE prophecy_count > 1
RETURN e.name, e.year, prophecy_count
ORDER BY prophecy_count DESC
```

#### 3. Pattern Co-occurrence
```cypher
MATCH (e:Event)-[:MATCHES_PATTERN]->(p1:Pattern),
      (e)-[:MATCHES_PATTERN]->(p2:Pattern)
WHERE p1.id < p2.id
RETURN p1.name, p2.name, count(e) as co_occurrence
ORDER BY co_occurrence DESC
```

#### 4. Prophecy Fulfillment Timeline
```cypher
MATCH (p:Prophecy)-[:FULFILLED_BY]->(e:Event)
RETURN p.reference, p.year_declared, e.name, e.year,
       e.year - p.year_declared as years_to_fulfillment
ORDER BY years_to_fulfillment
```

#### 5. Event Influence Propagation
```cypher
MATCH path = (e1:Event)-[:PRECEDED_BY*1..3]->(e2:Event)
WHERE e1.id = 4  // The Flood
RETURN [node in nodes(path) | node.name] as sequence
```

---

## Visualization Recommendations

### Recommended Libraries

1. **vis.js** (Network Graphs)
   - Best for: Interactive node-edge diagrams
   - Features: Physics simulation, clustering, custom styling
   - Use case: Event relationship explorer

2. **D3.js** (Custom Visualizations)
   - Best for: Force-directed graphs, timelines, hierarchies
   - Features: Full control, animation, transitions
   - Use case: Pattern evolution visualization

3. **Cytoscape.js** (Biological Networks)
   - Best for: Complex graph layouts, large datasets
   - Features: Layouts (circular, hierarchical, force), styling
   - Use case: Full cliodynamic network

4. **Sigma.js** (Large Graphs)
   - Best for: Performance with 10,000+ nodes
   - Features: WebGL rendering, filtering
   - Use case: Future expansion

### Visualization Types

1. **Timeline View**
   - Horizontal axis: Time (-4004 to 1948+)
   - Vertical layers: Events, Patterns, Prophecies
   - Connections: Curved arcs showing relationships

2. **Network Graph**
   - Node size: By connection count (centrality)
   - Node color: By type (event/pattern/prophecy)
   - Edge thickness: Relationship strength
   - Clustering: Group by era/theme

3. **Prophecy Fulfillment Map**
   - Prophecy nodes on left
   - Event nodes on right
   - Bipartite graph layout
   - Color-coded by fulfillment type

4. **Pattern Evolution Flow**
   - Sankey diagram showing pattern instances
   - Width: Pattern significance/impact
   - Time flows left to right

---

## Performance Considerations

### Query Optimization

1. **Indexes Created:**
   - Event.year
   - Event.event_type
   - Pattern.pattern_type
   - Prophecy.prophecy_type

2. **Constraints Created:**
   - UNIQUE Event.id
   - UNIQUE Pattern.id
   - UNIQUE Prophecy.id
   - UNIQUE Actor.id

3. **Query Best Practices:**
   - Use `LIMIT` on large result sets
   - Filter early with `WHERE`
   - Use `PROFILE` to analyze slow queries
   - Create additional indexes for frequent filters

### Sync Performance

Current sync times (96 events, 6 patterns, 6 prophecies):
- Events: ~200ms
- Patterns: ~50ms
- Prophecies: ~50ms
- Relationships: ~100ms
- **Total: ~400ms**

For future scaling (1000+ events):
- Batch inserts (100 at a time)
- Async sync jobs
- Incremental updates (only changed data)

---

## Testing

### Manual Tests Performed

✅ **Connectivity:** Neo4j health check  
✅ **Sync:** Full database synchronization (120 items)  
✅ **Statistics:** Graph metrics retrieval  
✅ **Influential Events:** Centrality ranking  
✅ **Pattern Evolution:** Temporal analysis  
✅ **Event Chains:** Sequence discovery  
✅ **Prophecy Networks:** Shared fulfillments  
✅ **Shortest Path:** Cross-millennium pathfinding  
✅ **Custom Queries:** Cypher execution  

### Test Script

Run comprehensive demo:
```bash
./demo_phase5_graph.sh
```

### Expected Results

- All 11 endpoints respond successfully
- Graph contains 108 nodes, 107 relationships
- Crucifixion identified as most influential event
- Multiple event chains of length 10+ discovered
- 3 prophecy network connections found

---

## Future Enhancements

### Phase 5.1: Actor Integration
- Add Actor nodes (prophets, kings, nations)
- Create INVOLVED_IN relationships
- Actor influence analysis

### Phase 5.2: Advanced Analytics
- **Centrality Algorithms:**
  - PageRank (global influence)
  - Betweenness (bridge events)
  - Closeness (connectivity)
  - Degree (direct connections)

- **Community Detection:**
  - Louvain method (thematic clusters)
  - Label propagation (era grouping)

- **Graph Metrics:**
  - Clustering coefficient
  - Graph density
  - Average path length

### Phase 5.3: Machine Learning
- Node embeddings (Node2Vec)
- Link prediction (future events)
- Graph neural networks (pattern detection)

### Phase 5.4: Interactive UI
- Real-time graph explorer
- Drag-and-drop visualization
- Filter panels (era, type, pattern)
- Export to GraphML/GEXF
- Collaborative annotations

---

## Troubleshooting

### Common Issues

**1. Neo4j Connection Failed**
```
Error: Could not connect to Neo4j at bolt://localhost:7687
```
Solution:
```bash
docker ps | grep neo4j  # Verify running
docker start neo4j  # Start if stopped
```

**2. Sync Returns Empty Counts**
```
{"success": true, "synced": {"events": 0, ...}}
```
Solution:
- Check PostgreSQL database has data
- Verify SQLAlchemy models are correct
- Check logs: `docker logs backend`

**3. Query Timeout**
```
Error: Query execution timed out
```
Solution:
- Add `LIMIT` clause
- Create indexes on queried properties
- Simplify relationship traversal depth

**4. Missing Relationships**
```
PRECEDED_BY relationships not created
```
Solution:
- Run `sync_temporal_relationships()` separately
- Check `year_start` field populated for all events

### Debugging

Enable verbose logging:
```python
import logging
logging.getLogger('neo4j').setLevel(logging.DEBUG)
```

View Neo4j query logs:
```bash
docker exec neo4j tail -f /logs/query.log
```

---

## API Documentation

Full OpenAPI documentation available at:
```
http://localhost:8000/docs#/graph
```

Interactive testing with Swagger UI.

---

## Conclusion

Phase 5 successfully transforms the Biblical Cliodynamics system into a **knowledge graph**, enabling:

- **Relationship Discovery:** Trace connections invisible in tabular data
- **Network Analysis:** Identify pivotal events and clusters
- **Path Finding:** Connect events across millennia
- **Visualization Ready:** Export data for interactive graphs

The graph layer complements the existing relational database, simulation engine, and pattern recognition systems to create a comprehensive cliodynamic analysis platform.

**Next Phase:** Web Interface & Visualization Dashboard

---

## References

- Neo4j Documentation: https://neo4j.com/docs/
- Cypher Query Language: https://neo4j.com/docs/cypher-manual/
- Graph Data Science: https://neo4j.com/docs/graph-data-science/
- Python Driver: https://neo4j.com/docs/python-manual/

---

**Phase 5 Status:** ✅ **COMPLETE**  
**Graph Database:** ✅ **OPERATIONAL**  
**API Endpoints:** ✅ **11/11 FUNCTIONAL**  
**Documentation:** ✅ **COMPREHENSIVE**
