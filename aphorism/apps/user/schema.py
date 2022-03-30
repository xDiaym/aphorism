from flask_restx.fields import String

from aphorism.apps.user import user_ns


UserModel = user_ns.model(
    "UserModel",
    {
        "name": String(),
        "slug": String(),
    },
)
