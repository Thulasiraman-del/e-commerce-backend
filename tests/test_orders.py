
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_auth_headers():
    unique_id = uuid4().hex[:8]

    username = f"ordertestuser_{unique_id}"
    email = f"ordertest_{unique_id}@example.com"

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
    unique_id = uuid4().hex[:8]

    response = client.post(
        "/api/categories/",
        json={
            "name": f"Order Test Category {unique_id}",
            "description": "Category for order testing",
        },
    )

    assert response.status_code == 201, response.text

    return response.json()["id"]


def create_product():
    category_id = create_category()

    unique_id = uuid4().hex[:8]

    response = client.post(
        "/api/products/",
        json={
            "name": f"Order Test Product {unique_id}",
            "description": "Product for order testing",
            "price": 1000,
            "stock": 20,
            "image_url": None,
            "category_id": category_id,
        },
    )

    assert response.status_code == 201, response.text

    return response.json()["id"]


def add_product_to_cart(
    product_id: int,
    headers: dict,
):
    response = client.post(
        "/api/cart/items",
        json={
            "product_id": product_id,
            "quantity": 2,
        },
        headers=headers,
    )

    assert response.status_code == 201, response.text


def test_create_order():
    headers = get_auth_headers()

    product_id = create_product()

    add_product_to_cart(
        product_id,
        headers,
    )

    response = client.post(
        "/api/orders/",
        headers=headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert "id" in data
    assert data["status"] == "pending"
    assert float(data["total_amount"]) == 2000.0


def test_get_orders():
    headers = get_auth_headers()

    product_id = create_product()

    add_product_to_cart(
        product_id,
        headers,
    )

    create_response = client.post(
        "/api/orders/",
        headers=headers,
    )

    assert create_response.status_code == 200, create_response.text

    response = client.get(
        "/api/orders/",
        headers=headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_single_order():
    headers = get_auth_headers()

    product_id = create_product()

    add_product_to_cart(
        product_id,
        headers,
    )

    create_response = client.post(
        "/api/orders/",
        headers=headers,
    )

    assert create_response.status_code == 200, create_response.text

    order_id = create_response.json()["id"]

    response = client.get(
        f"/api/orders/{order_id}",
        headers=headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == order_id
    assert data["status"] == "pending"

