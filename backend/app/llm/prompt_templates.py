"""
Prompt templates for Biblical analysis
"""

SYSTEM_PROMPT = """You are Sigandwa, an expert Biblical historian and cliodynamic analyst. Your knowledge is based on:

1. James Ussher's Annals of the World (1650) - Definitive Biblical chronology
2. Protestant historicist prophetic interpretation (William Miller tradition)
3. 7,440+ verified historical events from Creation (4004 BC) to present
4. Daniel's prophecies (70 weeks, 2300 days, 1260 years, four kingdoms)
5. Revelation's timeline (538-1798 AD papal supremacy, end-time events)

**Key Dates from Ussher's Chronology:**
- Creation: 4004 BC (October 23)
- Noah's Flood: 2348 BC
- Abraham's Birth: 1996 BC
- Exodus from Egypt: 1491 BC (Moses led Israelites out)
- Jerusalem Temple Completed: 1004 BC (Solomon)
- Babylonian Captivity: 586 BC
- Jesus Christ Birth: 4 BC
- Jesus Crucifixion: 33 AD

Core Principles:
- Scripture is the ultimate authority
- Year-day principle for time prophecies (Num 14:34, Ezek 4:6)
- Historicist interpretation: prophecies fulfilled in church history
- Ussher's chronology is foundational
- ALWAYS cite specific dates from the provided historical data

**IMPORTANT:** When answering questions about historical events, ALWAYS reference the specific dates and events from the provided context. If you don't have specific information, say "I don't have that specific date in my database" rather than guessing."""


def get_event_analysis_prompt(event: dict) -> str:
    """Generate prompt for analyzing a historical event"""
    return f"""Analyze this Biblical/historical event in depth:

**Event**: {event['name']}
**Date**: {event['year_start']} BC/AD
**Era**: {event['era']}
**Description**: {event['description']}
**Biblical Sources**: {event.get('biblical_source', 'N/A')}

Provide:
1. Historical context and significance
2. Biblical connections and fulfillment
3. Relevance to prophetic timeline
4. Impact on Biblical history

Keep response under 300 words."""


def get_prophecy_interpretation_prompt(prophecy: str, context: str = "") -> str:
    """Generate prompt for interpreting a prophecy"""
    return f"""Interpret this Biblical prophecy using the historicist method:

**Prophecy Text**: {prophecy}
{f"**Additional Context**: {context}" if context else ""}

Explain:
1. Historical fulfillment (dates, events, kingdoms)
2. Year-day principle application if applicable
3. Connection to Daniel's 4 kingdoms or Revelation's timeline
4. Modern relevance and remaining unfulfilled portions

Use Protestant Reformation scholarship (Miller, Smith, Andrews)."""


def get_chronology_question_prompt(question: str, relevant_events: list) -> str:
    """Generate prompt for answering chronology questions"""
    events_context = "\n".join([
        f"- {e['year_start']} BC/AD: {e['name']} ({e.get('biblical_source', 'historical')})"
        for e in relevant_events[:10]
    ])
    
    return f"""Answer this question about Biblical chronology:

**Question**: {question}

**Relevant Historical Events**:
{events_context}

Provide a detailed answer based on Ussher's chronology and Biblical sources. Cite specific dates and scripture references."""


def get_pattern_analysis_prompt(pattern: dict, matching_events: list) -> str:
    """Generate prompt for pattern analysis"""
    return f"""Analyze this historical pattern:

**Pattern**: {pattern['name']}
**Description**: {pattern['description']}
**Historical Occurrences**: {len(matching_events)} times

**Preconditions**:
{chr(10).join(f"- {p}" for p in pattern.get('preconditions', []))}

**Consequences**:
{chr(10).join(f"- {c}" for c in pattern.get('consequences', []))}

Explain:
1. Biblical examples of this pattern
2. Historical trajectory and outcomes
3. Current world state comparison
4. Prophetic implications

Base analysis on Biblical principles and historical precedent."""
