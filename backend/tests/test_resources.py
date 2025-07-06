"""
Script Name : test_resources.py
Description : Contains automated tests for the Resourcify API's resource CRUD endpoints using Pytest.
Usage       : Run tests with `pytest` command
Author      : @tonybnya
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.models.resource import Resource  # Add this import
from app.main import app

# Use SQLite in-memory database for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Override the get_db dependency for tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Create tables before tests
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)


def test_api_info():
    res = client.get("/api/v1/")
    assert res.status_code == 200, "Expected 200 OK for API info endpoint"
    json_data = res.json()
    assert "Resourcify API" in json_data.get("name", ""), "API name missing in response"


def test_create_resource():
    payload = {
        "name": "Postman",
        "category": "API Testing",
        "platform": "Web",
        "cost": "Freemium",
        "description": "API testing platform",
        "tags": ["api", "testing", "web"],
    }
    res = client.post("/api/v1/resources/", json=payload)
    assert res.status_code == 200, "Failed to create resource"
    data = res.json()
    assert data["name"] == "Postman"
    assert isinstance(data["id"], int), "Returned resource ID should be an integer"


def test_create_invalid_resource():
    # Missing required 'name' field
    invalid_payload = {
        "platform": "Web"
    }
    res = client.post("/api/v1/resources/", json=invalid_payload)
    assert res.status_code == 422, "Expected validation error for invalid payload"


def test_get_all_resources():
    res = client.get("/api/v1/resources/all")
    assert res.status_code == 200, "Failed to fetch all resources"
    resources = res.json()
    assert isinstance(resources, list), "Response should be a list"
    assert len(resources) >= 1, "There should be at least one resource"


def test_get_single_resource():
    res = client.get("/api/v1/resources/1")
    assert res.status_code == 200, "Failed to fetch resource by ID"
    data = res.json()
    assert data["name"] == "Postman"


def test_update_resource():
    update_payload = {
        "description": "Updated API tool",
        "tags": ["api", "devtools"],
    }
    res = client.put("/api/v1/resources/1", json=update_payload)
    assert res.status_code == 200, "Failed to update resource"
    data = res.json()
    assert data["description"] == "Updated API tool"
    assert "devtools" in data["tags"]


def test_delete_resource():
    res = client.delete("/api/v1/resources/1")
    assert res.status_code == 200, "Failed to delete resource"
    followup = client.get("/api/v1/resources/1")
    assert followup.status_code == 404, "Deleted resource should not be found"

    # Optional: Verify resource is no longer listed
    all_resources = client.get("/api/v1/resources/all").json()
    assert all(str(r["id"]) != "1" for r in all_resources), "Deleted resource ID still found in list"
