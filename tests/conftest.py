import sys
import pytest


sys.path.insert(0, "/app")


from main import app
from db import get_db
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)
