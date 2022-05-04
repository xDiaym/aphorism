from http import HTTPStatus
from typing import Any, Final

from flask import Response, jsonify, request
from flask_jwt_extended import current_user, jwt_required
from flask_restx import Resource, abort
from sqlalchemy import desc

from aphorism import db
from aphorism.apps.feed import feed_ns
from aphorism.apps.feed.logic import is_allowed_ext, save_voice_file
from aphorism.apps.feed.model import Post
from aphorism.apps.feed.schema.response import PostModel
from aphorism.apps.user.model import User


@feed_ns.route("/")
class PostController(Resource):
    default_offset: Final[int] = 0
    default_limit: Final[int] = 25

    @feed_ns.doc(security="Bearer")
    @feed_ns.marshal_list_with(PostModel)
    @feed_ns.response(int(HTTPStatus.OK), "Feed was compiled")
    @feed_ns.response(int(HTTPStatus.UNAUTHORIZED), "Invalid token")
    @jwt_required()
    def get(self) -> list[PostModel]:
        offset = int(request.args.get("offset", self.default_offset))
        limit = int(request.args.get("limit", self.default_limit))
        posts = (
            Post.query.join(User)
            .order_by(desc(Post.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )
        return list(map(Post.serialize, posts))

    @feed_ns.doc(security="Bearer")
    @feed_ns.marshal_with(PostModel)
    @feed_ns.response(int(HTTPStatus.CREATED), "Post was created", PostModel)
    @feed_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error")
    @feed_ns.response(int(HTTPStatus.UNAUTHORIZED), "Invalid token")
    @jwt_required()
    def post(self) -> tuple[dict[str, Any], int]:
        new_post = Post(**request.form, author=current_user.id)
        if "voice_file" in request.files:
            file = request.files["voice_file"]
            if not is_allowed_ext(file):  # FIXME: CRITICAL VULN
                abort(int(HTTPStatus.BAD_REQUEST), "Validation error", status="fail")
            fname = save_voice_file(file)
            new_post.add_voice_file(fname)
        current_user.posts.append(new_post)
        db.session.commit()
        return new_post.serialize(), HTTPStatus.CREATED


@feed_ns.route("/<int:post_id>")
class DeletePostController(Resource):
    @feed_ns.doc(security="Bearer")
    @feed_ns.response(int(HTTPStatus.OK), "Post was deleted")
    @feed_ns.response(int(HTTPStatus.NOT_FOUND), "Post wasn't found")
    @feed_ns.response(int(HTTPStatus.UNAUTHORIZED), "Invalid token")
    @jwt_required()
    def delete(self, post_id) -> Response:
        post = Post.query.get(post_id)
        if post is None:
            abort(int(HTTPStatus.NOT_FOUND), "Post wasn't found", status="fail")
        db.session.delete(post)
        db.session.commit()
        return jsonify({"ok": True})


@feed_ns.route("/like/<int:post_id>")
class LikeController(Resource):
    @feed_ns.doc(security="Bearer")
    @feed_ns.response(int(HTTPStatus.OK), "Like was set")
    @feed_ns.response(int(HTTPStatus.UNAUTHORIZED), "Invalid token")
    @feed_ns.response(int(HTTPStatus.NOT_FOUND), "Post wasn't found")
    @jwt_required()
    def put(self, post_id: int) -> Response:
        post = Post.query.filter_by(id=post_id).first()
        if post is None:
            abort(int(HTTPStatus.NOT_FOUND), "Post not found", status="fail")
        post.likes.append(current_user)
        db.session.commit()
        return jsonify({"ok": True})

    @feed_ns.doc(security="Bearer")
    @feed_ns.response(int(HTTPStatus.OK), "Like was removed")
    @feed_ns.response(int(HTTPStatus.UNAUTHORIZED), "Invalid token")
    @feed_ns.response(int(HTTPStatus.NOT_FOUND), "Post wasn't found")
    @jwt_required()
    def delete(self, post_id: int) -> Response:
        post = Post.query.filter_by(id=post_id).first()
        if post is None:
            abort(HTTPStatus.NOT_FOUND, "Post not found", status="fail")
        post.likes.remove(current_user)
        db.session.commit()
        return jsonify({"ok": True})
