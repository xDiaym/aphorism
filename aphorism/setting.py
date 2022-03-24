from abc import ABC
from os import environ
from pathlib import Path

BASEDIR = Path(__file__).resolve().parent.parent


class BaseSettings(ABC):
    JWT_SECRET_KEY = SECRET_KEY = environ["SECRET_KEY"]

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
