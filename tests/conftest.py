
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

_initial_activities = copy.deepcopy(activities)

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset the activities dict before each test
    activities.clear()
    activities.update(copy.deepcopy(_initial_activities))

@pytest.fixture
def client():
    return TestClient(app)
