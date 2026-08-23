import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))



from main import app
from db import get_db
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)
