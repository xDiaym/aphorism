from pathlib import Path

from flask import Blueprint, render_template, redirect, abort

from aphorism import db
from aphorism.apps.user.model import User

here = Path(__file__).resolve().parent

front = Blueprint(
    "frontend",
    __name__,
#    static_folder=here / "static",
    template_folder=(here / "templates").name,
)


@front.get("/")
def index() -> str:
    return render_template("index.html")


@front.get("/registration")
def registration() -> str:
    return render_template("registration.html")


@front.get("/login")
def login() -> str:
    return render_template("login.html")


@front.get("/feed/<slug>")
def feed(slug: str) -> str:
    user = User.find_by_slug(slug)
    if user is None:
        abort(404)
    return render_template("feed.html", user=user)


@front.errorhandler(404)
def not_found(e) -> tuple[str, int]:
    return render_template("404.html"), 404
