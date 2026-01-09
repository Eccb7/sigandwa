#!/usr/bin/env python3
"""
Seed major biblical prophecies into the database
Focus on Daniel's time prophecies and their fulfillments
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.prophecy import ProphecyText, ProphecyFulfillment, FulfillmentType
from app.models.chronology import ChronologyEvent


# Major Daniel Prophecies with structured data
DANIEL_PROPHECIES = [
    {
        "reference": "Daniel 9:24-27",
        "prophet": "Daniel",
        "year_declared": -538,
        "prophecy_type": "messianic",
        "scope": "international",
        "text": "Seventy weeks are determined upon thy people and upon thy holy city, to finish the transgression, and to make an end of sins, and to make reconciliation for iniquity, and to bring in everlasting righteousness, and to seal up the vision and prophecy, and to anoint the most Holy. Know therefore and understand, that from the going forth of the commandment to restore and to build Jerusalem unto the Messiah the Prince shall be seven weeks, and threescore and two weeks: the street shall be built again, and the wall, even in troublous times. And after threescore and two weeks shall Messiah be cut off, but not for himself: and the people of the prince that shall come shall destroy the city and the sanctuary...",
        "elements": {
            "total_period": "70 weeks = 490 prophetic days = 490 literal years",
            "segments": [
                {"duration": "7 weeks (49 years)", "event": "Rebuilding Jerusalem", "fulfilled": "457-408 BC"},
                {"duration": "62 weeks (434 years)", "event": "Until Messiah", "fulfilled": "408 BC - 27 AD"},
                {"duration": "1 week (7 years)", "event": "Messiah's ministry and covenant", "fulfilled": "27-34 AD"}
            ],
            "key_dates": {
                "decree": "457 BC - Artaxerxes' decree to restore Jerusalem",
                "messiah_appears": "27 AD - Jesus' baptism",
                "messiah_cut_off": "31 AD - Crucifixion (midst of week)",
                "covenant_confirmed": "34 AD - Gospel to Gentiles, Stephen martyred"
            },
            "fulfillments": [
                "Messiah appears exactly 483 years (69 weeks) after decree",
                "Messiah cut off (crucified) in midst of final week",
                "Sacrificial system ended with Jesus' death",
                "Gospel went to Gentiles after 490 years"
            ]
        }
    },
    {
        "reference": "Daniel 8:13-14",
        "prophet": "Daniel",
        "year_declared": -547,
        "prophecy_type": "sanctuary_judgment",
        "scope": "eschatological",
        "text": "Then I heard one saint speaking, and another saint said unto that certain saint which spake, How long shall be the vision concerning the daily sacrifice, and the transgression of desolation, to give both the sanctuary and the host to be trodden under foot? And he said unto me, Unto two thousand and three hundred days; then shall the sanctuary be cleansed.",
        "elements": {
            "total_period": "2300 prophetic days = 2300 literal years",
            "start_date": "457 BC - Same decree as 70 weeks prophecy",
            "end_date": "1844 AD - Investigative judgment begins",
            "key_events": {
                "sanctuary_trampled": "Daily sacrifice taken away, truth cast down",
                "cleansing_begins": "1844 AD - Day of Atonement antitype",
                "judgment": "Pre-advent investigative judgment"
            },
            "fulfillments": [
                "2300 years from 457 BC ends in 1844 AD",
                "Matches Daniel 7:9-10 judgment scene",
                "Sanctuary cleansing = investigative judgment",
                "Begins final phase of Christ's ministry"
            ]
        }
    },
    {
        "reference": "Daniel 7:23-25",
        "prophet": "Daniel",
        "year_declared": -553,
        "prophecy_type": "persecution",
        "scope": "eschatological",
        "text": "Thus he said, The fourth beast shall be the fourth kingdom upon earth, which shall be diverse from all kingdoms, and shall devour the whole earth, and shall tread it down, and break it in pieces. And the ten horns out of this kingdom are ten kings that shall arise: and another shall rise after them; and he shall be diverse from the first, and he shall subdue three kings. And he shall speak great words against the most High, and shall wear out the saints of the most High, and think to change times and laws: and they shall be given into his hand until a time and times and the dividing of time.",
        "elements": {
            "little_horn": "Power arising after Rome's division",
            "characteristics": [
                "Speaks against God",
                "Persecutes saints",
                "Changes times and laws",
                "Rules for time, times, and half a time"
            ],
            "time_period": "Time, times, dividing of time = 3.5 prophetic years = 1260 literal years",
            "start_date": "538 AD - Ostrogoths defeated, papal supremacy established",
            "end_date": "1798 AD - Pope captured by French, temporal power ended",
            "fulfillments": [
                "Roman Catholic papacy arose after Western Rome fell",
                "Persecuted dissenters during Middle Ages",
                "Changed Sabbath to Sunday",
                "Ruled 1260 years: 538-1798 AD"
            ]
        }
    },
    {
        "reference": "Daniel 12:6-7",
        "prophet": "Daniel",
        "year_declared": -536,
        "prophecy_type": "time_of_trouble",
        "scope": "eschatological",
        "text": "And one said to the man clothed in linen, which was upon the waters of the river, How long shall it be to the end of these wonders? And I heard the man clothed in linen, which was upon the waters of the river, when he held up his right hand and his left hand unto heaven, and sware by him that liveth for ever that it shall be for a time, times, and an half; and when he shall have accomplished to scatter the power of the holy people, all these things shall be finished.",
        "elements": {
            "time_period": "Time, times, and half = 3.5 years = 1260 days/years",
            "same_as": "Daniel 7:25, Revelation 11:2-3, 12:6, 13:5",
            "persecution_period": "1260 years of papal supremacy",
            "start_date": "538 AD",
            "end_date": "1798 AD",
            "scattering_power": "Holy people scattered/persecuted during this time"
        }
    },
    {
        "reference": "Daniel 2:31-45",
        "prophet": "Daniel",
        "year_declared": -603,
        "prophecy_type": "kingdom_succession",
        "scope": "international",
        "text": "Thou, O king, sawest, and behold a great image. This great image, whose brightness was excellent, stood before thee; and the form thereof was terrible. This image's head was of fine gold, his breast and his arms of silver, his belly and his thighs of brass, His legs of iron, his feet part of iron and part of clay. Thou sawest till that a stone was cut out without hands, which smote the image upon his feet that were of iron and clay, and brake them to pieces... And in the days of these kings shall the God of heaven set up a kingdom, which shall never be destroyed...",
        "elements": {
            "kingdoms": [
                {"metal": "Gold", "kingdom": "Babylon", "years": "605-539 BC"},
                {"metal": "Silver", "kingdom": "Medo-Persia", "years": "539-331 BC"},
                {"metal": "Bronze", "kingdom": "Greece", "years": "331-168 BC"},
                {"metal": "Iron", "kingdom": "Rome", "years": "168 BC - 476 AD"},
                {"metal": "Iron/Clay", "kingdom": "Divided Europe", "years": "476 AD - present"}
            ],
            "stone": "God's eternal kingdom",
            "fulfillments": [
                "Babylon conquered by Medo-Persia (539 BC)",
                "Medo-Persia conquered by Greece (331 BC)",
                "Greece conquered by Rome (168 BC)",
                "Rome divided into European kingdoms (476 AD)",
                "Europe remains divided - no reunification",
                "God's kingdom will destroy all earthly kingdoms"
            ]
        }
    },
    {
        "reference": "Daniel 7:1-8",
        "prophet": "Daniel",
        "year_declared": -553,
        "prophecy_type": "kingdom_succession",
        "scope": "international",
        "text": "Daniel spake and said, I saw in my vision by night, and, behold, the four winds of the heaven strove upon the great sea. And four great beasts came up from the sea, diverse one from another. The first was like a lion, and had eagle's wings... And behold another beast, a second, like to a bear... After this I beheld, and lo another, like a leopard... After this I saw in the night visions, and behold a fourth beast, dreadful and terrible, and strong exceedingly; and it had great iron teeth...",
        "elements": {
            "beasts": [
                {"animal": "Lion with eagle's wings", "kingdom": "Babylon", "years": "605-539 BC"},
                {"animal": "Bear raised on one side", "kingdom": "Medo-Persia", "years": "539-331 BC"},
                {"animal": "Leopard with 4 heads", "kingdom": "Greece", "years": "331-168 BC"},
                {"animal": "Terrible beast with iron teeth", "kingdom": "Rome", "years": "168 BC - 476 AD"}
            ],
            "ten_horns": "Ten kingdoms arising from Rome's division",
            "little_horn": "Papal power arising among the ten",
            "judgment": "Ancient of Days judges the little horn",
            "fulfillments": [
                "Same kingdoms as Daniel 2 but with more detail",
                "Little horn persecutes saints for 1260 years",
                "Judgment scene begins in 1844",
                "Son of Man receives everlasting kingdom"
            ]
        }
    }
]


# Link prophecies to historical events that fulfill them
PROPHECY_FULFILLMENTS = [
    {
        "prophecy_reference": "Daniel 9:24-27",
        "event_search": "Artaxerxes",
        "event_year": -457,
        "fulfillment_type": "complete",
        "confidence": 0.95,
        "explanation": "Artaxerxes' decree in 457 BC to restore and rebuild Jerusalem marks the starting point of the 70 weeks (490 years) prophecy. This decree fulfilled Isaiah's prophecy about Cyrus and began the countdown to Messiah."
    },
    {
        "prophecy_reference": "Daniel 9:24-27",
        "event_search": "Jesus.*baptism",
        "event_year": 27,
        "fulfillment_type": "complete",
        "confidence": 0.98,
        "explanation": "Jesus' baptism in 27 AD occurred exactly 483 years (69 weeks) after the 457 BC decree, marking Him as the Messiah the Prince. This was when Jesus was anointed with the Holy Spirit and began His public ministry."
    },
    {
        "prophecy_reference": "Daniel 9:24-27",
        "event_search": "crucif",
        "event_year": 31,
        "fulfillment_type": "complete",
        "confidence": 0.99,
        "explanation": "Messiah was 'cut off' (crucified) in 31 AD, 'in the midst of the week' (3.5 years into the final 7-year period). His death caused the sacrificial system to cease its meaning, as He was the ultimate sacrifice."
    },
    {
        "prophecy_reference": "Daniel 2:31-45",
        "event_search": "Babylon.*fell\|Cyrus.*conquered",
        "event_year": -539,
        "fulfillment_type": "complete",
        "confidence": 1.0,
        "explanation": "Babylon (gold head) was conquered by Medo-Persia (silver) in 539 BC when Cyrus took the city, exactly as prophesied. The kingdom transitioned from gold to silver."
    },
    {
        "prophecy_reference": "Daniel 2:31-45",
        "event_search": "Alexander.*Persia\|Greece.*conquered",
        "event_year": -331,
        "fulfillment_type": "complete",
        "confidence": 1.0,
        "explanation": "Alexander the Great conquered Medo-Persia at the Battle of Gaugamela in 331 BC, transitioning from silver (Medo-Persia) to bronze (Greece). This marked the third kingdom ruling the world."
    },
    {
        "prophecy_reference": "Daniel 2:31-45",
        "event_search": "Rome.*Greece\|Pydna",
        "event_year": -168,
        "fulfillment_type": "complete",
        "confidence": 0.95,
        "explanation": "Rome defeated Greece at the Battle of Pydna in 168 BC, becoming the iron kingdom. Rome's military might and organization made it 'strong as iron' that 'breaks in pieces and subdues all things.'"
    },
    {
        "prophecy_reference": "Daniel 7:23-25",
        "event_search": "Ostrogoths.*defeated\|538",
        "event_year": 538,
        "fulfillment_type": "complete",
        "confidence": 0.90,
        "explanation": "In 538 AD, the Ostrogoths were defeated, removing the last obstacle to papal supremacy. This began the 1260-year period of the 'little horn' speaking against the Most High and persecuting the saints."
    },
    {
        "prophecy_reference": "Daniel 7:23-25",
        "event_search": "Pope.*captured\|1798\|Berthier",
        "event_year": 1798,
        "fulfillment_type": "complete",
        "confidence": 0.95,
        "explanation": "In 1798 AD, French General Berthier captured Pope Pius VI, ending the temporal power of the papacy exactly 1260 years after 538 AD. This fulfilled the 'time, times, and half a time' prophecy."
    }
]


def seed_prophecies():
    """Seed major prophecies into database"""
    print("\n" + "="*70)
    print("  SEEDING DANIEL'S PROPHECIES")
    print("="*70 + "\n")
    
    db = SessionLocal()
    
    try:
        # Insert prophecies
        prophecy_count = 0
        for prop_data in DANIEL_PROPHECIES:
            # Check if already exists
            existing = db.query(ProphecyText).filter(
                ProphecyText.reference == prop_data["reference"]
            ).first()
            
            if existing:
                print(f"⏭️  Skipping: {prop_data['reference']} (already exists)")
                continue
            
            prophecy = ProphecyText(
                reference=prop_data["reference"],
                text=prop_data["text"],
                prophet=prop_data["prophet"],
                year_declared=prop_data["year_declared"],
                prophecy_type=prop_data["prophecy_type"],
                scope=prop_data["scope"],
                elements=prop_data["elements"]
            )
            
            db.add(prophecy)
            print(f"✅ Added prophecy: {prop_data['reference']} - {prop_data['prophecy_type']}")
            prophecy_count += 1
        
        db.commit()
        
        print(f"\n📊 Imported {prophecy_count} prophecies\n")
        
        # Link prophecies to fulfillment events
        print("🔗 Linking prophecies to historical events...\n")
        
        fulfillment_count = 0
        for fulfill_data in PROPHECY_FULFILLMENTS:
            # Find the prophecy
            prophecy = db.query(ProphecyText).filter(
                ProphecyText.reference == fulfill_data["prophecy_reference"]
            ).first()
            
            if not prophecy:
                print(f"⚠️  Prophecy not found: {fulfill_data['prophecy_reference']}")
                continue
            
            # Find matching event(s)
            # Try to find event by year and name pattern
            events = db.query(ChronologyEvent).filter(
                ChronologyEvent.year_start == fulfill_data["event_year"]
            ).all()
            
            if not events:
                print(f"⚠️  No event found for year {fulfill_data['event_year']}")
                continue
            
            # For now, link to first matching event
            # In production, would use more sophisticated matching
            event = events[0]
            
            # Check if fulfillment already exists
            existing_fulfillment = db.query(ProphecyFulfillment).filter(
                ProphecyFulfillment.prophecy_id == prophecy.id,
                ProphecyFulfillment.event_id == event.id
            ).first()
            
            if existing_fulfillment:
                print(f"⏭️  Fulfillment already linked: {prophecy.reference} → {event.name}")
                continue
            
            fulfillment = ProphecyFulfillment(
                prophecy_id=prophecy.id,
                event_id=event.id,
                fulfillment_type=FulfillmentType[fulfill_data["fulfillment_type"].upper()],
                confidence_score=fulfill_data["confidence"],
                explanation=fulfill_data["explanation"]
            )
            
            db.add(fulfillment)
            print(f"✅ Linked: {prophecy.reference} → {event.name} ({event.year_start})")
            fulfillment_count += 1
        
        db.commit()
        
        print(f"\n✨ Import complete!")
        print(f"   • Prophecies added: {prophecy_count}")
        print(f"   • Fulfillments linked: {fulfillment_count}")
        
        # Statistics
        total_prophecies = db.query(ProphecyText).count()
        total_fulfillments = db.query(ProphecyFulfillment).count()
        
        print(f"\n📈 Database totals:")
        print(f"   • Total prophecies: {total_prophecies}")
        print(f"   • Total fulfillments: {total_fulfillments}")
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_prophecies()
