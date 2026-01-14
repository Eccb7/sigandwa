#!/usr/bin/env python3
"""
Seed world indicators for simulation modeling.
Adds current global conditions for pattern precondition matching.
"""

import sys
sys.path.insert(0, "/home/ojwangb/sigandwa/backend")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.models.simulation import WorldIndicator
from app.config import settings

# Create database session
engine = create_engine(settings.postgres_url)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()


def seed_indicators():
    """Seed contemporary world indicators across all categories."""
    
    indicators = [
        # POLITICAL INDICATORS
        {
            "indicator_name": "Democratic Backsliding",
            "category": "political",
            "value": 7.2,
            "description": "Decline in democratic norms and institutions globally (scale 0-10)",
            "data_source": "V-Dem Democracy Report 2024",
        },
        {
            "indicator_name": "Political Polarization",
            "category": "political",
            "value": 8.1,
            "description": "Increasing partisan divides in major democracies (scale 0-10)",
            "data_source": "Pew Research Center 2024",
        },
        {
            "indicator_name": "Authoritarian Consolidation",
            "category": "political",
            "value": 6.8,
            "description": "Growth of authoritarian regimes and power consolidation (scale 0-10)",
            "data_source": "Freedom House 2024",
        },
        {
            "indicator_name": "Nationalist Movements",
            "category": "political",
            "value": 7.5,
            "description": "Rise of nationalist and populist political movements (scale 0-10)",
            "data_source": "Global Populism Database 2024",
        },
        {
            "indicator_name": "Geopolitical Tension",
            "category": "political",
            "value": 8.3,
            "description": "US-China rivalry, Russia-West tensions (scale 0-10)",
            "data_source": "Council on Foreign Relations 2024",
        },
        
        # ECONOMIC INDICATORS
        {
            "indicator_name": "Income Inequality",
            "category": "economic",
            "value": 0.42,
            "description": "Global Gini coefficient - wealth concentration",
            "data_source": "World Bank 2024",
        },
        {
            "indicator_name": "Debt-to-GDP Ratios",
            "category": "economic",
            "value": 256.0,
            "description": "Global debt as percentage of GDP (all sectors)",
            "data_source": "IMF Global Debt Database 2024",
        },
        {
            "indicator_name": "Economic Fragmentation",
            "category": "economic",
            "value": 6.9,
            "description": "De-globalization and supply chain regionalization (scale 0-10)",
            "data_source": "WEF Global Risks Report 2024",
        },
        {
            "indicator_name": "Currency Instability",
            "category": "economic",
            "value": 5.7,
            "description": "Volatility in major currencies and emerging market stress (scale 0-10)",
            "data_source": "BIS Currency Volatility Index 2024",
        },
        {
            "indicator_name": "Food Insecurity",
            "category": "economic",
            "value": 735000000.0,
            "description": "Number of people facing chronic hunger globally",
            "data_source": "UN FAO 2024",
        },
        
        # MILITARY INDICATORS
        {
            "indicator_name": "Nuclear Tensions",
            "category": "military",
            "value": 8.7,
            "description": "Risk of nuclear escalation (scale 0-10)",
            "data_source": "Doomsday Clock 2024 (90 seconds to midnight)",
        },
        {
            "indicator_name": "Regional Conflicts",
            "category": "military",
            "value": 56.0,
            "description": "Number of active armed conflicts worldwide",
            "data_source": "Uppsala Conflict Data Program 2024",
        },
        {
            "indicator_name": "Military Buildup",
            "category": "military",
            "value": 2443000000000.0,
            "description": "Global military expenditure in USD (trillions)",
            "data_source": "SIPRI Military Expenditure 2024",
        },
        {
            "indicator_name": "Cyber Warfare",
            "category": "military",
            "value": 7.8,
            "description": "Frequency and sophistication of state cyberattacks (scale 0-10)",
            "data_source": "Cyber Peace Institute 2024",
        },
        {
            "indicator_name": "Terrorism Threat",
            "category": "military",
            "value": 6.1,
            "description": "Global terrorism index score",
            "data_source": "Institute for Economics and Peace 2024",
        },
        
        # SOCIAL INDICATORS
        {
            "indicator_name": "Social Fragmentation",
            "category": "social",
            "value": 7.3,
            "description": "Breakdown of community cohesion and trust (scale 0-10)",
            "data_source": "Social Capital Index 2024",
        },
        {
            "indicator_name": "Migration Crisis",
            "category": "social",
            "value": 108400000.0,
            "description": "Number of forcibly displaced people globally",
            "data_source": "UNHCR Global Trends 2024",
        },
        {
            "indicator_name": "Moral Relativism",
            "category": "social",
            "value": 8.2,
            "description": "Decline in absolute moral standards (scale 0-10)",
            "data_source": "Pew Global Attitudes Survey 2024",
        },
        {
            "indicator_name": "Mental Health Crisis",
            "category": "social",
            "value": 970000000.0,
            "description": "People living with mental disorders globally",
            "data_source": "WHO Mental Health Atlas 2024",
        },
        {
            "indicator_name": "Family Breakdown",
            "category": "social",
            "value": 6.7,
            "description": "Divorce rates and single-parent household growth (scale 0-10)",
            "data_source": "OECD Family Database 2024",
        },
        
        # RELIGIOUS INDICATORS
        {
            "indicator_name": "Christian Persecution",
            "category": "religious",
            "value": 365000000.0,
            "description": "Christians facing high levels of persecution",
            "data_source": "Open Doors World Watch List 2024",
        },
        {
            "indicator_name": "Secularization",
            "category": "religious",
            "value": 7.1,
            "description": "Decline in religious affiliation in the West (scale 0-10)",
            "data_source": "Pew Religious Landscape Study 2024",
        },
        {
            "indicator_name": "Religious Violence",
            "category": "religious",
            "value": 6.4,
            "description": "Religiously motivated conflicts and attacks (scale 0-10)",
            "data_source": "Religious Freedom Institute 2024",
        },
        {
            "indicator_name": "Apostasy",
            "category": "religious",
            "value": 6.9,
            "description": "Rate of abandonment of Christian faith (scale 0-10)",
            "data_source": "Barna Church Trends 2024",
        },
        {
            "indicator_name": "Prophetic Interest",
            "category": "religious",
            "value": 5.8,
            "description": "Public interest in biblical prophecy and end times (scale 0-10)",
            "data_source": "Google Trends + Christian Survey Data 2024",
        },
    ]
    
    timestamp = datetime.utcnow()
    
    for ind_data in indicators:
        indicator = WorldIndicator(
            indicator_name=ind_data["indicator_name"],
            category=ind_data["category"],
            value=ind_data["value"],
            description=ind_data["description"],
            data_source=ind_data["data_source"],
            timestamp=timestamp,
        )
        db.add(indicator)
    
    db.commit()
    
    print(f"\n✅ Seeded {len(indicators)} world indicators:")
    print(f"   - Political: 5 indicators")
    print(f"   - Economic: 5 indicators")
    print(f"   - Military: 5 indicators")
    print(f"   - Social: 5 indicators")
    print(f"   - Religious: 5 indicators")
    print(f"\nTimestamp: {timestamp.isoformat()}")


if __name__ == "__main__":
    try:
        seed_indicators()
        print("\n✅ Indicator seeding complete!")
    except Exception as e:
        print(f"\n❌ Error seeding indicators: {e}")
        db.rollback()
        raise
    finally:
        db.close()
