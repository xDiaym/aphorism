from http import HTTPStatus

from flask import Response, jsonify
from flask_jwt_extended import jwt_required, current_user
from flask_restx import Resource, abort

from aphorism import db
from aphorism.apps.subscription import subscription_ns
from aphorism.apps.user.model import User
from aphorism.apps.subscription.model import subscriptions


@subscription_ns.route("/<slug>")
class SubscriptionResource(Resource):
    @subscription_ns.response(int(HTTPStatus.OK), "Successfully subscribed")
    @subscription_ns.response(int(HTTPStatus.CONFLICT), "Self subscription")
    @subscription_ns.response(int(HTTPStatus.UNAUTHORIZED), "Invalid token")
    @subscription_ns.response(int(HTTPStatus.NOT_FOUND), "User not found")
    @jwt_required()
    def post(self, slug: str) -> Response:
        publisher = User.find_by_slug(slug)
        if publisher is None:
            abort(int(HTTPStatus.NOT_FOUND), "User not found", status="fail")
        assert publisher is not None, "Publisher can't be None due check above"
        if publisher.id == current_user.id:
            abort(int(HTTPStatus.CONFLICT), "Self subscription", status="fail")
        current_user.subscriptions.append(publisher)
        db.session.commit()
        return jsonify(status="ok")

    @subscription_ns.response(int(HTTPStatus.OK), "Successfully unsubscribed")
    @subscription_ns.response(int(HTTPStatus.UNAUTHORIZED), "Invalid token")
    @subscription_ns.response(
        int(HTTPStatus.NOT_FOUND),
        "User or subscription not found",
    )
    @jwt_required()
    def delete(self, slug: str) -> Response:
        user = User.find_by_slug(slug)
        if user is None:
            abort(int(HTTPStatus.NOT_FOUND), "User not found", status="fail")
        assert user is not None, "user never None due to check above"
        subscription = db.session.query(subscriptions).filter_by(
            subscriber_id=current_user.id,
            publisher_id=user.id,
        )
        if subscription is None:
            abort(
                int(HTTPStatus.NOT_FOUND),
                "User or subscription not found",
                status="fail",
            )
        subscription.delete()
        db.session.commit()
        return jsonify(status="ok")
