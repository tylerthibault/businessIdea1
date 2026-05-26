from datetime import datetime
from ..extensions import db

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(254))
    phone = db.Column(db.String(50))
    company = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    quotes = db.relationship('Quote', backref='client', lazy='dynamic')

    def __repr__(self):
        return f'<Client {self.name}>'
