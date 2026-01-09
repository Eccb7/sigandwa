"""
Fine-tuning script for Biblical corpus
Prepares training data from database and documents
"""
import json
from pathlib import Path
from typing import List, Dict
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.chronology import ChronologyEvent
from ..models.prophecy import Prophecy
from .config import TrainingConfig


def prepare_training_data() -> List[Dict]:
    """
    Prepare training dataset from multiple sources:
    1. Chronology events (7,440+ events)
    2. Prophecies and fulfillments
    3. PDF text extracts (Ussher, Daniel, Revelation)
    """
    training_data = []
    config = TrainingConfig()
    
    # 1. Chronology Q&A pairs
    print("📚 Loading chronology events...")
    db: Session = SessionLocal()
    
    try:
        events = db.query(ChronologyEvent).all()
        
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
        
        # 2. Prophecy interpretations
        print("🔮 Loading prophecies...")
        prophecies = db.query(Prophecy).all()
        
        for prophecy in prophecies:
            training_data.append({
                "instruction": f"Interpret the prophecy: {prophecy.description}",
                "input": f"Biblical reference: {prophecy.biblical_reference}",
                "output": prophecy.interpretation or prophecy.description
            })
        
        print(f"✅ Total training examples: {len(training_data)}")
        
    finally:
        db.close()
    
    # 3. Add PDF text chunks (for context understanding)
    print("📄 Processing PDF extracts...")
    pdf_data = _process_pdf_extracts(config)
    training_data.extend(pdf_data)
    
    print(f"✅ Final dataset: {len(training_data)} examples")
    
    return training_data


def _process_pdf_extracts(config: TrainingConfig) -> List[Dict]:
    """Process PDF text files into training examples"""
    examples = []
    
    # Process each PDF file
    for pdf_file in [config.ussher_annals, config.daniel_gems, config.revelation_gems]:
        pdf_path = Path(pdf_file)
        if not pdf_path.exists():
            print(f"  ⚠️  Skipping {pdf_path.name} (not found)")
            continue
        
        print(f"  Processing {pdf_path.name}...")
        
        with open(pdf_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Split into chunks (every 1000 characters)
        chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
        
        for i, chunk in enumerate(chunks[:100]):  # Limit to 100 chunks per file
            # Create summarization tasks
            examples.append({
                "instruction": "Summarize this Biblical historical text:",
                "input": chunk,
                "output": chunk[:200] + "..."  # Simple truncation for now
            })
    
    return examples


def save_training_dataset(output_path: str = "./training_data.json"):
    """Generate and save training dataset"""
    print("🚀 Preparing training dataset...")
    data = prepare_training_data()
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(data)} training examples to {output_file}")
    
    # Split into train/val
    train_size = int(len(data) * 0.9)
    train_data = data[:train_size]
    val_data = data[train_size:]
    
    train_file = output_file.parent / "train.json"
    val_file = output_file.parent / "val.json"
    
    with open(train_file, 'w') as f:
        json.dump(train_data, f, indent=2, ensure_ascii=False)
    
    with open(val_file, 'w') as f:
        json.dump(val_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Split: {len(train_data)} train, {len(val_data)} validation")
    print(f"\n📊 Training data ready!")
    print(f"   Total examples: {len(data)}")
    print(f"   Train: {len(train_data)}")
    print(f"   Validation: {len(val_data)}")


if __name__ == "__main__":
    # Prepare dataset
    save_training_dataset()
    print("\n✅ Training data preparation complete!")
    print("   Files generated:")
    print("   - training_data.json (all data)")
    print("   - train.json (90% for training)")
    print("   - val.json (10% for validation)")
