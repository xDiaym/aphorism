import json
from dataclasses import dataclass
from typing import Any, Callable

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from werkzeug.test import TestResponse

from aphorism import create_app, db


@pytest.fixture
def app():
    app = create_app("testing")
    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture(autouse=True)
def database(app) -> SQLAlchemy:
    with app.app_context():
        db.drop_all()
        db.create_all()
    return db


@pytest.fixture
def get_user_reg_data() -> Callable[[], dict[str, str]]:
    # Oh, closure can cause memory leaks...
    index = 0

    def generate() -> dict[str, str]:
        nonlocal index
        data = {
            "name": "John Doe",
            "slug": f"john_doe_{index}",
            "email": f"johndoe{index}@mail.com",
            "password": "mypassword",
        }
        index += 1
        return data
    return generate


def register_user(test_client: FlaskClient, data: Any) -> TestResponse:
    return test_client.post(
        "/api/v1/auth/register",
        data=data,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )


@dataclass
class RegisteredUser:
    name: str
    slug: str
    email: str
    password: str
    token: str

    @property
    def auth(self) -> dict[str, str]:
        return {
            "email": self.email,
            "password": self.password,
        }


@pytest.fixture
def registered_user(
    client: FlaskClient,
    get_user_reg_data: Callable[[], dict[str, str]],
) -> RegisteredUser:
    """Create single user."""
    reg_data = get_user_reg_data()
    token = register_user(client, json.dumps(reg_data)).json["token"]
    return RegisteredUser(**reg_data, token=token)


@pytest.fixture
def registered_user_fabric(
    client: FlaskClient,
    get_user_reg_data: Callable[[], dict[str, str]],
) -> Callable[[], RegisteredUser]:
    """Registered user fabric"""
    def fabric() -> RegisteredUser:
        reg_data = get_user_reg_data()
        token = register_user(client, json.dumps(reg_data)).json["token"]
        return RegisteredUser(**reg_data, token=token)
    return fabric
