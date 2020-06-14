import flask_sqlalchemy
from datetime import datetime

db = flask_sqlalchemy.SQLAlchemy()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(self, text):
        self.text = text
