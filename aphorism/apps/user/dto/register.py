from flask_restx.fields import String

from aphorism.apps.user import user_ns

RegisterModel = user_ns.model(
    "RegisterModel",
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
            example="john_doe"
        ),
        "email": String(
            required=True,
            max_length=128,
            description="The user email",
            example="johndoe@mail.com"
        ),
        "password": String(
            required=True,
            description="The user password",
            min_length=8,
            max_length=128,
            example="mypassword",  # TODO: add password pattern filter
        ),
    },
)
