"""
Graph Analysis API Endpoints
Provides Neo4j graph query capabilities for relationship analysis.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from app.database import get_db
from app.config import settings
from app.graph import Neo4jConnection, GraphSync, GraphAnalyzer

router = APIRouter()


# Global Neo4j connection (initialized on first use)
_neo4j_conn = None


def get_neo4j() -> Neo4jConnection:
    """Get or create Neo4j connection."""
    global _neo4j_conn
    if _neo4j_conn is None:
        _neo4j_conn = Neo4jConnection(
            uri=settings.NEO4J_URI,
            user=settings.NEO4J_USER,
            password=settings.NEO4J_PASSWORD,
        )
    return _neo4j_conn


# ============================================================================
# Response Models
# ============================================================================


class GraphSyncResponse(BaseModel):
    """Response for graph sync operations."""

    success: bool
    synced: Dict[str, int]
    message: str


class GraphStatsResponse(BaseModel):
    """Response for graph statistics."""

    total_events: int
    total_patterns: int
    total_prophecies: int
    total_actors: int
    total_relationships: int
    avg_connections_per_event: float


class EventChainResponse(BaseModel):
    """Response for event chain queries."""

    chain: List[Dict[str, Any]]
    chain_length: int


class PatternClusterResponse(BaseModel):
    """Response for pattern cluster analysis."""

    event1: str
    year1: int
    event2: str
    year2: int
    shared_patterns: List[str]
    pattern_count: int


class InfluentialEventResponse(BaseModel):
    """Response for influential event analysis."""

    event_id: int
    event_name: str
    year: int
    event_type: str
    pattern_count: int
    prophecy_count: int
    total_connections: int


class PathResponse(BaseModel):
    """Response for shortest path queries."""

    path_nodes: List[Dict[str, Any]]
    relationship_types: List[str]
    path_length: int


# ============================================================================
# Endpoints
# ============================================================================


@router.get("/health")
def check_neo4j_health():
    """Check Neo4j connectivity."""
    neo4j = get_neo4j()
    is_connected = neo4j.verify_connectivity()

    return {
        "neo4j_connected": is_connected,
        "uri": settings.NEO4J_URI,
        "status": "healthy" if is_connected else "unavailable",
    }


@router.post("/sync", response_model=GraphSyncResponse)
def sync_graph(db: Session = Depends(get_db)):
    """
    Synchronize PostgreSQL data to Neo4j graph database.

    This creates nodes and relationships for:
    - Events
    - Patterns
    - Prophecies
    - Actors
    - All relationships (pattern matches, fulfillments, temporal connections)
    """
    try:
        neo4j = get_neo4j()
        sync = GraphSync(neo4j, db)

        synced = sync.sync_all()

        return GraphSyncResponse(
            success=True,
            synced=synced,
            message=f"Successfully synced {sum(synced.values())} items to Neo4j graph",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph sync failed: {str(e)}")


@router.get("/stats", response_model=GraphStatsResponse)
def get_graph_stats():
    """Get overall graph database statistics."""
    try:
        neo4j = get_neo4j()
        analyzer = GraphAnalyzer(neo4j)

        stats = analyzer.get_graph_statistics()

        return GraphStatsResponse(**stats)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve graph stats: {str(e)}"
        )


@router.get("/event-chains", response_model=List[EventChainResponse])
def get_event_chains(
    min_length: int = Query(3, description="Minimum chain length", ge=2, le=10)
):
    """
    Find chains of temporally connected events.

    Returns sequences of events connected by PRECEDED_BY relationships,
    showing historical progressions and cause-effect chains.
    """
    try:
        neo4j = get_neo4j()
        analyzer = GraphAnalyzer(neo4j)

        chains = analyzer.find_event_chains(min_length=min_length)

        return [EventChainResponse(**chain) for chain in chains]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to find event chains: {str(e)}"
        )


@router.get("/pattern-clusters", response_model=List[PatternClusterResponse])
def get_pattern_clusters():
    """
    Find events that share multiple patterns.

    Identifies events with similar characteristics by analyzing
    which patterns they match, revealing thematic connections
    across different historical periods.
    """
    try:
        neo4j = get_neo4j()
        analyzer = GraphAnalyzer(neo4j)

        clusters = analyzer.find_pattern_clusters()

        return [PatternClusterResponse(**cluster) for cluster in clusters]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to find pattern clusters: {str(e)}"
        )


@router.get("/prophecy-networks")
def get_prophecy_networks():
    """
    Find prophecies connected through shared fulfillment events.

    Reveals how different prophecies converge on the same historical
    events, showing prophetic interconnectedness.
    """
    try:
        neo4j = get_neo4j()
        analyzer = GraphAnalyzer(neo4j)

        networks = analyzer.find_prophecy_networks()

        return {"total_connections": len(networks), "connections": networks}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to find prophecy networks: {str(e)}"
        )


@router.get("/influential-events", response_model=List[InfluentialEventResponse])
def get_influential_events(
    limit: int = Query(10, description="Number of events to return", ge=1, le=50)
):
    """
    Find the most influential events based on connections.

    Ranks events by the number of patterns they match and
    prophecies they fulfill, identifying pivotal moments in history.
    """
    try:
        neo4j = get_neo4j()
        analyzer = GraphAnalyzer(neo4j)

        events = analyzer.find_influential_events(limit=limit)

        return [InfluentialEventResponse(**event) for event in events]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to find influential events: {str(e)}"
        )


@router.get("/pattern-evolution/{pattern_id}")
def get_pattern_evolution(pattern_id: int):
    """
    Trace how a specific pattern manifests across time.

    Shows all historical instances of a pattern in chronological order,
    revealing recurrence cycles and pattern development.
    """
    try:
        neo4j = get_neo4j()
        analyzer = GraphAnalyzer(neo4j)

        evolution = analyzer.find_pattern_evolution(pattern_id)

        return {
            "pattern_id": pattern_id,
            "total_instances": len(evolution),
            "chronological_instances": evolution,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to trace pattern evolution: {str(e)}"
        )


@router.get("/shortest-path", response_model=PathResponse)
def get_shortest_path(
    event1_id: int = Query(..., description="First event ID"),
    event2_id: int = Query(..., description="Second event ID"),
):
    """
    Find the shortest path between two events in the graph.

    Returns the connection path, showing how events are related
    through patterns, prophecies, and temporal relationships.
    """
    try:
        neo4j = get_neo4j()
        analyzer = GraphAnalyzer(neo4j)

        path = analyzer.find_shortest_path(event1_id, event2_id)

        if not path:
            raise HTTPException(
                status_code=404,
                detail=f"No path found between events {event1_id} and {event2_id}",
            )

        return PathResponse(**path)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to find shortest path: {str(e)}"
        )


@router.post("/query")
def execute_custom_query(
    query: str = Query(..., description="Cypher query to execute"),
    parameters: Optional[Dict[str, Any]] = None,
):
    """
    Execute a custom Cypher query (Advanced users only).

    Allows direct Neo4j Cypher queries for complex analysis.
    Use with caution - only read-only queries are recommended.
    """
    try:
        # Security: Only allow queries starting with MATCH or RETURN
        if not query.strip().upper().startswith(("MATCH", "RETURN", "CALL")):
            raise HTTPException(
                status_code=400,
                detail="Only MATCH, RETURN, and CALL queries are allowed",
            )

        neo4j = get_neo4j()
        results = neo4j.execute_query(query, parameters)

        return {"query": query, "result_count": len(results), "results": results}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Query execution failed: {str(e)}"
        )


@router.delete("/reset")
def reset_graph():
    """
    Delete all nodes and relationships from Neo4j.

    WARNING: This will clear the entire graph database!
    Use before re-syncing or for testing purposes.
    """
    try:
        neo4j = get_neo4j()

        # Delete all nodes and relationships
        neo4j.execute_write("MATCH (n) DETACH DELETE n")

        return {
            "success": True,
            "message": "Graph database cleared. Use /sync to repopulate.",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to reset graph: {str(e)}"
        )
