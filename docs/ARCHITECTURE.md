# System Architecture

## Overview

Sigandwa is a full-stack analytical platform that treats the Biblical timeline as an authoritative dataset for modeling civilizational patterns. The architecture is designed for analytical rigor, not theological interpretation.

---

## Design Philosophy

### Core Axioms

1. **History unfolds through patterns, not randomness**
2. **Prophecy encodes conditional trajectories**
3. **Collapse follows ignored correction**
4. **The future is bounded, not fixed**

These axioms are embedded in the system architecture, not left to interpretation.

---

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  (Next.js + D3.js - Visualization & User Interface)         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                         API Layer                            │
│            (FastAPI - RESTful Endpoints)                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Business Logic                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Chronology    │  │    Pattern      │  │  Simulation │ │
│  │     Engine      │  │   Recognition   │  │   Engine    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   Prophecy-     │  │    Insight      │                  │
│  │   Fulfillment   │  │   Generator     │                  │
│  │     Mapper      │  │                 │                  │
│  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        Data Layer                            │
│  ┌──────────────────────┐      ┌──────────────────────┐    │
│  │     PostgreSQL       │      │       Neo4j          │    │
│  │  (Timeline, Events)  │      │  (Relationships,     │    │
│  │                      │      │   Graph Patterns)    │    │
│  └──────────────────────┘      └──────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Architecture

### PostgreSQL: The Timeline Authority

**Purpose**: Authoritative chronology from Creation to Present

**Schema Design**:

```sql
chronology_events
├── id (PK)
├── name
├── year_start (indexed) -- Ussher-based
├── year_end (nullable)
├── year_start_min/max -- Uncertainty bounds
├── era (enum, indexed)
├── event_type (enum, indexed)
├── biblical_source
├── historical_source
└── metadata (JSONB)

actors
├── id (PK)
├── name (unique)
├── actor_type (nation, empire, person, institution)
├── year_start/end
└── description

patterns
├── id (PK)
├── name (unique)
├── pattern_type (rise, decline, collapse, recapitulation)
├── preconditions (JSONB)
├── indicators (JSONB)
├── outcomes (JSONB)
└── biblical_basis

prophecy_texts
├── id (PK)
├── reference (unique)
├── text
├── prophet
├── year_declared
├── elements (JSONB)
└── scope

prophecy_fulfillments
├── id (PK)
├── prophecy_id (FK)
├── event_id (FK)
├── fulfillment_type (enum)
├── confidence_score (0.0-1.0)
└── explanation
```

**Why PostgreSQL?**
- Temporal queries require strong ACID guarantees
- Complex JOINs for cross-era pattern matching
- Mature ecosystem for analytics

---

### Neo4j: The Relationship Graph

**Purpose**: Model complex relationships that SQL struggles with

**Node Types**:
- `(:Empire)` — Political entities
- `(:Prophecy)` — Prophetic declarations
- `(:Pattern)` — Recurring templates
- `(:Event)` — Mirror of PostgreSQL events

**Relationship Types**:
- `[:SUCCEEDED_BY]` — Empire succession
- `[:FULFILLS]` — Prophecy → Event
- `[:EXEMPLIFIES]` — Event → Pattern
- `[:RECAPITULATES]` — Pattern repetition across eras
- `[:CONTEMPORARY_WITH]` — Events in same timeframe

**Example Cypher Query**:
```cypher
// Find all empires that exemplify the "Pride Precedes Fall" pattern
MATCH (e:Empire)-[:EXEMPLIFIES]->(p:Pattern {name: 'Pride Precedes Fall'})
RETURN e.name, e.year_start, e.year_end
ORDER BY e.year_start
```

**Why Neo4j?**
- Graph traversals for pattern recapitulation
- Multi-hop relationship queries (e.g., "Which patterns led to which outcomes across which empires?")
- Prophecy fulfillment networks (partial, repeated, conditional)

---

## Core Modules

### 1. Chronology Engine

**Location**: `backend/app/chronology/engine.py`

**Responsibilities**:
- Maintain authoritative timeline
- Handle date uncertainty
- Temporal distance calculations
- Contemporaneous event discovery

**Key Methods**:
```python
class ChronologyEngine:
    def add_event(...)
    def get_events_in_range(year_start, year_end)
    def get_events_by_era(era)
    def calculate_temporal_distance(event1_id, event2_id)
    def find_contemporaneous_events(event_id, window_years)
```

**Temporal Indexing**:
- Years are absolute (negative = BC, positive = AD)
- Ussher chronology is the reference frame
- Uncertainty ranges stored separately

---

### 2. Event Ontology

**Location**: `backend/app/models/chronology.py`

**Classification Dimensions**:
- **Type**: Political, Economic, Religious, Military, Social, Natural, Prophetic
- **Era**: 18 distinct chronological periods
- **Actors**: Nations, empires, individuals, institutions

**Metadata Schema**:
```json
{
  "pattern": "exile_restoration",
  "consequences": ["diaspora", "temple_destruction"],
  "prophetic_significance": true,
  "historical_analogs": ["babylonian_exile", "roman_diaspora"]
}
```

---

### 3. Pattern Library

**Location**: `backend/app/patterns/` *(to be implemented)*

**Pattern Template**:
```python
class Pattern:
    name: str
    pattern_type: Enum  # rise, decline, collapse, recapitulation
    preconditions: List[str]
    indicators: List[str]
    typical_duration_years: int
    outcomes: List[str]
    historical_instances: List[int]  # Event IDs
    biblical_basis: str
```

**Core Patterns**:
1. **Moral Decay → Judgment** (Genesis Flood, Sodom, Jerusalem 586 BC, 70 AD)
2. **Pride → Humbling** (Babel, Nebuchadnezzar, Rome)
3. **Exile → Restoration** (Egypt, Babylon, modern Israel)
4. **Persecution → Growth** (Early church, underground movements)
5. **Unity → Fragmentation** (Divided Kingdom, Roman Empire, post-Westphalia)

---

### 4. Prophecy-Fulfillment Mapper

**Location**: `backend/app/prophecy/mapper.py` *(to be implemented)*

**Fulfillment Types**:
- **COMPLETE**: Fully and definitively fulfilled
- **PARTIAL**: Partially fulfilled, more may follow
- **REPEATED**: Pattern that recurs across eras
- **CONDITIONAL**: Fulfillment depends on response
- **PENDING**: Not yet fulfilled
- **SYMBOLIC**: Symbolic representation

**Example Mapping**:
```python
{
  "prophecy": "Daniel 2:31-45",
  "element": "Iron kingdom will be divided",
  "fulfillments": [
    {
      "event_id": 87,  # Fall of Western Rome (476 AD)
      "type": "PARTIAL",
      "confidence": 0.9
    },
    {
      "event_id": 92,  # Ongoing European fragmentation
      "type": "REPEATED",
      "confidence": 0.8
    }
  ]
}
```

---

### 5. Simulation Engine

**Location**: `backend/app/simulation/engine.py` *(to be implemented)*

**Process**:
1. **Input**: Current world indicators (political, economic, social, religious)
2. **Pattern Matching**: Identify historical analogs
3. **Trajectory Modeling**: Project conditional futures based on patterns
4. **Risk Assessment**: Calculate convergence of negative indicators
5. **Output**: Scenario trajectories (NOT date predictions)

**Example**:
```python
{
  "scenario_name": "Elite Overproduction + Moral Decay",
  "matched_patterns": ["pride_precedes_fall", "elite_conflict"],
  "historical_analogs": [
    {"event": "Fall of Rome", "similarity_score": 0.75},
    {"event": "French Revolution", "similarity_score": 0.68}
  ],
  "trajectory": {
    "near_term": "institutional_delegitimization",
    "mid_term": "social_fragmentation",
    "long_term": ["collapse", "radical_restructuring"]
  },
  "confidence": 0.65
}
```

---

### 6. Insight Layer

**Purpose**: Generate explanations grounded in historical precedent

**Location**: `backend/app/insights/` *(to be implemented)*

**Output Format**:
```json
{
  "query": "What happens when empires abandon moral foundations?",
  "historical_precedent": [
    {
      "event": "Fall of Rome",
      "year": 476,
      "mechanism": "moral_decay + military_overextension",
      "duration_years": 200
    }
  ],
  "pattern": "moral_decay_judgment",
  "explanation": "Historical record shows 100% correlation between sustained moral decay and eventual collapse across 12 major civilizations.",
  "current_indicators": {...}
}
```

---

## API Layer

**Framework**: FastAPI

**Why FastAPI?**
- Automatic OpenAPI documentation
- Pydantic validation
- Async support
- Type safety

**Endpoint Structure**:
```
/api/v1/
├── /chronology
│   ├── /events
│   ├── /events/{id}
│   ├── /events/{id}/contemporaneous
│   └── /summary
├── /patterns
│   ├── /
│   └── /{id}/instances
├── /prophecy
│   ├── /texts
│   └── /fulfillments
└── /simulation
    ├── /scenarios
    └── /run
```

---

## Deployment Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   Docker Compose                          │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │  PostgreSQL  │  │    Neo4j     │  │  FastAPI App   │ │
│  │   :5432      │  │  :7474/:7687 │  │    :8000       │ │
│  └──────────────┘  └──────────────┘  └────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

**Production Considerations**:
- Add Redis for caching
- Implement authentication (JWT)
- Rate limiting
- Database read replicas
- Load balancing

---

## Data Flow Example

**Query**: "What historical patterns preceded the Fall of Jerusalem in 586 BC?"

1. **API** receives request at `/api/v1/chronology/events/42`
2. **Chronology Engine** retrieves event from PostgreSQL
3. **Pattern Library** queries associated patterns via JOIN
4. **Neo4j Query** finds related pattern instances:
   ```cypher
   MATCH (e:Event {event_id: 42})-[:EXEMPLIFIES]->(p:Pattern)
   MATCH (p)<-[:EXEMPLIFIES]-(other:Event)
   WHERE other.year < -586
   RETURN other, p
   ```
5. **Insight Generator** synthesizes explanation
6. **API** returns structured response

---

## Security Considerations

### Current State (Development)
- Open API
- Local database access
- No authentication

### Production Requirements
- API key authentication
- Role-based access control (RBAC)
- Rate limiting per user
- Input sanitization
- SQL injection prevention (handled by SQLAlchemy)
- XSS protection (handled by FastAPI)

---

## Extensibility

### Adding New Data
- **Biblical Events**: Update `data/seed/biblical_timeline.py`
- **Historical Events**: Update `data/seed/historical_continuation.py`
- **Patterns**: Add to `patterns/` module
- **Prophecies**: Seed via API or direct DB

### Adding New Modules
- Follow existing structure: `app/<module_name>/`
- Create router in `app/api/routes/<module_name>.py`
- Register router in `app/main.py`

---

## Testing Strategy

- **Unit Tests**: Core logic (chronology engine, pattern matching)
- **Integration Tests**: API endpoints
- **Graph Tests**: Neo4j relationship integrity
- **Data Tests**: Seed data validation

**Run tests**:
```bash
cd backend
pytest
```

---

## Performance Considerations

### Database Optimization
- Indexes on frequently queried columns (year_start, era, event_type)
- JSONB for flexible metadata without schema bloat
- Connection pooling (SQLAlchemy default: 10)

### Query Optimization
- Limit result sets (default: 100, max: 1000)
- Use year ranges instead of full table scans
- Cache frequently accessed data (future: Redis)

### Graph Queries
- Use indexed properties for entry points
- Limit traversal depth
- Profile queries with `EXPLAIN`

---

## Monitoring & Observability

*To be implemented:*
- Prometheus metrics
- Grafana dashboards
- API response time tracking
- Database query performance
- Error rate monitoring

---

## Future Enhancements

1. **Vector Database** for semantic prophecy similarity
2. **Machine Learning** for pattern prediction confidence
3. **LLM Integration** for narrative synthesis
4. **Geospatial Layer** for empire territory visualization
5. **Timeline Visualization** with D3.js
6. **Export Functionality** (PDF reports, CSV datasets)
