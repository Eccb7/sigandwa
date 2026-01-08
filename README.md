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
- ✅ Biblical timeline (130+ events, Creation → 70 AD)
- ✅ Historical continuation (40+ events, Roman Empire → Contemporary)
- ✅ Alembic migrations
- ✅ Neo4j graph initialization (Daniel's empire succession)
- ✅ Comprehensive documentation
- ✅ Testing framework
- ✅ Setup automation

**Phase 2: Pattern Recognition & Analytics** (Next)
- Pattern library implementation
- Historical analog matching
- Event correlation analysis
- Pattern recapitulation tracking

**Phase 3: Prophecy-Fulfillment Mapping** (Planned)
- Prophecy text ingestion
- Fulfillment type classification
- Confidence scoring
- Multi-era fulfillment tracking

**Phase 4: Simulation & Projection** (Planned)
- Conditional trajectory modeling
- Risk vector calculation
- Historical analog weighting
- Scenario generation

**Phase 5: Visualization & Frontend** (Planned)
- Next.js dashboard
- D3.js interactive timeline
- Geopolitical overlays (Mapbox)
- Pattern visualization

## Data Summary

### Timeline Coverage
- **Biblical Era**: 4004 BC (Creation) → 70 AD (Fall of Jerusalem)
- **Historical Continuation**: 70 AD → 2023 (Present)
- **Total Events**: 170+ (130 Biblical, 40+ Historical)
- **Eras Covered**: 18 distinct chronological periods

### Key Datasets
1. **Creation → Flood** (4004-2348 BC) — 4 foundational events
2. **Patriarchs** (1921-1706 BC) — Abraham through Jacob's migration
3. **Exodus & Conquest** (1491-1426 BC) — Deliverance and settlement
4. **United Monarchy** (1095-975 BC) — Saul, David, Solomon
5. **Divided Kingdom** (975-586 BC) — Israel and Judah
6. **Exile & Restoration** (605-445 BC) — Babylon, return, rebuilding
7. **New Testament** (4 BC - 70 AD) — Christ, early church, diaspora
8. **Post-Biblical** (313-2023 AD) — Constantine → Contemporary

### Pattern Examples
- **Moral Decay → Judgment**: Flood, Sodom, Jerusalem 586 BC, Jerusalem 70 AD
- **Pride → Humbling**: Babel, Nebuchadnezzar, Rome
- **Exile → Restoration**: Egypt, Babylon, Modern Israel (1948)
- **Unity → Fragmentation**: Divided Kingdom, Roman Empire, Post-Westphalia
- **Persecution → Growth**: Early church, underground movements

### Graph Relationships
- **Empire Succession**: Babylon → Persia → Greece → Rome → Divided Rome
- **Pattern Instances**: Historical events linked to recurring patterns
- **Prophetic Framework**: Daniel's four kingdoms with fulfillments

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

**Q1 2026**
- ✅ Phase 1 complete
- Pattern library implementation
- Prophecy mapper MVP

**Q2 2026**
- Simulation engine
- Frontend dashboard alpha
- API authentication

**Q3 2026**
- D3.js timeline visualization
- Export functionality (PDF, CSV)
- Performance optimization

**Q4 2026**
- Public beta
- Documentation site
- Community contributions

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
