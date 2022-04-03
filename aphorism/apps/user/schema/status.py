from flask_restx.fields import  String

from apps import user_ns


StatusModel = user_ns.model(
    "StatusModel",
    {
        "status": String(length=128),
    }
)
