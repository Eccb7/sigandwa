#!/usr/bin/env python3
"""
Generate training dataset from Biblical corpus and database
Run this script to prepare data for fine-tuning
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from app.llm.fine_tune import prepare_training_data
from app.llm.config import TrainingConfig
import json

def main():
    config = TrainingConfig()
    output_dir = Path(config.data_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("  Biblical Corpus Training Data Generator")
    print("=" * 70)
    print()
    
    print("📚 Collecting training data from:")
    print(f"   - Chronology Database (7,440+ events)")
    print(f"   - Prophecy Database")
    print(f"   - Biblical documents (Ussher, Daniel, Revelation)")
    print()
    
    # Generate training data
    training_data = prepare_training_data()
    
    # Save to JSON
    output_file = output_dir / "biblical_corpus.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Generated {len(training_data)} training examples")
    print(f"📁 Saved to: {output_file}")
    print(f"📊 File size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")
    print()
    
    # Statistics
    instruction_types = {}
    for item in training_data:
        instruction = item.get('instruction', '').split()[0]
        instruction_types[instruction] = instruction_types.get(instruction, 0) + 1
    
    print("📈 Training Data Statistics:")
    for inst_type, count in sorted(instruction_types.items(), key=lambda x: -x[1]):
        print(f"   {inst_type}: {count} examples")
    
    print()
    print("🎯 Next Steps:")
    print("   1. Review the generated data in:", output_file)
    print("   2. Add custom documents to docs/ folder")
    print("   3. Use for fine-tuning with:")
    print("      - Unsloth (fast LoRA training)")
    print("      - HuggingFace Transformers + PEFT")
    print("      - axolotl framework")
    print()
    print("💡 See docs/LLM_DEPLOYMENT_GUIDE.md for training instructions")
    print()

if __name__ == "__main__":
    main()
