import pytest

from fastapi.testclient import TestClient

from app.main import app

from app.database import get_user_by_username

from tests.utils.data_loader import load_test_data



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


REGISTER_INVALID_CASES = load_test_data(
    "register_invalid_cases.json"
)
@pytest.mark.parametrize(
    "case",
    REGISTER_INVALID_CASES
)
def test_register_with_invalid_data(case,client):
    response = client.post(
        "/users/register",
        json=case["payload"],
    )

    assert response.status_code == case["expected_status"]