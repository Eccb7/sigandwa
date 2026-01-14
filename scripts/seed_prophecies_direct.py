#!/usr/bin/env python3
"""
Seed prophecy data directly to database using raw SQL
"""
import re
import json
from pathlib import Path
import psycopg2
from psycopg2.extras import execute_values

# Database connection
conn = psycopg2.connect(
    host="localhost",
    port=5434,
    database="sigandwa",
    user="sigandwa",
    password="sigandwa_dev"
)


def extract_prophecies_from_text(text_file: Path, prophet: str, year: int):
    """Extract prophecy texts from document"""
    prophecies = []
    
    with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find all verse references and extract surrounding context
    # Pattern: Book Chapter:Verse or Chapter:Verse
    pattern = r'(?:(?:Rev(?:elation)?|Dan(?:iel)?)\s+)?(\d+):(\d+(?:-\d+)?)'
    matches = re.finditer(pattern, content)
    
    book_name = "Revelation" if prophet == "John" else "Daniel"
    
    for match in matches:
        chapter = match.group(1)
        verses = match.group(2)
        reference = f"{book_name} {chapter}:{verses}"
        
        # Get context around the verse reference (500 chars before and after)
        start_pos = max(0, match.start() - 500)
        end_pos = min(len(content), match.end() + 1500)
        context = content[start_pos:end_pos]
        
        # Clean up and get main text
        paragraphs = [p.strip() for p in context.split('\n') if len(p.strip()) > 30]
        if paragraphs:
            text = ' '.join(paragraphs[:3])[:1000]  # First 3 lines, max 1000 chars
            
            # Get more context for interpretation
            interpretation = None
            if len(paragraphs) > 3:
                interpretation = ' '.join(paragraphs[3:6])[:1000]
            
            if text and len(text) > 50:  # Only add if we have meaningful text
                prophecies.append((
                    reference,
                    text,
                    prophet,
                    year,
                    'prophetic' if prophet == 'Daniel' else 'apocalyptic',
                    'end_times' if prophet == 'John' else 'kingdoms',
                    interpretation,
                    json.dumps({'chapter': int(chapter), 'verses': verses, 'source': f"{prophet.lower()}_gems"})
                ))
    
    # Remove duplicates based on reference
    seen = set()
    unique_prophecies = []
    for p in prophecies:
        if p[0] not in seen:
            seen.add(p[0])
            unique_prophecies.append(p)
    
    return unique_prophecies[:50]  # Limit to first 50 unique prophecies per book


def seed_prophecies():
    """Seed prophecy data"""
    cur = conn.cursor()
    
    try:
        # Clear existing
        print("🗑️  Clearing existing prophecies...")
        cur.execute("DELETE FROM prophecy_texts")
        conn.commit()
        
        all_prophecies = []
        
        # Revelation
        print("\n📖 Extracting from Revelation Gems...")
        rev_file = Path(__file__).parent.parent / "docs" / "revelation_gems.txt"
        if rev_file.exists():
            rev_prophecies = extract_prophecies_from_text(rev_file, "Revelation", 95)
            print(f"   Found {len(rev_prophecies)} Revelation prophecies")
            all_prophecies.extend(rev_prophecies)
        
        # Daniel  
        print("\n📖 Extracting from Daniel Gems...")
        dan_file = Path(__file__).parent.parent / "docs" / "daniel_gems.txt"
        if dan_file.exists():
            dan_prophecies = extract_prophecies_from_text(dan_file, "Daniel", -540)
            print(f"   Found {len(dan_prophecies)} Daniel prophecies")
            all_prophecies.extend(dan_prophecies)
        
        # Insert all
        if all_prophecies:
            print(f"\n💾 Inserting {len(all_prophecies)} prophecies...")
            execute_values(
                cur,
                """
                INSERT INTO prophecy_texts 
                (reference, text, prophet, year_declared, prophecy_type, scope, interpretation_notes, elements)
                VALUES %s
                """,
                all_prophecies,
                template="(%s, %s, %s, %s, %s, %s, %s, %s::jsonb)"
            )
            conn.commit()
            
            # Verify
            cur.execute("SELECT COUNT(*) FROM prophecy_texts")
            count = cur.fetchone()[0]
            print(f"✅ Seeded {count} prophecies!")
            
            # Sample
            cur.execute("SELECT reference, LEFT(text, 80) FROM prophecy_texts LIMIT 3")
            print("\n📝 Sample prophecies:")
            for ref, text in cur.fetchall():
                print(f"   • {ref}: {text}...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()


if __name__ == "__main__":
    print("=" * 70)
    print("🔮 PROPHECY DATA SEEDING")
    print("=" * 70)
    
    seed_prophecies()
    conn.close()
    
    print("\n" + "=" * 70)
    print("✅ Complete!")
