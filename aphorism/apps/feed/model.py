from datetime import datetime

from sqlalchemy.orm import backref

from aphorism import db
from aphorism.apps.user.model import User

post_likes = db.Table(
    "likes",
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    caption = db.Column(db.String(length=128))
    voice_file = db.Column(db.String(lenght=32))
    created_at = db.Column(db.DateTime, default=datetime.now)
    likes = db.relationship(
        "Post",
        secondary=post_likes,
        primaryjoin=post_likes.c.post_id == id,
        secondaryjoin=post_likes.c.user_id == User.id,
        backref=backref("User", lazy="subquery"),
        lazy="subquery",
    )

    def add_voice_file(self, fname: str) -> None:
        self.voice_file = fname
