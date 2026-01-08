"""
Neo4j graph database connection management.
"""

from neo4j import GraphDatabase, Driver
from typing import Optional
from contextlib import contextmanager

from app.config import settings


class Neo4jConnection:
    """
    Neo4j database connection manager.
    Handles graph relationships for empires, prophecy fulfillments, and pattern recapitulations.
    """

    def __init__(self):
        self._driver: Optional[Driver] = None

    def connect(self) -> Driver:
        """Establish connection to Neo4j database."""
        if self._driver is None:
            self._driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
            )
        return self._driver

    def close(self):
        """Close Neo4j connection."""
        if self._driver:
            self._driver.close()
            self._driver = None

    @contextmanager
    def session(self):
        """Context manager for Neo4j sessions."""
        driver = self.connect()
        session = driver.session()
        try:
            yield session
        finally:
            session.close()


# Global Neo4j connection instance
neo4j_conn = Neo4jConnection()


def get_neo4j():
    """Dependency for getting Neo4j sessions."""
    return neo4j_conn.session()
