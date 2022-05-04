from http import HTTPStatus
from pathlib import Path

from flask import Flask
from flask.testing import FlaskClient

from aphorism.apps.feed.model import Post
from tests.conftest import RegisteredUser
from tests.feed import create_post, remove_post


def test_delete_post_without_token(
    client: FlaskClient, registered_user: RegisteredUser, audio_file: Path
) -> None:
    create_response = create_post(client, registered_user.token, audio_file)
    response = remove_post(client, None, create_response.json.get("id"))
    assert response.status_code == int(HTTPStatus.UNAUTHORIZED)


def test_delete_nonexistent_post(
    client: FlaskClient, registered_user: RegisteredUser
) -> None:
    response = remove_post(client, registered_user.token, 0)
    assert response.status_code == int(HTTPStatus.NOT_FOUND)


def test_delete_post_ok(
    app: Flask,
    client: FlaskClient,
    registered_user: RegisteredUser,
    audio_file: Path,
) -> None:
    create_response = create_post(client, registered_user.token, audio_file)
    response = remove_post(
        client, registered_user.token, create_response.json.get("id")
    )
    assert response.status_code == int(HTTPStatus.OK)

    with app.app_context():
        p = Post.query.get(create_response.json.get("id"))
        assert p is None
