"""
Tests for the POST /activities/{activity_name}/unregister endpoint.
"""

import pytest


def test_unregister_from_activity_success(client):
    """
    Test that a student can successfully unregister from an activity.
    """
    response = client.post(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Unregistered michael@mergington.edu from Chess Club"


def test_unregister_removes_participant(client):
    """
    Test that unregistering removes the student from the participants list.
    """
    # Unregister existing participant
    client.post("/activities/Chess Club/unregister?email=michael@mergington.edu")
    
    # Verify participant was removed
    response = client.get("/activities")
    activities = response.json()
    
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert len(activities["Chess Club"]["participants"]) == 1


def test_unregister_activity_not_found(client):
    """
    Test that unregistering from a non-existent activity returns 404.
    """
    response = client.post(
        "/activities/Non Existent Club/unregister?email=student@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_student_not_registered(client):
    """
    Test that unregistering a student who is not signed up returns 400.
    """
    response = client.post(
        "/activities/Chess Club/unregister?email=notstudent@mergington.edu"
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student is not registered for this activity"


def test_unregister_then_signup_again(client):
    """
    Test that a student can unregister and then sign up again.
    """
    email = "michael@mergington.edu"
    
    # Unregister
    response1 = client.post(
        f"/activities/Chess Club/unregister?email={email}"
    )
    assert response1.status_code == 200
    
    # Sign up again
    response2 = client.post(
        f"/activities/Chess Club/signup?email={email}"
    )
    assert response2.status_code == 200
    
    # Verify they're in the participants list
    response3 = client.get("/activities")
    activities = response3.json()
    assert email in activities["Chess Club"]["participants"]


def test_unregister_multiple_students_same_activity(client):
    """
    Test that multiple students can unregister from the same activity.
    """
    # Chess Club has ["michael@mergington.edu", "daniel@mergington.edu"]
    client.post("/activities/Chess Club/unregister?email=michael@mergington.edu")
    client.post("/activities/Chess Club/unregister?email=daniel@mergington.edu")
    
    response = client.get("/activities")
    activities = response.json()
    
    assert len(activities["Chess Club"]["participants"]) == 0


def test_cannot_unregister_same_student_twice(client):
    """
    Test that unregistering the same student twice fails on the second attempt.
    """
    email = "michael@mergington.edu"
    
    # First unregister should succeed
    response1 = client.post(
        f"/activities/Chess Club/unregister?email={email}"
    )
    assert response1.status_code == 200
    
    # Second unregister should fail
    response2 = client.post(
        f"/activities/Chess Club/unregister?email={email}"
    )
    assert response2.status_code == 400
    data = response2.json()
    assert data["detail"] == "Student is not registered for this activity"


def test_unregister_from_different_activities(client):
    """
    Test that a student can unregister from multiple activities.
    """
    email = "michael@mergington.edu"
    
    # Add student to multiple activities
    client.post(f"/activities/Programming Class/signup?email={email}")
    client.post(f"/activities/Gym Class/signup?email={email}")
    
    # Unregister from some activities
    client.post(f"/activities/Chess Club/unregister?email={email}")
    client.post(f"/activities/Programming Class/unregister?email={email}")
    
    response = client.get("/activities")
    activities = response.json()
    
    assert email not in activities["Chess Club"]["participants"]
    assert email not in activities["Programming Class"]["participants"]
    assert email in activities["Gym Class"]["participants"]
