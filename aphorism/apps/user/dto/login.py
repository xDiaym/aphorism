from flask_restx.fields import String

from aphorism.apps.user import user_ns


LoginModel = user_ns.model(
    "LoginModel",
    {
        "email": String(
            required=True,
            max_length=128,
            description="The user email",
            example="johndoe@mail.com",
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
