import pytest


def test_login_success(client, registered_user):
    response = client.post(
        "/users/login",
        json=registered_user,
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Login successful",
        "username": "fiona",
    }


@pytest.mark.parametrize(
    "login_data",
    [
        {
            "username": "unknown-user",
            "password": "123456",
        },
        {
            "username": "fiona",
            "password": "wrong-password",
        },
    ],
)
def test_login_with_invalid_credentials(
    client,
    registered_user,
    login_data,
):
    response = client.post(
        "/users/login",
        json=login_data,
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid username or password"
    }


@pytest.mark.parametrize(
    "login_data",
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
            "password": "123456",
        },
        {
            "username": "fiona",
        },
    ],
)
def test_login_with_invalid_request(client, login_data):
    response = client.post(
        "/users/login",
        json=login_data,
    )

    assert response.status_code == 422