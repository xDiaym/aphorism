from flask.cli import FlaskGroup

from aphorism.wsgi import application


cli = FlaskGroup(application)


if __name__ == "__main__":
    cli()
