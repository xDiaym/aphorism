import pytest
from flask import Flask
from flask.testing import FlaskClient

from aphorism import create_app, db


@pytest.fixture
def app():
    app = create_app("testing")
    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture(autouse=True)
def database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
    return db
