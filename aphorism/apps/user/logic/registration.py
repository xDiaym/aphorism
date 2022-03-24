from http import HTTPStatus

from flask import Response, jsonify
from flask_restx import abort
from aphorism import db

from aphorism.apps.user import logger
from aphorism.apps.user.model import User


def register_user(name: str, slug: str, email: str, password: str) -> Response:
    if User.find_by_slug(slug) is not None:
        abort(
            int(HTTPStatus.CONFLICT),
            "User with this slug already exists.",
            status="fail",
        )
    new_user = User(name=name, slug=slug, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    logger.info("User(id=%i) registered", new_user.id)
    return _create_token_response(
        HTTPStatus.CREATED,
        new_user.create_new_token(),
    )


def _create_token_response(status_code: int, token: str) -> Response:
    response = jsonify(token=token)
    response.status_code = status_code
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    return response
