from flask_restx.fields import String

from aphorism.apps.feed import feed_ns

PostModel = feed_ns.model(
    "PostModel",
    {
        "caption": String(),
        "voice_file": String(),
    },
)
