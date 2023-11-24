from flask_login import UserMixin
from src import db


class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    role = db.Column(
        db.Enum('doctor', 'patient', 'admin', name='role_enum'),
        nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User:{self.username} ({self.name})>'
