from flask import Flask


def create_app() -> Flask:
    from aphorism.apps.user.view import user

    app = Flask(__name__)

    app.register_blueprint(user, url_prefix="/user")

    return app
