from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from aphorism.setting import settings_mapper

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(settings_mapper[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from aphorism.apps import api_v1_blueprint

    app.register_blueprint(api_v1_blueprint, url_prefix="/api/v1")

    return app
