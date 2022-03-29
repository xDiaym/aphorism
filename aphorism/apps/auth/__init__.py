import logging

from flask_restx import Namespace

auth_ns = Namespace("auth", description="auth related operations.")

logger = logging.getLogger()
