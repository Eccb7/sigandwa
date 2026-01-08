"""
Neo4j graph database initialization and schema setup.
Defines nodes and relationships for empire succession, prophecy fulfillment, and pattern recapitulation.
"""

from neo4j import GraphDatabase
from app.config import settings


class Neo4jInitializer:
    """
    Initializes Neo4j graph database with schema and constraints.

    Graph Structure:
    - (:Empire) nodes for political entities
    - (:Prophecy) nodes for prophetic texts
    - (:Pattern) nodes for recurring historical patterns
    - Various relationships connecting these entities
    """

    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    def close(self):
        """Close database connection."""
        self.driver.close()

    def create_constraints(self):
        """
        Create uniqueness constraints and indexes.
        This ensures data integrity and query performance.
        """
        with self.driver.session() as session:
            # Empire constraints
            session.run(
                """
                CREATE CONSTRAINT empire_name_unique IF NOT EXISTS
                FOR (e:Empire) REQUIRE e.name IS UNIQUE
                """
            )

            # Prophecy constraints
            session.run(
                """
                CREATE CONSTRAINT prophecy_reference_unique IF NOT EXISTS
                FOR (p:Prophecy) REQUIRE p.reference IS UNIQUE
                """
            )

            # Pattern constraints
            session.run(
                """
                CREATE CONSTRAINT pattern_name_unique IF NOT EXISTS
                FOR (pt:Pattern) REQUIRE pt.name IS UNIQUE
                """
            )

            # Event constraints
            session.run(
                """
                CREATE CONSTRAINT event_id_unique IF NOT EXISTS
                FOR (e:Event) REQUIRE e.event_id IS UNIQUE
                """
            )

            print("✓ Neo4j constraints created")

    def create_indexes(self):
        """Create indexes for common query patterns."""
        with self.driver.session() as session:
            # Index on year ranges for temporal queries
            session.run(
                """
                CREATE INDEX empire_year_start IF NOT EXISTS
                FOR (e:Empire) ON (e.year_start)
                """
            )

            session.run(
                """
                CREATE INDEX event_year IF NOT EXISTS
                FOR (e:Event) ON (e.year)
                """
            )

            print("✓ Neo4j indexes created")

    def seed_empire_succession(self):
        """
        Seed Daniel's empire succession: Babylon → Persia → Greece → Rome.
        This is the foundational prophetic framework for the entire system.
        """
        with self.driver.session() as session:
            # Create empires
            session.run(
                """
                MERGE (babylon:Empire {name: 'Babylon'})
                SET babylon.year_start = -626,
                    babylon.year_end = -539,
                    babylon.description = 'Neo-Babylonian Empire; first kingdom in Daniel 2',
                    babylon.daniel_kingdom = 'gold_head',
                    babylon.biblical_reference = 'Daniel 2:37-38'

                MERGE (persia:Empire {name: 'Medo-Persia'})
                SET persia.year_start = -539,
                    persia.year_end = -331,
                    persia.description = 'Persian Empire; second kingdom in Daniel 2',
                    persia.daniel_kingdom = 'silver_chest_arms',
                    persia.biblical_reference = 'Daniel 2:39a'

                MERGE (greece:Empire {name: 'Greece'})
                SET greece.year_start = -331,
                    greece.year_end = -63,
                    greece.description = 'Hellenistic Empire under Alexander and successors; third kingdom',
                    greece.daniel_kingdom = 'bronze_belly_thighs',
                    greece.biblical_reference = 'Daniel 2:39b'

                MERGE (rome:Empire {name: 'Rome'})
                SET rome.year_start = -63,
                    rome.year_end = 476,
                    rome.description = 'Roman Empire; fourth kingdom in Daniel 2',
                    rome.daniel_kingdom = 'iron_legs',
                    rome.biblical_reference = 'Daniel 2:40'

                MERGE (rome_divided:Empire {name: 'Divided Rome'})
                SET rome_divided.year_start = 476,
                    rome_divided.year_end = -1,
                    rome_divided.description = 'Post-Roman fragmentation; iron mixed with clay',
                    rome_divided.daniel_kingdom = 'feet_iron_clay',
                    rome_divided.biblical_reference = 'Daniel 2:41-43'

                // Create succession relationships
                MERGE (babylon)-[:SUCCEEDED_BY {year: -539, mechanism: 'conquest'}]->(persia)
                MERGE (persia)-[:SUCCEEDED_BY {year: -331, mechanism: 'conquest'}]->(greece)
                MERGE (greece)-[:SUCCEEDED_BY {year: -63, mechanism: 'conquest'}]->(rome)
                MERGE (rome)-[:FRAGMENTED_INTO {year: 476, mechanism: 'collapse'}]->(rome_divided)
                """
            )

            print("✓ Daniel's empire succession seeded in Neo4j")

    def seed_recapitulation_patterns(self):
        """
        Seed recurring patterns that echo across eras.
        These are templates that help identify historical analogs.
        """
        with self.driver.session() as session:
            session.run(
                """
                // Pattern: Moral Decay → Judgment
                MERGE (p1:Pattern {name: 'Moral Decay Leads to Judgment'})
                SET p1.description = 'Societies that reject moral standards face collapse',
                    p1.biblical_basis = 'Genesis 6-7 (Flood), Judges cycle, Prophetic warnings',
                    p1.indicators = ['increasing_violence', 'sexual_immorality', 'injustice', 'idolatry'],
                    p1.outcome = 'divine_judgment_or_natural_collapse'

                // Pattern: Pride → Humbling
                MERGE (p2:Pattern {name: 'Pride Precedes Fall'})
                SET p2.description = 'Nations or individuals who exalt themselves are brought low',
                    p2.biblical_basis = 'Proverbs 16:18, Babel, Nebuchadnezzar, Herod',
                    p2.indicators = ['imperial_overreach', 'self_deification', 'hubris'],
                    p2.outcome = 'sudden_downfall'

                // Pattern: Exile → Restoration
                MERGE (p3:Pattern {name: 'Exile and Restoration'})
                SET p3.description = 'Displacement followed by return and rebuilding',
                    p3.biblical_basis = 'Babylonian exile, Egyptian bondage',
                    p3.indicators = ['foreign_oppression', 'prophetic_hope', 'remnant_preservation'],
                    p3.outcome = 'eventual_return_and_renewal'

                // Pattern: Persecution → Growth
                MERGE (p4:Pattern {name: 'Persecution Strengthens Faith'})
                SET p4.description = 'Opposition to faith leads to its spread and purification',
                    p4.biblical_basis = 'Early church persecution, Daniel in Babylon',
                    p4.indicators = ['state_hostility', 'martyrdom', 'underground_growth'],
                    p4.outcome = 'expansion_through_suffering'

                // Pattern: Unity → Fragmentation
                MERGE (p5:Pattern {name: 'Political Unity Followed by Fragmentation'})
                SET p5.description = 'United empires inevitably divide',
                    p5.biblical_basis = 'United → Divided Kingdom, Roman Empire division',
                    p5.indicators = ['succession_disputes', 'regional_autonomy', 'elite_conflict'],
                    p5.outcome = 'multiple_weaker_successor_states'

                // Pattern: Prophetic Fulfillment Delay
                MERGE (p6:Pattern {name: 'Delayed Fulfillment with Multiple Echoes'})
                SET p6.description = 'Prophecies often have near and far fulfillments',
                    p6.biblical_basis = 'Isaiah 7:14, Joel 2, Olivet Discourse',
                    p6.indicators = ['partial_fulfillment', 'typological_recurrence'],
                    p6.outcome = 'ultimate_complete_fulfillment'
                """
            )

            print("✓ Recapitulation patterns seeded in Neo4j")

    def link_patterns_to_empires(self):
        """
        Connect historical patterns to specific empire instances.
        This demonstrates where patterns manifested in history.
        """
        with self.driver.session() as session:
            session.run(
                """
                MATCH (babylon:Empire {name: 'Babylon'})
                MATCH (pride:Pattern {name: 'Pride Precedes Fall'})
                MERGE (babylon)-[:EXEMPLIFIES {
                    strength: 10,
                    example: 'Nebuchadnezzar\'s seven years of madness',
                    biblical_ref: 'Daniel 4'
                }]->(pride)

                MATCH (rome:Empire {name: 'Rome'})
                MATCH (unity_frag:Pattern {name: 'Political Unity Followed by Fragmentation'})
                MERGE (rome)-[:EXEMPLIFIES {
                    strength: 9,
                    example: 'Division into Eastern and Western empires, then further fragmentation',
                    year: 395
                }]->(unity_frag)

                MATCH (persia:Empire {name: 'Medo-Persia'})
                MATCH (exile:Pattern {name: 'Exile and Restoration'})
                MERGE (persia)-[:FACILITATES {
                    strength: 10,
                    example: 'Cyrus decree allowing Jewish return',
                    biblical_ref: 'Ezra 1:1-4'
                }]->(exile)
                """
            )

            print("✓ Patterns linked to empires")

    def initialize_all(self):
        """Run all initialization steps."""
        print("\n" + "=" * 60)
        print("Initializing Neo4j Graph Database")
        print("=" * 60 + "\n")

        self.create_constraints()
        self.create_indexes()
        self.seed_empire_succession()
        self.seed_recapitulation_patterns()
        self.link_patterns_to_empires()

        print("\n" + "=" * 60)
        print("✓ Neo4j initialization complete")
        print("=" * 60 + "\n")

        self.close()


if __name__ == "__main__":
    initializer = Neo4jInitializer()
    initializer.initialize_all()
