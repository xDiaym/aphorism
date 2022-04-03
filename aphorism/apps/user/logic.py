from flask_jwt_extended import current_user

from aphorism import db
from aphorism.apps.user import logger


def change_status(status: str) -> None:
    current_user.status = status
    db.session.add(current_user)
    db.session.commit()
    logger.info("User(id=%i) change status to '%s'", current_user.id, status)
