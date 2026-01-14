#!/usr/bin/env python3
"""
Seed prophecy data from Revelation Gems and Daniel Gems
"""
import sys
import re
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.prophecy import ProphecyText, FulfillmentType
from app.config import settings

# Create database engine
engine = create_engine(settings.postgres_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def extract_prophecies_from_revelation(text_file: Path):
    """Extract prophecy texts from Revelation Gems"""
    prophecies = []
    
    with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Split by chapters or sections
    # Look for patterns like "Chapter" or verse references
    sections = re.split(r'\n\s*(?:CHAPTER|Chapter)\s+\d+', content)
    
    for i, section in enumerate(sections[1:], 1):  # Skip first empty section
        # Extract verse references (e.g., Rev 1:1, Revelation 2:3)
        verse_refs = re.findall(r'(?:Rev(?:elation)?\.?\s+)?(\d+):(\d+(?:-\d+)?)', section[:500])
        
        if verse_refs:
            chapter, verses = verse_refs[0]
            reference = f"Revelation {chapter}:{verses}"
            
            # Get first meaningful paragraph as prophecy text
            paragraphs = [p.strip() for p in section.split('\n\n') if len(p.strip()) > 50]
            if paragraphs:
                text = paragraphs[0][:500]  # First 500 chars
                
                # Extract interpretation notes (look for explanatory text)
                interpretation = None
                if len(paragraphs) > 1:
                    interpretation = paragraphs[1][:500]
                
                prophecies.append({
                    'reference': reference,
                    'text': text,
                    'chapter': int(chapter),
                    'interpretation': interpretation
                })
    
    return prophecies


def extract_prophecies_from_daniel(text_file: Path):
    """Extract prophecy texts from Daniel Gems"""
    prophecies = []
    
    with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Split by chapters
    sections = re.split(r'\n\s*(?:CHAPTER|Chapter)\s+\d+', content)
    
    for i, section in enumerate(sections[1:], 1):
        verse_refs = re.findall(r'(?:Dan(?:iel)?\.?\s+)?(\d+):(\d+(?:-\d+)?)', section[:500])
        
        if verse_refs:
            chapter, verses = verse_refs[0]
            reference = f"Daniel {chapter}:{verses}"
            
            paragraphs = [p.strip() for p in section.split('\n\n') if len(p.strip()) > 50]
            if paragraphs:
                text = paragraphs[0][:500]
                
                interpretation = None
                if len(paragraphs) > 1:
                    interpretation = paragraphs[1][:500]
                
                prophecies.append({
                    'reference': reference,
                    'text': text,
                    'chapter': int(chapter),
                    'interpretation': interpretation
                })
    
    return prophecies


def seed_prophecies():
    """Seed prophecy data into database"""
    db = SessionLocal()
    
    try:
        # Clear existing prophecies
        print("🗑️  Clearing existing prophecies...")
        db.query(ProphecyText).delete()
        db.commit()
        
        # Extract from Revelation
        print("\n📖 Extracting prophecies from Revelation Gems...")
        rev_file = Path(__file__).parent.parent / "docs" / "revelation_gems.txt"
        if rev_file.exists():
            rev_prophecies = extract_prophecies_from_revelation(rev_file)
            print(f"   Found {len(rev_prophecies)} Revelation prophecies")
            
            for p in rev_prophecies:
                prophecy = ProphecyText(
                    reference=p['reference'],
                    text=p['text'],
                    prophet='John',
                    year_declared=95,  # ~95 AD when Revelation was written
                    prophecy_type='apocalyptic',
                    scope='end_times',
                    interpretation_notes=p.get('interpretation'),
                    elements={'chapter': p['chapter'], 'source': 'revelation_gems'}
                )
                db.add(prophecy)
        else:
            print(f"   ⚠️  File not found: {rev_file}")
        
        # Extract from Daniel
        print("\n📖 Extracting prophecies from Daniel Gems...")
        dan_file = Path(__file__).parent.parent / "docs" / "daniel_gems.txt"
        if dan_file.exists():
            dan_prophecies = extract_prophecies_from_daniel(dan_file)
            print(f"   Found {len(dan_prophecies)} Daniel prophecies")
            
            for p in dan_prophecies:
                prophecy = ProphecyText(
                    reference=p['reference'],
                    text=p['text'],
                    prophet='Daniel',
                    year_declared=-540,  # ~540 BC
                    prophecy_type='prophetic',
                    scope='kingdoms',
                    interpretation_notes=p.get('interpretation'),
                    elements={'chapter': p['chapter'], 'source': 'daniel_gems'}
                )
                db.add(prophecy)
        else:
            print(f"   ⚠️  File not found: {dan_file}")
        
        # Commit all
        db.commit()
        
        # Count results
        total = db.query(ProphecyText).count()
        print(f"\n✅ Seeded {total} prophecies successfully!")
        
        # Show sample
        sample = db.query(ProphecyText).limit(3).all()
        if sample:
            print("\n📝 Sample prophecies:")
            for p in sample:
                print(f"   • {p.reference}: {p.text[:80]}...")
        
    except Exception as e:
        print(f"\n❌ Error seeding prophecies: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 70)
    print("🔮 PROPHECY DATA SEEDING")
    print("=" * 70)
    
    seed_prophecies()
    
    print("\n" + "=" * 70)
    print("✅ Prophecy seeding complete!")
