from http import HTTPStatus
from typing import Any

from flask import Response, jsonify
from flask_restx import abort

from aphorism import db, jwt

from aphorism.apps.auth import logger
from aphorism.apps.user.model import User
from aphorism.apps.auth.model import TokenBlockList


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
    # FIXME: SRP violation
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


# TODO: move in new file
@jwt.token_in_blocklist_loader
def check_if_token_revoked(_jwt_header: Any, jwt_payload: dict) -> bool:
    token = TokenBlockList.find_by_jti(jwt_payload["jti"])
    return token is not None


def revoke_token(token_payload: dict[str, str]) -> Response:
    jti = token_payload["jti"]
    db.session.add(TokenBlockList(jti=jti))
    db.session.commit()
    logger.info("Token of User(id=%i) revoked", token_payload["sub"])
    return jsonify(message="Token revoked")


def login(email: str, password: str) -> Response:
    user = User.find_by_email(email)
    if user is None:
        abort(int(HTTPStatus.BAD_REQUEST), "Invalid credentials", status="fail")
    if user.check_password(password):
        logger.info("User(id=%i) logged in", user.id)
        return _create_token_response(
            int(HTTPStatus.OK),
            user.create_new_token(),
        )
    abort(int(HTTPStatus.BAD_REQUEST), "Invalid credentials", status="fail")
