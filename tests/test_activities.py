import pytest
from fastapi import status

# AAA: Arrange-Act-Assert pattern is used in all tests

def test_get_activities(client):
    # Arrange: (nothing to arrange for this test)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert f"Signed up {email} for {activity}" in response.json()["message"]

    # Cleanup: Remove the test participant
    client.delete(f"/activities/{activity}/unregister", params={"email": email})

def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already registered
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Activity not found" in response.json()["detail"]

def test_unregister_success(client):
    # Arrange
    activity = "Chess Club"
    email = "tempuser@mergington.edu"
    # Add user first
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert f"Unregistered {email} from {activity}" in response.json()["message"]

def test_unregister_not_registered(client):
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "not registered" in response.json()["detail"]

def test_unregister_nonexistent_activity(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Activity not found" in response.json()["detail"]
