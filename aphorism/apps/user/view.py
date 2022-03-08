from flask import Blueprint

user = Blueprint("user", __name__)


@user.get("/<name>")
def get_user(name: str) -> str:
    return name
