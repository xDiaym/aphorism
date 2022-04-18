from http import HTTPStatus
from pathlib import Path

from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from aphorism.apps.feed.model import Post, post_likes
from aphorism.apps.user.model import User
from tests.conftest import RegisteredUser
from tests.feed import create_post, like


def test_set_like_without_token(
    client: FlaskClient,
    registered_user: RegisteredUser,
    audio_file: Path,
) -> None:
    post_response = create_post(client, registered_user.token, audio_file)
    response = like(client, None, post_response.json.get("id"))
    assert response.status_code == int(HTTPStatus.UNAUTHORIZED)


def test_set_like_on_nonexistent_post(
    client: FlaskClient, registered_user: RegisteredUser
) -> TestResponse:
    response = like(client, registered_user.token, 0)
    assert response.status_code == int(HTTPStatus.NOT_FOUND)


def test_set_like_ok(
    app: Flask,
    client: FlaskClient,
    registered_user: RegisteredUser,
    audio_file: Path,
) -> TestResponse:
    post_response = create_post(client, registered_user.token, audio_file)
    response = like(client, registered_user.token, post_response.json.get("id"))
    assert response.status_code == int(HTTPStatus.OK)

    with app.app_context():
        u = Post.query.join(post_likes, post_likes.c.user_id == User.id).first()
        assert u is not None
        assert u.slug == registered_user.slug
