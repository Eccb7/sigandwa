#!/usr/bin/env python3
"""
Parse James Ussher's Annals of the World text file and generate event seed data
This script extracts dated events from the full Annals text (53,882 lines)
"""

import re
from typing import List, Dict, Optional, Tuple
from pathlib import Path


class UssherAnnalsParser:
    """Parser for extracting events from Ussher's Annals text file"""
    
    def __init__(self, annals_file: str):
        self.annals_file = Path(annals_file)
        self.events: List[Dict] = []
        
        # Regex patterns for parsing
        self.date_pattern = re.compile(r'(\d+[a-d]?)\s*AM,\s*(\d+)\s*JP,\s*(\d+)\s*(BC|AD)')
        self.entry_pattern = re.compile(r'^(\d+)\.\s+(.+)', re.MULTILINE)
        
        # Era classifications based on year ranges
        # Mapped to match ChronologyEra enum in database
        self.era_ranges = [
            (-4004, -2349, "creation_to_flood"),
            (-2348, -2007, "patriarchs"),  # flood_to_abraham + patriarchs
            (-2006, -1491, "egyptian_bondage"),  # egypt_to_exodus → egyptian_bondage
            (-1490, -1406, "exodus_to_judges"),
            (-1405, -1051, "exodus_to_judges"),  # judges → exodus_to_judges
            (-1050, -931, "united_monarchy"),
            (-930, -586, "divided_kingdom"),
            (-585, -516, "exile"),  # babylonian_exile → exile
            (-515, -4, "post_exile"),  # second_temple → post_exile
            (5, 100, "early_church"),
            (101, 1650, "early_church")  # church_age → early_church
        ]
        
        # Biblical source mapping
        self.biblical_books = {
            'Ge': 'Genesis', 'Ex': 'Exodus', 'Le': 'Leviticus', 'Nu': 'Numbers',
            'De': 'Deuteronomy', 'Jos': 'Joshua', 'Jud': 'Judges', 'Ru': 'Ruth',
            '1Sa': '1 Samuel', '2Sa': '2 Samuel', '1Ki': '1 Kings', '2Ki': '2 Kings',
            '1Ch': '1 Chronicles', '2Ch': '2 Chronicles', 'Ezr': 'Ezra', 'Ne': 'Nehemiah',
            'Es': 'Esther', 'Job': 'Job', 'Ps': 'Psalms', 'Pr': 'Proverbs',
            'Ec': 'Ecclesiastes', 'So': 'Song of Solomon', 'Isa': 'Isaiah',
            'Jer': 'Jeremiah', 'La': 'Lamentations', 'Eze': 'Ezekiel', 'Da': 'Daniel',
            'Ho': 'Hosea', 'Joe': 'Joel', 'Am': 'Amos', 'Ob': 'Obadiah', 'Jon': 'Jonah',
            'Mic': 'Micah', 'Na': 'Nahum', 'Hab': 'Habakkuk', 'Zep': 'Zephaniah',
            'Hag': 'Haggai', 'Zec': 'Zechariah', 'Mal': 'Malachi',
            'Mt': 'Matthew', 'Mr': 'Mark', 'Lu': 'Luke', 'Joh': 'John', 'Ac': 'Acts',
            'Ro': 'Romans', '1Co': '1 Corinthians', '2Co': '2 Corinthians',
            'Ga': 'Galatians', 'Eph': 'Ephesians', 'Php': 'Philippians',
            'Col': 'Colossians', '1Th': '1 Thessalonians', '2Th': '2 Thessalonians',
            '1Ti': '1 Timothy', '2Ti': '2 Timothy', 'Tit': 'Titus', 'Phm': 'Philemon',
            'Heb': 'Hebrews', 'Jas': 'James', '1Pe': '1 Peter', '2Pe': '2 Peter',
            '1Jo': '1 John', '2Jo': '2 John', '3Jo': '3 John', 'Jude': 'Jude',
            'Re': 'Revelation'
        }
    
    def extract_biblical_references(self, text: str) -> List[str]:
        """Extract biblical references from text (e.g., Ge 1:1, Ex 12:41)"""
        references = []
        for abbrev, full_name in self.biblical_books.items():
            # Pattern: Book chapter:verse
            pattern = rf'{re.escape(abbrev)}\s+(\d+):(\d+(?:-\d+)?(?:,\d+)?)'
            matches = re.findall(pattern, text)
            for match in matches:
                references.append(f"{full_name} {match[0]}:{match[1]}")
        return references
    
    def determine_era(self, year: int) -> str:
        """Determine which era a year belongs to"""
        for start, end, era in self.era_ranges:
            if start <= year <= end:
                return era
        return "early_church"  # Default for dates beyond range
    
    def classify_event_type(self, description: str, biblical_refs: List[str]) -> str:
        """Classify event type based on description content"""
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ['battle', 'war', 'conquered', 'defeated', 'siege', 'military', 'army']):
            return "military"
        elif any(word in desc_lower for word in ['king', 'reign', 'emperor', 'throne', 'crowned', 'ruler']):
            return "political"
        elif any(word in desc_lower for word in ['temple', 'priest', 'worship', 'sacrifice', 'altar', 'god', 'lord', 'faith', 'covenant', 'prophecy']):
            return "religious"
        elif any(word in desc_lower for word in ['born', 'died', 'married', 'family', 'son', 'daughter']):
            return "social"  # Changed from "cultural" to match EventType enum
        elif any(word in desc_lower for word in ['famine', 'drought', 'earthquake', 'flood']):
            return "natural"  # Changed from "environmental" to match EventType enum
        elif biblical_refs:
            return "religious"
        else:
            return "social"  # Changed from "cultural" to match EventType enum
    
    def extract_key_actors(self, description: str) -> List[str]:
        """Extract proper names that are likely key actors"""
        actors = []
        
        # Common biblical names pattern (capitalized words)
        name_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'
        potential_names = re.findall(name_pattern, description)
        
        # Filter out common words that aren't names
        exclude = {'God', 'Lord', 'The', 'When', 'After', 'Before', 'This', 'That', 
                  'Now', 'Then', 'Also', 'About', 'During', 'Since', 'While',
                  'From', 'Into', 'Upon', 'Among', 'Through', 'Between'}
        
        for name in potential_names:
            if name not in exclude and len(name) > 2:
                actors.append(name)
        
        return list(set(actors))[:5]  # Max 5 actors
    
    def parse_annals(self) -> List[Dict]:
        """Parse the entire Annals text file"""
        print(f"📖 Parsing {self.annals_file.name}...")
        
        with open(self.annals_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        current_year = None
        current_am = None
        current_jp = None
        current_era_marker = None
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if line contains a date marker
            date_match = self.date_pattern.search(line)
            if date_match:
                am, jp, year_num, era_marker = date_match.groups()
                current_am = am
                current_jp = jp
                current_era_marker = era_marker
                
                # Convert to negative for BC, positive for AD
                if era_marker == 'BC':
                    current_year = -int(year_num)
                else:
                    current_year = int(year_num)
                
                i += 1
                continue
            
            # Check if line starts with entry number
            entry_match = self.entry_pattern.match(line)
            if entry_match and current_year is not None:
                entry_num = entry_match.group(1)
                description_start = entry_match.group(2)
                
                # Collect full description (may span multiple lines)
                description_lines = [description_start]
                i += 1
                
                # Continue reading lines until we hit another entry or date
                while i < len(lines):
                    next_line = lines[i].strip()
                    
                    # Stop if we hit another date or entry number or empty line
                    if (self.date_pattern.search(next_line) or 
                        self.entry_pattern.match(next_line) or
                        not next_line):
                        break
                    
                    description_lines.append(next_line)
                    i += 1
                
                full_description = ' '.join(description_lines)
                
                # Limit description length
                if len(full_description) > 500:
                    full_description = full_description[:497] + "..."
                
                # Extract biblical references
                biblical_refs = self.extract_biblical_references(full_description)
                biblical_source = ', '.join(biblical_refs) if biblical_refs else None
                
                # Determine era and event type
                era = self.determine_era(current_year)
                event_type = self.classify_event_type(full_description, biblical_refs)
                
                # Extract key actors
                actors = self.extract_key_actors(full_description)
                
                # Create name from first 10 words of description
                name_words = full_description.split()[:10]
                name = ' '.join(name_words)
                if len(full_description) > len(name):
                    name += "..."
                
                # Build event dict
                event = {
                    "name": name,
                    "description": full_description,
                    "year_start": current_year,
                    "era": era,
                    "event_type": event_type,
                }
                
                if biblical_source:
                    event["biblical_source"] = biblical_source
                
                if actors:
                    event["key_actors"] = actors
                
                event["source_references"] = [f"Ussher Annals {current_am} AM, {current_jp} JP, Entry {entry_num}"]
                
                event["extra_data"] = {
                    "ussher_date": f"{year_num} {current_era_marker}",
                    "annals_reference": f"{current_am} AM, {current_jp} JP",
                    "entry_number": entry_num
                }
                
                self.events.append(event)
                continue
            
            i += 1
        
        print(f"✅ Extracted {len(self.events)} events from Annals")
        return self.events
    
    def generate_seed_file(self, output_file: str):
        """Generate Python seed file with all events"""
        print(f"📝 Generating seed file: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('"""\n')
            f.write('Ussher\'s Annals of the World - Extended Seed Data\n')
            f.write('Auto-generated from James Ussher\'s Annals text file\n')
            f.write(f'Total events: {len(self.events)}\n')
            f.write('"""\n\n')
            f.write('USSHER_ANNALS_EVENTS = [\n')
            
            for idx, event in enumerate(self.events):
                f.write('    {\n')
                for key, value in event.items():
                    if isinstance(value, str):
                        # Escape quotes in strings
                        value = value.replace('\\', '\\\\').replace('"', '\\"')
                        f.write(f'        "{key}": "{value}",\n')
                    elif isinstance(value, list):
                        f.write(f'        "{key}": {value!r},\n')
                    elif isinstance(value, dict):
                        f.write(f'        "{key}": {value!r},\n')
                    else:
                        f.write(f'        "{key}": {value},\n')
                
                if idx < len(self.events) - 1:
                    f.write('    },\n')
                else:
                    f.write('    }\n')
            
            f.write(']\n')
        
        print(f"✅ Generated {output_file} with {len(self.events)} events")
    
    def print_statistics(self):
        """Print statistics about parsed events"""
        print("\n" + "="*70)
        print("USSHER ANNALS PARSING STATISTICS")
        print("="*70)
        
        # Total events
        print(f"\n📊 Total Events: {len(self.events)}")
        
        # Events by era
        print("\n📅 Events by Era:")
        era_counts = {}
        for event in self.events:
            era = event['era']
            era_counts[era] = era_counts.get(era, 0) + 1
        
        for era, count in sorted(era_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {era}: {count}")
        
        # Events by type
        print("\n🏷️  Events by Type:")
        type_counts = {}
        for event in self.events:
            event_type = event['event_type']
            type_counts[event_type] = type_counts.get(event_type, 0) + 1
        
        for event_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {event_type}: {count}")
        
        # Year range
        years = [e['year_start'] for e in self.events]
        if years:
            print(f"\n📆 Year Range: {min(years)} to {max(years)}")
            print(f"   Span: {max(years) - min(years)} years")
        
        # Biblical references
        with_biblical_refs = sum(1 for e in self.events if e.get('biblical_source'))
        print(f"\n📖 Events with Biblical References: {with_biblical_refs} ({with_biblical_refs/len(self.events)*100:.1f}%)")
        
        print("\n" + "="*70 + "\n")


def main():
    """Main execution"""
    annals_file = "/home/ojwangb/sigandwa/docs/James-Usher-Annals-of-the-World.txt"
    output_file = "/home/ojwangb/sigandwa/data/seed/ussher_annals_extended.py"
    
    parser = UssherAnnalsParser(annals_file)
    events = parser.parse_annals()
    
    if events:
        parser.print_statistics()
        parser.generate_seed_file(output_file)
        
        print("✨ Success! You can now import these events:")
        print(f"   1. Review the generated file: {output_file}")
        print(f"   2. Import events: python import_ussher_data.py")
    else:
        print("❌ No events were parsed from the Annals file")


if __name__ == "__main__":
    main()
