"""API blueprint configuration."""
from flask import Blueprint
from flask_restx import Api

# FIXME: strange import order
from aphorism.apps.auth.controllers import auth_ns
from aphorism.apps.user.controllers import user_ns
from aphorism.apps.subscription.controllers import subscription_ns

api_v1_blueprint = Blueprint("api_v1", __name__)
authorizations = {
    "Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}
}

api_v1 = Api(
    api_v1_blueprint,
    version="1.0",
    title="Aphorism API documentation",
    description="Welcome to the Aphorism documentation!",
    doc="/docs",
    authorizations=authorizations,
)

api_v1.add_namespace(auth_ns, path="/auth")
api_v1.add_namespace(user_ns, path="/user")
api_v1.add_namespace(subscription_ns, path="/subscription")
