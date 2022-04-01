from aphorism import db


class TokenBlockList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)

    @classmethod
    def find_by_jti(cls, jti: str) -> str | None:
        return cls.query.filter_by(jti=jti).first()
