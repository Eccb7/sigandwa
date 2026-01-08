# Sigandwa: Biblical Cliodynamic Analysis System

A platform for analyzing civilizational patterns through Biblical chronology and historical continuation, enabling conditional trajectory simulation based on millennia of precedent.

## System Purpose

- Uses Biblical historical record and prophetic texts as primary dataset
- Treats Biblical chronology as continuous, authoritative timeline (Creation → Present)
- Identifies recurring civilizational, geopolitical, and institutional patterns
- Simulates conditional future trajectories without date-setting or speculation

## Core Principles

- Prophecy treated as conditional historical projection
- Explicit cause-effect modeling
- No hard predictions; only scenario trajectories and risk convergence
- No theology, belief enforcement, or modern ideology injection

## Architecture

### Backend (`backend/`)
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Data Validation**: Pydantic

### Databases
- **PostgreSQL**: Chronological timeline, events, patterns
- **Neo4j**: Empire relationships, prophecy-fulfillment graphs

### Frontend (`frontend/`)
- **Framework**: Next.js
- **Visualization**: D3.js

## Modules

1. **Chronology Engine** — Unified timeline with uncertainty ranges
2. **Event Ontology** — Normalized Biblical and historical events
3. **Pattern Library** — Rise, decline, collapse, recapitulation templates
4. **Prophecy-Fulfillment Mapper** — Links prophetic texts to historical outcomes
5. **Simulation Engine** — Conditional trajectory modeling
6. **Insight Layer** — Explanations grounded in historical precedent

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Node.js 18+ (for frontend)

### Setup

```bash
# Clone repository
git clone git@github.com:Eccb7/sigandwa.git
cd sigandwa

# Start databases
docker-compose up -d

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start API server
uvicorn app.main:app --reload

# Setup frontend (in separate terminal)
cd frontend
npm install
npm run dev
```

### API Documentation

Once running, visit:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Project Status

**Phase 1: Foundation & Chronology Engine** (✅ Complete)
- ✅ Project structure and infrastructure
- ✅ PostgreSQL + Neo4j database schemas
- ✅ Chronology Engine with uncertainty handling
- ✅ FastAPI with documented endpoints
- ✅ Biblical timeline (96 events, Creation → Present)
- ✅ Alembic migrations
- ✅ Comprehensive documentation
- ✅ Testing framework
- ✅ Setup automation

**Phase 2: Pattern Recognition & Analytics** (✅ Complete)
- ✅ Pattern library implementation (6 biblical patterns)
- ✅ Historical analog matching
- ✅ Event correlation analysis
- ✅ Pattern detection and linking (5 instances)
- ✅ Pattern analysis API endpoints

**Phase 3: Prophecy-Fulfillment Mapping** (✅ Complete)
- ✅ Prophecy text ingestion (6 core prophecies)
- ✅ Fulfillment type classification
- ✅ Confidence scoring (95-98%)
- ✅ Multi-era fulfillment tracking (7 fulfillments)
- ✅ Prophecy analysis API endpoints

**Phase 4: Simulation & Projection Engine** (✅ Complete)
- ✅ Conditional trajectory modeling
- ✅ Risk vector calculation (25 world indicators)
- ✅ Historical analog weighting
- ✅ Scenario generation
- ✅ Precondition detection
- ✅ Prophetic timeline analysis

**Phase 5: Graph Analysis & Network Visualization** (✅ Complete)
- ✅ Neo4j integration module (470 lines)
- ✅ Graph synchronization engine
- ✅ Network analysis algorithms (11 endpoints)
- ✅ Event chain discovery
- ✅ Pattern evolution tracking
- ✅ Prophecy network mapping
- ✅ Shortest path analysis
- ✅ Custom Cypher query support

**Phase 6: Frontend Application & Dashboard** (✅ Complete)
- ✅ Next.js 14 application setup (472 packages)
- ✅ Complete API integration layer (43 endpoints)
- ✅ TypeScript type system (150+ lines)
- ✅ Responsive navigation (desktop + mobile)
- ✅ Dashboard with statistics and risk assessment
- ✅ Timeline visualization (96 events)
- ✅ Pattern analysis page with modal details
- ✅ Prophecy fulfillment tracker with networks
- ✅ Simulation dashboard with indicators
- ✅ Graph network explorer with path finder
- ✅ Real-time data with React Query caching

## Data Summary

### Timeline Coverage
- **Biblical Era**: -4004 (Creation) → 2025 (Present)
- **Total Events**: 96 chronological events
- **Eras Covered**: 18 distinct chronological periods

### Key Datasets
1. **Creation → Flood** (-4004 to -2348) — Foundational events
2. **Patriarchs** (-1921 to -1706) — Abraham through Jacob's migration
3. **Exodus & Conquest** (-1491 to -1426) — Deliverance and settlement
4. **United Monarchy** (-1095 to -975) — Saul, David, Solomon
5. **Divided Kingdom** (-975 to -586) — Israel and Judah
6. **Exile & Restoration** (-605 to -445) — Babylon, return, rebuilding
7. **New Testament** (4 BC - 70 AD) — Christ, early church, diaspora
8. **Modern Era** (1948-2025) — Israel restoration, contemporary events

### Pattern Library (6 Templates)
- **Moral Decay → Judgment**: Flood, Sodom (preconditions: moral_relativism, injustice)
- **Pride → Humbling**: Babel, Pharaoh, Nebuchadnezzar (typical duration: 40 years)
- **Exile → Restoration**: Babylonian exile → Return (duration: 2000 years)
- **Unity → Fragmentation**: Divided Kingdom, post-Babel dispersion
- **Persecution → Growth**: Early church under Rome (duration: 300 years)
- **Delayed Fulfillment**: Abraham → Isaac (25 years), prophecy fulfillments

### Graph Database (Neo4j)
- **108 Nodes**: 96 Events, 6 Patterns, 6 Prophecies
- **107 Relationships**: MATCHES_PATTERN (5), FULFILLED_BY (7), PRECEDED_BY (95)
- **Analysis**: Event chains, pattern evolution, prophecy networks, influence ranking
- **Performance**: Sub-200ms queries, 2.1 avg connections per event

## Documentation

- **[API Reference](docs/API.md)** — Endpoint documentation with examples
- **[Architecture](docs/ARCHITECTURE.md)** — System design and data flow
- **[Deployment Guide](docs/DEPLOYMENT.md)** — Setup, troubleshooting, production
- **[Contributing](CONTRIBUTING.md)** — Guidelines for contributions

## Technology Stack

**Backend**
- Python 3.11+ with FastAPI
- Pydantic for validation
- SQLAlchemy ORM
- Alembic migrations

**Databases**
- PostgreSQL 15 (timeline, events, patterns)
- Neo4j 5.15 (graph relationships)

**Testing**
- pytest with coverage
- SQLite for test database

**DevOps**
- Docker Compose
- Automated setup script

## Performance

- Chronology queries: <50ms for 1000 events
- Graph traversals: <100ms for multi-hop relationships
- API response time: <200ms (95th percentile)
- Database indexes: 8 on frequently queried fields

## Use Cases

1. **Historical Research** — Query events by era, type, or actor
2. **Pattern Analysis** — Identify recurring civilizational cycles
3. **Analog Discovery** — Find historical parallels to current events
4. **Timeline Visualization** — Generate interactive chronologies
5. **Prophecy Study** — Track fulfillment across eras
6. **Scenario Modeling** — Project conditional trajectories

## API Examples

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Get all events in the Exile period
response = requests.get(f"{BASE_URL}/chronology/events", params={"era": "EXILE"})
events = response.json()

# Find contemporaneous events (within 10 years)
response = requests.get(f"{BASE_URL}/chronology/events/42/contemporaneous")
related = response.json()

# Get timeline summary
response = requests.get(f"{BASE_URL}/chronology/summary")
summary = response.json()
print(f"Total events: {summary['total_events']}")
```

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code standards
- Data quality guidelines
- Pull request process
- Community guidelines

Focus areas:
- Historical accuracy
- Pattern identification
- Code quality
- Documentation

## Roadmap

**Q1 2026** (✅ Complete)
- ✅ Phase 1: Foundation & Chronology
- ✅ Phase 2: Pattern Recognition
- ✅ Phase 3: Prophecy-Fulfillment Mapping
- ✅ Phase 4: Simulation Engine
- ✅ Phase 5: Graph Analysis & Network Visualization

**Q2 2026** (✅ Complete)
- ✅ Phase 6: Frontend Dashboard (Next.js 14)
- ✅ Dashboard with statistics and risk visualization
- ✅ Timeline page with 96 events
- ✅ Pattern analysis with modal details
- ✅ Prophecy fulfillment tracker
- ✅ Simulation dashboard with indicators
- ✅ Graph network explorer

**Q3 2026** (Planned)
- D3.js interactive timeline (zoom, pan, scrubber)
- vis.js graph network visualization (108 nodes)
- Recharts statistical visualizations
- Advanced features (search, export, filtering)
- API authentication & authorization
- Performance optimization
- Mobile responsive enhancements

**Q4 2026** (Planned)
- Public beta release
- Documentation site
- Community contributions
- Tutorial videos

## Acknowledgments

- **James Ussher** — Chronology framework (Annals of the World, 1650)
- **Peter Turchin** — Cliodynamics methodology
- **Daniel's Prophecy** — Empire succession framework
- Open source community

## License

MIT — See [LICENSE](LICENSE) for details

## Contact

- **GitHub**: https://github.com/Eccb7/sigandwa
- **Issues**: https://github.com/Eccb7/sigandwa/issues
- **Discussions**: https://github.com/Eccb7/sigandwa/discussions

---

**Note**: This is an analytical platform, not a theological system. It models historical patterns without date-setting predictions or ideological interpretation.
