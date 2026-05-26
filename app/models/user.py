from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False, default='')
    business_name = db.Column(db.String(200))
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    quotes = db.relationship('Quote', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    clients = db.relationship('Client', backref='owner', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

    def __repr__(self):
        return f'<User {self.email}>'
