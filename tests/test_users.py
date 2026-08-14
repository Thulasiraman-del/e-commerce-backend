from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_current_user():
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "test_auth@example.com",
            "password": "Test@12345",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "testuser_auth"
    assert data["email"] == "test_auth@example.com"
    assert "id" in data
    assert "is_active" in data
    assert "created_at" in data