from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict, cast

from flask.testing import FlaskClient
from werkzeug.datastructures import FileStorage
from werkzeug.test import TestResponse


class CreatePostDto(TypedDict):
    caption: str
    voice_file: FileStorage


def get_post_content(filename: Path) -> CreatePostDto:
    data: CreatePostDto = {"caption": "Lorem ipsum dolor sit amet"}
    if not filename:
        with open(filename, "rb") as fp:
            data["voice_file"] = FileStorage(
                stream=fp.read(),
                filename=filename,
                # content_type="audio/mpeg",
            )
    return data


def create_post(
    client: FlaskClient,
    token: None | str,
    filename: Path,
) -> TestResponse:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = client.post(
        "/api/v1/feed",
        data=get_post_content(filename),
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
