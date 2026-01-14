# Training Data

LLM training datasets for the Sigandwa Biblical Cliodynamic Analysis System.

## 📊 Files

- **training_data.json** (8.4 MB) - Complete dataset with 15,988 examples
- **train.json** (7.2 MB) - Training subset (14,389 examples, 90%)
- **val.json** (1.2 MB) - Validation subset (1,599 examples, 10%)

## 📚 Dataset Composition

### Chronology Q&A (15,588 examples)
Generated from 7,302 historical events:
- "What happened in [year]?" queries
- Event explanations
- Biblical source references
- Covers Creation (4004 BC) to Early Church (73 AD)

### Document Chunks (400 examples)
Extracted from biblical source texts:
- 100 chunks from Ussher's Annals
- 100 chunks from Daniel Gems
- 100 chunks from Revelation Gems
- 100 chunks from Studies in Daniel

## 🔄 Regeneration

To regenerate the training data:

```bash
cd ~/Desktop/WAZI\ LABS\ AFRICA/sigandwa
python3 scripts/generate_training_data.py
```

This will create fresh datasets in this directory based on current database state.

## 📖 Format

Each example follows the instruction-tuning format:

```json
{
  "instruction": "What happened in 4004 BC?",
  "input": "",
  "output": "In the beginning God created the heaven and the earth..."
}
```

## 🎯 Usage

These datasets are ready for:
- Fine-tuning LiquidAI LFM2-1.2B-RAG model
- Training custom biblical chronology models
- RAG (Retrieval Augmented Generation) systems
- Historical pattern recognition

---

**Generated:** January 14, 2026  
**Source Events:** 7,302  
**Total Examples:** 15,988
