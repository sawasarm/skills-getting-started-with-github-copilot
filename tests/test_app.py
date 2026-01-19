import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    response = client.post("/activities/Chess Club/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Clean up: remove test participant
    data = client.get("/activities").json()
    data["Chess Club"]["participants"].remove("tester@mergington.edu")

def test_signup_duplicate():
    # Add participant first
    client.post("/activities/Chess Club/signup?email=dupe@mergington.edu")
    # Try duplicate
    response = client.post("/activities/Chess Club/signup?email=dupe@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"
    # Clean up
    data = client.get("/activities").json()
    data["Chess Club"]["participants"].remove("dupe@mergington.edu")
