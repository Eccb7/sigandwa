#!/usr/bin/env python3
"""
Generate LLM training dataset from biblical sources
"""
import sys
import json
from pathlib import Path

# Add backend to path (script now in scripts/ subdirectory)
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.chronology import ChronologyEvent
from app.models.prophecy import ProphecyText
from app.config import settings

# Create database engine
engine = create_engine(settings.postgres_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def prepare_training_data():
    """Prepare training dataset from multiple sources"""
    training_data = []
    
    # 1. Chronology Q&A pairs
    print("📚 Loading chronology events...")
    db = SessionLocal()
    
    try:
        events = db.query(ChronologyEvent).all()
        print(f"   Found {len(events)} chronology events")
        
        for event in events:
            year_display = f"{abs(event.year_start)} {'BC' if event.year_start < 0 else 'AD'}"
            
            # Create Q&A pairs
            training_data.append({
                "instruction": f"What happened in {year_display}?",
                "input": "",
                "output": f"{event.name}. {event.description or 'No additional details available.'}" + (
                    f" Biblical source: {event.biblical_source}" if event.biblical_source else ""
                )
            })
            
            training_data.append({
                "instruction": f"Explain the event: {event.name}",
                "input": "",
                "output": f"In {year_display}, {event.description or event.name}" + (
                    f" This is recorded in {event.biblical_source}." if event.biblical_source else ""
                )
            })
            
            if event.biblical_source:
                training_data.append({
                    "instruction": f"What Biblical event is recorded in {event.biblical_source}?",
                    "input": "",
                    "output": f"{event.name}. {event.description or 'This event occurred in ' + year_display}"
                })
        
        print(f"✅ Generated {len(training_data)} training examples from chronology")
        
        # 2. Prophecy interpretations (skip if table doesn't exist)
        print("🔮 Loading prophecies...")
        try:
            prophecies = db.query(ProphecyText).all()
            print(f"   Found {len(prophecies)} prophecies")
            
            for prophecy in prophecies:
                training_data.append({
                    "instruction": f"Interpret the prophecy: {prophecy.text[:200]}",
                    "input": f"Biblical reference: {prophecy.biblical_reference}",
                    "output": prophecy.interpretation_notes or prophecy.text[:300]
                })
        except Exception as e:
            print(f"   ⚠️  Skipping prophecies (table not yet created): {e}")
        
        print(f"✅ Total training examples from database: {len(training_data)}")
        
    finally:
        db.close()
    
    # 3. Add PDF text chunks (for context understanding)
    print("📄 Processing Biblical text documents...")
    pdf_files = [
        "./docs/James-Usher-Annals-of-the-World.txt",
        "./docs/daniel_gems.txt",
        "./docs/revelation_gems.txt",
        "./docs/Studies-in-the-Book-of-Daniel.txt"
    ]
    
    for pdf_file in pdf_files:
        pdf_path = Path(__file__).parent.parent / pdf_file  # Adjust for scripts/ location
        if not pdf_path.exists():
            print(f"  ⚠️  Skipping {pdf_path.name} (not found)")
            continue
        
        print(f"  Processing {pdf_path.name}...")
        
        try:
            with open(pdf_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Split into chunks (every 1000 characters)
            chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
            
            for i, chunk in enumerate(chunks[:100]):  # Limit to 100 chunks per file
                # Create summarization tasks
                training_data.append({
                    "instruction": "Summarize this Biblical historical text:",
                    "input": chunk,
                    "output": chunk[:200] + "..."  # Simple truncation for now
                })
            
            print(f"    ✅ Added {min(100, len(chunks))} examples from {pdf_path.name}")
        except Exception as e:
            print(f"    ❌ Error processing {pdf_path.name}: {e}")
    
    print(f"\n✅ Final dataset: {len(training_data)} examples")
    
    return training_data


def save_training_dataset(output_path: str = "./data/training/training_data.json"):
    """Generate and save training dataset"""
    print("🚀 Preparing training dataset...")
    print("=" * 70)
    
    data = prepare_training_data()
    
    output_file = Path(__file__).parent.parent / output_path  # Adjust for scripts/ location
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Save complete dataset
    print(f"\n💾 Saving datasets...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(data)} training examples to {output_file}")
    
    # Split into train/val
    train_size = int(len(data) * 0.9)
    train_data = data[:train_size]
    val_data = data[train_size:]
    
    train_file = output_file.parent / "train.json"
    val_file = output_file.parent / "val.json"
    
    with open(train_file, 'w', encoding='utf-8') as f:
        json.dump(train_data, f, indent=2, ensure_ascii=False)
    
    with open(val_file, 'w', encoding='utf-8') as f:
        json.dump(val_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Split: {len(train_data)} train, {len(val_data)} validation")
    
    print("\n" + "=" * 70)
    print("📊 Training Data Summary")
    print("=" * 70)
    print(f"   Total examples: {len(data)}")
    print(f"   Training set: {len(train_data)}")
    print(f"   Validation set: {len(val_data)}")
    print(f"\n📁 Files generated:")
    print(f"   - {output_file} (all data)")
    print(f"   - {train_file} (90% for training)")
    print(f"   - {val_file} (10% for validation)")
    print("=" * 70)


if __name__ == "__main__":
    save_training_dataset()
    print("\n✅ Training data preparation complete!")
