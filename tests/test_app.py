import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

# Test POST /activities/{activity_name}/signup
@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "testuser@mergington.edu"),
])
def test_signup_for_activity(activity, email):
    # Remove if exists
    client.delete(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Try duplicate
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400

# Test DELETE /activities/{activity_name}/signup
@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "testuser@mergington.edu"),
])
def test_remove_participant(activity, email):
    # Ensure exists
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]
    # Try removing again
    response_missing = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response_missing.status_code == 404
