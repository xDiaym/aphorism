from http import HTTPStatus
from pathlib import Path
from time import sleep
from typing import Callable

from flask.testing import FlaskClient

from tests.conftest import RegisteredUser
from tests.feed import create_post
from tests.subscription import subscribe


def test_get_posts_without_token(client: FlaskClient) -> None:
    response = client.get("/api/v1/feed/")
    assert response.status_code == int(HTTPStatus.UNAUTHORIZED)


def test_get_posts_ok(
    client: FlaskClient,
    registered_user_fabric: Callable[[], RegisteredUser],
    audio_file: Path,
) -> None:
    u1, u2 = registered_user_fabric(), registered_user_fabric()
    create_post(client, u1.token, audio_file)
    # Otherwise posts will be created at the same time and '==' will return True.
    # We need to check chronological sorting
    sleep(0.001)
    create_post(client, u2.token, audio_file)
    u3 = registered_user_fabric()
    subscribe(client, u3.token, u1.slug)
    subscribe(client, u3.token, u2.slug)
    headers = (
        {
            "Authorization": f"Bearer {u3.token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if u3.token
        else {}
    )
    response = client.get("/api/v1/feed/", headers=headers)
    assert response.status_code == int(HTTPStatus.OK)
    assert len(response.json) == 2
    # FIXME: convert to datetime
    assert response.json[0]["created_at"] > response.json[1]["created_at"]
    assert response.json[0]["author"] == u2.slug


def test_get_posts_with_offset_and_limit(
    client: FlaskClient,
    registered_user_fabric: Callable[[], RegisteredUser],
    audio_file: Path,
) -> None:
    u1, u2, u3 = (
        registered_user_fabric(),
        registered_user_fabric(),
        registered_user_fabric(),
    )
    create_post(client, u1.token, audio_file)
    sleep(0.001)
    create_post(client, u2.token, audio_file)
    sleep(0.001)
    create_post(client, u3.token, audio_file)
    u4 = registered_user_fabric()
    subscribe(client, u4.token, u1.slug)
    subscribe(client, u4.token, u2.slug)
    subscribe(client, u4.token, u3.slug)
    headers = {"Authorization": f"Bearer {u4.token}"} if u4.token else {}
    response = client.get(
        "/api/v1/feed/", headers=headers, query_string={"limit": "1", "offset": "1"}
    )
    assert response.status_code == int(HTTPStatus.OK)
    assert len(response.json) == 1
    assert response.json[0]["author"] == u2.slug
