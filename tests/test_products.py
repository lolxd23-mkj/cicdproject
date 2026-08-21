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
