from http import HTTPStatus

from flask import request, Response
from flask_restx import Resource

from aphorism.apps.user import user_ns
from aphorism.apps.user.dto.register import RegisterModel
from aphorism.apps.user.logic.registration import register_user


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
        return register_user(**request.get_json())


@user_ns.route("/login")
class LoginUser(Resource):
    def post(self):
        pass


@user_ns.route("/logout")
class Logout(Resource):
    @user_ns.doc(security="Bearer")
    def post(self):
        pass
