# Scripts Directory

All utility scripts for the Sigandwa system.

## 🚀 Setup Scripts

- `setup.sh` - Main system setup (run first)
- `setup_database.py` - Initialize PostgreSQL schema
- `setup_llm.sh` - Install LLM components
- `setup_llm_cpu.sh` - CPU-only LLM setup
- `setup_llm_venv.sh` - Create LLM virtual environment

## ▶️ System Control

- `start_system.sh` - Start all services
- `stop_system.sh` - Stop all services

## 📊 Data Management

- `import_ussher_data.py` - Import Ussher Annals chronology
- `generate_training_data.py` - Generate LLM training datasets
- `parse_ussher_annals.py` - Parse Ussher source text
- `seed_indicators.py` - Seed indicator data
- `seed_prophecy_data.py` - Seed prophecy data

## 🔗 Graph Database

- `link_patterns.py` - Link pattern relationships
- `link_prophecies.py` - Link prophecy relationships

## 🧪 Testing

- `test_system.py` - System integration tests
- `test_system_status.py` - Quick health check
- `test_llm.sh` - Test LLM functionality
- `verify_integration.sh` - Verify biblical source integration

## 🎬 Demos

- `demo_phase4.sh` - Phase 4 demonstration
- `demo_phase5_graph.sh` - Phase 5 graph demonstration

## Usage

All scripts should be run from the project root:

```bash
# From project root
cd ~/Desktop/WAZI\ LABS\ AFRICA/sigandwa

# Run any script
./scripts/verify_integration.sh
python3 scripts/generate_training_data.py
```
