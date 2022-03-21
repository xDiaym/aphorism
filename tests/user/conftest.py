import pytest


@pytest.fixture
def user() -> dict[str, str]:
    return {
          "name": "John Doe",
          "slug": "john_doe",
          "email": "johndoe@mail.com",
          "password": "mypassword",
    }
