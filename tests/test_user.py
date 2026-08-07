def test_get_exsiting_user(client, registered_user):
    response = client.get(
        f"/user/{registered_user['username']}"
    )
    assert response.status_code == 200
    assert response.json() == {
        "username": "fiona"
    }


def test_get_nonexistent_user(client):
    response = client.get("/user/unknown-user")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found"
    }