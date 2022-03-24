from typing import Any

from aphorism import db, jwt
from aphorism.apps.user.model import TokenBlockList


@jwt.token_in_blocklist_loader
def check_if_token_revoked(_jwt_header: Any, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = TokenBlockList.query.filter(jti=jti).first_or_none()
    return token is not None
