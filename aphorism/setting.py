from abc import ABC
from datetime import timedelta
from os import environ
from pathlib import Path


BASEDIR = Path(__file__).resolve().parent.parent


class BaseSettings(ABC):
    JWT_SECRET_KEY = SECRET_KEY = environ["SECRET_KEY"]
    COOKIE_LIFETIME = timedelta(weeks=8)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
            user=environ["POSTGRES_USER"],
            password=environ["POSTGRES_PASSWORD"],
            host=environ["DATABASE_HOST"],
            port=environ["DATABASE_PORT"],
            db=environ["POSTGRES_DB"],
        )
    )

    RESTX_MASK_SWAGGER = False  # noqa
    UPLOAD_FOLDER = Path(environ["UPLOAD_DIRECTORY"]).resolve()
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # 200 MB


class DevelopmentSettings(BaseSettings):
    DEBUG = True


class TestingSetting(BaseSettings):
    TESTING = True


class ProductionSettings(BaseSettings):
    pass


settings_mapper = {
    "development": DevelopmentSettings,
    "testing": TestingSetting,
    "production": ProductionSettings,
    "default": ProductionSettings,
}
