import json
from http import HTTPStatus
from typing import Any

from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from aphorism.apps.user.model import User


def register_user(test_client: FlaskClient, data: Any) -> TestResponse:
    return test_client.post(
        "/api/v1/user/register",
        data=data,
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    )


def test_register_validation(client: FlaskClient) -> None:
    response = register_user(client, data="test")
    assert response.status_code == int(HTTPStatus.BAD_REQUEST)


def test_register_new_user(
    client: FlaskClient,
    app: Flask,
    user: dict[str, str],
) -> None:
    response = register_user(client, data=json.dumps(user))
    assert "token" in response.json
    assert response.status_code == int(HTTPStatus.CREATED)

    with app.app_context():
        db_user = User.query.first()
        assert db_user.name == user["name"]
        assert db_user.slug == user["slug"]
        assert db_user.email == user["email"]


def test_user_already_exist(client: FlaskClient, user: dict[str, str]) -> None:
    register_user(client, data=json.dumps(user))
    response = register_user(client, data=json.dumps(user))
    assert response.status_code == int(HTTPStatus.CONFLICT)
