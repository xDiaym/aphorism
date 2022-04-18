from datetime import datetime

from aphorism import db

post_likes = db.Table(
    "likes",
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    caption = db.Column(db.String(length=128))
    voice_file = db.Column(db.String(length=32))
    created_at = db.Column(db.DateTime, default=datetime.now)
    likes = db.relationship(
        "Post",
        secondary=post_likes,
        lazy="subquery",
    )

    # XXX: use field instead
    def add_voice_file(self, fname: str) -> None:
        self.voice_file = fname
