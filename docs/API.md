# Sigandwa API Reference

## Overview

Sigandwa provides a RESTful API for accessing the Biblical Cliodynamic Analysis System. All endpoints return JSON and follow standard HTTP conventions.

**Base URL**: `http://localhost:8000/api/v1`

---

## Authentication

Currently, the API is open for development. Production deployments should implement authentication.

---

## Endpoints

### System Health

#### `GET /`
Root endpoint with system information.

**Response**:
```json
{
  "name": "Sigandwa",
  "version": "0.1.0",
  "description": "Biblical Cliodynamic Analysis System",
  "docs": "/docs"
}
```

#### `GET /health`
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

---

## Chronology

### Get Events

#### `GET /api/v1/chronology/events`
Retrieve chronology events with optional filtering.

**Query Parameters**:
- `year_start` (integer, optional): Start year (negative for BC)
- `year_end` (integer, optional): End year (negative for BC)
- `era` (string, optional): Filter by era
- `event_type` (string, optional): Filter by event type
- `limit` (integer, optional): Maximum results (default: 100, max: 1000)

**Eras**:
- `CREATION_TO_FLOOD`
- `FLOOD_TO_ABRAHAM`
- `PATRIARCHS`
- `EGYPTIAN_BONDAGE`
- `EXODUS_TO_JUDGES`
- `UNITED_MONARCHY`
- `DIVIDED_KINGDOM`
- `EXILE`
- `POST_EXILE`
- `INTERTESTAMENTAL`
- `NEW_TESTAMENT`
- `EARLY_CHURCH`
- `ROMAN_EMPIRE`
- `MEDIEVAL`
- `REFORMATION`
- `COLONIAL`
- `MODERN`
- `CONTEMPORARY`

**Event Types**:
- `POLITICAL`
- `ECONOMIC`
- `RELIGIOUS`
- `MILITARY`
- `SOCIAL`
- `NATURAL`
- `PROPHETIC`

**Example Request**:
```bash
GET /api/v1/chronology/events?year_start=-1000&year_end=-500&event_type=MILITARY
```

**Example Response**:
```json
[
  {
    "id": 42,
    "name": "Fall of Jerusalem",
    "description": "Nebuchadnezzar destroys Jerusalem and Solomon's Temple",
    "year_start": -586,
    "year_end": null,
    "era": "EXILE",
    "event_type": "MILITARY",
    "biblical_source": "2 Kings 25",
    "metadata": {
      "pattern": "covenant_unfaithfulness_exile",
      "temple_destroyed": true
    }
  }
]
```

---

### Get Single Event

#### `GET /api/v1/chronology/events/{event_id}`
Retrieve a specific event by ID.

**Path Parameters**:
- `event_id` (integer, required): Event ID

**Response**: Single event object

---

### Create Event

#### `POST /api/v1/chronology/events`
Add a new event to the chronology.

**Request Body**:
```json
{
  "name": "Event Name",
  "year_start": -1000,
  "era": "UNITED_MONARCHY",
  "event_type": "POLITICAL",
  "description": "Optional description",
  "year_end": -990,
  "biblical_source": "1 Kings 10",
  "metadata": {}
}
```

**Response**: Created event object with ID

---

### Get Contemporaneous Events

#### `GET /api/v1/chronology/events/{event_id}/contemporaneous`
Find events occurring around the same time as a specified event.

**Path Parameters**:
- `event_id` (integer, required): Reference event ID

**Query Parameters**:
- `window_years` (integer, optional): Years before/after to search (default: 10)

**Example**:
```bash
GET /api/v1/chronology/events/42/contemporaneous?window_years=5
```

**Use Case**: Identify correlations between events in different domains (e.g., political upheaval coinciding with religious reformation).

---

### Get Timeline Summary

#### `GET /api/v1/chronology/summary`
Get statistical summary of the timeline.

**Query Parameters**:
- `start_year` (integer, optional): Start year for summary
- `end_year` (integer, optional): End year for summary

**Response**:
```json
{
  "total_events": 150,
  "era_distribution": {
    "EXILE": 12,
    "UNITED_MONARCHY": 18,
    "NEW_TESTAMENT": 25
  },
  "type_distribution": {
    "POLITICAL": 45,
    "RELIGIOUS": 60,
    "MILITARY": 30
  },
  "year_range": {
    "start": -4004,
    "end": 2026
  }
}
```

---

## Events

*Endpoints under development*

---

## Patterns

*Endpoints under development*

---

## Prophecy

*Endpoints under development*

---

## Simulation

*Endpoints under development*

---

## Error Responses

All endpoints use standard HTTP status codes:

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid parameters
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

**Error Format**:
```json
{
  "detail": "Error message description"
}
```

---

## Interactive Documentation

Sigandwa provides interactive API documentation via Swagger UI:

**Swagger UI**: http://localhost:8000/docs

This interface allows you to:
- Browse all endpoints
- View request/response schemas
- Execute API calls directly from the browser
- Test authentication flows

---

## Rate Limiting

*To be implemented in production*

---

## Examples

### Query Biblical Events in Exile Period

```bash
curl -X GET "http://localhost:8000/api/v1/chronology/events?era=EXILE" \
  -H "accept: application/json"
```

### Find Events Around 586 BC

```bash
curl -X GET "http://localhost:8000/api/v1/chronology/events?year_start=-600&year_end=-570" \
  -H "accept: application/json"
```

### Add Custom Event

```bash
curl -X POST "http://localhost:8000/api/v1/chronology/events" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Custom Historical Event",
    "year_start": -750,
    "era": "DIVIDED_KINGDOM",
    "event_type": "SOCIAL",
    "description": "A significant social development"
  }'
```

---

## Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Get timeline summary
response = requests.get(f"{BASE_URL}/chronology/summary")
summary = response.json()
print(f"Total events: {summary['total_events']}")

# Query specific era
response = requests.get(
    f"{BASE_URL}/chronology/events",
    params={"era": "NEW_TESTAMENT"}
)
events = response.json()
for event in events:
    print(f"{event['year_start']}: {event['name']}")

# Create new event
new_event = {
    "name": "Test Event",
    "year_start": -1000,
    "era": "UNITED_MONARCHY",
    "event_type": "POLITICAL"
}
response = requests.post(
    f"{BASE_URL}/chronology/events",
    json=new_event
)
created = response.json()
print(f"Created event ID: {created['id']}")
```
