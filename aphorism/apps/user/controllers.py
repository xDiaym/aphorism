from http import HTTPStatus

from flask import Response, jsonify, request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, abort

from aphorism.apps.user import user_ns
from aphorism.apps.user.schema.user import UserModel
from aphorism.apps.user.model import User
from aphorism.apps.user.logic import change_status


@user_ns.route("/<slug>")
class UserController(Resource):
    @user_ns.marshal_with(UserModel)
    @user_ns.response(int(HTTPStatus.OK), "User found")
    @user_ns.response(int(HTTPStatus.NOT_FOUND), "User not found")
    def get(self, slug: str) -> UserModel:
        user = User.find_by_slug(slug)
        if user is None:
            abort(int(HTTPStatus.NOT_FOUND), "User not found.", status="fail")
        return user


@user_ns.route("/status")
class StatusController(Resource):
    @user_ns.doc(security="Bearer")
    @user_ns.response(int(HTTPStatus.OK), "Status updated")
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error")
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), "Invalid token")
    @jwt_required()
    def post(self) -> Response:
        change_status(request.json["status"])
        return jsonify({"ok": True})
