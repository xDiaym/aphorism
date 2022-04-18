from flask_restx.fields import String, Integer

from aphorism.apps.feed import feed_ns


PostModel = feed_ns.model(
    "PostModel",
    {
        "id": Integer(),
        "author": String(),
        "voice_file": String(),
        "likes": Integer(),
        "caption": String(required=False),
    },
)
