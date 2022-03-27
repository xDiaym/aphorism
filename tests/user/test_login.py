import json
from http import HTTPStatus

from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from tests.user.conftest import RegisteredUser


def login(client: FlaskClient, auth: dict[str, str]) -> TestResponse:
    return client.post(
        "/api/v1/user/login",
        data=json.dumps(auth),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )


def test_login_without_credentials(client: FlaskClient) -> None:
    response = login(client, {})
    assert response.status_code == int(HTTPStatus.BAD_REQUEST)
    assert response.json["message"] == "Input payload validation failed"


def test_login_with_valid_credentials(
    client: FlaskClient,
    registered_user: RegisteredUser,
) -> None:
    response = login(client, registered_user.auth)
    assert response.status_code == int(HTTPStatus.OK)
    assert "token" in response.json


def test_login_with_invalid_email(
    client: FlaskClient,
    registered_user: RegisteredUser,
) -> None:
    auth = registered_user.auth
    auth["email"] = "invalid@email.com"
    response = login(client, auth)
    assert response.status_code == int(HTTPStatus.BAD_REQUEST)
    assert response.json["message"] == "Invalid credentials"


def test_login_with_invalid_password(
    client: FlaskClient,
    registered_user: RegisteredUser,
) -> None:
    auth = registered_user.auth
    auth["password"] = "invalid_password"
    response = login(client, auth)
    assert response.status_code == int(HTTPStatus.BAD_REQUEST)
    assert response.json["message"] == "Invalid credentials"
