from http import HTTPStatus
from typing import Callable

from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from tests.conftest import RegisteredUser
from tests.feed import create_post


def add_post(
    client: FlaskClient, registered_user_fabric: Callable[[], RegisteredUser]
) -> TestResponse:
    u1 = registered_user_fabric()
    response = create_post(client, u1)
    assert response.status_code == int(HTTPStatus.OK)
