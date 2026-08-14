
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_auth_headers():
    register_response = client.post(
        "/api/auth/register",
        json={
            "username": "carttestuser",
            "email": "carttest@example.com",
            "password": "Test@12345",
        },
    )

    if register_response.status_code not in (201, 400):
        raise AssertionError(register_response.text)

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "carttest@example.com",
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
            "name": "Cart Test Category",
            "description": "Category for cart testing",
        },
    )

    if response.status_code == 201:
        return response.json()["id"]

    if response.status_code == 400:
        response = client.get("/api/categories/")

        assert response.status_code == 200, response.text

        categories = response.json()

        for category in categories:
            if category["name"] == "Cart Test Category":
                return category["id"]

    raise AssertionError(response.text)


def create_product():
    category_id = create_category()

    response = client.post(
        "/api/products/",
        json={
            "name": "Cart Test Product",
            "description": "Product for cart testing",
            "price": 1000,
            "stock": 20,
            "image_url": None,
            "category_id": category_id,
        },
    )

    assert response.status_code == 201, response.text

    return response.json()["id"]


def test_get_cart():
    headers = get_auth_headers()

    response = client.get(
        "/api/cart/",
        headers=headers,
    )

    assert response.status_code == 200, response.text


def test_add_product_to_cart():
    product_id = create_product()
    headers = get_auth_headers()

    response = client.post(
        "/api/cart/items",
        json={
            "product_id": product_id,
            "quantity": 1,
        },
        headers=headers,
    )

    assert response.status_code == 201, response.text

    data = response.json()

    assert data["product_id"] == product_id
    assert data["quantity"] == 1


def test_update_cart_item():
    product_id = create_product()
    headers = get_auth_headers()

    add_response = client.post(
        "/api/cart/items",
        json={
            "product_id": product_id,
            "quantity": 1,
        },
        headers=headers,
    )

    assert add_response.status_code == 201, add_response.text

    update_response = client.put(
        f"/api/cart/items/{product_id}",
        json={
            "quantity": 3,
        },
        headers=headers,
    )

    assert update_response.status_code == 200, update_response.text

    data = update_response.json()

    assert data["product_id"] == product_id
    assert data["quantity"] == 3


def test_remove_product_from_cart():
    product_id = create_product()
    headers = get_auth_headers()

    add_response = client.post(
        "/api/cart/items",
        json={
            "product_id": product_id,
            "quantity": 1,
        },
        headers=headers,
    )

    assert add_response.status_code == 201, add_response.text

    remove_response = client.delete(
        f"/api/cart/items/{product_id}",
        headers=headers,
    )

    assert remove_response.status_code == 200, remove_response.text

    assert remove_response.json()["message"] == (
        "Product removed from cart"
    )
