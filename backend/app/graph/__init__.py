"""
Neo4j Graph Database Integration
Manages graph relationships between events, patterns, and prophecies.
"""

from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class Neo4jConnection:
    """Neo4j database connection manager."""

    def __init__(self, uri: str, user: str, password: str):
        """Initialize Neo4j connection."""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Close the database connection."""
        if self.driver:
            self.driver.close()

    def verify_connectivity(self) -> bool:
        """Verify connection to Neo4j database."""
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 as num")
                return result.single()["num"] == 1
        except Exception as e:
            logger.error(f"Neo4j connectivity error: {e}")
            return False

    def execute_query(self, query: str, parameters: Optional[Dict] = None) -> List[Dict]:
        """Execute a Cypher query and return results."""
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [dict(record) for record in result]

    def execute_write(self, query: str, parameters: Optional[Dict] = None) -> Any:
        """Execute a write transaction."""
        with self.driver.session() as session:
            return session.write_transaction(lambda tx: tx.run(query, parameters or {}))


class GraphSync:
    """Synchronize PostgreSQL data to Neo4j graph database."""

    def __init__(self, neo4j_conn: Neo4jConnection, postgres_session):
        """Initialize graph sync manager."""
        self.neo4j = neo4j_conn
        self.db = postgres_session

    def initialize_schema(self):
        """Create constraints and indexes in Neo4j."""
        constraints = [
            "CREATE CONSTRAINT event_id IF NOT EXISTS FOR (e:Event) REQUIRE e.id IS UNIQUE",
            "CREATE CONSTRAINT pattern_id IF NOT EXISTS FOR (p:Pattern) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT prophecy_id IF NOT EXISTS FOR (pr:Prophecy) REQUIRE pr.id IS UNIQUE",
            "CREATE CONSTRAINT actor_id IF NOT EXISTS FOR (a:Actor) REQUIRE a.id IS UNIQUE",
        ]

        indexes = [
            "CREATE INDEX event_year IF NOT EXISTS FOR (e:Event) ON (e.year)",
            "CREATE INDEX event_category IF NOT EXISTS FOR (e:Event) ON (e.category)",
            "CREATE INDEX pattern_type IF NOT EXISTS FOR (p:Pattern) ON (p.pattern_type)",
            "CREATE INDEX prophecy_type IF NOT EXISTS FOR (pr:Prophecy) ON (pr.prophecy_type)",
        ]

        for constraint in constraints:
            try:
                self.neo4j.execute_write(constraint)
            except Exception as e:
                logger.warning(f"Constraint creation warning: {e}")

        for index in indexes:
            try:
                self.neo4j.execute_write(index)
            except Exception as e:
                logger.warning(f"Index creation warning: {e}")

    def sync_events(self) -> int:
        """Sync chronology events to Neo4j."""
        from app.models.chronology import ChronologyEvent

        events = self.db.query(ChronologyEvent).all()

        query = """
        MERGE (e:Event {id: $id})
        SET e.name = $name,
            e.year = $year,
            e.year_start = $year_start,
            e.year_end = $year_end,
            e.era = $era,
            e.event_type = $event_type,
            e.description = $description
        """

        count = 0
        for event in events:
            params = {
                "id": event.id,
                "name": event.name,
                "year": event.year_start,  # Use year_start as primary year
                "year_start": event.year_start,
                "year_end": event.year_end,
                "era": str(event.era.value) if event.era else "",
                "event_type": str(event.event_type.value) if event.event_type else "",
                "description": event.description or "",
            }
            self.neo4j.execute_write(query, params)
            count += 1

        logger.info(f"Synced {count} events to Neo4j")
        return count

    def sync_patterns(self) -> int:
        """Sync patterns to Neo4j."""
        from app.models.chronology import Pattern

        patterns = self.db.query(Pattern).all()

        query = """
        MERGE (p:Pattern {id: $id})
        SET p.name = $name,
            p.pattern_type = $pattern_type,
            p.description = $description,
            p.typical_duration_years = $typical_duration_years
        """

        count = 0
        for pattern in patterns:
            params = {
                "id": pattern.id,
                "name": pattern.name,
                "pattern_type": pattern.pattern_type,
                "description": pattern.description or "",
                "typical_duration_years": pattern.typical_duration_years,
            }
            self.neo4j.execute_write(query, params)
            count += 1

        logger.info(f"Synced {count} patterns to Neo4j")
        return count

    def sync_prophecies(self) -> int:
        """Sync prophecies to Neo4j."""
        from app.models.prophecy import ProphecyText

        prophecies = self.db.query(ProphecyText).all()

        query = """
        MERGE (pr:Prophecy {id: $id})
        SET pr.reference = $reference,
            pr.prophecy_type = $prophecy_type,
            pr.year_declared = $year_declared,
            pr.prophet = $prophet,
            pr.scope = $scope,
            pr.text = $text
        """

        count = 0
        for prophecy in prophecies:
            params = {
                "id": prophecy.id,
                "reference": prophecy.reference,
                "prophecy_type": prophecy.prophecy_type or "",
                "year_declared": prophecy.year_declared,
                "prophet": prophecy.prophet or "",
                "scope": prophecy.scope or "",
                "text": prophecy.text[:500] if prophecy.text else "",  # Truncate for graph
            }
            self.neo4j.execute_write(query, params)
            count += 1

        logger.info(f"Synced {count} prophecies to Neo4j")
        return count

    def sync_actors(self) -> int:
        """Sync actors to Neo4j."""
        from app.models.chronology import Actor

        actors = self.db.query(Actor).all()

        query = """
        MERGE (a:Actor {id: $id})
        SET a.name = $name,
            a.actor_type = $actor_type,
            a.description = $description
        """

        count = 0
        for actor in actors:
            params = {
                "id": actor.id,
                "name": actor.name,
                "actor_type": actor.actor_type,
                "description": actor.description or "",
            }
            self.neo4j.execute_write(query, params)
            count += 1

        logger.info(f"Synced {count} actors to Neo4j")
        return count

    def sync_event_patterns(self) -> int:
        """Sync event-pattern relationships."""
        from app.models.chronology import ChronologyEvent, Pattern
        from sqlalchemy import text

        # Query the join table directly
        query_sql = text("SELECT event_id, pattern_id FROM event_patterns")
        results = self.db.execute(query_sql).fetchall()

        cypher_query = """
        MATCH (e:Event {id: $event_id})
        MATCH (p:Pattern {id: $pattern_id})
        MERGE (e)-[r:MATCHES_PATTERN]->(p)
        """

        count = 0
        for row in results:
            params = {
                "event_id": row[0],
                "pattern_id": row[1],
            }
            self.neo4j.execute_write(cypher_query, params)
            count += 1

        logger.info(f"Synced {count} event-pattern relationships to Neo4j")
        return count

    def sync_prophecy_fulfillments(self) -> int:
        """Sync prophecy-event fulfillment relationships."""
        from app.models.prophecy import ProphecyFulfillment

        fulfillments = self.db.query(ProphecyFulfillment).all()

        query = """
        MATCH (pr:Prophecy {id: $prophecy_id})
        MATCH (e:Event {id: $event_id})
        MERGE (pr)-[r:FULFILLED_BY {
            fulfillment_type: $fulfillment_type,
            confidence_score: $confidence_score,
            elements_fulfilled: $elements_fulfilled
        }]->(e)
        """

        count = 0
        for fulfillment in fulfillments:
            params = {
                "prophecy_id": fulfillment.prophecy_id,
                "event_id": fulfillment.event_id,
                "fulfillment_type": fulfillment.fulfillment_type,
                "confidence_score": fulfillment.confidence_score,
                "elements_fulfilled": str(fulfillment.elements_fulfilled or []),
            }
            self.neo4j.execute_write(query, params)
            count += 1

        logger.info(f"Synced {count} prophecy fulfillments to Neo4j")
        return count

    def sync_event_actors(self) -> int:
        """Sync event-actor relationships."""
        from sqlalchemy import text

        # Query the join table directly
        query_sql = text("SELECT event_id, actor_id FROM event_actors")
        results = self.db.execute(query_sql).fetchall()

        cypher_query = """
        MATCH (e:Event {id: $event_id})
        MATCH (a:Actor {id: $actor_id})
        MERGE (a)-[r:INVOLVED_IN]->(e)
        """

        count = 0
        for row in results:
            params = {
                "event_id": row[0],
                "actor_id": row[1],
            }
            self.neo4j.execute_write(cypher_query, params)
            count += 1

        logger.info(f"Synced {count} event-actor relationships to Neo4j")
        return count

    def sync_temporal_relationships(self) -> int:
        """Create PRECEDED_BY relationships between chronologically adjacent events."""
        query = """
        MATCH (e1:Event)
        MATCH (e2:Event)
        WHERE e1.year < e2.year
        WITH e1, e2, e2.year - e1.year AS year_diff
        ORDER BY year_diff
        WITH e1, collect(e2)[0] AS next_event
        WHERE next_event IS NOT NULL
        MERGE (e1)-[r:PRECEDED_BY {
            years_between: next_event.year - e1.year
        }]->(next_event)
        """

        self.neo4j.execute_write(query)
        logger.info("Created temporal PRECEDED_BY relationships")
        return 1

    def sync_all(self) -> Dict[str, int]:
        """Sync all data from PostgreSQL to Neo4j."""
        logger.info("Starting full graph sync...")

        self.initialize_schema()

        results = {
            "events": self.sync_events(),
            "patterns": self.sync_patterns(),
            "prophecies": self.sync_prophecies(),
            "actors": self.sync_actors(),
            "event_patterns": self.sync_event_patterns(),
            "prophecy_fulfillments": self.sync_prophecy_fulfillments(),
            "event_actors": self.sync_event_actors(),
        }

        # Create temporal relationships
        self.sync_temporal_relationships()

        logger.info(f"Graph sync complete: {results}")
        return results


class GraphAnalyzer:
    """Analyze graph relationships and extract insights."""

    def __init__(self, neo4j_conn: Neo4jConnection):
        """Initialize graph analyzer."""
        self.neo4j = neo4j_conn

    def find_event_chains(self, min_length: int = 3) -> List[Dict]:
        """Find chains of connected events."""
        query = f"""
        MATCH path = (e1:Event)-[:PRECEDED_BY*{min_length}..10]->(e2:Event)
        RETURN [node in nodes(path) | {{
            id: node.id,
            name: node.name,
            year: node.year
        }}] AS chain,
        length(path) AS chain_length
        ORDER BY chain_length DESC
        LIMIT 20
        """

        return self.neo4j.execute_query(query, {"min_length": min_length})

    def find_pattern_clusters(self) -> List[Dict]:
        """Find events that share multiple patterns."""
        query = """
        MATCH (e1:Event)-[:MATCHES_PATTERN]->(p:Pattern)<-[:MATCHES_PATTERN]-(e2:Event)
        WHERE e1.id < e2.id
        WITH e1, e2, collect(p.name) AS shared_patterns
        WHERE size(shared_patterns) > 1
        RETURN e1.name AS event1,
               e1.year AS year1,
               e2.name AS event2,
               e2.year AS year2,
               shared_patterns,
               size(shared_patterns) AS pattern_count
        ORDER BY pattern_count DESC
        LIMIT 20
        """

        return self.neo4j.execute_query(query)

    def find_prophecy_networks(self) -> List[Dict]:
        """Find prophecies fulfilled by related events."""
        query = """
        MATCH (pr1:Prophecy)-[:FULFILLED_BY]->(e:Event)<-[:FULFILLED_BY]-(pr2:Prophecy)
        WHERE pr1.id < pr2.id
        RETURN pr1.reference AS prophecy1,
               pr2.reference AS prophecy2,
               e.name AS shared_event,
               e.year AS event_year
        ORDER BY e.year
        """

        return self.neo4j.execute_query(query)

    def find_influential_events(self, limit: int = 10) -> List[Dict]:
        """Find events with the most connections (patterns + fulfillments)."""
        query = """
        MATCH (e:Event)
        OPTIONAL MATCH (e)-[:MATCHES_PATTERN]->(p:Pattern)
        OPTIONAL MATCH (pr:Prophecy)-[:FULFILLED_BY]->(e)
        WITH e,
             count(DISTINCT p) AS pattern_count,
             count(DISTINCT pr) AS prophecy_count
        RETURN e.id AS event_id,
               e.name AS event_name,
               e.year AS year,
               e.event_type AS event_type,
               pattern_count,
               prophecy_count,
               pattern_count + prophecy_count AS total_connections
        ORDER BY total_connections DESC
        LIMIT $limit
        """

        return self.neo4j.execute_query(query, {"limit": limit})

    def find_pattern_evolution(self, pattern_id: int) -> List[Dict]:
        """Trace how a pattern manifests across time."""
        query = """
        MATCH (p:Pattern {id: $pattern_id})<-[:MATCHES_PATTERN]-(e:Event)
        RETURN e.id AS event_id,
               e.name AS event_name,
               e.year AS year,
               e.event_type AS event_type,
               e.description AS description
        ORDER BY e.year
        """

        return self.neo4j.execute_query(query, {"pattern_id": pattern_id})

    def find_shortest_path(self, event1_id: int, event2_id: int) -> Dict:
        """Find shortest path between two events."""
        query = """
        MATCH (e1:Event {id: $event1_id})
        MATCH (e2:Event {id: $event2_id})
        MATCH path = shortestPath((e1)-[*]-(e2))
        RETURN [node in nodes(path) | {
            id: node.id,
            name: node.name,
            year: node.year,
            type: labels(node)[0]
        }] AS path_nodes,
        [rel in relationships(path) | type(rel)] AS relationship_types,
        length(path) AS path_length
        """

        results = self.neo4j.execute_query(
            query, {"event1_id": event1_id, "event2_id": event2_id}
        )
        return results[0] if results else {}

    def get_graph_statistics(self) -> Dict[str, Any]:
        """Get overall graph statistics."""
        queries = {
            "total_events": "MATCH (e:Event) RETURN count(e) AS count",
            "total_patterns": "MATCH (p:Pattern) RETURN count(p) AS count",
            "total_prophecies": "MATCH (pr:Prophecy) RETURN count(pr) AS count",
            "total_actors": "MATCH (a:Actor) RETURN count(a) AS count",
            "total_relationships": "MATCH ()-[r]->() RETURN count(r) AS count",
            "avg_connections_per_event": """
                MATCH (e:Event)
                OPTIONAL MATCH (e)-[r]-()
                WITH e, count(r) AS connections
                RETURN avg(connections) AS avg_connections
            """,
        }

        stats = {}
        for key, query in queries.items():
            result = self.neo4j.execute_query(query)
            if key == "avg_connections_per_event":
                stats[key] = round(result[0].get("avg_connections", 0), 2)
            else:
                stats[key] = result[0].get("count", 0)

        return stats
