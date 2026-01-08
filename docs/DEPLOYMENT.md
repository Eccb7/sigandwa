# Deployment Guide

## Quick Start (Development)

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### One-Command Setup

```bash
./setup.sh
```

This script will:
1. Create Python virtual environment
2. Install dependencies
3. Start PostgreSQL and Neo4j containers
4. Run database migrations
5. Seed Biblical timeline data
6. Initialize Neo4j graph

### Manual Setup

If you prefer step-by-step:

```bash
# 1. Create .env file
cp .env.example .env

# 2. Start databases
docker-compose up -d

# 3. Setup Python environment
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Run migrations
alembic upgrade head

# 5. Seed data
cd ../data/seed
python seed_db.py
python init_neo4j.py

# 6. Start API server
cd ../../backend
uvicorn app.main:app --reload
```

---

## Access Points

Once running:

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
  - User: `sigandwa`
  - Password: `sigandwa_dev`
  - Database: `sigandwa`
- **Neo4j Browser**: http://localhost:7474
  - User: `neo4j`
  - Password: `sigandwa_dev`

---

## Verification

### Test API

```bash
# Health check
curl http://localhost:8000/health

# Get timeline summary
curl http://localhost:8000/api/v1/chronology/summary

# Query Biblical events
curl "http://localhost:8000/api/v1/chronology/events?era=EXILE&limit=5"
```

### Test Database

```bash
# PostgreSQL
docker exec -it sigandwa_postgres psql -U sigandwa -d sigandwa -c "SELECT COUNT(*) FROM chronology_events;"

# Neo4j
docker exec -it sigandwa_neo4j cypher-shell -u neo4j -p sigandwa_dev "MATCH (e:Empire) RETURN e.name, e.year_start;"
```

### Run Tests

```bash
cd backend
pytest
```

---

## Project Structure

```
sigandwa/
├── backend/
│   ├── app/
│   │   ├── api/              # API routes
│   │   ├── chronology/       # Chronology engine
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── config.py         # Configuration
│   │   ├── database.py       # PostgreSQL connection
│   │   ├── neo4j_db.py       # Neo4j connection
│   │   └── main.py           # FastAPI app
│   ├── tests/                # Test suite
│   ├── requirements.txt      # Python dependencies
│   └── alembic.ini           # Migration config
├── database/
│   └── migrations/           # Alembic migrations
├── data/
│   └── seed/                 # Seed data scripts
│       ├── biblical_timeline.py
│       ├── historical_continuation.py
│       ├── seed_db.py
│       └── init_neo4j.py
├── docs/                     # Documentation
│   ├── API.md
│   └── ARCHITECTURE.md
├── docker-compose.yml        # Database containers
├── setup.sh                  # Setup script
└── README.md
```

---

## Common Tasks

### Add New Biblical Events

1. Edit `data/seed/biblical_timeline.py`
2. Add event dictionary to `BIBLICAL_EVENTS` list
3. Run: `python data/seed/seed_db.py`

### Add Historical Events

1. Edit `data/seed/historical_continuation.py`
2. Add event to `HISTORICAL_CONTINUATION` list
3. Run: `python data/seed/seed_db.py`

### Query Chronology

```python
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.chronology.engine import ChronologyEngine

db = SessionLocal()
engine = ChronologyEngine(db)

# Get events in exile period
events = engine.get_events_in_range(-600, -500)
for event in events:
    print(f"{event.year_start}: {event.name}")
```

### Query Neo4j Graph

```cypher
// Find empire succession
MATCH path = (e1:Empire)-[:SUCCEEDED_BY*]->(e2:Empire)
RETURN e1.name, e2.name;

// Find patterns with most historical instances
MATCH (e:Event)-[:EXEMPLIFIES]->(p:Pattern)
RETURN p.name, COUNT(e) AS instances
ORDER BY instances DESC;
```

---

## Troubleshooting

### Database Connection Errors

**Problem**: Cannot connect to PostgreSQL/Neo4j

**Solution**:
```bash
# Check containers are running
docker-compose ps

# Check logs
docker-compose logs postgres
docker-compose logs neo4j

# Restart containers
docker-compose restart
```

### Migration Errors

**Problem**: Alembic migration fails

**Solution**:
```bash
# Reset database
docker-compose down -v
docker-compose up -d

# Wait for startup
sleep 10

# Run migrations
cd backend
alembic upgrade head
```

### Import Errors

**Problem**: Python module not found

**Solution**:
```bash
# Ensure virtual environment is activated
source backend/venv/bin/activate

# Reinstall dependencies
pip install -r backend/requirements.txt
```

### Port Conflicts

**Problem**: Port already in use

**Solution**:
Edit `docker-compose.yml` and change port mappings:
```yaml
ports:
  - "5433:5432"  # Change first number
```

---

## Environment Variables

Key variables in `.env`:

```bash
# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=sigandwa
POSTGRES_PASSWORD=sigandwa_dev
POSTGRES_DB=sigandwa

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=sigandwa_dev

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS (add frontend URL when ready)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

---

## Production Deployment

### Security Checklist

- [ ] Change all default passwords
- [ ] Generate secure `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure HTTPS/TLS
- [ ] Enable API authentication
- [ ] Set up rate limiting
- [ ] Configure CORS properly
- [ ] Use managed databases (RDS, Atlas, etc.)
- [ ] Set up monitoring (Prometheus, Grafana)
- [ ] Configure backups

### Docker Production Build

```dockerfile
# Dockerfile (create in backend/)
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t sigandwa-api ./backend
docker run -p 8000:8000 sigandwa-api
```

### Cloud Deployment Options

**AWS**:
- RDS (PostgreSQL)
- EC2 or ECS (API)
- Neo4j on EC2 or Aura

**Google Cloud**:
- Cloud SQL
- Cloud Run (API)
- Neo4j Aura

**Azure**:
- Azure Database for PostgreSQL
- Container Instances (API)
- Neo4j Aura

---

## Data Backup

### PostgreSQL Backup

```bash
# Backup
docker exec sigandwa_postgres pg_dump -U sigandwa sigandwa > backup.sql

# Restore
docker exec -i sigandwa_postgres psql -U sigandwa sigandwa < backup.sql
```

### Neo4j Backup

```bash
# Backup (requires Neo4j Enterprise or manual export)
docker exec sigandwa_neo4j neo4j-admin dump --database=neo4j --to=/tmp/neo4j-backup.dump

# Copy from container
docker cp sigandwa_neo4j:/tmp/neo4j-backup.dump ./neo4j-backup.dump
```

---

## Performance Tuning

### PostgreSQL

Edit `docker-compose.yml`:
```yaml
postgres:
  environment:
    POSTGRES_SHARED_BUFFERS: 256MB
    POSTGRES_WORK_MEM: 4MB
    POSTGRES_MAINTENANCE_WORK_MEM: 64MB
```

### Neo4j

Edit `docker-compose.yml`:
```yaml
neo4j:
  environment:
    NEO4J_dbms_memory_heap_max__size: 2G
    NEO4J_dbms_memory_pagecache_size: 1G
```

### API

Use Gunicorn with workers:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## Monitoring

### API Metrics

Add to `requirements.txt`:
```
prometheus-fastapi-instrumentator==6.1.0
```

In `app/main.py`:
```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

Access metrics: http://localhost:8000/metrics

### Database Monitoring

```bash
# PostgreSQL stats
docker exec sigandwa_postgres psql -U sigandwa -d sigandwa -c "SELECT * FROM pg_stat_activity;"

# Neo4j queries
# Access Neo4j Browser → Database Information → Queries
```

---

## Support & Documentation

- **API Docs**: http://localhost:8000/docs
- **Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **API Reference**: [docs/API.md](docs/API.md)
- **GitHub**: https://github.com/Eccb7/sigandwa

---

## Next Steps

1. **Implement Pattern Library** — Add pattern recognition module
2. **Build Simulation Engine** — Create trajectory modeling
3. **Add Frontend** — Next.js dashboard with D3.js visualizations
4. **Expand Data** — Add more historical events and patterns
5. **Implement Prophecy Mapper** — Link prophecies to fulfillments
6. **Add Authentication** — JWT-based API security
7. **Create Exports** — PDF reports, CSV datasets

---

## License

MIT

---

## Contributing

This is a research and analytical tool. Contributions should focus on:
- Historical accuracy
- Data integrity
- Pattern identification
- Code quality

Avoid:
- Theological speculation
- Date-setting predictions
- Ideological interpretation
