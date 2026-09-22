import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_teacher_login_returns_token():
    response = client.post("/teacher/login", json={"username": "teacher", "password": "secret"})

    assert response.status_code == 200
    body = response.json()
    assert "token" in body
    assert body["token"]


def test_student_signup_requires_teacher_login():
    response = client.post("/activities/Chess Club/signup?email=student@mergington.edu")

    assert response.status_code == 403
    assert response.json()["detail"] == "Teacher login required"


def test_teacher_can_register_student():
    login_response = client.post("/teacher/login", json={"username": "teacher", "password": "secret"})
    token = login_response.json()["token"]

    response = client.post(
        "/activities/Chess Club/signup?email=student-allowed@mergington.edu",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up student-allowed@mergington.edu for Chess Club"
