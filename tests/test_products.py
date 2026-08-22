def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_nonexistent_product(client):
    response = client.get("/products/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_create_product(client):
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

def test_create_product_invalid_price(client):
    response = client.post(
        "/products",
        json={
            "name": "Monitor",
            "price": "not-a-number"
        }
    )

    assert response.status_code == 422

def test_create_product_zero_price(client):
    response = client.post(
        "/products",
        json={
            "name": "Free Monitor",
            "price": 0
        }
    )

    assert response.status_code == 422

def test_create_product_negative_price(client):
    response = client.post(
        "/products",
        json={
            "name": "Broken Monitor",
            "price": -1
        }
    )

    assert response.status_code == 422


def test_create_product_minimum_valid_price(client):
    response = client.post(
        "/products",
        json={
            "name": "Cheap Monitor",
            "price": 0.01
        }
    )

    assert response.status_code == 200


def test_get_products(client):
    response = client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_existing_product(client):
    create_response = client.post(
        "/products",
        json={
            "name": "GET_TEST_PRODUCT",
            "price": 100
        }
    )

    assert create_response.status_code == 200

    product_id = create_response.json()["id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "GET_TEST_PRODUCT"
    assert data["price"] == 100

def test_update_product(client):
    create_response = client.post(
        "/products",
        json={
            "name": "OLD_NAME",
            "price": 100
        }
    )

    assert create_response.status_code == 200

    product_id = create_response.json()["id"]

    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "UPDATED_NAME",
            "price": 200
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "UPDATED_NAME"
    assert data["price"] == 200

def test_update_nonexistent_product(client):
    response = client.put(
        "/products/999999",
        json={
            "name": "Does Not Exist",
            "price": 100
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found"
    }

def test_delete_product(client):
    create_response = client.post(
        "/products",
        json={
            "name": "DELETE_TEST_PRODUCT",
            "price": 50
        }
    )

    assert create_response.status_code == 200

    product_id = create_response.json()["id"]

    response = client.delete(
        f"/products/{product_id}"
    )

    assert response.status_code == 200
    assert response.status_code == 200
    assert response.json() == {
        "message": "Product deleted successfully"
    }

    get_response = client.get(
        f"/products/{product_id}"
    )

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Product not found"
    }

def test_delete_nonexistent_product(client):
    response = client.delete("/products/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found"
    }
