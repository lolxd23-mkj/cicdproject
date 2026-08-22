import sys
import os
import pytest


sys.path.insert(0, "/app")


from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from main import app
from db import get_db
from fastapi.testclient import TestClient
from alembic import command
from alembic.config import Config

DATABASE_HOST = os.getenv("DATABASE_HOST", "postgres")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_USER = os.getenv("DATABASE_USER", "ecommerce")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "ecommerce_password")

TEST_DATABASE_URL = (
    f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}/ecommerce_test"
)

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def migrate_test_database():
    alembic_cfg = Config("/app/alembic.ini")

    command.upgrade(alembic_cfg, "head")

@pytest.fixture(autouse=True)
def cleanup_products():
    yield

    db = TestingSessionLocal()

    try:
        db.execute(text("TRUNCATE TABLE products RESTART IDENTITY"))
        db.commit()
    finally:
        db.close()

@pytest.fixture
def client():
    return TestClient(app)
