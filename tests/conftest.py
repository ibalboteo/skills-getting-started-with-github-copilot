"""
Pytest configuration and fixtures for FastAPI app tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app
import copy


@pytest.fixture
def client():
    """
    Provides a TestClient instance for making requests to the FastAPI app.
    Each test gets a fresh instance to avoid state pollution.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset activities state before each test to ensure test isolation.
    This fixture automatically runs before every test (autouse=True).
    """
    from src import app as app_module
    
    # Save the original activities state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball training and games",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis skills development and friendly matches",
            "schedule": "Tuesdays and Thursdays, 4:30 PM - 5:30 PM",
            "max_participants": 12,
            "participants": ["jessica@mergington.edu", "marcus@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Music Band": {
            "description": "Join the school band and perform in concerts",
            "schedule": "Tuesdays and Fridays, 3:45 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation skills and compete in debate tournaments",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["zoe@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["ryan@mergington.edu", "maya@mergington.edu"]
        }
    }
    
    # Reset activities to original state before test
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original_activities))
    
    yield
    
    # Clean up after test (optional, but good practice)
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original_activities))
