"""
Basic API tests to verify system functionality.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    """Create test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root_endpoint():
    """Test root endpoint returns system information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Sigandwa"
    assert "version" in data


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_get_timeline_summary(test_db):
    """Test timeline summary endpoint."""
    response = client.get("/api/v1/chronology/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_events" in data
    assert "era_distribution" in data
    assert "type_distribution" in data


def test_create_event(test_db):
    """Test creating a new chronology event."""
    event_data = {
        "name": "Test Event",
        "year_start": -1000,
        "era": "UNITED_MONARCHY",
        "event_type": "RELIGIOUS",
        "description": "A test event",
    }

    response = client.post("/api/v1/chronology/events", json=event_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Event"
    assert data["year_start"] == -1000


def test_get_events_by_era(test_db):
    """Test filtering events by era."""
    # First create a test event
    event_data = {
        "name": "Test Monarchy Event",
        "year_start": -1000,
        "era": "UNITED_MONARCHY",
        "event_type": "POLITICAL",
    }
    client.post("/api/v1/chronology/events", json=event_data)

    # Query by era
    response = client.get("/api/v1/chronology/events?era=UNITED_MONARCHY")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
