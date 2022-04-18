from http import HTTPStatus

from flask import Response, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from flask_restx import Resource, abort
from sqlalchemy import desc

from aphorism import db
from aphorism.apps.feed import feed_ns
from aphorism.apps.feed.logic import is_allowed_ext, save_voice_file
from aphorism.apps.feed.model import Post
from aphorism.apps.feed.schema.create import CreatePostModel
from aphorism.apps.feed.schema.response import PostModel


@feed_ns.route("/")
class PostController(Resource):
    @feed_ns.doc(security="Bearer")
    @feed_ns.marshal_list_with(CreatePostModel)
    @feed_ns.response(int(HTTPStatus.OK), "Feed was compiled")
    @feed_ns.response(int(HTTPStatus.UNAUTHORIZED), "Invalid token")
    @jwt_required()
    def get(self) -> list[CreatePostModel]:
        offset = request.json["offset"]
        limit = request.json["limit"]
        posts = (
            current_user.subscriptions.query(Post)
            .order_by(desc(Post.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )
        return posts

    @feed_ns.doc(security="Bearer")
    @feed_ns.marshal_with(CreatePostModel)
    @feed_ns.response(int(HTTPStatus.CREATED), "Post was created", PostModel)
    @feed_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error")
    @feed_ns.response(int(HTTPStatus.UNAUTHORIZED), "Invalid token")
    @jwt_required()
    def post(self) -> Response:
        new_post = Post(**request.json)
        if "voice_file" in request.files:
            file = request.files["voice_file"]
            if not is_allowed_ext(file):
                abort(int(HTTPStatus.BAD_REQUEST), "Validation error", status="fail")
            fname = save_voice_file(file)
            new_post.add_voice_file(fname)
        current_user.posts.append(new_post)
        db.session.merge(current_user)
        db.session.commit()
        return new_post


@feed_ns.route("/like/<int:post_id>")
class LikeController(Resource):
    @feed_ns.doc(security="Bearer")
    @feed_ns.response(int(HTTPStatus.OK), "Like was set")
    @feed_ns.response(int(HTTPStatus.UNAUTHORIZED), "Invalid token")
    @feed_ns.response(int(HTTPStatus.NOT_FOUND), "Post wasn't found")
    @jwt_required()
    def put(self, post_id: int) -> Response:
        post = db.session.query(Post).get(post_id)
        post.likes.append(current_user)
        db.session.commit()
        return jsonify({"ok": True})

    @feed_ns.doc(security="Bearer")
    @feed_ns.response(int(HTTPStatus.OK), "Like was removed")
    @feed_ns.response(int(HTTPStatus.UNAUTHORIZED), "Invalid token")
    @feed_ns.response(int(HTTPStatus.NOT_FOUND), "Post wasn't found")
    @jwt_required()
    def delete(self, post_id: int) -> Response:
        post = db.session.query(Post).get(post_id)
        post.likes.remove(current_user)
        db.session.commit()
        return jsonify({"ok": True})
