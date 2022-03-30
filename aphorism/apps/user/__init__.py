import logging

from flask_restx import Namespace

user_ns = Namespace("user", description="User related operations.")

logger = logging.getLogger()
