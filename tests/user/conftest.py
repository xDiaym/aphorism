import json
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
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    )

@pytest.fixture
def registered_user(client: FlaskClient, user: dict[str, str]) -> str:
    return register_user(client, json.dumps(user)).json["token"]

