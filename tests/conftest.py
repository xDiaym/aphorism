import json
from dataclasses import dataclass
from typing import Any

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
def user() -> dict[str, str]:
    return {
        "name": "John Doe",
        "slug": "john_doe",
        "email": "johndoe@mail.com",
        "password": "mypassword",
    }


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
    user: dict[str, str],
) -> RegisteredUser:
    token = register_user(client, json.dumps(user)).json["token"]
    return RegisteredUser(**user, token=token)
