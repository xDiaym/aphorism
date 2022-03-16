from os import environ

from aphorism import create_app


configuration = environ.get("FLASK_ENV", "default")
application = create_app(configuration)
