# Sigandwa Quick Start

Get the Biblical Cliodynamic Analysis System running in **under 5 minutes**.

---

## Prerequisites

Ensure you have:
- Python 3.11+
- Docker & Docker Compose
- Git

---

## Installation

```bash
# Clone repository
git clone git@github.com:Eccb7/sigandwa.git
cd sigandwa

# Run automated setup
./setup.sh
```

This will:
1. Create Python virtual environment
2. Install all dependencies
3. Start PostgreSQL and Neo4j containers
4. Run database migrations
5. Seed 170+ historical events
6. Initialize graph relationships

**Wait time**: ~3-4 minutes (first run)

---

## Start API Server

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

**API Running**: http://localhost:8000  
**Interactive Docs**: http://localhost:8000/docs

---

## First Queries

### 1. Health Check
```bash
curl http://localhost:8000/health
```

**Response**:
```json
{"status": "healthy", "version": "0.1.0"}
```

---

### 2. Timeline Summary
```bash
curl http://localhost:8000/api/v1/chronology/summary
```

**Response**:
```json
{
  "total_events": 170,
  "era_distribution": {
    "EXILE": 9,
    "UNITED_MONARCHY": 11,
    "NEW_TESTAMENT": 15,
    ...
  },
  "type_distribution": {
    "POLITICAL": 45,
    "RELIGIOUS": 60,
    "MILITARY": 40,
    ...
  },
  "year_range": {
    "start": -4004,
    "end": 2023
  }
}
```

---

### 3. Query Biblical Events
```bash
curl "http://localhost:8000/api/v1/chronology/events?era=EXILE&limit=3"
```

**Response**:
```json
[
  {
    "id": 55,
    "name": "First Babylonian Siege",
    "description": "Nebuchadnezzar besieges Jerusalem; Daniel taken captive",
    "year_start": -605,
    "year_end": null,
    "era": "EXILE",
    "event_type": "MILITARY",
    "biblical_source": "Daniel 1:1-6",
    "metadata": {
      "first_wave_exile": true,
      "daniel_ministry_begins": true
    }
  },
  ...
]
```

---

### 4. Find Events Around 586 BC
```bash
curl "http://localhost:8000/api/v1/chronology/events?year_start=-600&year_end=-570"
```

**Returns**: Fall of Jerusalem, Ezekiel's visions, etc.

---

### 5. Interactive Documentation

Visit: http://localhost:8000/docs

- Browse all endpoints
- Try queries in the browser
- See request/response schemas
- No Postman needed!

---

## Python Client

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Get all New Testament events
response = requests.get(
    f"{BASE_URL}/chronology/events",
    params={"era": "NEW_TESTAMENT"}
)
events = response.json()

for event in events:
    print(f"{event['year_start']} AD: {event['name']}")

# Output:
# -4 AD: Birth of Jesus Christ
# 27 AD: Baptism of Jesus
# 30 AD: Crucifixion and Resurrection
# 30 AD: Pentecost
# ...
```

---

## Database Access

### PostgreSQL
```bash
# Connect to database
docker exec -it sigandwa_postgres psql -U sigandwa -d sigandwa

# Example queries
SELECT name, year_start, era FROM chronology_events WHERE era = 'UNITED_MONARCHY';
SELECT COUNT(*) FROM chronology_events GROUP BY event_type;
```

### Neo4j
Visit: http://localhost:7474

**Username**: `neo4j`  
**Password**: `sigandwa_dev`

**Example Cypher Query**:
```cypher
// Find empire succession
MATCH (e1:Empire)-[:SUCCEEDED_BY]->(e2:Empire)
RETURN e1.name AS from_empire, e2.name AS to_empire, e1.year_end AS year;
```

---

## Common Queries

### Find Contemporaneous Events
```bash
# Find events around the same time as event ID 42
curl "http://localhost:8000/api/v1/chronology/events/42/contemporaneous?window_years=10"
```

### Filter by Event Type
```bash
# Get all military events
curl "http://localhost:8000/api/v1/chronology/events?event_type=MILITARY&limit=5"
```

### Query Historical Continuation
```bash
# Get modern era events
curl "http://localhost:8000/api/v1/chronology/events?era=MODERN"
```

---

## Verify Installation

Run tests:
```bash
cd backend
pytest
```

**Expected**: All tests pass ✅

---

## Troubleshooting

### Docker containers won't start
```bash
# Check if ports are available
docker-compose ps

# Restart containers
docker-compose restart

# View logs
docker-compose logs postgres
docker-compose logs neo4j
```

### API won't start
```bash
# Ensure virtual environment is activated
source backend/venv/bin/activate

# Check dependencies
pip install -r backend/requirements.txt

# Check database connection
python -c "from app.database import engine; print(engine.connect())"
```

### Database empty
```bash
# Reseed database
cd data/seed
python seed_db.py
```

---

## Next Steps

1. **Explore API**: http://localhost:8000/docs
2. **Read Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
3. **Check API Reference**: [docs/API.md](docs/API.md)
4. **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Stop Services

```bash
# Stop API
Ctrl+C in terminal

# Stop databases
docker-compose down

# Stop and remove data
docker-compose down -v  # ⚠️ Removes all data
```

---

## Key Resources

- **Documentation**: `docs/` directory
- **Seed Data**: `data/seed/`
- **API Routes**: `backend/app/api/routes/`
- **Models**: `backend/app/models/`
- **Tests**: `backend/tests/`

---

## Support

- **Issues**: https://github.com/Eccb7/sigandwa/issues
- **Discussions**: https://github.com/Eccb7/sigandwa/discussions
- **Docs**: Read [DEPLOYMENT.md](docs/DEPLOYMENT.md) for comprehensive guide

---

**You're now running a Biblical Cliodynamic Analysis System!** 🎉

Query the timeline, explore patterns, and discover historical analogs across millennia of recorded history.
