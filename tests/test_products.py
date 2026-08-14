from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def create_category():
    response = client.post(
        "/api/categories/",
        json={
            "name": "Test Electronics",
            "description": "Category for product tests",
        },
    )

    if response.status_code == 201:
        return response.json()["id"]

    categories_response = client.get(
        "/api/categories/"
    )

    assert categories_response.status_code == 200

    categories = categories_response.json()

    for category in categories:
        if category["name"] == "Test Electronics":
            return category["id"]

    raise AssertionError(
        "Test category could not be created or found"
    )


def test_create_product():
    category_id = create_category()

    response = client.post(
        "/api/products/",
        json={
            "name": "Test Laptop",
            "description": "Laptop created during testing",
            "price": 59999.99,
            "stock": 10,
            "image_url": "https://example.com/laptop.jpg",
            "category_id": category_id,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Laptop"
    assert data["description"] == "Laptop created during testing"
    assert Decimal(str(data["price"])) == Decimal("59999.99")
    assert data["stock"] == 10
    assert data["category_id"] == category_id
    assert "id" in data


def test_get_products():
    response = client.get(
        "/api/products/"
    )

    assert response.status_code == 200

    products = response.json()

    assert isinstance(products, list)


def test_get_product():
    category_id = create_category()

    create_response = client.post(
        "/api/products/",
        json={
            "name": "Test Phone",
            "description": "Phone created during testing",
            "price": 29999.99,
            "stock": 20,
            "image_url": None,
            "category_id": category_id,
        },
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    response = client.get(
        f"/api/products/{product_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Test Phone"


def test_get_products_by_category():
    category_id = create_category()

    response = client.get(
        f"/api/products/category/{category_id}"
    )

    assert response.status_code == 200

    products = response.json()

    assert isinstance(products, list)

    for product in products:
        assert product["category_id"] == category_id


def test_update_product():
    category_id = create_category()

    create_response = client.post(
        "/api/products/",
        json={
            "name": "Product Before Update",
            "description": "Original description",
            "price": 1000,
            "stock": 5,
            "image_url": None,
            "category_id": category_id,
        },
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    response = client.put(
        f"/api/products/{product_id}",
        json={
            "name": "Product After Update",
            "price": 1500,
            "stock": 10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Product After Update"
    assert Decimal(str(data["price"])) == Decimal("1500")
    assert data["stock"] == 10


def test_delete_product():
    category_id = create_category()

    create_response = client.post(
        "/api/products/",
        json={
            "name": "Product To Delete",
            "description": "Temporary product",
            "price": 500,
            "stock": 2,
            "image_url": None,
            "category_id": category_id,
        },
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/api/products/{product_id}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/api/products/{product_id}"
    )

    assert get_response.status_code == 404