from flask_restx.fields import String, Integer, DateTime

from aphorism.apps.feed import feed_ns

PostModel = feed_ns.model(
    "PostModel",
    {
        "id": Integer(),
        "author": String(),
        "caption": String(),
        "voice_file": String(),
        "created_at": DateTime(),
        "likes": Integer(),
    },
)
