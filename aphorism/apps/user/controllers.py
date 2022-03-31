from http import HTTPStatus

from flask_restx import Resource, abort

from aphorism.apps.user import user_ns
from aphorism.apps.user.schema import UserModel
from aphorism.apps.user.model import User


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
