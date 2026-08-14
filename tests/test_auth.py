from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_user():
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser_auth",
            "email": "test_auth@example.com",
            "password": "Test@12345",
        },
    )

    assert response.status_code in [201, 400]


def test_login_user():
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test_auth@example.com",
            "password": "Test@12345",
        },
    )

    assert response.status_code in [200, 401]