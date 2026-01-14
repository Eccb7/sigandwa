#!/bin/bash
# Move training data files
mv training_data.json train.json val.json data/training/ 2>/dev/null

# Move scripts
mv demo_phase4.sh demo_phase5_graph.sh scripts/ 2>/dev/null
mv generate_training_data.py import_ussher_data.py scripts/ 2>/dev/null
mv link_patterns.py link_prophecies.py scripts/ 2>/dev/null
mv parse_ussher_annals.py seed_indicators.py seed_prophecy_data.py scripts/ 2>/dev/null
mv setup_database.py test_system.py test_system_status.py scripts/ 2>/dev/null
mv verify_integration.sh scripts/ 2>/dev/null
mv alembic.ini database/ 2>/dev/null

# Move LLM setup scripts
mv setup_llm.sh setup_llm_cpu.sh setup_llm_venv.sh test_llm.sh scripts/ 2>/dev/null

echo "✅ Cleanup complete!"
echo ""
echo "📁 New structure:"
echo "  • data/training/ - Training datasets (3 files)"
echo "  • scripts/ - All executable scripts (17 files)"
echo "  • Root stays clean with only essential files"
