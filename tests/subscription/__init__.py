from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def subscribe(
    client: FlaskClient,
    token: None | str,
    publisher: str,
) -> TestResponse:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return client.post(
        f"/api/v1/subscription/{publisher}",
        headers=headers,
    )
