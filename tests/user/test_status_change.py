import json
from http import HTTPStatus

from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from tests.conftest import RegisteredUser


def set_status(
    client: FlaskClient, status: str, headers: dict[str, str]
) -> TestResponse:
    data = json.dumps({"status": status})
    headers.update(
        {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    )
    return client.post("/api/v1/user/status", data=data, headers=headers)


def get_status(client: FlaskClient, slug: str) -> None:
    return client.get(f"/api/v1/user/{slug}").json["status"]


def test_status_change(
    client: FlaskClient,
    registered_user: RegisteredUser,
) -> None:
    status = "example"
    headers = {"Authorization": f"Bearer {registered_user.token}"}
    response = set_status(client, status, headers)
    assert response.status_code == int(HTTPStatus.OK)
    assert get_status(client, registered_user.slug) == status


def test_status_change_without_token(client: FlaskClient) -> None:
    response = set_status(client, "example", {})
    assert response.status_code == int(HTTPStatus.UNAUTHORIZED)
