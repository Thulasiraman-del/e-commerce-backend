
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_auth_headers():
    unique_id = uuid4().hex[:8]

    username = f"addresstest_{unique_id}"
    email = f"addresstest_{unique_id}@example.com"

    register_response = client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "Test@12345",
        },
    )

    assert register_response.status_code == 201, register_response.text

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "Test@12345",
        },
    )

    assert login_response.status_code == 200, login_response.text

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def create_address(headers):
    response = client.post(
        "/api/addresses/",
        json={
            "address_line": "123 Main Street",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "postal_code": "600001",
            "country": "India",
        },
        headers=headers,
    )

    assert response.status_code == 201, response.text

    return response.json()


def test_create_address():
    headers = get_auth_headers()

    response = client.post(
        "/api/addresses/",
        json={
            "address_line": "123 Main Street",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "postal_code": "600001",
            "country": "India",
        },
        headers=headers,
    )

    assert response.status_code == 201, response.text

    data = response.json()

    assert "id" in data
    assert "user_id" in data
    assert data["address_line"] == "123 Main Street"
    assert data["city"] == "Chennai"
    assert data["state"] == "Tamil Nadu"
    assert data["postal_code"] == "600001"
    assert data["country"] == "India"


def test_get_addresses():
    headers = get_auth_headers()

    create_address(headers)

    response = client.get(
        "/api/addresses/",
        headers=headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_address():
    headers = get_auth_headers()

    address = create_address(headers)
    address_id = address["id"]

    response = client.get(
        f"/api/addresses/{address_id}",
        headers=headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == address_id
    assert data["address_line"] == "123 Main Street"
    assert data["city"] == "Chennai"


def test_delete_address():
    headers = get_auth_headers()

    address = create_address(headers)
    address_id = address["id"]

    response = client.delete(
        f"/api/addresses/{address_id}",
        headers=headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["message"] == "Address deleted successfully"

    get_response = client.get(
        f"/api/addresses/{address_id}",
        headers=headers,
    )

    assert get_response.status_code == 404


def test_update_address():
    headers = get_auth_headers()

    address = create_address(headers)
    address_id = address["id"]

    response = client.put(
        f"/api/addresses/{address_id}",
        json={
            "address_line": "456 Updated Street",
            "city": "Bangalore",
            "state": "Karnataka",
            "postal_code": "560001",
            "country": "India",
        },
        headers=headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == address_id
    assert data["address_line"] == "456 Updated Street"
    assert data["city"] == "Bangalore"
    assert data["state"] == "Karnataka"
    assert data["postal_code"] == "560001"
    assert data["country"] == "India"

