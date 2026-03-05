"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """
    Test that GET /activities returns all activities with correct structure.
    """
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Verify expected activities are present
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities
    assert "Basketball Team" in activities
    assert "Tennis Club" in activities
    assert "Art Studio" in activities
    assert "Music Band" in activities
    assert "Debate Team" in activities
    assert "Science Club" in activities
    
    assert len(activities) == 9


def test_get_activities_has_correct_structure(client):
    """
    Test that each activity has the expected fields.
    """
    response = client.get("/activities")
    activities = response.json()
    
    # Check structure of an activity
    chess_club = activities["Chess Club"]
    
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_get_activities_participants_populated(client):
    """
    Test that activities have participants populated correctly.
    """
    response = client.get("/activities")
    activities = response.json()
    
    # Chess Club should have 2 participants
    assert len(activities["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]
    
    # Programming Class should have 2 participants
    assert len(activities["Programming Class"]["participants"]) == 2
    assert "emma@mergington.edu" in activities["Programming Class"]["participants"]
    assert "sophia@mergington.edu" in activities["Programming Class"]["participants"]
    
    # Basketball Team should have 1 participant
    assert len(activities["Basketball Team"]["participants"]) == 1
    assert "alex@mergington.edu" in activities["Basketball Team"]["participants"]
