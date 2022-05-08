from datetime import datetime
from typing import Any

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
    voice_file = db.Column(db.String(length=36))  # 32 char of hash + ".mp4"
    created_at = db.Column(db.DateTime, default=datetime.now)
    likes = db.relationship(
        "User",
        secondary=post_likes,
        lazy="subquery",
    )

    # XXX: use field instead
    def add_voice_file(self, fname: str) -> None:
        self.voice_file = fname

    def serialize(self) -> dict[str, Any]:  # noqa
        """Return json representation of model.

        We make that, because we need authors slug, not id.
        :return: json representation
        """
        author_slug = User.query.filter_by(id=self.author).first().slug
        likes = db.session.query(post_likes).filter_by(post_id=self.id).count()
        return {
            "id": self.id,
            "author": author_slug,
            "caption": self.caption,
            "voice_file": self.voice_file,
            "created_at": self.created_at,
            "likes": likes
        }
