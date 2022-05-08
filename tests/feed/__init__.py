from pathlib import Path
from typing import TypedDict, IO

from flask.testing import FlaskClient
from werkzeug.datastructures import FileStorage
from werkzeug.test import TestResponse


class CreatePostDto(TypedDict):
    caption: str
    voice_file: tuple[IO, str]


def get_post_content(filename: Path) -> CreatePostDto:
    data: CreatePostDto = {"caption": "Lorem ipsum dolor sit amet"}
    if filename:
        # We must close file, but we need opened IO stream
        data["voice_file"] = (open(filename, "rb"), filename.name)
    return data


def create_post(
    client: FlaskClient,
    token: None | str,
    filename: None | Path,
) -> TestResponse:
    data = get_post_content(filename) if filename else {}
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = client.post(
        "/api/v1/feed/",
        data=data,
        headers=headers,
        content_type="multipart/form-data",
    )
    return response


def like(
    client: FlaskClient,
    token: None | str,
    post_id: int,
) -> TestResponse:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return client.put(
        f"/api/v1/feed/like/{post_id}",
        headers=headers,
    )


def unlike(
    client: FlaskClient,
    token: None | str,
    post_id: int,
) -> TestResponse:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return client.delete(
        f"/api/v1/feed/like/{post_id}",
        headers=headers,
    )
