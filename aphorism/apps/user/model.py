from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from aphorism import db


class User(db.Model):
    # TODO: mark as nonnull
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=32))
    slug = db.Column(db.String(length=16), unique=True)
    email = db.Column(db.String(length=128), unique=True)
    password = db.Column(db.String(length=128))
    status = db.Column(db.String(length=128))

    def __init__(self, password: str, *args: str, **kwargs: str) -> None:
        super().__init__(password=password, *args, **kwargs)
        self.password = generate_password_hash(password)

    def create_new_token(self) -> str:
        return create_access_token(identity=self.id)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_slug(cls, slug: str) -> "User | None":
        return cls.query.filter_by(slug=slug).first()

    @classmethod
    def find_by_email(cls, email: str) -> "User | None":
        return cls.query.filter_by(email=email).first()
