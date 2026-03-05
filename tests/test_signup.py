"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_for_activity_success(client):
    """
    Test that a student can successfully sign up for an activity.
    """
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Signed up newstudent@mergington.edu for Chess Club"


def test_signup_updates_participant_list(client):
    """
    Test that signing up for an activity adds the student to the participants list.
    """
    # Sign up new student
    client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
    
    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]
    assert len(activities["Chess Club"]["participants"]) == 3


def test_signup_activity_not_found(client):
    """
    Test that signing up for a non-existent activity returns 404.
    """
    response = client.post(
        "/activities/Non Existent Club/signup?email=student@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_student_already_signed_up(client):
    """
    Test that a student cannot sign up for the same activity twice.
    """
    # First signup should succeed
    response1 = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    assert response1.status_code == 200
    
    # Second signup should fail
    response2 = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    
    assert response2.status_code == 400
    data = response2.json()
    assert data["detail"] == "Student already signed up for this activity"


def test_signup_existing_participant_still_cannot_resign(client):
    """
    Test that an existing participant cannot sign up again.
    """
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"


def test_signup_multiple_students_same_activity(client):
    """
    Test that multiple students can sign up for the same activity.
    """
    client.post("/activities/Chess Club/signup?email=student1@mergington.edu")
    client.post("/activities/Chess Club/signup?email=student2@mergington.edu")
    client.post("/activities/Chess Club/signup?email=student3@mergington.edu")
    
    response = client.get("/activities")
    activities = response.json()
    
    assert "student1@mergington.edu" in activities["Chess Club"]["participants"]
    assert "student2@mergington.edu" in activities["Chess Club"]["participants"]
    assert "student3@mergington.edu" in activities["Chess Club"]["participants"]
    assert len(activities["Chess Club"]["participants"]) == 5


def test_signup_student_can_join_multiple_activities(client):
    """
    Test that a student can sign up for multiple different activities.
    """
    student_email = "versatile@mergington.edu"
    
    # Sign up for multiple activities
    client.post(f"/activities/Chess Club/signup?email={student_email}")
    client.post(f"/activities/Programming Class/signup?email={student_email}")
    client.post(f"/activities/Basketball Team/signup?email={student_email}")
    
    response = client.get("/activities")
    activities = response.json()
    
    assert student_email in activities["Chess Club"]["participants"]
    assert student_email in activities["Programming Class"]["participants"]
    assert student_email in activities["Basketball Team"]["participants"]
