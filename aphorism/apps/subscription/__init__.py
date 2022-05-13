import logging

from flask_restx import Namespace

subscription_ns = Namespace(
    "subscription",
    description="Subscription related operations.",
)

logger = logging.getLogger()
