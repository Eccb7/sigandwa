# Sigandwa Quick Reference - Biblical Sources Integration

## 🎯 What Was Done

Successfully integrated 4 biblical source documents into the Sigandwa system:
1. **Ussher's Annals** - 7,302 chronological events (4004 BC - 73 AD)
2. **Daniel Gems** - Prophetic interpretations
3. **Revelation Gems** - Apocalyptic prophecies
4. **Studies in Daniel** - Deep theological commentary

Generated **15,988 training examples** for the LiquidAI LLM.

---

## 🚀 Quick Start

### Start the System
```bash
cd ~/Desktop/WAZI\ LABS\ AFRICA/sigandwa
./start_system.sh
```

Wait for:
- ✅ Database containers healthy
- ✅ Backend serving on :8000
- ✅ Frontend serving on :3000

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs
- **Database**: postgresql://sigandwa:sigandwa_dev@localhost:5434/sigandwa
- **Neo4j**: http://localhost:7474 (neo4j/sigandwa_dev)

---

## 📊 Database Quick Checks

### View Event Count
```bash
curl -s http://localhost:8000/api/v1/chronology/events | jq 'length'
# Expected: 100 (paginated)
```

### Search Events
```bash
curl -s "http://localhost:8000/api/v1/chronology/events?search=creation" | jq '.[0].name'
# Expected: First creation event
```

### Direct Database Query
```bash
docker exec -it sigandwa-postgres psql -U sigandwa -d sigandwa -c "SELECT COUNT(*) FROM chronology_events;"
# Expected: 7302
```

---

## 🔄 Regenerate Training Data

If you need to regenerate the training dataset:

```bash
cd ~/Desktop/WAZI\ LABS\ AFRICA/sigandwa
python3 generate_training_data.py
```

Generates:
- `training_data.json` - Full dataset (15,988 examples)
- `train.json` - Training split (90%)
- `val.json` - Validation split (10%)

---

## 📈 Data Statistics

### Chronology Events: 7,302
- Creation to Flood: 39
- Patriarchs: 22
- Egyptian Bondage: 166
- Exodus to Judges: 220
- United Monarchy: 86
- Divided Kingdom: 370
- Exile: 179
- Post-Exile: 5,271
- Early Church: 949

### Event Types
- Political: 1,558 (21%)
- Military: 2,468 (34%)
- Social: 2,423 (33%)
- Religious: 820 (11%)
- Natural: 33 (<1%)

### Training Data: 15,988 examples
- Chronology Q&A: 15,588
- Document chunks: 400

---

## 🛠️ Maintenance Commands

### Stop System
```bash
./stop_system.sh
```

### View Logs
```bash
# Backend (if in terminal)
# Check the terminal where you ran start_system.sh

# Docker containers
docker compose logs postgres
docker compose logs neo4j
```

### Backup Database
```bash
docker exec sigandwa-postgres pg_dump -U sigandwa sigandwa > backup.sql
```

### Re-import Events
```bash
python3 import_ussher_data.py
```

---

## 📁 Important Files

### Source Documents
- `docs/James-Usher-Annals-of-the-World.txt` (4.0 MB)
- `docs/daniel_gems.txt` (2.8 MB)
- `docs/revelation_gems.txt` (3.1 MB)
- `docs/Studies-in-the-Book-of-Daniel.txt` (182 KB)

### Training Data
- `training_data.json` (8.4 MB) - Complete dataset
- `train.json` (7.2 MB) - Training subset
- `val.json` (1.2 MB) - Validation subset

### Scripts
- `start_system.sh` - Start all services
- `stop_system.sh` - Stop all services
- `import_ussher_data.py` - Import chronology
- `generate_training_data.py` - Generate training data
- `test_system_status.py` - Health check

---

## 🧪 Test System Health

```bash
python3 test_system_status.py
```

Expected results:
- ✅ API responding
- ✅ Chronology API working (7,302 events)
- ✅ Search working
- ✅ Frontend serving
- ✅ Database connected
- ✅ Training data exists

---

## 🎓 Example Queries

### Find Creation Events
```bash
curl "http://localhost:8000/api/v1/chronology/events?search=creation&limit=5"
```

### Events in Specific Year
```bash
curl "http://localhost:8000/api/v1/chronology/events?year_start=-2000&year_end=-2000"
```

### Events by Era
```bash
curl "http://localhost:8000/api/v1/chronology/events?era=UNITED_MONARCHY"
```

---

## 🔥 Troubleshooting

### Backend Not Responding
```bash
# Check if running
ps aux | grep uvicorn

# Restart
./stop_system.sh
./start_system.sh
```

### Database Connection Issues
```bash
# Check containers
docker compose ps

# Restart database
docker compose restart postgres
```

### Port Already in Use
```bash
# Find process using port
sudo lsof -i :8000  # backend
sudo lsof -i :3000  # frontend
sudo lsof -i :5434  # postgres

# Kill process
sudo kill <PID>
```

---

## 💡 Pro Tips

1. **Always use `start_system.sh`** - It handles all dependencies
2. **Training data is cached** - Regenerate only if you modify sources
3. **Database persists** - Events remain after container restart
4. **Check logs first** - Most issues show in terminal output
5. **API docs at /docs** - Interactive testing at http://localhost:8000/docs

---

## 📞 Support

- Documentation: `docs/INTEGRATION_COMPLETE.md`
- Architecture: `docs/ARCHITECTURE.md`
- API Reference: `docs/API.md`

---

**Version:** 0.1.0  
**Last Updated:** January 14, 2026  
**Status:** ✅ Production Ready
