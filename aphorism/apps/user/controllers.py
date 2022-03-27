from http import HTTPStatus

from flask import request, Response
from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Resource

from aphorism.apps.user import user_ns
from aphorism.apps.user.dto.register import RegisterModel
from aphorism.apps.user.dto.login import LoginModel
from aphorism.apps.user.logic.registration import (
    register_user,
    revoke_token,
    login,
)


@user_ns.route("/register")
class RegisterUser(Resource):
    @user_ns.expect(RegisterModel, validate=True)
    @user_ns.response(int(HTTPStatus.CREATED), "Successfully register.")
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @user_ns.response(int(HTTPStatus.CONFLICT), "User already exist.")
    @user_ns.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR),
        "Internal server error.",
    )
    def post(self) -> Response:
        # FIXME: non-strict validation can cause errors
        return register_user(**request.get_json())


@user_ns.route("/login")
class LoginUser(Resource):
    @user_ns.expect(LoginModel, validate=True)
    @user_ns.response(int(HTTPStatus.OK), "Successfully login.")
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    def post(self) -> Response:
        auth_data = request.json
        return login(auth_data["email"], auth_data["password"])


@user_ns.route("/logout")
class Logout(Resource):
    @user_ns.doc(security="Bearer")
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), "No token provided.")
    @user_ns.response(int(HTTPStatus.OK), "Token successfully withdrawn.")
    @jwt_required()
    def delete(self) -> Response:
        return revoke_token(get_jwt())
