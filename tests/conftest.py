import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import clear_user


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    clear_user()


@pytest.fixture
def registered_user(client):
    user_data = {
        "username": "fiona",
        "password": "123456",
    }

    response = client.post(
        "/users/register",
        json=user_data,
    )

    assert response.status_code == 201

    return user_data