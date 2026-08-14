
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_auth_headers():
    unique_id = uuid4().hex[:8]

    username = f"paymenttest_{unique_id}"
    email = f"paymenttest_{unique_id}@example.com"

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


def create_category():
    response = client.post(
        "/api/categories/",
        json={
            "name": f"Payment Category {uuid4().hex[:8]}",
            "description": "Category for payment testing",
        },
    )

    assert response.status_code == 201, response.text

    return response.json()["id"]


def create_product():
    category_id = create_category()

    response = client.post(
        "/api/products/",
        json={
            "name": f"Payment Product {uuid4().hex[:8]}",
            "description": "Product for payment testing",
            "price": 1000,
            "stock": 20,
            "image_url": None,
            "category_id": category_id,
        },
    )

    assert response.status_code == 201, response.text

    return response.json()["id"]


def create_order(headers):
    product_id = create_product()

    cart_response = client.post(
        "/api/cart/items",
        json={
            "product_id": product_id,
            "quantity": 2,
        },
        headers=headers,
    )

    assert cart_response.status_code == 201, cart_response.text

    order_response = client.post(
        "/api/orders/",
        headers=headers,
    )

    assert order_response.status_code == 200, order_response.text

    return order_response.json()


def test_create_payment():
    headers = get_auth_headers()

    order = create_order(headers)

    order_id = order["id"]

    response = client.post(
        f"/api/payments/{order_id}",
        json={
            "payment_method": "card",
        },
        headers=headers,
    )

    assert response.status_code in (200, 201), response.text

    data = response.json()

    assert "id" in data
    assert data["order_id"] == order_id
    assert float(data["amount"]) == 2000.0
    assert data["status"] == "pending"


def test_get_payment():
    headers = get_auth_headers()

    order = create_order(headers)

    order_id = order["id"]

    create_payment_response = client.post(
        f"/api/payments/{order_id}",
        json={
            "payment_method": "card",
        },
        headers=headers,
    )

    assert create_payment_response.status_code in (200, 201), (
        create_payment_response.text
    )

    response = client.get(
        f"/api/payments/{order_id}",
        headers=headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["order_id"] == order_id
    assert float(data["amount"]) == 2000.0


def test_complete_payment():
    headers = get_auth_headers()

    order = create_order(headers)

    order_id = order["id"]

    create_payment_response = client.post(
        f"/api/payments/{order_id}",
        json={
            "payment_method": "card",
        },
        headers=headers,
    )

    assert create_payment_response.status_code in (200, 201), (
        create_payment_response.text
    )

    payment_id = create_payment_response.json()["id"]

    response = client.put(
        f"/api/payments/{payment_id}/complete",
        headers=headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == payment_id
    assert data["status"] == "completed"

