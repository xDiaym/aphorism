import json
from dataclasses import dataclass
from typing import Any

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


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
        "/api/v1/user/register",
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
