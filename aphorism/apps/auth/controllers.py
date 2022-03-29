from http import HTTPStatus

from flask import request, Response
from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Resource

from aphorism.apps.auth import auth_ns
from aphorism.apps.auth.schema.register import RegisterModel
from aphorism.apps.auth.schema.login import LoginModel
from aphorism.apps.auth.logic.registration import (
    register_user,
    revoke_token,
    login,
)


@auth_ns.route("/register")
class RegisterUser(Resource):
    @auth_ns.expect(RegisterModel, validate=True)
    @auth_ns.response(int(HTTPStatus.CREATED), "Successfully register.")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.CONFLICT), "User already exist.")
    @auth_ns.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR),
        "Internal server error.",
    )
    def post(self) -> Response:
        # FIXME: non-strict validation can cause errors
        return register_user(**request.get_json())


@auth_ns.route("/login")
class LoginUser(Resource):
    @auth_ns.expect(LoginModel, validate=True)
    @auth_ns.response(int(HTTPStatus.OK), "Successfully login.")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    def post(self) -> Response:
        auth_data = request.json
        return login(auth_data["email"], auth_data["password"])


@auth_ns.route("/logout")
class Logout(Resource):
    @auth_ns.doc(security="Bearer")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), "No token provided.")
    @auth_ns.response(int(HTTPStatus.OK), "Token successfully withdrawn.")
    @jwt_required()
    def delete(self) -> Response:
        return revoke_token(get_jwt())
