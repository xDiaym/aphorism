from datetime import datetime, timedelta

import jwt
from flask import current_app
from werkzeug.security import generate_password_hash

from aphorism import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=32))
    slug = db.Column(db.String(length=16), unique=True)
    email = db.Column(db.String(length=128), unique=True)
    password = db.Column(db.String(length=128))

    def __init__(self, password: str, *args: str, **kwargs: str) -> None:
        super().__init__(password=password, *args, **kwargs)
        self.password = generate_password_hash(password)

    def create_new_token(self) -> str:
        now = datetime.now()
        expire = now + timedelta(days=7)  # FIXME: magic number
        payload = dict(id=self.id, exp=expire)
        secret = current_app.config["SECRET_KEY"]
        return jwt.encode(payload, secret, algorithm="HS256")

    @staticmethod
    def decode_token(token: str) -> str:
        if token.startswith("Bearer "):
            token = token.split("Bearer")[1].strip()
        secret = current_app.config["SECRET_KEY"]
        try:
            payload = jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return Result.error("")
        except jwt.InvalidTokenError:
            error = "Invalid token. Please log in again."
            return Result.Fail(error)

    @classmethod
    def find_by_slug(cls, slug: str) -> "User | None":
        return cls.query.filter_by(slug=slug).first()
