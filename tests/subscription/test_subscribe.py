from http import HTTPStatus
from typing import Callable

from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from aphorism.apps.subscription.model import subscriptions
from aphorism.apps.user.model import User
from tests.subscription import subscribe
from tests.conftest import RegisteredUser


def test_self_subscription(
    client: FlaskClient,
    registered_user: RegisteredUser,
) -> None:
    response = subscribe(client, registered_user.token, registered_user.slug)
    assert response.status_code == int(HTTPStatus.CONFLICT)


def test_subscription_on_user_that_does_not_exist(
    client: FlaskClient,
    registered_user: RegisteredUser,
) -> None:
    response = subscribe(client, registered_user.token, "does-not-exists")
    assert response.status_code == int(HTTPStatus.NOT_FOUND)


def test_subscription_without_token(
    client: FlaskClient,
    registered_user: RegisteredUser,
) -> None:
    response = subscribe(client, None, registered_user.slug)
    assert response.status_code == int(HTTPStatus.UNAUTHORIZED)


def test_subscription_ok(
    app: Flask,
    client: FlaskClient,
    registered_user_fabric: Callable[[], RegisteredUser],
) -> None:
    u1, u2 = registered_user_fabric(), registered_user_fabric()
    response = subscribe(client, u2.token, u1.slug)
    assert response.status_code == int(HTTPStatus.OK)

    with app.app_context():
        u = User.query.join(subscriptions, subscriptions.c.subscriber_id == User.id).first()
        assert u is not None
        assert u.slug == u2.slug
