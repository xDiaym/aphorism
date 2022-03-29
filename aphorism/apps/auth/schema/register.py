from flask_restx.fields import String

from aphorism.apps.auth import auth_ns
from aphorism.apps.auth.schema.login import LoginModel


RegisterModel = auth_ns.inherit(
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
