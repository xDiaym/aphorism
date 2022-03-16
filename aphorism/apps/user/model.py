from aphorism import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=32))
    slug = db.Column(db.String(length=16), unique=True)
    email = db.Column(db.String(length=128), unique=True)
    password = db.Column(db.String(length=128))
