from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from aphorism.setting import settings_mapper

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name: str = "default") -> Flask:
    from aphorism.apps.user.view import user

    app = Flask(__name__)
    app.config.from_object(settings_mapper[config_name])
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(user, url_prefix="/user")

    return app
