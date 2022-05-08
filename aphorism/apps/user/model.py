import hashlib

from flask_jwt_extended import create_access_token
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash

from aphorism import db
from aphorism.apps.subscription.model import subscriptions


class User(db.Model):
    # TODO: mark as nonnull
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=32))
    slug = db.Column(db.String(length=16), unique=True)
    email = db.Column(db.String(length=128), unique=True)
    password = db.Column(db.String(length=128))
    status = db.Column(db.String(length=128))
    subscriptions = db.relationship(
        "User",
        secondary=subscriptions,
        primaryjoin=subscriptions.c.subscriber_id == id,
        secondaryjoin=subscriptions.c.publisher_id == id,
        backref=backref("subscribers", lazy="subquery"),
        lazy="subquery",
    )
    posts = db.relationship("Post")

    def __init__(self, password: str, *args: str, **kwargs: str) -> None:
        super().__init__(password=password, *args, **kwargs)
        self.password = generate_password_hash(password)

    def create_new_token(self) -> str:
        return create_access_token(identity=self.id)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def gravatar_hash(self) -> str:
        return hashlib.md5(self.slug.encode()).hexdigest()

    def subscriptions_count(self) -> int:
        return len(self.subscriptions)

    def subscribers_count(self) -> int:
        return (
            db.session.query(subscriptions)
            .filter_by(subscriber_id=self.id)
            .count()
        )

    @classmethod
    def find_by_slug(cls, slug: str) -> "User | None":
        return cls.query.filter_by(slug=slug).first()

    @classmethod
    def find_by_email(cls, email: str) -> "User | None":
        return cls.query.filter_by(email=email).first()
