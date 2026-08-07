import pytest

from fastapi.testclient import TestClient

from app.main import app

from app.database import get_user_by_username


# client = TestClient(app)


# def setup_function():
#     users.clear()

# @pytest.fixture(autouse=True)
# def clear_users():
#     users.clear()


def test_register_user_success(client):
    response = client.post(
        "/users/register",
        json={
            "username": "fiona",
            "password": "123456",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "message": "User registered successfully",
        "username": "fiona",
    }
    stored_user = get_user_by_username("fiona")

    assert stored_user is not None
    assert stored_user["username"] == "fiona"


def test_register_duplicate_username(client):
    client.post(
        "/users/register",
        json={
            "username": "fiona",
            "password": "123456",
        },
    )

    response = client.post(
        "/users/register",
        json={
            "username": "fiona",
            "password": "another-password",
        },
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Username already exists"
    }


@pytest.mark.parametrize(
    "payload",
    [
        {
            "username": "fi",
            "password": "123456",
        },
        {
            "username": "fiona",
            "password": "123",
        },
        {
            "username": "",
            "password": "123456",
        },
        {
            "username": "fiona",
            "password": "",
        },
    ],
)
def test_register_with_invalid_data(payload,client):
    response = client.post(
        "/users/register",
        json=payload,
    )

    assert response.status_code == 422