from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_auth_headers():
    unique_id = uuid4().hex[:8]

    username = f"statustest_{unique_id}"
    email = f"statustest_{unique_id}@example.com"

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


def create_product(headers):
    response = client.post(
        "/api/products/",
        json={
            "name": f"Status Product {uuid4().hex[:8]}",
            "description": "Product for order status testing",
            "price": 100.00,
            "stock": 10,
            "image_url": None,
            "category_id": 1,
        },
        headers=headers,
    )

    assert response.status_code == 201, response.text

    return response.json()


def create_order(headers):
    product = create_product(headers)

    cart_response = client.post(
        "/api/cart/items",
        json={
            "product_id": product["id"],
            "quantity": 1,
        },
        headers=headers,
    )

    assert cart_response.status_code in (200, 201), cart_response.text

    order_response = client.post(
        "/api/orders/",
        headers=headers,
    )

    assert order_response.status_code in (200, 201), order_response.text

    return order_response.json()


def test_update_order_pending_to_confirmed():
    headers = get_auth_headers()
    order = create_order(headers)

    response = client.put(
        f"/api/orders/{order['id']}/status",
        json={
            "status": "confirmed",
        },
        headers=headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == order["id"]
    assert data["status"] == "confirmed"


def test_update_order_confirmed_to_shipped():
    headers = get_auth_headers()
    order = create_order(headers)

    response = client.put(
        f"/api/orders/{order['id']}/status",
        json={
            "status": "confirmed",
        },
        headers=headers,
    )

    assert response.status_code == 200, response.text

    response = client.put(
        f"/api/orders/{order['id']}/status",
        json={
            "status": "shipped",
        },
        headers=headers,
    )

    assert response.status_code == 200, response.text
    assert response.json()["status"] == "shipped"


def test_update_order_shipped_to_delivered():
    headers = get_auth_headers()
    order = create_order(headers)

    response = client.put(
        f"/api/orders/{order['id']}/status",
        json={
            "status": "shipped",
        },
        headers=headers,
    )

    assert response.status_code == 200, response.text

    response = client.put(
        f"/api/orders/{order['id']}/status",
        json={
            "status": "delivered",
        },
        headers=headers,
    )

    assert response.status_code == 200, response.text
    assert response.json()["status"] == "delivered"


def test_update_order_invalid_status():
    headers = get_auth_headers()
    order = create_order(headers)

    response = client.put(
        f"/api/orders/{order['id']}/status",
        json={
            "status": "invalid_status",
        },
        headers=headers,
    )

    assert response.status_code == 400, response.text

    data = response.json()

    assert "Invalid order status" in data["detail"]


def test_update_delivered_order():
    headers = get_auth_headers()
    order = create_order(headers)

    response = client.put(
        f"/api/orders/{order['id']}/status",
        json={
            "status": "delivered",
        },
        headers=headers,
    )

    assert response.status_code == 200, response.text

    response = client.put(
        f"/api/orders/{order['id']}/status",
        json={
            "status": "confirmed",
        },
        headers=headers,
    )

    assert response.status_code == 400, response.text

    data = response.json()

    assert data["detail"] == "Delivered orders cannot be updated"


def test_update_cancelled_order():
    headers = get_auth_headers()
    order = create_order(headers)

    response = client.put(
        f"/api/orders/{order['id']}/status",
        json={
            "status": "cancelled",
        },
        headers=headers,
    )

    assert response.status_code == 200, response.text

    response = client.put(
        f"/api/orders/{order['id']}/status",
        json={
            "status": "confirmed",
        },
        headers=headers,
    )

    assert response.status_code == 400, response.text

    data = response.json()

    assert data["detail"] == "Cancelled orders cannot be updated"


def test_update_another_users_order():
    owner_headers = get_auth_headers()
    other_user_headers = get_auth_headers()

    order = create_order(owner_headers)

    response = client.put(
        f"/api/orders/{order['id']}/status",
        json={
            "status": "confirmed",
        },
        headers=other_user_headers,
    )

    assert response.status_code == 403, response.text

    data = response.json()

    assert data["detail"] == "You do not have access to this order"