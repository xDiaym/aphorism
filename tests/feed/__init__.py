from flask.testing import FlaskClient
from werkzeug.datastructures import FileStorage
from werkzeug.test import TestResponse

from tests.conftest import RegisteredUser


def get_post_content() -> dict[str, str | FileStorage]:
    voice_file = FileStorage(
        stream=open("example_sound.mp3", "rb"),
        filename="example.mp3",
        content_type="audio/mpeg",
    )
    data = {"caption": "Lorem ipsum dolor sit amet", "voice_file": voice_file}
    return data


def create_post(
    client: FlaskClient,
    registered_user: RegisteredUser,
) -> TestResponse:
    headers = (
        {"Authorization": f"Bearer {registered_user.token}"}
        if registered_user.token
        else {}
    )
    return client.post(
        f"/api/v1/feed",
        data=get_post_content(),
        headers=headers,
        content_type="multipart/form-data",
    )
