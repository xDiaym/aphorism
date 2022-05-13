from http import HTTPStatus

from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from tests.conftest import RegisteredUser


def get_user(client: FlaskClient, slug: str) -> TestResponse:
    return client.get(f"/api/v1/user/{slug}")


def test_get_non_existing_user(client: FlaskClient) -> None:
    response = get_user(client, "does-not-exist")
    assert response.status_code == int(HTTPStatus.NOT_FOUND)
    assert "User not found" in response.json["message"]


def test_get_existing_user(
    client: FlaskClient,
    registered_user: RegisteredUser,
) -> None:
    response = get_user(client, registered_user.slug)
    assert response.status_code == int(HTTPStatus.OK)
    assert response.json["name"] == registered_user.name
    assert response.json["slug"] == registered_user.slug
