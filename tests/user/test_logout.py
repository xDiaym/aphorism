from http import HTTPStatus

from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from tests.user.conftest import RegisteredUser


def logout(client: FlaskClient, token: str) -> TestResponse:
    return client.delete(
        "/api/v1/user/logout",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )


def test_logout_without_token(client: FlaskClient) -> None:
    response = client.delete("/api/v1/user/logout")
    assert response.status_code == int(HTTPStatus.UNAUTHORIZED)
    # FIXME: different response schema
    assert response.json["msg"] == "Missing Authorization Header"


def test_logout_successfully(
    client: FlaskClient,
    registered_user: RegisteredUser,
) -> None:
    response = logout(client, registered_user.token)
    assert response.status_code == int(HTTPStatus.OK)
    assert response.json["message"] == "Token revoked"


def test_logout_after_logout(
    client: FlaskClient,
    registered_user: RegisteredUser,
) -> None:
    first_response = logout(client, registered_user.token)
    assert first_response.status_code == int(HTTPStatus.OK)
    assert first_response.json["message"] == "Token revoked"

    second_response = logout(client, registered_user.token)
    assert second_response.status_code == int(HTTPStatus.UNAUTHORIZED)
    assert second_response.json["msg"] == "Token has been revoked"
