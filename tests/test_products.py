import sys
sys.path.insert(0, "/app")

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_nonexistent_product():
    response = client.get("/products/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_create_product():
    response = client.post(
        "/products",
        json={
            "name": "PYTEST_PRODUCT",
            "price": 999
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["name"] == "PYTEST_PRODUCT"
    assert data["price"] == 999

def test_create_product():
    response = client.post(
        "/products",
        json={
            "name": "PYTEST_PRODUCT",
            "price": 999
        }
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["name"] == "PYTEST_PRODUCT"
    assert data["price"] == 999

def test_create_product_invalid_price():
    response = client.post(
        "/products",
        json={
            "name": "Monitor",
            "price": "not-a-number"
        }
    )

    assert response.status_code == 422

def test_create_product_zero_price():
    response = client.post(
        "/products",
        json={
            "name": "Free Monitor",
            "price": 0
        }
    )

    assert response.status_code == 422

def test_create_product_negative_price():
    response = client.post(
        "/products",
        json={
            "name": "Broken Monitor",
            "price": -1
        }
    )

    assert response.status_code == 422


def test_create_product_minimum_valid_price():
    response = client.post(
        "/products",
        json={
            "name": "Cheap Monitor",
            "price": 0.01
        }
    )

    assert response.status_code == 200
