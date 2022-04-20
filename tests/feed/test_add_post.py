from http import HTTPStatus
from pathlib import Path

from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from aphorism.apps.feed.model import Post
from aphorism.apps.user.model import User
from tests.conftest import RegisteredUser
from tests.feed import create_post


def test_add_post_without_token(client: FlaskClient, audio_file: Path) -> None:
    response = create_post(client, None, audio_file)
    assert response.status_code == int(HTTPStatus.UNAUTHORIZED)


def test_add_post_with_wrong_format(
    client: FlaskClient, registered_user: RegisteredUser
) -> None:
    this_file = Path(__file__)
    response = create_post(client, registered_user.token, this_file)
    assert response.status_code == int(HTTPStatus.BAD_REQUEST)


def test_add_post_without_file(
    app: Flask, client: FlaskClient, registered_user: RegisteredUser
) -> None:
    response = create_post(client, registered_user.token, None)
    assert response.status_code == int(HTTPStatus.CREATED)

    with app.app_context():
        u = User.query.filter(User.slug == registered_user.slug).first()
        assert u.posts is not None


def test_add_post_ok(
    app: Flask,
    client: FlaskClient,
    registered_user: RegisteredUser,
    audio_file: Path,
) -> None:
    response = create_post(client, registered_user.token, audio_file)
    assert response.status_code == int(HTTPStatus.CREATED)

    with app.app_context():
        u = User.query.filter(User.slug == registered_user.slug).first()
        assert u.posts is not None
