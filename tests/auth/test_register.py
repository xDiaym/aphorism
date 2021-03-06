import json
from http import HTTPStatus
from typing import Callable

from flask import Flask
from flask.testing import FlaskClient

from aphorism.apps.user.model import User
from tests.conftest import register_user


def test_register_validation(client: FlaskClient) -> None:
    response = register_user(client, data="test")
    assert response.status_code == int(HTTPStatus.BAD_REQUEST)


def test_register_new_user(
    client: FlaskClient,
    app: Flask,
    get_user_reg_data: Callable[[], dict[str, str]],
) -> None:
    user = get_user_reg_data()
    response = register_user(client, data=json.dumps(user))
    assert "token" in response.json
    assert response.status_code == int(HTTPStatus.CREATED)

    with app.app_context():
        db_user = User.query.first()
        assert db_user.name == user["name"]
        assert db_user.slug == user["slug"]
        assert db_user.email == user["email"]


def test_user_already_exist(
    client: FlaskClient,
    get_user_reg_data: Callable[[], dict[str, str]],
) -> None:
    user = get_user_reg_data()
    register_user(client, data=json.dumps(user))
    response = register_user(client, data=json.dumps(user))
    assert response.status_code == int(HTTPStatus.CONFLICT)
