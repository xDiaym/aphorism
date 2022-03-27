from flask_restx.fields import String

from aphorism.apps.user import user_ns
from aphorism.apps.user.dto.login import LoginModel


RegisterModel = user_ns.inherit(
    "RegisterModel",
    LoginModel,
    {
        "name": String(
            required=True,
            max_length=32,
            description="The user name",
            example="John Doe",
        ),
        "slug": String(
            required=True,
            max_length=16,
            description="Short user nick",
            example="john_doe",
        ),
    },
)
