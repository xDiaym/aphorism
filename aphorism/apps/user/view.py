from flask import Blueprint, Response

user = Blueprint("user", __name__)


@user.get("/<slug>")
def get_user(slug: str) -> str:
    return slug
